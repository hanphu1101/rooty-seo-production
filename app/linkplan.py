"""
Kế hoạch liên kết nội bộ cho MỘT trang đích (VD tour 3 đảo) theo mô hình silo kim tự tháp:

        [Trang đích — trang tour, nơi chốt đơn]        ← sức mạnh dồn lên đây
          ↑                 ↑
   [Danh mục]       [Bài trụ — bài thông tin chính của chủ đề]
          ↑                 ↑   ↑
   [Bài vệ tinh 1] ⇄ [Bài vệ tinh 2] ⇄ [Bài vệ tinh 3] …   ← mỗi bài trả lời 1 câu hỏi con, link lên trụ + đích,
                                                              nối ngang có chọn lọc (bánh xe NHỎ trong cụm)
Không làm "bánh xe / kim tự tháp link" kiểu cũ bằng site vệ tinh bên ngoài (Web 2.0, PBN, tier 2–3): đó là link spam.
"""
from __future__ import annotations

import re
import unicodedata
import urllib.parse
from collections import Counter

GENERIC = re.compile(r"^(đặt ngay!?|tại đây|xem thêm|xem ngay|chi tiết|xem chi tiết|click|bấm vào đây|nhấn vào đây|đây|link|đọc thêm|"
                     r"read more|here|more|tìm hiểu thêm|xem|book now|\[ảnh\].*)$", re.I)
STOP = set("phu quoc tour o tai va cua cho voi nhung cac gi nao co khong la bao nhieu nen di 1 ngay gia".split())
MIX = {"Chính xác": 0.15, "Gần đúng / biến thể": 0.55, "Thương hiệu / URL": 0.10, "Mô tả tự nhiên": 0.20}


def sa(s):
    s = unicodedata.normalize("NFD", s or "").replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def core_tokens(kw):
    return [t for t in re.findall(r"[a-z0-9]+", sa(kw)) if t not in STOP]


def anchor_kind(anchor, kw):
    a = sa(anchor).strip()
    if not a or GENERIC.search(anchor.strip()):
        return "Chung chung"
    if "rooty" in a or "rootytrip" in a or a.startswith("http"):
        return "Thương hiệu / URL"
    k = sa(kw).strip()
    if a == k or a.replace(" phu quoc", "") == k.replace(" phu quoc", ""):
        return "Chính xác"
    ct = core_tokens(kw)
    if ct and all(t in a.split() for t in ct):
        return "Gần đúng / biến thể"
    return "Mô tả tự nhiên"


def related_terms(text):
    """Địa danh / chủ đề con hay đi cùng (Hòn X Y, Bãi X, Nam/Bắc đảo, san hô…) từ nội dung trang đích."""
    found = re.findall(r"\b(?:Hòn|Bãi|Mũi|Làng|Suối|Rạch)\s+[A-ZĐÀ-Ỹ][\wÀ-ỹ]+(?:\s+[A-ZĐÀ-Ỹ][\wÀ-ỹ]+)?", text or "")
    found += re.findall(r"\b(?:Nam|Bắc) đảo\b|\blặn ngắm san hô\b|\bcâu cá\b|\bcano\b", text or "", re.I)
    c = Counter(f.strip() for f in found)
    return [w for w, n in c.most_common(12) if n >= 2]


def build(target, keyword, pages, edges, kw_rows, texts, extra_terms=None, max_sat=12):
    """
    target: URL trang đích · pages: [fields bảng Trang đích] · edges: link nội bộ từ crawl · kw_rows: [fields bảng Từ khoá]
    texts: {url: nội dung bài} (bài tiếng Việt) · extra_terms: chủ đề con người dùng thêm.
    """
    t = target.rstrip("/") + "/"
    by_url = {p.get("URL"): p for p in pages}
    tp = by_url.get(t) or {}
    ct = core_tokens(keyword)
    terms = list(dict.fromkeys([x for x in (extra_terms or []) if x.strip()] + related_terms(texts.get(t, ""))))
    term_a = [sa(x) for x in terms]
    in_content = Counter(e["to"] for e in edges if e.get("zone") == "nội dung")

    # 1 · hiện trạng link vào trang đích
    inbound = [e for e in edges if e["to"] == t]
    cont = [e for e in inbound if e.get("zone") == "nội dung"]
    mix_now = Counter(anchor_kind(e.get("anchor", ""), keyword) for e in cont)

    # 2 · ứng viên vệ tinh: bài viết tiếng Việt cùng chủ đề
    core_re = re.compile(r"(?<![a-z0-9])" + r"\s+".join(map(re.escape, ct)) + r"(?![a-z0-9])") if ct else None

    def rel(p):
        u = p.get("URL", "")
        title = p.get("Tiêu đề") or p.get("H1") or ""
        if p.get("Loại trang") not in ("Bài viết", "Danh mục") or re.search(r"/(en|ru|ko|zh-hans|ja)/", u) or re.match(r"\s*(thông báo|tuyển dụng)", title, re.I):
            return 0
        head = sa(" ".join([title, p.get("H1") or "", u.replace("-", " ")]))
        body = sa(texts.get(u, ""))
        s = 0
        if core_re and core_re.search(head):
            s += 6
        s += 2 * sum(1 for x in set(term_a) if x in head)
        if core_re and body and core_re.search(body):
            s += 2
        s += min(sum(1 for x in set(term_a) if x in body), 3) * 0.5
        return s
    cands = []
    for p in pages:
        r = rel(p)
        if r >= 3:
            auth = in_content.get(p["URL"], 0) + (p.get("GSC lượt nhấp") or 0) / 10
            cands.append((r, auth, p))
    cands.sort(key=lambda x: (-x[0], -x[1]))
    # bài trụ: bài liên quan nhất có tiêu đề chứa đủ từ chính, nhiều link vào nhất
    pillar = next((p for r, a, p in sorted(cands, key=lambda x: (-(x[0] >= 6), -x[1], -x[0])) if r >= 6), None)
    cands = [c for c in cands if c[2].get("Loại trang") == "Bài viết" or c[2] is pillar]
    sats = [p for r, a, p in cands if p is not pillar][:max_sat]
    # danh mục đang chứa trang đích (link từ menu/nội dung của trang danh mục)
    cats = Counter(e["from"] for e in inbound if by_url.get(e["from"], {}).get("Loại trang") == "Danh mục")
    category = cats.most_common(1)[0][0] if cats else None

    # 3 · kho anchor theo loại
    variants = [k.get("Từ khoá") for k in kw_rows if k.get("Từ khoá") and all(x in sa(k["Từ khoá"]).split() for x in ct)
                and not re.search(r"bao nhiêu|nào|gì|không|đâu|nên|ở đâu|review|đánh giá|kinh nghiệm|\?", k["Từ khoá"], re.I)]
    short = re.sub(r"\s*phú quốc\s*", " ", keyword, flags=re.I).strip()
    extra_v = [short, re.sub(r"^tour\s+", "tour cano ", short, flags=re.I)] if short.lower().startswith("tour") else [short]
    pool = {"Chính xác": [keyword],
            "Gần đúng / biến thể": list(dict.fromkeys([v for v in variants if sa(v) != sa(keyword) and len(v.split()) <= 8][:12] + extra_v)),
            "Thương hiệu / URL": [f"{keyword} của Rooty Trip", f"{keyword} Rooty Trip"],
            "Mô tả tự nhiên": [f"lịch trình {keyword} chi tiết", f"giá và lịch trình {keyword}", f"đặt {keyword}"]}
    existing = {(e["from"], e["to"]) for e in edges if e.get("zone") == "nội dung" and anchor_kind(e.get("anchor", ""), keyword) != "Chung chung"}
    generic_only = {(e["from"], e["to"]) for e in edges if e.get("zone") == "nội dung"} - existing

    links = []

    def need(src, dst, role, why):
        if not src or not dst or src == dst:
            return
        g = (src, dst) in generic_only
        links.append({"from": src, "to": dst, "role": role + (" · đổi anchor" if g else ""),
                      "why": ("Đang chỉ link bằng «Đặt ngay!» / ảnh / «xem thêm» — Google không hiểu trang đích nói gì; thêm 1 link chữ mô tả. " if g else "") + why,
                      "has": (src, dst) in existing})
    need(category, t, "Danh mục → Đích", "Trang danh mục giới thiệu tour bằng anchor mô tả, không chỉ nút/ảnh")
    if pillar:
        need(pillar["URL"], t, "Trụ → Đích", "Bài trụ link lên trang tour ngay trong 1/3 đầu bài (đoạn nói về giá/đặt tour)")
        need(t, pillar["URL"], "Đích → Trụ", "Trang tour link về bài trụ cho khách muốn đọc kỹ (kinh nghiệm, nên đi không)")
    for p in sats:
        need(p["URL"], t, "Vệ tinh → Đích", "Bài vệ tinh nhắc tới tour → link lên trang tour, anchor mô tả")
        if pillar:
            need(p["URL"], pillar["URL"], "Vệ tinh → Trụ", "Bài vệ tinh link lên bài trụ cùng chủ đề")
    # nối ngang có chọn lọc: mỗi vệ tinh ↔ 1 vệ tinh gần nhất (cùng địa danh)
    for i, p in enumerate(sats):
        hp = sa((p.get("Tiêu đề") or "") + " " + p["URL"])
        best = None
        for q in sats:
            if q is p:
                continue
            hq = sa((q.get("Tiêu đề") or "") + " " + q["URL"])
            sh = sum(1 for x in term_a if x in hp and x in hq)
            if sh and (not best or sh > best[0]):
                best = (sh, q)
        if best:
            need(p["URL"], best[1]["URL"], "Vệ tinh ⇄ Vệ tinh", "Hai bài cùng địa danh/chủ đề con — nối ngang (tối đa 1–2 link)")

    # 4 · gán anchor theo tỉ lệ mục tiêu + tìm câu đặt link
    from linkbuild import find_sentence
    WIDGET = re.compile(r"[^.!?]{0,140}?\d[\d.,]*\s*(?:đ|₫|vnđ|vnd)[^.!?]{0,60}?(?:đặt ngay|book now)!?", re.I)
    texts = {u: WIDGET.sub(" ", x or "") for u, x in texts.items()}   # bỏ khung giới thiệu tour (ảnh + giá + «Đặt ngay») khi tìm câu
    want = {k: v for k, v in MIX.items()}
    used = Counter({k: mix_now.get(k, 0) for k in MIX})
    rot = {}
    for L in links:
        if L["has"]:
            continue
        if L["to"] != t:
            dst = by_url.get(L["to"], {})
            title = re.split(r"[:?–|]", dst.get("H1") or dst.get("Tiêu đề") or "")[0].strip()
            ppool = [k.get("Từ khoá") for k in kw_rows if k.get("Từ khoá") and all(x in sa(k["Từ khoá"]).split() for x in ct)
                     and re.search(r"review|kinh nghiệm|đánh giá|có nên|nên đi|đáng đi|có gì", k["Từ khoá"], re.I)] if L["to"] == (pillar or {}).get("URL") else []
            ppool += [title] + ([" ".join(title.split()[:5])] if len(title.split()) > 5 else [])
            ppool = list(dict.fromkeys(ppool))
            k0 = rot[L["to"]] = rot.get(L["to"], -1) + 1          # xoay vòng anchor, không lặp một cụm cho mọi link
            ppool = ppool[k0 % len(ppool):] + ppool[:k0 % len(ppool)] if ppool else [title]
            L["anchor"], L["kind"], L["sentence"] = ppool[0], "Mô tả tự nhiên", ""
            for a in ppool:
                hit = find_sentence(texts.get(L["from"], ""), a)
                if hit:
                    L["anchor"], L["sentence"] = hit
                    break
            if not L["sentence"]:
                L["sentence"] = f"[Cần thêm câu] VD: «Nếu còn phân vân, đọc bài {L['anchor']} trước khi đặt tour.»"
            continue
        total = sum(used.values()) + 1
        order = sorted(MIX, key=lambda k: used[k] / total - want[k])   # loại đang thiếu nhiều nhất trước
        placed = False
        for kind in order:
            for a in pool[kind]:
                hit = find_sentence(texts.get(L["from"], ""), a)
                if hit:
                    L.update(anchor=hit[0], kind=kind, sentence=hit[1])
                    used[kind] += 1
                    placed = True
                    break
            if placed:
                break
        if not placed:
            kind = order[0]
            a = (pool[kind] or pool["Mô tả tự nhiên"])[0]
            L.update(anchor=a, kind=kind, sentence=f"[Cần thêm câu] VD: «Nếu muốn đi trong ngày, bạn có thể tham khảo {a} — giá, lịch trình và điểm đón cập nhật.»")
            used[kind] += 1
    summary = {"target": t, "keyword": keyword, "title": tp.get("H1") or tp.get("Tiêu đề") or "",
               "inbound": len(inbound), "inbound_content": len(cont), "inbound_menu": len(inbound) - len(cont),
               "generic": mix_now.get("Chung chung", 0), "mix_now": dict(mix_now), "mix_target": MIX, "mix_after": dict(used),
               "category": category, "pillar": pillar and {"url": pillar["URL"], "title": pillar.get("H1") or pillar.get("Tiêu đề")},
               "satellites": [{"url": p["URL"], "title": p.get("H1") or p.get("Tiêu đề"), "inlinks": in_content.get(p["URL"], 0),
                               "linksTarget": (p["URL"], t) in existing} for p in sats],
               "terms": terms, "links": links,
               "top_anchors": Counter(e.get("anchor", "") for e in cont).most_common(6)}
    return summary
