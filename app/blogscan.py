"""
Quét toàn bộ bài blog (WordPress REST API, mọi ngôn ngữ) tìm 8 loại lỗi nội dung hay làm blog rớt top:
đổi năm giả · thiếu trải nghiệm · lạc chủ đề · trùng từ khoá · chèn thương mại · đa ngôn ngữ/mỏng/đã gộp · link tự thân · tác giả.

Mỗi lỗi có nhãn ĐÃ KIỂM (đo chính xác) hoặc NGHI VẤN (máy đoán theo dấu hiệu — người đọc lại để xác nhận).
Kết quả trả về đúng định dạng fixtrack (type, url, lang, detail, note) để nạp vào bảng «Sửa lỗi từng trang».
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import unicodedata
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

UA = "Mozilla/5.0 (compatible; RootySEO/1.0)"
DEFAULT_LANGS = ["", "en", "ru", "ko", "zh-hans", "ja", "fr", "de"]

# loại lỗi → (mức tin cậy, mô tả cách đo) — tên loại GIỮ NGUYÊN để khớp dữ liệu đã nhập từ file kiểm chứng
KINDS = {
    "Đổi năm giả": ("ĐÃ KIỂM", "Tiêu đề/slug ghi năm hiện tại, bài đăng từ năm trước và thân bài nhắc năm đó ≤ 1 lần (năm chỉ nằm trên tiêu đề)."),
    "Link tự thân": ("ĐÃ KIỂM", "Link trong thân bài trỏ về chính URL của bài (không tính link mục lục #)."),
    "Đa ngôn ngữ": ("ĐÃ KIỂM", "Bài ngoại ngữ quá ngắn (< 350 từ, tiếng Trung < 600 chữ Hán), hoặc bài đã 301 sang URL khác nhưng vẫn để Published, hoặc trả 404."),
    "Tác giả": ("ĐÃ KIỂM", "Một người đứng tên phần lớn bài (> 40%), kể cả bài các ngôn ngữ khác."),
    "Trùng từ khóa": ("NGHI VẤN", "Slug cùng ngôn ngữ trùng phần lớn từ chính, hoặc cùng nhóm khách sạn/resort tổng hợp. Xác nhận bằng GSC Truy vấn × Trang."),
    "Lạc chủ đề": ("NGHI VẤN", "Tiêu đề/slug không gắn Phú Quốc hay địa danh trên đảo. Người đọc lại — có bài thật ra ở Phú Quốc mà tên không ghi."),
    "Thiếu trải nghiệm": ("NGHI VẤN", "Bài ≥ 1.500 từ mà không có dấu hiệu trải nghiệm thật nào (HDV, đoàn khách, «chúng tôi đã»…). Người đọc lại để xác nhận."),
    "Thương mại": ("NGHI VẤN", "Mật độ link tới trang tour/vé ≥ 2/1.000 từ hoặc ≥ 5 câu kêu gọi đặt. Không phải lỗi chắc chắn."),
}

PQ_PLACES = ["phu quoc", "phuquoc", "an thoi", "duong dong", "ham ninh", "ganh dau", "cua can", "bai thom", "hon thom", "hon mong tay",
             "hon gam ghi", "hon may rut", "hon dam ngang", "hon roi", "hon dua", "4 dao", "3 dao", "bai sao", "bai dai", "bai truong", "bai khem",
             "bai ong lang", "bai vong", "bai xep", "sunset town", "dia trung hai", "thi tran hoang hon", "grand world", "vinwonders", "vin wonders",
             "vinpearl", "safari", "sun world", "sun group", "cap treo", "cable car", "dinh cau", "suoi tranh", "cho dem", "night market",
             "nam dao", "mui ong bon", "mui ganh dau", "rach vem", "nuoc mam", "ho tieu", "ngoc trai", "cau hon", "kiss bridge", "bac dao",
             "nha tu", "symphony of the sea", "kiss of the sea", "sunset sanato", "hon dau", "duong dong", "an thoi", "ganh", "dao ngoc",
             "phu-quoc", "pq ", "rooty", "corona", "casino", "sun premier", "la festa", "regent", "pullman", "melia", "wyndham", "seashells"]
EXP_VI = re.compile(r"\b(chúng tôi|chúng mình|team rooty|hdv|hướng dẫn viên|dẫn đoàn|đoàn khách|khách của rooty|khách hàng của chúng tôi|"
                    r"kinh nghiệm thực tế|thực tế cho thấy|lần (gần nhất|trước)|mình đã|tôi đã|đã từng đi|tự chụp|ảnh: rooty|mẹo)\b", re.I)
EXP_EN = re.compile(r"\b(we|our (guide|team|tour|guests|customers)|rooty trip|tour guide|in our experience|i (visited|went|tried)|tip:|tips)\b", re.I)
CTA = re.compile(r"đặt ngay|đặt tour|đặt vé|đặt phòng|liên hệ ngay|gọi ngay|book now|booking now|inbox|nhắn zalo|đặt combo|예약|забронировать|立即预订", re.I)
HOTEL = re.compile(r"\b(khach-san|resort|homestay|nghi-duong|hotel|villa)\b")
SLUG_STOP = set("phu quoc o tai va cua cho voi nhung cac gi nao the la co khong nhat moi 2024 2025 2026 2027 review kinh nghiem du lich "
                "chi tiet top dep the gioi viet nam in the of and to a for best guide what how is are".split())


def _get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), dict(r.headers)


def strip_accents(s):
    s = unicodedata.normalize("NFD", s or "").replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def text_of(h):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h or "", flags=re.S | re.I)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", h)).split())


def path_of(u):
    p = urllib.parse.urlsplit(u).path
    return "/" + p.strip("/") + "/" if p.strip("/") else "/"


def size_of(text, lang):
    if lang.lower().startswith("zh") or lang.lower() == "ja":
        return len(re.findall(r"[㐀-鿿]", text)), "chữ Hán"
    return len(re.findall(r"\w+", text)), "từ"


def detect_langs(site):
    try:
        body, _ = _get(site.rstrip("/") + "/")
        h = body.decode("utf-8", "replace")
        langs = {""}
        for m in re.finditer(r'hreflang=["\']([\w-]+)["\'][^>]*href=["\']([^"\']+)|href=["\']([^"\']+)["\'][^>]*hreflang=["\']([\w-]+)', h):
            href = m.group(2) or m.group(3)
            seg = path_of(href).strip("/").split("/")[0] if href else ""
            if seg and len(seg) <= 7 and re.fullmatch(r"[a-z]{2}(-[a-z]+)?", seg):
                langs.add(seg)
        return sorted(langs, key=lambda x: (x != "", x)) if len(langs) > 1 else DEFAULT_LANGS
    except Exception:
        return DEFAULT_LANGS


def fetch_posts(site, say=lambda m: None):
    site = site.rstrip("/")
    posts = []
    for lang in detect_langs(site):
        base = f"{site}/{lang}" if lang else site
        page = 1
        while True:
            url = f"{base}/wp-json/wp/v2/posts?per_page=100&page={page}&status=publish&_fields=id,link,slug,date,modified,title,author,content"
            try:
                body, hd = _get(url)
                data = json.loads(body)
            except Exception:
                break
            if not isinstance(data, list) or not data:
                break
            for p in data:
                if lang and f"/{lang}/" not in p.get("link", ""):
                    continue   # plugin trả lại bài tiếng Việt khi ngôn ngữ không có
                posts.append({"id": p["id"], "lang": (lang or "vi").upper().split("-")[0], "link": p["link"], "slug": p.get("slug", ""),
                              "date": p.get("date", "")[:10], "modified": p.get("modified", "")[:10], "author": p.get("author"),
                              "title": html.unescape(re.sub(r"<[^>]+>", "", p["title"]["rendered"])), "html": p["content"]["rendered"]})
            total_pages = int(hd.get("X-WP-TotalPages") or hd.get("x-wp-totalpages") or 1)
            say(f"Đọc bài {lang.upper() or 'VI'}: trang {page}/{total_pages}")
            if page >= total_pages:
                break
            page += 1
    seen, out = set(), []
    for p in posts:
        if p["link"] not in seen:
            seen.add(p["link"])
            out.append(p)
    return out


def fetch_authors(site):
    try:
        body, _ = _get(site.rstrip("/") + "/wp-json/wp/v2/users?per_page=100&_fields=id,name,link")
        return {u["id"]: u for u in json.loads(body)}
    except Exception:
        return {}


def _status(url):
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
        from geo_audit import fetch
        from geo_audit import decode
        st, body, hd, _ = fetch(url, follow=False)
        title = h1 = ""
        if st == 200:
            h = decode(body, hd)
            m = re.search(r"<title[^>]*>(.*?)</title>", h, re.S | re.I)
            title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""
            m = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S | re.I)
            h1 = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""
        return st, (hd.get("location") or hd.get("Location") or ""), title, h1
    except Exception:
        return None, "", "", ""


# ------------------------------------------------------------------ 8 phép đo

def scan(site, product_paths=None, today=None, say=lambda m: None, check_status=True):
    today = today or dt.date.today()
    year = str(today.year)
    posts = fetch_posts(site, say)
    authors = fetch_authors(site)
    host = urllib.parse.urlsplit(site).netloc.replace("www.", "")
    product_paths = set(product_paths or [])
    items = []
    stats = {"posts": len(posts), "by_lang": dict(Counter(p["lang"] for p in posts))}

    def add(kind, p, detail):
        items.append({"type": kind, "url": path_of(p["link"]), "lang": p["lang"], "detail": detail, "note": KINDS[kind][1]})

    if check_status:
        say(f"Kiểm mã trả về của {len(posts)} bài (bài đã gộp/301, 404)…")
        with ThreadPoolExecutor(max_workers=8) as ex:
            for p, (st, loc, t, h1) in zip(posts, ex.map(lambda p: _status(p["link"]), posts)):
                p["status"], p["location"], p["seo_title"], p["h1"] = st, loc, t, h1
    for p in posts:
        text = text_of(p["html"])
        p["text"] = text
        n, unit = size_of(text, p["lang"])
        p["size"], p["unit"] = n, unit
        me = path_of(p["link"])
        hrefs = [h for h in re.findall(r'<a\s[^>]*href=["\']([^"\']+)', p["html"], re.I)]
        abs_links = [urllib.parse.urljoin(p["link"], h) for h in hrefs if not h.startswith("#")]
        internal = [u for u in abs_links if urllib.parse.urlsplit(u).netloc.replace("www.", "") == host]
        # 1 · đổi năm giả
        shown = " · ".join(dict.fromkeys(x for x in (p.get("h1"), p.get("seo_title"), p["title"]) if x))
        yt = re.findall(r"\b(20\d\d)\b", shown + " " + p["slug"])
        if year in yt and p["date"][:4] < year:
            n_year = len(re.findall(r"\b" + year + r"\b", text))
            old = len(re.findall(r"\b(?:2019|202[0-4])\b", text))
            if n_year <= 1:
                add("Đổi năm giả", p, f"NN: {p['lang']} · Tiêu đề: {shown[:160]} · Ngày đăng: {p['date']} · Sửa lần cuối: {p['modified']} · "
                                     f"Nhắc năm ≤2024: {old} · Nhắc {year} trong thân bài: {n_year} · Số từ: {n}")
        # 7 · link tự thân
        own = [h for h, u in zip(hrefs, [urllib.parse.urljoin(p["link"], h) for h in hrefs]) if "#" not in h
               and path_of(u.split("#")[0]) == me and urllib.parse.urlsplit(u).netloc.replace("www.", "") == host]
        if own:
            anchors = re.findall(r'<a\s[^>]*href=["\'](?:' + "|".join(re.escape(h) for h in set(own)) + r')["\'][^>]*>(.*?)</a>', p["html"], re.I | re.S)
            add("Link tự thân", p, f"NN: {p['lang']} · Số link tự thân: {len(own)} · Anchor text: " + " | ".join(text_of(a)[:80] for a in anchors[:3]))
        # 6 · đa ngôn ngữ / mỏng / đã gộp
        if p.get("status") in (301, 302, 307, 308):
            add("Đa ngôn ngữ", p, f"Loại: Bài đã gộp (chuyển hướng sang bài khác) nhưng vẫn để Published · Trạng thái: → {path_of(p['location']) if p['location'] else '?'}")
        elif p.get("status") in (404, 410):
            add("Đa ngôn ngữ", p, f"Loại: URL {p['status']} · Trạng thái: {p['status']} · Ghi chú: bài Published nhưng trang trả {p['status']}")
        elif p["lang"] != "VI" and ((unit == "từ" and n < 350) or (unit == "chữ Hán" and n < 600)):
            add("Đa ngôn ngữ", p, f"Loại: Bài ngoại ngữ ngắn · Trạng thái: {n} {unit}")
        # 2 · thiếu trải nghiệm
        if unit == "từ" and n >= 1500:
            sig = len((EXP_VI if p["lang"] == "VI" else EXP_EN).findall(text))
            if sig == 0:
                add("Thiếu trải nghiệm", p, f"NN: {p['lang']} · Số dấu hiệu trải nghiệm: {sig} · Số từ: {n}")
        # 3 · lạc chủ đề
        hay = strip_accents(shown + " " + p["slug"].replace("-", " ")) + " "
        if not any(pl in hay for pl in PQ_PLACES):
            add("Lạc chủ đề", p, f"NN: {p['lang']} · Số từ: {n} · Lý do: tiêu đề/slug không gắn Phú Quốc hay địa danh trên đảo — «{p['title'][:90]}»")
        # 5 · thương mại
        prod = [u for u in internal if path_of(u) in product_paths or re.search(r"/(tour|ve|combo|san-pham|product|tours?)[-/]", path_of(u))]
        cta = len(CTA.findall(text))
        per_k = round(len(prod) / max(n, 1) * 1000, 1) if unit == "từ" else 0
        if (unit == "từ" and n >= 300 and per_k >= 2) or cta >= 5:
            add("Thương mại", p, f"NN: {p['lang']} · Link tới tour/vé: {len(prod)} · Câu kêu gọi đặt: {cta} · Số từ: {n} · Link/1.000 từ: {per_k}")
    # 4 · trùng từ khoá (theo ngôn ngữ)
    groups = defaultdict(list)
    for p in posts:
        toks = [t for t in strip_accents(p["slug"]).split("-") if t and t not in SLUG_STOP and not t.isdigit()]
        p["toks"] = set(toks)
        groups[p["lang"]].append(p)
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for lang, ps in groups.items():
        hotels = [p for p in ps if HOTEL.search(p["slug"]) and not re.search(r"review|-chi-tiet", p["slug"])]
        for a in hotels[1:]:
            parent[find(a["link"])] = find(hotels[0]["link"])
        for i, a in enumerate(ps):
            for b in ps[i + 1:]:
                if len(a["toks"]) < 2 or len(b["toks"]) < 2:
                    continue
                inter = len(a["toks"] & b["toks"])
                if inter >= 2 and inter / len(a["toks"] | b["toks"]) >= 0.6:
                    parent[find(a["link"])] = find(b["link"])
    clusters = defaultdict(list)
    for p in posts:
        if p["link"] in parent:
            clusters[find(p["link"])].append(p)
    for root, ps in clusters.items():
        if len(ps) < 2:
            continue
        ps.sort(key=lambda p: -p["size"])
        common = Counter(t for p in ps for t in p["toks"]).most_common(3)
        name = " ".join(t for t, c in common if c >= 2) or "khách sạn / resort"
        items.append({"type": "Trùng từ khóa", "url": path_of(ps[0]["link"]), "lang": ps[0]["lang"],
                      "detail": f"Cụm chủ đề: {name} ({ps[0]['lang']}) · Số bài: {len(ps)} · Các URL: " + " · ".join(path_of(p["link"]) for p in ps),
                      "note": KINDS["Trùng từ khóa"][1]})
    # 8 · tác giả
    cnt = Counter(p["author"] for p in posts)
    if posts and cnt:
        top, k = cnt.most_common(1)[0]
        share = k / len(posts)
        langs = Counter(p["lang"] for p in posts if p["author"] == top)
        stats["author"] = {"name": (authors.get(top) or {}).get("name", str(top)), "share": round(share * 100), "langs": dict(langs),
                           "page": (authors.get(top) or {}).get("link", "")}
        if share > 0.4:
            for p in posts:
                if p["author"] == top:
                    add("Tác giả", p, f"NN: {p['lang']} · Tác giả: {stats['author']['name']} ({round(share * 100)}% số bài, ngôn ngữ: "
                                      + ", ".join(f"{l} {c}" for l, c in langs.items()) + ")")
    stats["counts"] = dict(Counter(i["type"] for i in items))
    overview = {k: {"ten": k, "ket_luan": KINDS[k][0], "so_bai": stats["counts"].get(k, 0), "cach_do": KINDS[k][1]} for k in KINDS}
    return items, overview, stats
