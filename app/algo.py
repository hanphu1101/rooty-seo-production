"""
Theo dõi thuật toán Google từ nguồn CHÍNH THỨC:
- Google Search Status Dashboard (status.search.google.com/incidents.json): ngày bắt đầu / kết thúc mỗi đợt core update, spam update, sự cố.
- Blog Google Search Central (developers.google.com/search/blog/feed.xml): thông báo chính sách, tính năng mới.
Đo ảnh hưởng mỗi đợt lên rootytrip.com bằng số liệu GSC theo ngày đã nhập ở B10.
Kèm danh sách chính sách spam của Google (developers.google.com/search/docs/essentials/spam-policies) → checklist "lên top không vi phạm".
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import urllib.request
from xml.etree import ElementTree as ET

UA = "Mozilla/5.0 (compatible; RootySEO/1.0)"
INCIDENTS = "https://status.search.google.com/incidents.json"
DASHBOARD = "https://status.search.google.com/"
BLOG = "https://developers.google.com/search/blog/feed.xml"
POLICY_URL = "https://developers.google.com/search/docs/essentials/spam-policies"

KINDS = ["Core update", "Spam update", "Discover update", "Reviews update", "Helpful content", "Sự cố hệ thống", "Khác"]
TODO = {
    "Core update": "Đang triển khai: KHÔNG sửa vội, thứ hạng còn dao động. Xong 1–2 tuần: so GSC 2 kỳ (trước/sau đợt) theo trang & truy vấn → trang giảm: đọc lại theo tiêu chí nội dung hữu ích (trải nghiệm thật, đúng ý định, thông tin cập nhật thật, tác giả rõ ràng), so với trang vừa lên top thay mình. Không xoá/viết lại hàng loạt chỉ vì một đợt.",
    "Spam update": "Nếu traffic giảm rõ sau đợt: rà checklist «Chính sách spam» ở tab này (link mua/đổi, nội dung sản xuất hàng loạt, nhồi từ khoá, trang doorway, đổi ngày giả) và GSC → Bảo mật & Thao tác thủ công. Không giảm → không cần làm gì.",
    "Discover update": "Chỉ ảnh hưởng Google Discover (không phải kết quả tìm kiếm). Xem GSC → Discover; ảnh lớn ≥ 1200px, tiêu đề không giật tít.",
    "Reviews update": "Bài review/so sánh: cần trải nghiệm thật, ảnh tự chụp, ưu/nhược cụ thể, so sánh có tiêu chí.",
    "Helpful content": "Rà các bài viết cho máy tìm kiếm hơn là cho người đọc: bài tổng hợp chung chung, thiếu trải nghiệm thật (xem mục Sửa lỗi từng trang ở B5).",
    "Sự cố hệ thống": "Sự cố kỹ thuật của Google (thu thập/lập chỉ mục/hiển thị). Số liệu GSC những ngày này có thể lệch — không kết luận và không sửa site vì nó.",
    "Khác": "Đọc thông báo gốc, ghi việc liên quan Rooty (nếu có).",
}


def _get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def kind_of(name: str, service: str = "") -> str:
    n = (name or "").lower()
    if "core update" in n:
        return "Core update"
    if "spam" in n:
        return "Spam update"
    if "discover" in n:
        return "Discover update"
    if "review" in n:
        return "Reviews update"
    if "helpful" in n:
        return "Helpful content"
    if (service or "").lower() != "ranking" or re.search(r"issue|experiencing|indexing|crawling|serving", n):
        return "Sự cố hệ thống"
    return "Khác"


def _d(s):
    return s[:10] if s else ""


def fetch_updates() -> list[dict]:
    data = json.loads(_get(INCIDENTS))
    out = []
    for x in data:
        upd = x.get("most_recent_update") or {}
        out.append({"id": x.get("id"), "name": x.get("external_desc") or "", "kind": kind_of(x.get("external_desc"), x.get("service_name")),
                    "begin": _d(x.get("begin")), "end": _d(x.get("end")), "done": bool(x.get("end")),
                    "service": x.get("service_name") or "", "url": DASHBOARD + (x.get("uri") or ""),
                    "note": " ".join((upd.get("text") or "").split())[:900]})
    return out


RELEVANT = re.compile(r"update|ranking|spam|policy|policies|core|helpful|review|ai overview|ai mode|structured data|schema|search console|"
                      r"robots|crawl|index|sitemap|page experience|core web vitals|e-e-a-t|quality|deprecat|local|travel|hotel|image", re.I)
HIGH = re.compile(r"core update|spam|policy|policies|ranking|helpful|ai overview|ai mode|deprecat", re.I)


def fetch_blog(limit=30) -> list[dict]:
    root = ET.fromstring(_get(BLOG))
    out = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        desc = html.unescape(re.sub(r"<[^>]+>", " ", it.findtext("description") or ""))
        desc = " ".join(desc.split())
        try:
            date = dt.datetime.strptime((it.findtext("pubDate") or "")[:16], "%a, %d %b %Y").date().isoformat()
        except ValueError:
            date = ""
        txt = title + " " + desc
        rel = "Cao" if HIGH.search(txt) else ("Vừa" if RELEVANT.search(txt) else "Thấp")
        out.append({"title": title, "link": (it.findtext("link") or "").strip(), "date": date, "desc": desc[:700], "rel": rel})
        if len(out) >= limit:
            break
    return out


def impact(daily: list, begin: str, end: str, window=14) -> dict:
    """So lượt nhấp/hiển thị TB/ngày của `window` ngày trước khi đợt bắt đầu với `window` ngày sau khi đợt kết thúc."""
    if not daily or not begin:
        return {"status": "Chưa có số liệu", "text": "Chưa nhập GSC theo ngày (B10 · file Ngày)"}
    if not end:
        return {"status": "Đang triển khai", "text": "Đợt chưa xong — đo sau khi Google báo hoàn tất"}
    b = dt.date.fromisoformat(begin)
    e = dt.date.fromisoformat(end)
    by = {r[0]: r for r in daily}
    pre = [by[(b - dt.timedelta(days=i)).isoformat()] for i in range(1, window + 1) if (b - dt.timedelta(days=i)).isoformat() in by]
    post = [by[(e + dt.timedelta(days=i)).isoformat()] for i in range(1, window + 1) if (e + dt.timedelta(days=i)).isoformat() in by]
    if len(pre) < window * 0.6 or len(post) < window * 0.6:
        return {"status": "Chưa có số liệu", "text": f"Thiếu số liệu GSC quanh đợt (có {len(pre)} ngày trước, {len(post)} ngày sau; cần ≥ {int(window * 0.6)} mỗi bên)"}
    c0, c1 = sum(x[1] for x in pre) / len(pre), sum(x[1] for x in post) / len(post)
    i0, i1 = sum(x[2] for x in pre) / len(pre), sum(x[2] for x in post) / len(post)
    ch = lambda a, z: round((z / a - 1) * 100, 1) if a else None
    cc, ic = ch(c0, c1), ch(i0, i1)
    if cc is None:
        st = "Chưa có số liệu"
    elif cc <= -10:
        st = "Giảm"
    elif cc >= 10:
        st = "Tăng"
    else:
        st = "Không đáng kể"
    return {"status": st, "before": round(c0, 1), "after": round(c1, 1), "clicks": cc, "impr": ic,
            "text": f"Lượt nhấp TB/ngày {round(c0, 1)} → {round(c1, 1)} ({'+' if (cc or 0) > 0 else ''}{cc}%) · hiển thị {'+' if (ic or 0) > 0 else ''}{ic}% "
                    f"(so {len(pre)} ngày trước khi bắt đầu với {len(post)} ngày sau khi xong). Du lịch có mùa vụ — so thêm cùng kỳ năm trước trước khi kết luận."}


# ------------------------------------------------------------------ chính sách spam của Google → checklist cho Rooty
# (tên gốc theo trang chính sách; phần giải thích & rủi ro là tóm tắt riêng cho Rooty Trip)
POLICIES = [
    ("scaled-content", "Scaled content abuse", "Nội dung sản xuất hàng loạt", "Tạo rất nhiều trang chủ yếu để kéo thứ hạng, ít giá trị cho người đọc — bằng AI, ghép/xào nội dung, hay cách nào cũng vậy.",
     "Viết bài AI hàng loạt theo danh sách từ khoá, bài tổng hợp chung chung không có trải nghiệm thật, nhân bản bài sang 5 ngôn ngữ mà không biên tập.",
     "B5 · Sửa lỗi từng trang (Thiếu trải nghiệm) · GEO #20 «Thông tin riêng Rooty» · mọi bài AI viết phải qua Cổng 2–4."),
    ("link-spam", "Link spam", "Link spam (mua/bán/đổi link)", "Mua hoặc bán link để tăng thứ hạng, trao đổi link quá mức, link tự động, anchor nhồi từ khoá, link ẩn trong widget/footer của site khác.",
     "Mua bài PR/guest post có link dofollow mà không gắn rel=sponsored, đổi link với đại lý tour, PBN, comment/forum spam.",
     "B9 · Liên kết: backlink có chi phí phải là Nofollow/sponsored; anchor chính xác từ khoá ≤ 30%."),
    ("doorways", "Doorway abuse", "Trang cửa ngõ (doorway)", "Nhiều trang gần giống nhau nhắm từng biến thể từ khoá / địa điểm, cùng dẫn khách về một đích.",
     "Hàng loạt bài «khách sạn gần X / gần Y / ở Z» na ná nhau; landing page cho từng tỉnh khởi hành chỉ khác tên tỉnh.",
     "B5 · Sửa lỗi từng trang (Trùng từ khoá) · B10 · Xung đột từ khoá."),
    ("keyword-stuffing", "Keyword stuffing", "Nhồi từ khoá", "Lặp từ khoá hoặc danh sách địa danh/số điện thoại không tự nhiên để thao túng thứ hạng.",
     "Lặp «tour Phú Quốc giá rẻ» nhiều lần trong một đoạn, khối danh sách từ khoá cuối bài, alt ảnh toàn từ khoá.",
     "B7 · Onpage (đọc lại title/H1/alt) — đọc to đoạn văn, thấy gượng là nhồi."),
    ("hidden-text-and-links", "Hidden text and link abuse", "Chữ / link ẩn", "Chữ hoặc link chỉ để máy đọc: trùng màu nền, cỡ chữ 0, giấu sau ảnh, đẩy ra ngoài màn hình.",
     "Đoạn từ khoá trắng trên nền trắng, link ẩn trong footer theme mua sẵn.",
     "Kiểm tay theme/footer; Ctrl+A trên trang xem có chữ lạ."),
    ("cloaking", "Cloaking", "Cloaking (hiện khác cho Google và người dùng)", "Cho Google thấy nội dung khác với người đọc thấy.",
     "Plugin/caching trả trang khác cho Googlebot; trang chỉ hiện giá khi là bot.",
     "GSC → Kiểm tra URL → Xem trang đã thu thập, so với trang thật."),
    ("sneaky-redirects", "Sneaky redirects", "Chuyển hướng lén", "Chuyển người dùng sang trang khác với trang Google đã thấy (VD chỉ chuyển khách vào từ điện thoại).",
     "Redirect theo thiết bị/quốc gia sang trang đặt tour đối tác.",
     "B5 · crawl (redirect) — mọi 301 phải về trang cùng chủ đề."),
    ("expired-domains", "Expired domain abuse", "Lạm dụng tên miền hết hạn", "Mua tên miền cũ có uy tín rồi đặt nội dung không liên quan để ăn thứ hạng.",
     "Mua domain du lịch cũ rồi 301 hoặc đặt bài trỏ link về rootytrip.com.", "Không làm. Kiểm khi được chào bán «domain có backlink»."),
    ("site-reputation", "Site reputation policy", "Lạm dụng uy tín site", "Đăng nội dung bên thứ ba trên site có uy tín chủ yếu để hưởng thứ hạng của site đó.",
     "Cho đối tác đặt bài quảng cáo không liên quan trên rootytrip.com; thuê đăng bài lên báo lớn trong chuyên mục «coupon/đối tác» chỉ để lấy link.",
     "Bài đối tác trên site phải do Rooty biên tập, đúng chủ đề Phú Quốc."),
    ("thin-affiliate-pages", "Thin affiliation", "Trang tiếp thị liên kết mỏng", "Trang chỉ chép mô tả sản phẩm/link đặt phòng từ nơi khác, không thêm giá trị.",
     "Bài review khách sạn chỉ chép mô tả từ Agoda/Booking kèm link đặt.", "Bài review cần ảnh tự chụp, trải nghiệm thật, ưu/nhược cụ thể."),
    ("scraped-content", "Scraping", "Sao chép nội dung", "Lấy nội dung từ site khác (kể cả sửa nhẹ / dịch / spin) mà không thêm giá trị riêng.",
     "Chép bảng giá, lịch trình của Sun World/Vinpearl hay của đại lý khác; dịch bài nước ngoài.",
     "Cổng 3 (kiểm chứng): số liệu ghi nguồn, viết lại bằng trải nghiệm của Rooty."),
    ("user-generated-spam", "User-generated spam", "Spam do người dùng tạo", "Bình luận, hồ sơ, diễn đàn bị spam chèn link.",
     "Bình luận WordPress đầy link lạ.", "Bật duyệt bình luận, gắn rel=ugc, chặn spam (Akismet)."),
    ("hacked-content", "Hacked content", "Nội dung bị hack", "Site bị chèn trang/link/mã độc mà chủ site không biết.",
     "Plugin WordPress cũ bị chèn trang cờ bạc, link ẩn.", "GSC → Bảo mật; cập nhật WordPress/plugin; crawl thấy URL lạ thì báo ngay."),
    ("malicious-practices", "Malicious practices", "Hành vi độc hại", "Phần mềm độc hại, quảng cáo lừa tải, thay đổi trình duyệt người dùng.", "Mã quảng cáo/plugin lạ.", "GSC → Bảo mật."),
    ("misleading-functionality", "Misleading functionality", "Tính năng gây hiểu nhầm", "Hứa một dịch vụ/công cụ nhưng dẫn khách tới quảng cáo hoặc thứ khác.",
     "Nút «Tra giá tour» dẫn sang form thu số điện thoại không có giá.", "Mọi nút/công cụ làm đúng như tên."),
    ("machine-generated-traffic", "Machine-generated traffic", "Truy vấn tự động vào Google", "Gửi truy vấn tự động hàng loạt tới Google (VD tool check thứ hạng cào Google không qua API).",
     "Dùng tool tự gõ Google hàng nghìn lần/ngày để check vị trí, hoặc thuê click giả.", "Dùng GSC / công cụ có API chính thức; không thuê click."),
    ("policy-circumvention", "Policy circumvention", "Lách chính sách", "Cố tình lách các chính sách trên (VD lập site/domain mới để tiếp tục làm điều đã bị phạt).", "—", "Không làm."),
    ("scam-and-fraud", "Scam and fraud", "Lừa đảo", "Mạo danh doanh nghiệp, dịch vụ giả, hứa hẹn sai sự thật.", "Giá «từ 99k» không có thật, giả làm đơn vị chính thức của Sun World.",
     "Giá trên web phải đặt được thật; ghi rõ Rooty là đại lý/đơn vị lữ hành."),
]

# không phải chính sách spam nhưng Google xếp vào nhóm làm giảm chất lượng → Rooty đang dính
EXTRA = [
    ("fake-freshness", "Freshness manipulation (không phải chính sách spam riêng — thuộc nhóm thao túng)", "Đổi năm / ngày cập nhật giả",
     "Chỉ đổi năm trên tiêu đề hoặc ngày cập nhật mà nội dung không đổi để trông «mới».",
     "Đổi «2025» thành «2026» trên tiêu đề hằng năm mà không cập nhật giá, lịch, thông tin trong bài.",
     "B5 · Sửa lỗi từng trang (Đổi năm giả) · GEO #22."),
]


def policy_seed():
    rows = [{"Chính sách": vi, "Tên gốc": en, "Mã": code, "Nhóm": "Chính sách spam", "Nghĩa là gì": what, "Rủi ro với Rooty": risk,
             "Cách kiểm": how, "Trạng thái": "Chưa kiểm", "Nguồn": f"{POLICY_URL}#{code}"} for code, en, vi, what, risk, how in POLICIES]
    rows += [{"Chính sách": vi, "Tên gốc": en, "Mã": code, "Nhóm": "Thao túng khác", "Nghĩa là gì": what, "Rủi ro với Rooty": risk,
              "Cách kiểm": how, "Trạng thái": "Chưa kiểm", "Nguồn": POLICY_URL} for code, en, vi, what, risk, how in EXTRA]
    return rows
