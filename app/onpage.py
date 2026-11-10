"""
Bước 7 · Tối ưu SEO Onpage — chấm từng trang theo 5 hạng mục: Title · Meta Description · Heading · URL · Hình ảnh.
  quick(row, kw)  — chấm nhanh từ dòng báo cáo crawl (không tải lại trang)
  deep(url, kw)   — tải trang, chấm đủ tiêu chí con + gợi ý Title/Meta
"""
from __future__ import annotations

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

AREAS = ["Title", "Meta", "Heading", "URL chuẩn", "Hình ảnh"]
BRAND = re.compile(r"rooty", re.I)
CTA = re.compile(r"đặt|book|liên hệ|gọi|zalo|xem ngay|khám phá|nhận|ưu đãi|tư vấn|ngay|giá tốt|giảm|chọn", re.I)
STOP_SLUG = {"va", "la", "cua", "thi", "nhung", "cac", "mot", "cho", "voi", "o", "tai", "the", "and", "of"}
GENERIC_IMG = re.compile(r"^(img|image|dsc|dscn|screenshot|screen-shot|photo|pic|untitled|ảnh|anh|z\d{6,}|\d{6,})[-_ ]?\d*$", re.I)
STOP_KW = set("giá bao nhiêu tiền ở đâu có gì không nên kinh nghiệm review là đi thế nào những các và cho tại của một từ với".split())


def strip_accents(s: str) -> str:
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def tokens(s: str) -> list[str]:
    return [t for t in re.findall(r"\w+", (s or "").lower()) if t not in STOP_KW and (len(t) > 1 or t.isdigit())]


def cover(kw: str, text: str) -> float:
    """Tỷ lệ từ chính của từ khoá xuất hiện trong text (so cả có dấu và không dấu)."""
    kt = tokens(kw)
    if not kt:
        return 1.0
    t = (text or "").lower()
    ta = strip_accents(t)
    return sum(1 for k in kt if k in t or strip_accents(k) in ta) / len(kt)


def _c(name, ok, detail):
    return (name, bool(ok), detail)


# ------------------------------------------------------------------ các tiêu chí theo hạng mục

def check_title(title: str, kw: str | None):
    t = " ".join((title or "").split())
    L = len(t)
    out = [_c("Dài 50–60 ký tự (không bị cắt trên Google)", 50 <= L <= 60, f"{L} ký tự")]
    if kw:
        first_half = t[: max(len(t) // 2, 25)]
        out.append(_c("Có từ khoá chính, đặt gần đầu", cover(kw, t) >= 0.6 and cover(kw, first_half) >= 0.5,
                      f"{round(cover(kw, t) * 100)}% từ khoá có trong title · {round(cover(kw, first_half) * 100)}% ở nửa đầu"))
    out.append(_c("Có thương hiệu ở cuối (| Rooty Trip)", bool(BRAND.search(t[-20:])), "có" if BRAND.search(t[-20:]) else "không thấy ở cuối"))
    return out


def check_meta(meta: str, kw: str | None):
    m = " ".join((meta or "").split())
    out = [_c("Dài 120–160 ký tự", 120 <= len(m) <= 160, f"{len(m)} ký tự" if m else "không có meta description")]
    if kw:
        out.append(_c("Chứa từ khoá chính", m and cover(kw, m) >= 0.6, f"{round(cover(kw, m) * 100)}% từ khoá"))
    out.append(_c("Có lời kêu gọi hành động (đặt, xem, liên hệ, ưu đãi…)", bool(CTA.search(m)), (CTA.search(m).group(0) if CTA.search(m) else "không thấy")))
    return out


def check_heading(h1s: list[str], h2s: list[str], title: str, kw: str | None, related: list[str] | None = None):
    out = [_c("Đúng 1 thẻ H1", len(h1s) == 1, f"{len(h1s)} H1")]
    h1 = h1s[0] if h1s else ""
    if kw:
        out.append(_c("H1 chứa từ khoá chính", cover(kw, h1) >= 0.6, f"{round(cover(kw, h1) * 100)}% · «{h1[:70]}»"))
    tt, th = set(tokens(title)), set(tokens(h1))
    sim = len(tt & th) / max(len(th), 1) if th else 0
    out.append(_c("H1 gần giống Title", sim >= 0.5, f"{round(sim * 100)}% từ của H1 có trong Title"))
    content_h2 = [h for h in h2s if h.lower() not in ("tin tức liên quan", "có thể bạn sẽ thích", "bài viết liên quan")]
    out.append(_c("Có ≥ 2 thẻ H2 chia ý chính", len(content_h2) >= 2, f"{len(content_h2)} H2"))
    if kw and content_h2:
        pool = set(tokens(kw)) | {t for r in (related or []) for t in tokens(r)}
        hit = sum(1 for h in content_h2 if set(tokens(h)) & pool)
        out.append(_c("H2 chứa từ khoá phụ / liên quan (≥ 30%)", hit / len(content_h2) >= 0.3, f"{hit}/{len(content_h2)} H2"))
    return out


def check_url(url: str, kw: str | None):
    path = urllib.parse.urlsplit(url).path
    raw = urllib.parse.unquote(path)
    segs = [s for s in raw.strip("/").split("/") if s]
    last = segs[-1] if segs else ""
    words = [w for w in re.split(r"[-_]", last) if w]
    # "3n2d" trong URL = "3 ngày 2 đêm" trong từ khoá
    expanded = set(re.split(r"[-_]", re.sub(r"(\d)n(\d)d", r"\1-ngay-\2-dem", last)))
    out = [
        _c("Không dấu, viết thường", raw == strip_accents(raw).lower() and "%" not in path, raw if raw != strip_accents(raw).lower() else "đạt"),
        _c("Phân cách bằng dấu gạch ngang (-), không gạch dưới/khoảng trắng", "_" not in raw and " " not in raw, "đạt" if "_" not in raw else "có dấu _"),
        _c("Ngắn gọn (≤ 75 ký tự, ≤ 8 từ ở đoạn cuối)", len(raw) <= 75 and len(words) <= 8, f"{len(raw)} ký tự · {len(words)} từ"),
        _c("Không chứa từ dư thừa (va, la, cua, thi…) hoặc ngày tháng", not (set(words) & STOP_SLUG) and not re.search(r"/20\d\d/\d\d/", raw),
           ", ".join(sorted(set(words) & STOP_SLUG)) or ("có ngày tháng" if re.search(r"/20\d\d/\d\d/", raw) else "đạt")),
    ]
    if kw and segs:
        slug_tokens = set(words) | expanded
        kt = [strip_accents(t) for t in tokens(kw) if t not in ("phú", "quốc")] or [strip_accents(t) for t in tokens(kw)]
        hit = sum(1 for t in kt if t in slug_tokens) / max(len(kt), 1)
        out.append(_c("Chứa từ khoá chính", hit >= 0.6, f"{round(hit * 100)}% từ khoá có trong URL"))
    return out


def check_images(imgs: list[tuple[str, str]], kw: str | None, sizes: dict | None = None):
    """imgs: [(src tuyệt đối, alt)]"""
    if not imgs:
        return [_c("Có ảnh minh hoạ", False, "không có ảnh nội dung")]
    names = [urllib.parse.unquote(os.path.basename(urllib.parse.urlsplit(s).path)) for s, _ in imgs]
    stem = [re.sub(r"(-\d+x\d+)?\.\w+$", "", n) for n in names]
    bad_name = [n for n, s in zip(names, stem) if s != strip_accents(s).lower() or "_" in s or " " in s or GENERIC_IMG.match(s)]
    alts = [a for _, a in imgs if a.strip()]
    webp = [s for s, _ in imgs if re.search(r"\.(webp|avif)(\?|$)", s, re.I)]
    out = [
        _c("Tên file không dấu, có gạch ngang, có nghĩa (≥ 90% ảnh)", len(bad_name) / len(imgs) <= 0.1,
           f"{len(imgs) - len(bad_name)}/{len(imgs)} đạt" + (f" · VD chưa đạt: {', '.join(bad_name[:3])}" if bad_name else "")),
        _c("Có thẻ alt (≥ 90% ảnh)", len(alts) / len(imgs) >= 0.9, f"{len(alts)}/{len(imgs)} ảnh có alt"),
    ]
    if kw:
        kw_alt = [a for a in alts if cover(kw, a) >= 0.5]
        stuffed = [a for a in alts if len(re.findall(re.escape(tokens(kw)[0]), a.lower())) > 2] if tokens(kw) else []
        out.append(_c("Alt mô tả ảnh, có từ khoá ở vài ảnh, không nhồi nhét", 1 <= len(kw_alt) and not stuffed,
                      f"{len(kw_alt)} alt chứa từ khoá" + (f" · {len(stuffed)} alt nhồi từ khoá" if stuffed else "")))
    out.append(_c("Định dạng WebP/AVIF (≥ 80% ảnh)", len(webp) / len(imgs) >= 0.8, f"{len(webp)}/{len(imgs)} ảnh"))
    if sizes:
        big = [(u, s) for u, s in sizes.items() if s > 200 * 1024]
        out.append(_c("Dung lượng ≤ 200KB", not big, f"{len(sizes) - len(big)}/{len(sizes)} ảnh mẫu đạt" + (f" · lớn nhất {round(max(s for _, s in big) / 1024)}KB" if big else "")))
    return out


# ------------------------------------------------------------------ tổng hợp

def summarize(groups: dict) -> tuple[dict, int, str]:
    """groups: {hạng mục: [(tên, ok, chi tiết)]} → ({hạng mục: Đạt/Chưa đạt}, điểm, văn bản chi tiết)"""
    res, lines, total, passed = {}, [], 0, 0
    for area, items in groups.items():
        ok = all(i[1] for i in items) if items else False
        res[area] = "Đạt" if ok else "Chưa đạt"
        total += len(items)
        passed += sum(1 for i in items if i[1])
        lines.append(f"■ {area}: {'ĐẠT' if ok else 'CHƯA ĐẠT'}")
        lines += [f"  {'✅' if i[1] else '❌'} {i[0]} — {i[2]}" for i in items]
    return res, round(passed / max(total, 1) * 100), "\n".join(lines)


def quick(row: dict, kw: str | None = None) -> tuple[dict, int]:
    """Chấm nhanh từ báo cáo crawl: Title, Meta, Heading (H1), URL. Ảnh để «Chưa kiểm»."""
    h1 = [row.get("h1", "")] * int(row.get("h1_count") or 0) if row.get("h1_count") not in (None, "", "0") else []
    groups = {
        "Title": check_title(row.get("title", ""), kw),
        "Meta": check_meta(row.get("meta_description", ""), kw),
        "Heading": [i for i in check_heading(h1, [], row.get("title", ""), kw) if not i[0].startswith(("Có ≥ 2", "H2"))],
        "URL chuẩn": check_url(row.get("url", ""), kw),
    }
    res, score, _ = summarize(groups)
    res["Hình ảnh"] = "Chưa kiểm"
    return res, score


def title_case(s: str) -> str:
    # Viết hoa chữ đầu mỗi từ như các title hiện có của Rooty ("Tour Phú Quốc Trọn Gói"), giữ nguyên 3N2Đ/4★
    return " ".join(w if re.search(r"\d", w) else w[:1].upper() + w[1:] for w in s.split())


def suggest_title(kw: str, h1: str) -> str:
    base = title_case((kw or h1 or "").strip())
    tail = " | Rooty Trip"
    extra = [": Giá, Lịch Trình 2026", " 2026: Giá & Kinh Nghiệm", ": Giá & Kinh Nghiệm", " Giá Tốt 2026", ""]
    for e in extra:
        t = base + e + tail
        if 50 <= len(t) <= 60:
            return t
    t = base + tail
    if len(t) <= 60:
        return t
    # quá dài → bỏ phần sau dấu – : , rồi cắt ở ranh giới từ (không dùng dấu …)
    short = re.split(r"\s[–\-:|]\s|,", base)[0].strip()
    if len(short + tail) <= 60 and len(short) >= 15:
        return short + tail
    room = 60 - len(tail)
    cut = base[:room]
    return cut[: cut.rfind(" ")].rstrip(" ,–-:") + tail if " " in cut else cut + tail


def suggest_meta(kw: str, opening: str) -> str:
    """Bản nháp: câu trả lời ngắn từ đoạn mở + lời kêu gọi hành động, 120–160 ký tự. Người viết nên sửa lại."""
    cta = " Đặt qua Zalo để được tư vấn miễn phí."
    room = 158 - len(cta)
    text = " ".join(opening.split())
    sent = re.split(r"(?<=[.!?])\s+", text)
    body = ""
    for s in sent:
        if not re.search(r"[.!?]$", s) or len(body) + len(s) + 1 > room:
            break
        body = (body + " " + s).strip()
    # chỉ dùng câu hoàn chỉnh, có từ khoá, dài vừa đủ; nếu không → mẫu có chỗ trống để người viết điền
    if len(body) < 60 or (kw and cover(kw, body) < 0.6):
        return f"{title_case(kw)}: [1 câu trả lời ngắn — giá từ…, gồm…, thời gian…].{cta}"
    m = (body + cta).strip()
    if len(m) < 120:
        m = m.rstrip(".") + " HDV bản địa, giá tốt."
    return m[:160]


def deep(url: str, kw: str | None, related: list[str] | None = None) -> dict:
    st, body, hd, _ = fetch(url)
    if st != 200:
        return {"error": f"Trang trả mã {st}"}
    html = decode(body, hd)
    p = PageParser()
    try:
        p.feed(html)
    except Exception:
        pass
    title = " ".join(p.title.split())
    meta = p.meta.get("description", "")
    h1 = [t for tag, t in p.headings if tag == "h1"]
    h2 = [t for tag, t in p.headings if tag == "h2"]
    # Chưa gán từ khoá chính → bỏ các tiêu chí phụ thuộc từ khoá (chấm theo H1 dài sẽ trượt oan)
    base_for_title = kw or (h1[0] if h1 else title)
    imgs = []
    for tag in re.findall(r"<img\b[^>]*>", html, re.I):
        src = (re.search(r'\b(?:data-lazy-src|data-src|src)=["\']([^"\']+)["\']', tag) or [None, ""])[1]
        if not src or src.startswith("data:") or src.endswith(".svg") or re.search(r"logo|icon|avatar|flag|emoji|gravatar", src, re.I):
            continue
        alt = (re.search(r'\balt=["\']([^"\']*)["\']', tag) or [None, ""])[1]
        imgs.append((urllib.parse.urljoin(url, src), alt))
    imgs = list(dict.fromkeys(imgs))

    def size(u):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, method="HEAD", headers={"User-Agent": "Mozilla/5.0"}), timeout=15) as r:
                return u, int(r.headers.get("content-length") or 0)
        except Exception:
            return u, 0
    with ThreadPoolExecutor(6) as ex:
        sizes = {u: s for u, s in ex.map(size, [s for s, _ in imgs[:12]]) if s}
    groups = {
        "Title": check_title(title, kw),
        "Meta": check_meta(meta, kw),
        "Heading": check_heading(h1, h2, title, kw, related),
        "URL chuẩn": check_url(url, kw),
        "Hình ảnh": check_images(imgs, kw, sizes),
    }
    res, score, text = summarize(groups)
    opening = " ".join(p.text_after_h1)
    opening = re.sub(r"^.*?(Lượt xem:\s*\d[\d.,]*)", "", opening)  # bỏ khối tác giả/ngày nếu có
    sug_t, sug_m = suggest_title(base_for_title, h1[0] if h1 else ""), suggest_meta(base_for_title, opening)
    kwline = f"Từ khoá chấm: «{kw}»" if kw else "⚠ Trang chưa có từ khoá chính (gán ở cột «Từ khoá chính» hoặc bảng Từ khoá B2/B3) — chưa chấm các tiêu chí về từ khoá"
    head = f"{kwline}\nTitle hiện tại ({len(title)}): {title}\nMeta hiện tại ({len(meta)}): {meta or '—'}\n"
    return {"res": res, "score": score, "detail": head + text, "title": title, "meta": meta,
            "sug_title": sug_t if res["Title"] != "Đạt" else "", "sug_meta": sug_m if res["Meta"] != "Đạt" else ""}
