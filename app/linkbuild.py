"""
Bước 9 · Link building: bản đồ link nội bộ (từ crawl), gợi ý link nội bộ theo câu có sẵn trong bài,
kiểm backlink còn sống, tìm link gãy (broken link building), phân loại anchor.
"""
from __future__ import annotations

import csv
import glob
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0, str(ROOT / "scripts"))
from geo_audit import PageParser, decode, fetch  # noqa: E402
from crawl_site import LinkParser  # noqa: E402

GENERIC = re.compile(r"^(tại đây|xem thêm|xem ngay|chi tiết|xem chi tiết|click|click here|bấm vào đây|nhấn vào đây|đây|link|đọc thêm|read more|here|more|tìm hiểu thêm|xem)$", re.I)


def strip_accents(s: str) -> str:
    s = unicodedata.normalize("NFD", (s or "").replace("đ", "d").replace("Đ", "D"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def latest_links(reports_dir: Path):
    fs = glob.glob(str(reports_dir / "crawl-*.links.tsv"))
    return max(fs, key=os.path.getmtime) if fs else None


def load_edges(reports_dir: Path) -> list[dict]:
    f = latest_links(reports_dir)
    if not f:
        return []
    with open(f, encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def anchor_class(anchor: str, brand="rooty", domain="rootytrip.com") -> str:
    a = (anchor or "").strip().lower()
    if not a or a.startswith("[ảnh]"):
        return "Ảnh / trống"
    if domain in a or a.startswith("http"):
        return "URL"
    if brand in a:
        return "Thương hiệu"
    if GENERIC.match(a):
        return "Chung chung"
    return "Từ khoá / mô tả"


def internal_stats(edges: list[dict]) -> dict:
    content = [e for e in edges if e.get("zone") == "nội dung"]
    generic = [e for e in content if anchor_class(e["anchor"]) == "Chung chung"]
    empty = [e for e in content if anchor_class(e["anchor"]) == "Ảnh / trống"]
    out_content: dict[str, int] = {}
    for e in content:
        out_content[e["from"]] = out_content.get(e["from"], 0) + 1
    heavy = sorted(((u, n) for u, n in out_content.items() if n > 100), key=lambda x: -x[1])
    in_content: dict[str, int] = {}
    for e in content:
        in_content[e["to"]] = in_content.get(e["to"], 0) + 1
    return {"total": len(edges), "content": len(content), "menu_footer": len(edges) - len(content),
            "generic": generic, "empty": empty, "heavy": heavy, "in_content": in_content,
            "zones": {z: sum(1 for e in edges if e.get("zone") == z) for z in {e.get("zone") for e in edges}}}


# ------------------------------------------------------------------ gợi ý link nội bộ

def phrases_for(f: dict) -> list[str]:
    """Các cụm có thể làm anchor cho trang đích: từ khoá chính, rút gọn từ H1."""
    out = []
    if f.get("Từ khoá chính"):
        out.append(f["Từ khoá chính"])
    h = f.get("H1") or f.get("Tiêu đề") or ""
    h = re.sub(r"\(.*?\)", " ", h)
    h = re.split(r"\s[–\-:|]\s|:|,", h)[0]
    h = re.sub(r"\b(\d+n\d+[dđ]|\d+\s*ngày(\s*\d+\s*đêm)?|\d+\s*sao|\d★|20\d\d)\b", " ", h, flags=re.I)
    h = " ".join(h.lower().split())
    if len(h.split()) >= 2:
        out.append(h)
        no_pq = " ".join(re.sub(r"\bphú quốc\b", " ", h).split())
        if len(no_pq.split()) >= 3 and no_pq != h:   # "khách sạn" quá chung → không dùng làm anchor
            out.append(no_pq)
    seen, res = set(), []
    for p in out:
        p = p.lower().strip()
        if p and p not in seen and len(p.split()) >= 2:
            seen.add(p)
            res.append(p)
    return res


END_MARK = re.compile(r"(Tin tức liên quan|Có thể bạn sẽ thích|Bài viết liên quan|Bài viết cùng chủ đề|Related posts)", re.I)


def page_text(url: str) -> str:
    """Chỉ phần thân bài: sau H1, bỏ khối tác giả/ngày/lượt xem, cắt trước khung tin liên quan."""
    st, body, hd, _ = fetch(url)
    if st != 200:
        return ""
    p = PageParser()
    try:
        p.feed(decode(body, hd))
    except Exception:
        pass
    text = unicodedata.normalize("NFC", " ".join(" ".join(p.text_after_h1 or p.body_text).split()))
    m = re.search(r"Lượt xem:\s*[\d.,]+", text[:400])
    if m:
        text = text[m.end():]
    m = END_MARK.search(text)
    if m:
        text = text[:m.start()]
    return text.strip()


def find_sentence(text: str, phrase: str):
    """Tìm câu chứa cụm (không phân biệt dấu/hoa thường). Trả (anchor đúng như trong bài, câu)."""
    text = unicodedata.normalize("NFC", text)
    ta, pa = strip_accents(text).lower(), strip_accents(phrase).lower()
    if len(ta) != len(text):          # phòng ký tự lạ làm lệch vị trí
        return None
    m = re.search(r"(?<!\w)" + re.escape(pa) + r"(?!\w)", ta)   # khớp nguyên cụm, không dính chữ khác
    if not m:
        return None
    i = m.start()
    if strip_accents(text[i:i + len(phrase)]).lower() != pa:
        return None
    s = max(text.rfind(".", 0, i), text.rfind("!", 0, i), text.rfind("?", 0, i)) + 1
    e = min([x for x in (text.find(".", i), text.find("!", i), text.find("?", i)) if x >= 0] or [len(text)])
    sentence = text[s:e + 1].strip()
    if len(sentence) > 260:
        sentence = "…" + text[max(i - 110, 0): i + len(phrase) + 110].strip() + "…"
    return text[i:i + len(phrase)], sentence


def suggest_internal(targets: list[dict], sources: list[str], existing: set, say=lambda m: None, per_target=4, max_sources=220):
    """targets: [{url, phrases}] · sources: URL bài viết · existing: {(from, to)} link đã có."""
    sources = sources[:max_sources]
    say(f"Đọc nội dung {len(sources)} bài viết…")
    with ThreadPoolExecutor(6) as ex:
        texts = dict(zip(sources, ex.map(lambda u: _safe_text(u), sources)))
    out = []
    for t in targets:
        n = 0
        for src, text in texts.items():
            if n >= per_target or not text or src.rstrip("/") == t["url"].rstrip("/"):
                continue
            if (src, t["url"]) in existing or (src.rstrip("/") + "/", t["url"]) in existing:
                continue
            for ph in t["phrases"]:
                hit = find_sentence(text, ph)
                if hit:
                    out.append({"from": src, "to": t["url"], "anchor": hit[0], "sentence": hit[1]})
                    n += 1
                    break
    return out


def _safe_text(u):
    try:
        return page_text(u)
    except Exception:
        return ""


# ------------------------------------------------------------------ backlink

def check_backlink(source: str, target: str) -> dict:
    """Mở trang nguồn, tìm link trỏ tới target (URL hoặc tên miền)."""
    try:
        st, body, hd, _ = fetch(source)
    except Exception as e:
        return {"status": "Lỗi", "detail": f"Không mở được trang nguồn: {e}"}
    if st != 200:
        return {"status": "Lỗi", "detail": f"Trang nguồn trả mã {st}"}
    lp = LinkParser()
    try:
        lp.feed(decode(body, hd))
    except Exception:
        pass
    tdom = urllib.parse.urlsplit(target if target.startswith("http") else "https://" + target).netloc.replace("www.", "")
    tpath = urllib.parse.urlsplit(target).path.rstrip("/") if target.startswith("http") else ""
    hits = []
    for it in lp.items:
        u = urllib.parse.urljoin(source, it["href"])
        p = urllib.parse.urlsplit(u)
        if p.netloc.replace("www.", "") == tdom:
            exact = not tpath or p.path.rstrip("/") == tpath
            hits.append((exact, it, u))
    if not hits:
        return {"status": "Mất link", "detail": f"Không còn link nào tới {tdom} trên trang nguồn"}
    hits.sort(key=lambda x: (not x[0], x[1]["zone"] != "nội dung"))
    exact, it, u = hits[0]
    rel = it["rel"]
    attr = "Nofollow" if re.search(r"nofollow|sponsored|ugc", rel) else "Dofollow"
    zone = {"nội dung": "Trong nội dung", "footer": "Footer", "sidebar": "Sidebar", "menu": "Menu/header"}.get(it["zone"], it["zone"])
    detail = f"Link tới {u} · anchor «{it['anchor'] or '(trống)'}» · {attr}{' (' + rel + ')' if rel else ''} · vị trí: {zone}" + ("" if exact else " · ⚠ trỏ tới URL khác trang đích dự kiến")
    return {"status": "Đang live", "attr": attr, "zone": zone, "anchor": it["anchor"], "detail": detail}


def find_broken(page: str, limit=80, say=lambda m: None) -> list[dict]:
    """Broken link building: link ra ngoài bị gãy trên một trang tài nguyên của website khác."""
    st, body, hd, _ = fetch(page)
    if st != 200:
        raise RuntimeError(f"Trang trả mã {st}")
    lp = LinkParser()
    lp.feed(decode(body, hd))
    host = urllib.parse.urlsplit(page).netloc.replace("www.", "")
    ext, seen = [], set()
    for it in lp.items:
        u = urllib.parse.urljoin(page, it["href"].strip()).split("#")[0]
        p = urllib.parse.urlsplit(u)
        if p.scheme not in ("http", "https") or p.netloc.replace("www.", "") == host or u in seen:
            continue
        if re.search(r"facebook|twitter|x\.com|instagram|youtube|tiktok|linkedin|pinterest|zalo|google\.|apple\.com|t\.me|whatsapp|messenger", p.netloc) \
                or re.search(r"/(share|sharer|intent|dialog)\b|[?&](url|u)=http", u, re.I):
            continue   # bỏ nút chia sẻ / mạng xã hội
        seen.add(u)
        ext.append((u, it["anchor"]))
    ext = ext[:limit]
    say(f"Kiểm {len(ext)} link ra ngoài…")

    def status(u):
        safe = urllib.parse.quote(u, safe=":/?#[]@!$&'()*+,;=%~")
        for method in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(safe, method=method, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=15) as r:
                    return r.status
            except urllib.error.HTTPError as e:
                if method == "HEAD" and e.code in (403, 405, 501):
                    continue
                return e.code
            except urllib.error.URLError as e:
                reason = str(e.reason)
                if re.search(r"getaddrinfo|Name or service not known|nodename nor servname|No address", reason):
                    return "tên miền không còn"
                if method == "GET":
                    return "không xác định"   # SSL, timeout, mạng chập chờn → không kết luận là gãy
            except Exception:
                if method == "GET":
                    return "không xác định"
        return "không xác định"
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda x: (x[0], x[1], status(x[0])), ext))
    return [{"url": u, "anchor": a, "status": s} for u, a, s in res
            if (isinstance(s, int) and s >= 400 and s not in (401, 403, 429)) or s == "tên miền không còn"]


def quality(f: dict) -> int:
    """Điểm chất lượng backlink 0–100: uy tín, liên quan, vị trí, dofollow."""
    dr = f.get("Uy tín (DR/DA)") or 0
    s = min(dr, 80) / 80 * 40
    s += {"Cao": 30, "Vừa": 18, "Thấp": 5}.get(f.get("Liên quan chủ đề"), 0)
    s += {"Trong nội dung": 20, "Hồ sơ/bio": 10, "Sidebar": 6, "Footer": 4, "Menu/header": 6}.get(f.get("Vị trí đặt"), 0)
    s += 10 if f.get("Thuộc tính") == "Dofollow" else 3
    return round(s)
