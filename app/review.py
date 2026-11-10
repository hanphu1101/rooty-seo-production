"""
Bước 10 · Review: nhận diện & xử lý file CSV xuất từ Google Search Console / GA4,
phát hiện xung đột từ khoá, phân loại content audit (giữ / cập nhật / gộp / xoá-noindex), cảnh báo biến động tuần.
"""
from __future__ import annotations

import re
import urllib.parse
from collections import defaultdict


def _h(s):
    return (s or "").strip().lower()


def detect(header: list[str]) -> tuple[str, dict]:
    """→ (loại file, {vai trò: chỉ số cột})"""
    h = [_h(x) for x in header]

    def idx(*pats):
        for i, x in enumerate(h):
            if any(re.search(p, x) for p in pats):
                return i
        return -1
    c = {
        "date": idx(r"^ngày$", r"^date$", r"^ngày ", r"^date "),
        "query": idx(r"truy vấn", r"quer", r"^từ khoá", r"^keyword"),
        "page": idx(r"^trang hàng đầu", r"^top pages", r"^page$", r"^trang$", r"^url$", r"^landing page", r"^trang đích", r"page path", r"đường dẫn trang"),
        "clicks": idx(r"lượt nhấp", r"^clicks", r"nhấp chuột"),
        "impr": idx(r"hiển thị", r"impression"),
        "ctr": idx(r"^ctr"),
        "pos": idx(r"vị trí", r"position"),
        "sessions": idx(r"^phiên", r"^sessions", r"phiên tương tác$"),
        "users": idx(r"người dùng", r"^users", r"total users"),
        "eng": idx(r"tỷ lệ tương tác", r"engagement rate"),
        "time": idx(r"thời gian tương tác", r"engagement time", r"average engagement"),
        "conv": idx(r"sự kiện chính", r"key events", r"chuyển đổi", r"conversions"),
    }
    if c["sessions"] >= 0 and c["page"] >= 0:
        return "ga4_pages", c
    if c["date"] >= 0 and c["clicks"] >= 0:
        return "gsc_dates", c
    if c["query"] >= 0 and c["page"] >= 0 and (c["clicks"] >= 0 or c["impr"] >= 0):
        return "gsc_query_page", c
    if c["page"] >= 0 and (c["clicks"] >= 0 or c["impr"] >= 0):
        return "gsc_pages", c
    if c["query"] >= 0 and (c["clicks"] >= 0 or c["impr"] >= 0):
        return "gsc_queries", c
    return "unknown", c


def num(v, dec=False):
    if v is None:
        return None
    s = str(v).strip().replace("%", "").replace(" ", "")
    if not s or s in ("-", "(not set)"):
        return None
    if re.fullmatch(r"\d{1,2}:\d{2}(:\d{2})?", s):  # 0:01:23 → giây
        parts = [int(x) for x in s.split(":")]
        return sum(p * 60 ** i for i, p in enumerate(reversed(parts)))
    if dec:
        if "," in s and "." not in s:
            s = s.replace(",", ".")
        elif "," in s and "." in s:
            s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    else:
        s = re.sub(r"[.,](?=\d{3}\b)", "", s)
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def norm_url(u: str, site: str) -> str:
    u = (u or "").strip()
    if u.startswith("/"):
        u = site.rstrip("/") + u
    p = urllib.parse.urlsplit(u)
    return (p.netloc.replace("www.", "").lower() + p.path.rstrip("/")).lower()


def parse_date(s: str):
    s = (s or "").strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s) or re.match(r"(\d{4})(\d{2})(\d{2})$", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
    return None


def months_from_dates(rows, c):
    agg = defaultdict(lambda: {"clicks": 0, "impr": 0, "posw": 0.0})
    daily = []
    for r in rows:
        d = parse_date(r[c["date"]]) if c["date"] < len(r) else None
        if not d:
            continue
        cl = num(r[c["clicks"]]) or 0
        im = num(r[c["impr"]]) or 0 if c["impr"] >= 0 else 0
        pos = num(r[c["pos"]], True) if c["pos"] >= 0 else None
        a = agg[d[:7]]
        a["clicks"] += cl
        a["impr"] += im
        if pos:
            a["posw"] += pos * im
        daily.append((d, cl, im))
    out = {}
    for m, a in agg.items():
        out[m] = {"Lượt nhấp": int(a["clicks"]), "Hiển thị": int(a["impr"]),
                  "CTR %": round(a["clicks"] / a["impr"] * 100, 2) if a["impr"] else None,
                  "Vị trí TB": round(a["posw"] / a["impr"], 1) if a["impr"] and a["posw"] else None}
    return out, sorted(daily)


def week_alert(daily):
    """So 7 ngày gần nhất với 7 ngày trước đó."""
    if len(daily) < 14:
        return None
    last, prev = daily[-7:], daily[-14:-7]
    c1, c0 = sum(x[1] for x in last), sum(x[1] for x in prev)
    i1, i0 = sum(x[2] for x in last), sum(x[2] for x in prev)
    ch = lambda a, b: round((a / b - 1) * 100, 1) if b else None
    return {"from": last[0][0], "to": last[-1][0], "clicks": c1, "clicksPrev": c0, "clicksChange": ch(c1, c0),
            "impr": i1, "imprPrev": i0, "imprChange": ch(i1, i0)}


def cannibalization(rows, c, site, min_share=0.1, min_impr=20):
    by_q = defaultdict(list)
    for r in rows:
        q = (r[c["query"]] or "").strip().lower()
        p = r[c["page"]] if c["page"] < len(r) else ""
        if not q or not p:
            continue
        by_q[q].append((p, num(r[c["clicks"]]) or 0 if c["clicks"] >= 0 else 0, num(r[c["impr"]]) or 0 if c["impr"] >= 0 else 0,
                        num(r[c["pos"]], True) if c["pos"] >= 0 else None))
    out = []
    for q, ps in by_q.items():
        tot = sum(x[2] for x in ps)
        if tot < min_impr:
            continue
        ps = [x for x in ps if x[2] / tot >= min_share]
        if len({norm_url(x[0], site) for x in ps}) < 2:
            continue
        ps.sort(key=lambda x: (-x[1], -x[2]))
        out.append({"Từ khoá": q, "Số trang": len(ps), "Hiển thị": int(tot), "Lượt nhấp": int(sum(x[1] for x in ps)),
                    "Trang nên giữ": ps[0][0],
                    "Các URL": "\n".join(f"{x[0]} · {int(x[1])} nhấp · {int(x[2])} hiển thị" + (f" · vị trí {x[3]}" if x[3] else "") for x in ps)})
    return sorted(out, key=lambda x: -x["Hiển thị"])


EXPECTED_CTR = [(1.5, 25), (2.5, 15), (3.5, 10), (5.5, 6), (10.5, 3), (20.5, 1)]


def expected_ctr(pos):
    for lim, v in EXPECTED_CTR:
        if pos <= lim:
            return v
    return 0.5


def classify(f: dict, dup_h1: set) -> tuple[str, str]:
    """Đề xuất content audit cho một trang (dựa trên số liệu GSC/GA4 đã nhập + crawl)."""
    kind = f.get("Loại trang") or ""
    cl, im = f.get("GSC lượt nhấp"), f.get("GSC hiển thị")
    pos, ctr = f.get("GSC vị trí"), f.get("GSC CTR %")
    words = f.get("Số từ") or 0
    eng = f.get("GA4 tương tác %")
    conv = f.get("GA4 chuyển đổi") or 0
    money = kind in ("Trang tour/sản phẩm", "Danh mục", "Trang chủ", "Trang thương hiệu")
    if cl is None and im is None:
        return "Theo dõi", "Chưa có số liệu GSC cho trang này (trang mới, chưa có hiển thị, hoặc file nhập chưa có)"
    cl, im = cl or 0, im or 0
    reasons = []
    if cl >= 30 and (pos is None or pos <= 10) and (eng is None or eng >= 30):
        return "Giữ", f"{int(cl)} lượt nhấp, vị trí {pos or '?'}" + (f", tương tác {eng}%" if eng is not None else "") + (f", {int(conv)} chuyển đổi" if conv else "")
    if im >= 200 and pos and 8 <= pos <= 30:
        reasons.append(f"nhiều hiển thị ({int(im)}) nhưng ở vị trí {pos} — gần top, cập nhật nội dung/thiếu ý so với đối thủ")
    if im >= 200 and pos and ctr is not None and ctr < expected_ctr(pos) * 0.5:
        reasons.append(f"CTR {ctr}% thấp so với mức thường gặp ở vị trí {pos} (~{expected_ctr(pos)}%) — viết lại Title/Meta")
    if eng is not None and eng < 30 and cl >= 10:
        reasons.append(f"tỷ lệ tương tác GA4 thấp ({eng}%) — nội dung chưa đúng ý định")
    if reasons:
        return "Cập nhật / viết lại", "; ".join(reasons)
    if money:
        if cl < 10:
            return "Cập nhật / viết lại", f"trang bán/thương hiệu ít traffic ({int(cl)} nhấp, {int(im)} hiển thị) — tối ưu onpage, thêm link nội bộ"
        return "Theo dõi", f"{int(cl)} nhấp · {int(im)} hiển thị"
    h1 = (f.get("H1") or "").strip().lower()
    if words and words < 300 and cl < 5 and (h1 in dup_h1):
        return "Gộp", f"bài mỏng ({words} từ), {int(cl)} nhấp, trùng chủ đề với bài khác — gộp vào bài mạnh hơn + 301"
    if cl == 0 and im < 50:
        if kind == "Trang tag":
            return "Noindex", f"trang tag không có traffic ({int(im)} hiển thị)"
        if words < 600:
            return "Xoá / 301", f"0 lượt nhấp, {int(im)} hiển thị, {words} từ — xoá và 301 về trang liên quan, hoặc gộp"
        return "Cập nhật / viết lại", f"bài dài ({words} từ) nhưng không có traffic — kiểm ý định tìm kiếm & lập chỉ mục"
    if words and words < 300 and cl < 5:
        return "Gộp", f"bài mỏng ({words} từ), chỉ {int(cl)} nhấp — gộp vào bài cùng chủ đề"
    return "Theo dõi", f"{int(cl)} nhấp · {int(im)} hiển thị · vị trí {pos or '?'}"
