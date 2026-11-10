"""
Công cụ cho Bước 2–4: đoán ý định, mở rộng từ khoá bằng gợi ý Google, gợi ý gom nhóm (topic cluster),
soi nhanh website đối thủ, phân loại từ khoá đối thủ (Common/Gap). Chỉ dùng thư viện chuẩn.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0, str(ROOT / "scripts"))
from geo_audit import PageParser, decode, fetch, jsonld_types, sitemap_urls  # noqa: E402


# ------------------------------------------------------------------ ý định & giai đoạn

def guess_intent(k: str) -> str:
    k = k.lower()
    if "rooty" in k:
        return "Điều hướng"
    if re.search(r"nên |hay |so sánh|review|đánh giá|uy tín|tốt nhất|top |kinh nghiệm|có nên", k):
        return "Cân nhắc"
    if re.search(r"giá|bao nhiêu tiền|đặt|book|mua|(^|\s)(tour|combo|vé|khách sạn|resort|cano|thuê xe)(\s|$)", k):
        return "Mua"
    return "Thông tin"


INTENT_STAGE = {"Thông tin": "Nhận thức", "Cân nhắc": "Cân nhắc", "Mua": "Quyết định", "Điều hướng": "Quyết định"}


def map_tool_intent(s: str) -> str | None:
    """Ý định từ Ahrefs/Semrush (Informational, Navigational, Commercial, Transactional)."""
    s = (s or "").lower()
    if "transac" in s:
        return "Mua"
    if "commerc" in s:
        return "Cân nhắc"
    if "navig" in s or "branded" in s:
        return "Điều hướng"
    if "inform" in s:
        return "Thông tin"
    return None


# ------------------------------------------------------------------ gợi ý Google (autocomplete)

MODIFIERS = ["giá", "bao nhiêu tiền", "có gì", "ở đâu", "kinh nghiệm", "nên", "review", "tốt nhất", "2026",
             "trọn gói", "cho gia đình", "lịch trình", "từ", "tháng"]
LETTERS = list("abcdghklmnpqstv")


def google_suggest(q: str) -> list[str]:
    url = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(
        {"client": "firefox", "hl": "vi", "gl": "vn", "q": q})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read()
        cs = re.search(r"charset=([\w-]+)", r.headers.get("content-type", "")) or None
    for enc in ([cs.group(1)] if cs else []) + ["utf-8", "latin-1"]:
        try:
            data = json.loads(raw.decode(enc))
            return [s for s in data[1] if isinstance(s, str)]
        except (UnicodeDecodeError, ValueError, LookupError, IndexError):
            continue
    return []


def _core_tokens(s):
    # giữ cả chữ số ("4 đảo" ≠ "3 đảo"), bỏ ký tự đơn lẻ
    return [t for t in re.findall(r"\w+", s.lower()) if len(t) > 1 or t.isdigit()]


def expand_seed(seed: str, log=lambda m: None, delay=0.25) -> list[str]:
    """Trả về danh sách từ khoá gợi ý liên quan tới seed (đã bỏ trùng)."""
    queries = [seed] + [f"{seed} {m}" for m in MODIFIERS] + [f"{seed} {c}" for c in LETTERS]
    need = set(_core_tokens(seed)) - {"phú", "quốc"} or set(_core_tokens(seed))
    out, seen = [], set()
    for i, q in enumerate(queries, 1):
        try:
            for s in google_suggest(q):
                s2 = " ".join(s.lower().split())
                # giữ gợi ý còn chứa ít nhất 1 từ chính của seed (bỏ gợi ý lạc đề)
                if s2 not in seen and need & set(_core_tokens(s2)) and not JUNK.search(s2):
                    seen.add(s2)
                    out.append(s2)
        except Exception as e:
            log(f"  lỗi '{q}': {e}")
        if i % 10 == 0:
            log(f"  {seed}: {i}/{len(queries)} truy vấn, {len(out)} gợi ý")
        time.sleep(delay)
    return out


# ------------------------------------------------------------------ gợi ý gom nhóm

STOP = set("""giá bao nhiêu tiền ở đâu có gì không nên kinh nghiệm review đánh giá tốt nhất top mới nhất cập nhật chi tiết
là đi thế nào như những các và cho tại của một từ với năm 2024 2025 2026 2027 uy tín rẻ ưu đãi hot
phú quốc pq gồm bao
""".split())  # "phú quốc": mọi từ khoá của Rooty đều về Phú Quốc nên không dùng để tách nhóm
CLUSTER_RULES = [
    (r"rooty", "Thương hiệu"),
    (r"\bvé\b|cáp treo|vinwonders|safari|grand world|kiss of the sea|show", "Vé tham quan"),
    (r"combo|khách sạn|resort|homestay|villa", "Combo & khách sạn"),
    (r"tour.*(đảo|cano|hòn|lặn|san hô)|(\d|bốn|ba) đảo|hòn thơm|hòn móng tay|lặn ngắm", "Tour đảo"),
    (r"tour.*(trọn gói|\dn\dđ|\d ngày|ngày \d đêm)", "Tour trọn gói"),
    (r"tour", "Tour trong ngày"),
    (r"lịch trình|chi phí|kinh nghiệm|tháng|mùa|thời tiết|đi lại|di chuyển|mang gì|tự túc", "Lên kế hoạch"),
    (r"ăn gì|quán|nhà hàng|đặc sản|hải sản|món|chợ đêm|ẩm thực", "Ẩm thực"),
]


JUNK = re.compile(r"tuyển dụng|việc làm|tuyen dung|giám đốc|sở du lịch|mã số thuế|mức lương|lương bao nhiêu")


def is_junk(k: str) -> bool:
    """Từ khoá không phải khách tìm mua tour (tuyển dụng, cơ quan nhà nước…)."""
    return bool(JUNK.search(k.lower()))


def _expand_abbr(k: str) -> str:
    k = k.lower()
    # 3n2d / 3n2đ / 3N2Đ → 3 ngày 2 đêm ; "4 ngày 3 đêm" giữ nguyên
    k = re.sub(r"(\d)\s*n\s*(\d)\s*[dđ]\b", r"\1 ngày \2 đêm", k)
    k = re.sub(r"\bpq\b", "phú quốc", k)
    return k


def norm_key(k: str) -> str:
    k = _expand_abbr(k)
    toks = [t for t in _core_tokens(k) if t not in STOP and not re.fullmatch(r"20\d\d", t)]
    return " ".join(sorted(set(toks)))


def guess_cluster(k: str) -> str:
    k = k.lower()
    for pat, name in CLUSTER_RULES:
        if re.search(pat, k):
            return name
    return "Điểm đến"


def suggest_groups(rows: list[dict]) -> dict:
    """rows: [{record_id, fields}] của bảng Từ khoá. Trả về {record_id: {trường: giá trị}} chỉ cho ô đang trống."""
    groups: dict[str, list] = {}
    updates = {}
    for r in rows:
        f = r["fields"]
        if f.get("Trạng thái") == "Bỏ":
            continue
        if is_junk(f.get("Từ khoá", "")):
            updates[r["record_id"]] = {"Trạng thái": "Bỏ", "Ghi chú": "Tự loại: không phải ý định mua tour"}
            continue
        key = (f.get("Từ khoá cha") or "").strip().lower() or norm_key(f.get("Từ khoá", ""))
        groups.setdefault(key, []).append(r)
    for key, rs in groups.items():
        vol = lambda r: (r["fields"].get("Lượng tìm") or r["fields"].get("Hiển thị") or 0)
        abbr = lambda r: bool(re.search(r"\d\s*n\s*\d\s*[dđ]\b", r["fields"].get("Từ khoá", "").lower()))
        # tên nhóm: lượng tìm cao nhất → cách viết đầy đủ (không viết tắt 3n2d) → ngắn nhất
        rs.sort(key=lambda r: (-vol(r), abbr(r), len(r["fields"].get("Từ khoá", ""))))
        head = rs[0]["fields"].get("Từ khoá", "")
        url = next((r["fields"].get("Trang đích") for r in rs if r["fields"].get("Trang đích")), "")
        for i, r in enumerate(rs):
            f, ch = r["fields"], {}
            if not f.get("Nhóm URL"):
                ch["Nhóm URL"] = head
            if not f.get("Cụm chủ đề"):
                ch["Cụm chủ đề"] = guess_cluster(head)
            if not f.get("Vai trò"):
                ch["Vai trò"] = "Từ khoá chính" if i == 0 else "Từ khoá phụ"
            if url and not f.get("Trang đích"):
                ch["Trang đích"] = url
            if ch:
                updates[r["record_id"]] = ch
    return updates


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower().replace("đ", "d"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:80]


# ------------------------------------------------------------------ Bước 6: câu hỏi khách hay hỏi & chấm bài theo intent

Q_PREFIX = ["có nên", "bao nhiêu", "ở đâu", "có gì", "như thế nào", "mấy giờ", "khi nào", "là gì", "có đáng", "nên", "kinh nghiệm", "cần mang gì"]
QUESTION_RE = re.compile(r"(không|bao nhiêu|ở đâu|có gì|thế nào|mấy|khi nào|là gì|có nên|nên |có đáng|cần|gì|sao|hay )")


def suggest_questions(kw: str, limit=25) -> list[str]:
    """Câu hỏi thật từ gợi ý Google cho từ khoá (thay cho People Also Ask khi không đọc được SERP)."""
    out, seen = [], set()
    for q in [kw] + [f"{kw} {p}" for p in Q_PREFIX] + [f"{p} {kw}" for p in ("có nên", "kinh nghiệm", "nên")]:
        try:
            for s in google_suggest(q):
                s = " ".join(s.lower().split())
                if s not in seen and QUESTION_RE.search(s) and not JUNK.search(s):
                    seen.add(s)
                    out.append(s)
        except Exception:
            pass
        time.sleep(0.2)
        if len(out) >= limit:
            break
    return out[:limit]


def content_check(url: str, kw: str, intent: str) -> tuple[int, str]:
    """Chấm một trang đã đăng theo Bước 6. Trả về (điểm 0–100, chi tiết từng tiêu chí)."""
    st, body, hd, _ = fetch(url)
    if st != 200:
        return 0, f"Trang trả mã {st} — không chấm được"
    html = decode(body, hd)
    p = PageParser()
    try:
        p.feed(html)
    except Exception:
        pass
    words = " ".join(p.body_text).split()
    h1 = [t for tag, t in p.headings if tag == "h1"]
    h2 = [t for tag, t in p.headings if tag == "h2"]
    h3 = [t for tag, t in p.headings if tag == "h3"]
    opening = " ".join(" ".join(p.text_after_h1).split()[:150])
    core = [t for t in _core_tokens(kw) if t not in STOP] or _core_tokens(kw)
    in_open = sum(1 for t in core if t in opening.lower()) / max(len(core), 1)
    content_h2 = [h for h in h2 if h.lower() not in ("tin tức liên quan", "có thể bạn sẽ thích", "bài viết liên quan")]
    q_ratio = sum(1 for h in content_h2 if h.strip().endswith("?") or QUESTION_RE.search(h.lower())) / max(len(content_h2), 1)
    n_table = len(re.findall(r"<table\b", html, re.I))
    n_list = len(re.findall(r"<(ul|ol)\b", html, re.I))
    n_img = len(re.findall(r"<img\b", html, re.I))
    has_video = bool(re.search(r"youtube\.com/embed|youtu\.be|<video\b|tiktok\.com/embed", html, re.I))
    types, _, _ = jsonld_types(p.jsonld)
    junk = [k for k in ("Tác giả:", "Ngày đăng:", "Lượt xem:") if k in opening[:250]]
    text = " ".join(p.body_text)
    pm = re.search(r"\d{1,3}(?:[.,]\d{3})+\s*(?:đ|₫|vnđ|vnd|đồng)\b|(?:đ|₫|vnđ)\s*\d{1,3}(?:[.,]\d{3})+|giá\s*(?:từ|chỉ)?\s*:?\s*\d{1,3}(?:[.,]\d{3})+", text, re.I)
    price = bool(pm)
    contact_price = len(re.findall(r"(?:đơn giá|giá)\s*:?\s*(?:tổng\s*:\s*)?liên hệ", text, re.I))
    cta = bool(re.search(r"zalo\.me|href=[\"']tel:|m\.me/|<form\b", html, re.I))
    phone = bool(re.search(r"(?<!\d)0[35789]\d(?:[\s.]?\d){7}(?!\d)", text))
    checks = [
        ("Trả lời ngay đầu bài: từ khoá chính có trong 150 từ đầu", in_open >= 0.6, f"{round(in_open*100)}% từ chính của «{kw}» có trong đoạn mở"),
        ("Đoạn mở không bị khối tác giả/ngày chen giữa", not junk, ", ".join(junk) or "sạch"),
        ("Đúng 1 H1", len(h1) == 1, f"{len(h1)} H1"),
        ("Có cấu trúc H2 (≥ 3) và H3", len(content_h2) >= 3 and len(h3) >= 1, f"{len(content_h2)} H2 · {len(h3)} H3"),
        ("Có danh sách (bullet)", n_list >= 1, f"{n_list} danh sách"),
        ("Có hình ảnh minh hoạ (≥ 3)", n_img >= 3, f"{n_img} ảnh"),
    ]
    if intent == "Thông tin":
        checks += [("H2 là câu hỏi người dùng (≥ 30%)", q_ratio >= 0.3, f"{round(q_ratio*100)}% H2 dạng câu hỏi"),
                   ("Đủ độ sâu (≥ 800 từ)", len(words) >= 800, f"{len(words)} từ"),
                   ("Có bảng tóm tắt dữ kiện hoặc video", n_table >= 1 or has_video, f"{n_table} bảng · video: {'có' if has_video else 'không'}")]
    elif intent == "Cân nhắc":
        checks += [("Có bảng so sánh", n_table >= 1, f"{n_table} bảng"),
                   ("Heading thể hiện so sánh/đánh giá (so sánh, vs, nên, top, review)", any(re.search(r"so sánh| vs |nên|top|review|đánh giá|ưu|nhược", h.lower()) for h in h2 + h1), "theo H1/H2"),
                   ("Đủ độ sâu (≥ 1.000 từ)", len(words) >= 1000, f"{len(words)} từ"),
                   ("Có lời mời sang trang tour/đặt", cta, "Zalo/gọi/form" if cta else "không thấy")]
    elif intent == "Mua":
        checks += [("Có giá hiển thị", price, (f"thấy giá «{pm.group(0)}»" if price else "không thấy giá")
                    + (f" · {contact_price} chỗ ghi «Liên hệ» thay vì giá — khách và Google thích giá cụ thể" if contact_price else "")),
                   ("Có nút đặt/liên hệ (Zalo, gọi, form)", cta, "có" if cta else "không thấy"),
                   ("Có schema Product/TouristTrip/Offer hoặc FAQ", bool(set(types) & {"Product", "TouristTrip", "Offer", "FAQPage", "Trip"}), ", ".join(types[:6]) or "không"),
                   ("Có bảng lịch trình/giá hoặc danh sách bao gồm", n_table >= 1 or n_list >= 2, f"{n_table} bảng · {n_list} danh sách")]
    elif intent == "Điều hướng":
        checks += [("Có số điện thoại/hotline dạng chữ", phone, "có" if phone else "không thấy"),
                   ("Có nút liên hệ", cta, "có" if cta else "không thấy"),
                   ("Có schema Organization/LocalBusiness", bool(set(types) & {"Organization", "TravelAgency", "LocalBusiness"}), ", ".join(types[:6]) or "không")]
    passed = sum(1 for _, ok, _ in checks if ok)
    score = round(passed / len(checks) * 100)
    lines = [f"Chấm theo ý định «{intent or 'chưa chọn'}» · {passed}/{len(checks)} tiêu chí · {len(words)} từ"]
    lines += [f"{'✅' if ok else '❌'} {name} — {detail}" for name, ok, detail in checks]
    return score, "\n".join(lines)


# ------------------------------------------------------------------ soi website đối thủ

def scan_site(url: str) -> str:
    if not url.startswith("http"):
        url = "https://" + url
    p = urllib.parse.urlsplit(url)
    base = f"{p.scheme}://{p.netloc}"
    lines = []
    st, body, hd, ttfb = fetch(url)
    if st in (401, 403, 406, 429, 503):
        lines.append(f"⚠ Website chặn truy cập tự động (mã {st}) — các chỉ số trang không đo được. "
                     "Kiểm tay: mở trang bằng trình duyệt, đo tốc độ bằng PageSpeed Insights (pagespeed.web.dev), xem chỉ số bằng Ahrefs/Semrush.")
        try:
            rs, rb, rh, _ = fetch(base + "/robots.txt")
            urls = sitemap_urls(base, decode(rb, rh) if rs == 200 else "", 20000)
            if urls:
                lines.append(f"Sitemap: {'≥ 20.000' if len(urls) >= 20000 else len(urls)} URL")
        except Exception:
            pass
        return "\n".join(lines)
    html = decode(body, hd)
    pp = PageParser()
    try:
        pp.feed(html)
    except Exception:
        pass
    lines.append(f"Trang chủ: mã {st} · phản hồi {round(ttfb * 1000)}ms · HTML {round(len(body) / 1024)}KB · nén {hd.get('content-encoding') or 'không'}")
    lines.append(f"Title ({len(pp.title.strip())} ký tự): {' '.join(pp.title.split())[:120]}")
    md = pp.meta.get("description", "")
    lines.append(f"Meta description: {'có, ' + str(len(md)) + ' ký tự' if md else 'không có'}")
    h1 = [t for tag, t in pp.headings if tag == "h1"]
    lines.append(f"H1: {len(h1)} thẻ{' — ' + h1[0][:80] if h1 else ''}")
    lines.append(f"Mobile viewport: {'có' if 'width=device-width' in pp.meta.get('viewport', '') else 'KHÔNG'}")
    types, same_as, errs = jsonld_types(pp.jsonld)
    lines.append(f"Schema: {', '.join(types[:10]) or 'không có'}{' · có sameAs' if same_as else ''}{' · LỖI JSON-LD' if errs else ''}")
    alts = sorted(set(re.findall(r'<link[^>]+hreflang=["\']([^"\']+)["\']', html, re.I)))
    if alts:
        lines.append("hreflang: " + ", ".join(alts[:10]))
    try:
        rs, rb, rh, _ = fetch(base + "/robots.txt")
        robots = decode(rb, rh) if rs == 200 else ""
        urls = sitemap_urls(base, robots, 20000)
        lines.append(f"Sitemap: {'≥ 20.000' if len(urls) >= 20000 else len(urls)} URL" if urls else "Sitemap: không đọc được")
        if urls:
            blog = [u for u in urls if re.search(r"/(blog|tin-tuc|kinh-nghiem|cam-nang|news|guide)/", u)]
            if blog:
                lines.append(f"  trong đó ~{len(blog)} URL dạng blog/cẩm nang")
    except Exception as e:
        lines.append(f"Sitemap: lỗi ({e})")
    return "\n".join(lines)


# ------------------------------------------------------------------ từ khoá đối thủ

def classify_competitor_kw(dt_rows, rooty_rows) -> dict:
    """So từ khoá đối thủ với bảng Từ khoá của Rooty → {record_id: {trường}}."""
    rooty = {}
    for r in rooty_rows:
        k = " ".join(str(r["fields"].get("Từ khoá", "")).lower().split())
        if k:
            rooty[k] = r["fields"].get("Vị trí")
    out = {}
    for r in dt_rows:
        f = r["fields"]
        k = " ".join(str(f.get("Từ khoá", "")).lower().split())
        pos_r = rooty.get(k)
        pos_d = f.get("Vị trí đối thủ")
        vol = f.get("Lượng tìm") or 0
        ch = {}
        if pos_r in (None, "") or (isinstance(pos_r, (int, float)) and pos_r > 50):
            ch["Phân loại"] = "Gap — Rooty chưa có"
        elif pos_d not in (None, "") and float(pos_r) > float(pos_d):
            ch["Phân loại"] = "Common — đối thủ hơn"
        else:
            ch["Phân loại"] = "Common — Rooty hơn"
        if pos_r not in (None, ""):
            ch["Vị trí Rooty"] = pos_r
        if not f.get("Cơ hội"):
            ch["Cơ hội"] = "Cao" if vol >= 500 and guess_intent(k) in ("Mua", "Cân nhắc") else ("Vừa" if vol >= 100 else "Thấp")
        out[r["record_id"]] = ch
    return out
