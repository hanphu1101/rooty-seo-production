"""
Chẩn đoán rớt top 4 bước — gom mọi thứ app đã có thành một báo cáo:
① Rớt thật không, từ ngày nào (GSC theo ngày)  ② Trùng đợt cập nhật thuật toán nào (Google Search Status)
③ Kiểm từng giả thuyết trên toàn blog (blogscan: ĐÃ KIỂM / NGHI VẤN) + GEO + chính sách spam
④ Xếp thứ tự việc sửa theo mức liên quan tới kiểu rớt.
Không kết luận "nguyên nhân" khi chưa có số liệu GSC — khi đó chỉ là "lỗi đang có".
"""
from __future__ import annotations

import datetime as dt

# điểm nền: mức nặng của từng loại lỗi với thứ hạng (theo chính sách / tài liệu Google; 3 = cao)
BASE = {"Trùng từ khóa": 3, "Đổi năm giả": 3, "Thiếu trải nghiệm": 2, "Lạc chủ đề": 2, "Tác giả": 1, "Đa ngôn ngữ": 1,
        "Thương mại": 1, "Link tự thân": 1}
# loại đợt → loại lỗi được tăng ưu tiên khi ngày rớt trùng đợt đó
BOOST = {"Spam update": {"Đổi năm giả": 2, "Trùng từ khóa": 2, "Thiếu trải nghiệm": 1, "Lạc chủ đề": 1, "Thương mại": 1},
         "Core update": {"Thiếu trải nghiệm": 2, "Lạc chủ đề": 2, "Trùng từ khóa": 1, "Tác giả": 1, "Đổi năm giả": 1},
         "Helpful content": {"Thiếu trải nghiệm": 2, "Lạc chủ đề": 1}}
WHY = {
    "Trùng từ khóa": "Nhiều bài cùng tranh một nhóm từ khoá → Google không biết chọn bài nào, các bài kéo nhau xuống; nhiều trang na ná nhau còn gần với «trang cửa ngõ» trong chính sách spam.",
    "Đổi năm giả": "Năm mới chỉ nằm trên tiêu đề, thân bài không có thông tin năm đó → thao túng độ mới; dễ bị hạ ở các đợt spam/core.",
    "Thiếu trải nghiệm": "Bài dài nhưng không có trải nghiệm thật → không khác nội dung tổng hợp; core update ưu tiên nội dung có trải nghiệm, thông tin riêng.",
    "Lạc chủ đề": "Bài ngoài phạm vi Phú Quốc làm loãng chủ đề chính của site → giảm độ tin cậy chủ đề (topical authority).",
    "Tác giả": "Một người đứng tên phần lớn bài mọi ngôn ngữ, thiếu xác minh (schema Person, hồ sơ cá nhân) → tín hiệu E-E-A-T yếu.",
    "Đa ngôn ngữ": "Bài ngoại ngữ quá mỏng, bài đã gộp vẫn Published → rác chỉ mục, ảnh hưởng nhỏ.",
    "Thương mại": "Nhiều link/CTA bán hàng trong bài thông tin → trải nghiệm đọc kém; thường không phải nguyên nhân chính.",
    "Link tự thân": "Link trỏ về chính bài — Google gần như bỏ qua; sửa cho sạch, không kỳ vọng tăng hạng.",
}


def _roll(xs, k=7):
    out = []
    for i in range(len(xs)):
        w = xs[max(0, i - k + 1): i + 1]
        out.append(sum(w) / len(w))
    return out


def trend(daily):
    """daily: [(yyyy-mm-dd, clicks, impr)] → mô tả xu hướng & ngày bắt đầu rớt."""
    if not daily or len(daily) < 28:
        return {"ok": False, "text": "Chưa có số liệu GSC theo ngày (cần ≥ 28 ngày) — nhập file «Ngày» ở tab B10 (GSC → Hiệu suất → 6 tháng → Xuất)."}
    daily = sorted(daily)
    days = [d for d, *_ in daily]
    clicks = [c for _, c, _ in daily]
    r = _roll(clicks)
    last28, prev28 = sum(clicks[-28:]), sum(clicks[-56:-28]) if len(clicks) >= 56 else None
    ch28 = round((last28 / prev28 - 1) * 100, 1) if prev28 else None
    peak_i = max(range(len(r) - 7), key=lambda i: r[i]) if len(r) > 14 else 0
    peak, now = r[peak_i], r[-1]
    drop = peak and now < peak * 0.8
    start = None
    if drop:
        for i in range(peak_i, len(r)):
            if r[i] < peak * 0.9:
                start = days[i]
                break
    txt = (f"Số liệu {days[0]} → {days[-1]} ({len(days)} ngày). 28 ngày gần nhất: {int(last28)} lượt nhấp"
           + (f" ({'+' if ch28 > 0 else ''}{ch28}% so 28 ngày trước)" if ch28 is not None else "")
           + f". Đỉnh TB 7 ngày {round(peak, 1)}/ngày quanh {days[peak_i]}, hiện {round(now, 1)}/ngày.")
    if drop:
        txt += f" → RỚT THẬT: giảm {round((1 - now / peak) * 100)}% so với đỉnh, bắt đầu khoảng {start}."
    else:
        txt += " → Không thấy rớt mạnh (hiện ≥ 80% mức đỉnh). Có thể chỉ một số trang/từ khoá rớt — xem B10 · Content audit."
    return {"ok": True, "drop": bool(drop), "start": start, "peak": round(peak, 1), "now": round(now, 1), "ch28": ch28, "text": txt}


def overlap(start, updates, before=10, after=14):
    """Đợt cập nhật có khoảng thời gian chạm vào [start − before, start + after]."""
    if not start:
        return []
    s = dt.date.fromisoformat(start)
    out = []
    for u in updates:
        if not u.get("begin"):
            continue
        b = dt.date.fromisoformat(u["begin"])
        e = dt.date.fromisoformat(u["end"]) if u.get("end") else dt.date.today()
        if b <= s + dt.timedelta(days=after) and e >= s - dt.timedelta(days=before):
            out.append(u)
    return out


def rank(counts, conf, hits):
    kinds_hit = {u["kind"] for u in hits}
    rows = []
    for k, n in counts.items():
        if not n:
            continue
        sc = BASE.get(k, 1) + sum(BOOST.get(kd, {}).get(k, 0) for kd in kinds_hit)
        rows.append((sc, n, k))
    rows.sort(key=lambda x: (-x[0], -x[1]))
    return [{"kind": k, "count": n, "score": sc, "conf": conf.get(k, ""), "why": WHY.get(k, "")} for sc, n, k in rows]


def report(site, tr, updates, hits, scan_stats, conf, ranked, geo, policy, today=None):
    today = today or dt.date.today()
    L = [f"# Chẩn đoán rớt top — {site}", f"_Ngày {today:%d/%m/%Y} · máy chạy tự động · nhãn **[ĐÃ KIỂM]** = đo chính xác, **[NGHI VẤN]** = máy đoán theo dấu hiệu, người đọc lại để xác nhận._", ""]
    L += ["## ① Có rớt thật không?", ("[ĐÃ KIỂM] " if tr["ok"] else "⚠ ") + tr["text"], ""]
    L += ["## ② Trùng đợt cập nhật thuật toán nào?"]
    if not tr.get("start"):
        recent = [u for u in updates if u.get("kind") in ("Core update", "Spam update")][:4]
        L.append("Chưa xác định được ngày bắt đầu rớt nên chưa đối chiếu được. Các đợt core/spam gần nhất: "
                 + "; ".join(f"{u['name']} ({u['begin']} → {u.get('end') or 'đang chạy'})" for u in recent) + ".")
    elif hits:
        L.append("[ĐÃ KIỂM] Ngày bắt đầu rớt " + tr["start"] + " trùng với: " + "; ".join(f"**{u['name']}** ({u['begin']} → {u.get('end') or 'đang chạy'})" for u in hits) + ".")
        kinds = {u["kind"] for u in hits}
        if "Spam update" in kinds:
            L.append("→ Trùng **spam update**: ưu tiên lỗi kiểu thao túng (đổi năm giả, bài na ná nhau / trùng từ khoá, nội dung hàng loạt). Kiểm thêm Search Console → Thao tác thủ công.")
        if "Core update" in kinds:
            L.append("→ Trùng **core update**: ưu tiên chất lượng — trải nghiệm thật, đúng ý định, chủ đề tập trung. Không xoá/viết lại hàng loạt; sửa dần và đo.")
    else:
        L.append(f"[ĐÃ KIỂM] Ngày bắt đầu rớt {tr['start']} KHÔNG trùng đợt cập nhật nào → nghiêng về kỹ thuật (lập chỉ mục, redirect, tốc độ — tab B5), đối thủ vượt lên, hoặc mùa vụ du lịch (so cùng kỳ năm trước).")
    L.append("")
    L += ["## ③ Kiểm từng giả thuyết trên toàn blog",
          f"Quét {scan_stats.get('posts', 0)} bài (" + ", ".join(f"{k} {v}" for k, v in scan_stats.get("by_lang", {}).items()) + ") qua WordPress REST API + HTML công khai.", "",
          "| # | Lỗi | Số bài | Nhãn | Vì sao ảnh hưởng thứ hạng |", "|---|---|---|---|---|"]
    for i, r in enumerate(ranked, 1):
        L.append(f"| {i} | {r['kind']} | {r['count']} | [{r['conf']}] | {r['why']} |")
    a = scan_stats.get("author")
    if a:
        L.append(f"\nTác giả: {a['name']} đứng tên {a['share']}% số bài (" + ", ".join(f"{k} {v}" for k, v in a["langs"].items()) + ").")
    if geo:
        L.append(f"\nGEO (đã chấm {geo['pages']} bài): điểm TB {geo['avg']}/100 · {geo['gate']} bài qua đủ 4 cửa chặn · yếu nhất: {geo['weak']}.")
    if policy:
        L.append("\nChính sách spam có rủi ro: " + "; ".join(f"{n} ({st})" for n, st in policy) + ".")
    L.append("")
    L += ["## ④ Thứ tự sửa đề xuất"]
    for i, r in enumerate(ranked[:6], 1):
        L.append(f"{i}. **{r['kind']}** — {r['count']} bài [{r['conf']}]. Xem «Cần sửa gì» từng dòng ở tab B5 · Sửa lỗi từng trang.")
    L += ["", "Mỗi lần sửa: đổi trạng thái → «Đã sửa» (app tự chụp số liệu GSC làm mốc trước) → sau ≥ 4 tuần nhập GSC mới → «Đo hiệu quả», so với nhóm chưa sửa.",
          "", "## Giới hạn của báo cáo",
          "- " + ("Có số liệu GSC nên ① ② là đo thật." if tr["ok"] else "**Chưa có số liệu GSC theo ngày**: ③ là các lỗi ĐANG CÓ, chưa chứng minh là NGUYÊN NHÂN rớt."),
          "- Nhãn NGHI VẤN cần người đọc lại bài trước khi sửa; máy có thể đoán sai.",
          "- Chưa so trang nào rớt nhiều nhất: cần xuất GSC Trang 2 kỳ (so sánh) — xem B10 · Content audit."]
    return "\n".join(L)
