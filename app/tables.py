"""
Các bảng dữ liệu theo 10 bước SEO (Discovery → Improving → Create & Optimize → Promotion → Evaluate),
dữ liệu mẫu, và hàm nạp dữ liệu từ báo cáo crawl / GEO audit.
"""
from __future__ import annotations

import csv
import glob
import os
import re
from pathlib import Path


def F(name, kind="text", options=None):
    """kind: text · long · url · select · num · dec · date"""
    return {"n": name, "k": kind, "o": options}


JOURNEY = ["Nhận thức", "Cân nhắc", "Quyết định", "Sử dụng & giữ chân", "Trung thành & giới thiệu"]
EMOTION = ["😀 Hào hứng", "🙂 Hài lòng", "😐 Phân vân", "😟 Lo lắng", "😡 Bực bội"]
DATA_SOURCES = ["Phỏng vấn sale/CSKH", "Phỏng vấn HDV", "Khảo sát khách", "Tin nhắn Zalo/Fanpage", "Đánh giá Google/Tripadvisor",
                "Dữ liệu đặt tour/CRM", "GA4", "Search Console", "Mạng xã hội/nhóm du lịch", "Đối thủ/OTA", "Báo cáo ngành"]
INTENT = ["Thông tin", "Điều hướng", "Cân nhắc", "Mua"]
CONTENT_TYPES = ["Cẩm nang điểm đến", "Bảng giá", "So sánh", "Lịch trình", "Danh sách", "Trang tour/combo", "Trang thương hiệu", "FAQ"]
PAGE_KIND = ["Trang chủ", "Danh mục", "Trang tour/sản phẩm", "Bài viết", "Trang thương hiệu", "Trang tag", "Ngôn ngữ khác", "Khác"]
SILO_ROLE = ["Pillar (trụ cột)", "Cluster (vệ tinh)", "Trang sản phẩm", "Khác"]
GEO_POINTS = ["G0 · Chấm mức & số nền", "G1 · Cho máy đọc được", "G2 · Website là nguồn sự thật", "G3 · Cấu trúc đoạn trong bài",
              "G4 · Được nhắc ở nơi khác", "G5 · Đo → báo cáo"]
GEO_STATUS = ["Chưa làm", "Đang làm", "Đạt", "Chưa đạt", "Không áp dụng"]
AI_ENGINES = ["ChatGPT", "Gemini", "Google AI Overview", "Google AI Mode", "Perplexity", "Copilot", "Claude"]
PROFILE_GROUPS = ["Website chính", "Mạng xã hội", "Xác thực bên thứ ba", "Danh bạ & citation", "OTA & đánh giá"]
PROFILES = [
    ("Website rootytrip.com", "Website chính"),
    ("Facebook Page", "Mạng xã hội"), ("YouTube", "Mạng xã hội"), ("Instagram", "Mạng xã hội"), ("TikTok", "Mạng xã hội"),
    ("LinkedIn công ty", "Mạng xã hội"), ("X (Twitter)", "Mạng xã hội"), ("Pinterest", "Mạng xã hội"), ("Zalo OA", "Mạng xã hội"),
    ("Google Business Profile", "Xác thực bên thứ ba"), ("Bing Places", "Xác thực bên thứ ba"),
    ("Apple Business Connect", "Xác thực bên thứ ba"), ("Wikidata", "Xác thực bên thứ ba"),
    ("Trang Vàng Việt Nam", "Danh bạ & citation"), ("Danh bạ doanh nghiệp lữ hành (Cục Du lịch Quốc gia)", "Danh bạ & citation"),
    ("Foursquare", "Danh bạ & citation"),
    ("Tripadvisor", "OTA & đánh giá"), ("Klook", "OTA & đánh giá"), ("Traveloka", "OTA & đánh giá"),
]
SEED_TYPES = ["Tên sản phẩm", "Thương hiệu", "Tính năng / đặc điểm", "Nhu cầu cốt lõi", "Địa điểm"]
CHECK = ["Đạt", "Chưa đạt", "Chưa kiểm"]
PRIORITY = ["Cao", "Vừa", "Thấp"]
AUDIT_AREAS = ["Technical SEO", "Silo", "UX/UI", "Onsite", "Entity"]
TECH_GROUPS = ["Crawl & index", "Robots & sitemap", "HTTPS & bảo mật", "Mã lỗi & redirect", "Tốc độ & CWV", "Mobile", "Schema",
               "Đa ngôn ngữ", "Bot AI", "Log & giám sát",
               "Phân cấp", "Topical map & phễu", "Liên kết nội bộ",
               "Điều hướng", "CTA & chuyển đổi", "Hành vi người dùng (GA4)", "Di động",
               "Thẻ meta & heading", "Chất lượng nội dung", "Hình ảnh & media",
               "NAP", "Schema thực thể", "Social & citation"]

# Checklist audit 5 hạng mục: (mã, mục, hạng mục, nhóm, mức, tự động?, cách kiểm / cách sửa)
TECH_CHECKLIST = [
    # ===== 1. TECHNICAL SEO
    ("T01", "robots.txt tồn tại và trả mã 200", "Technical SEO", "Robots & sitemap", "🔴 Cao", True, "Mở /robots.txt. Thiếu → tạo bằng plugin SEO (Rank Math/Yoast)."),
    ("T02", "robots.txt không chặn toàn site, CSS, JS, ảnh", "Technical SEO", "Robots & sitemap", "🔴 Cao", True, "Không có 'Disallow: /' cho Googlebot; không chặn /wp-content/, /wp-includes/ (Google cần CSS/JS để hiển thị trang)."),
    ("T03", "robots.txt khai báo Sitemap", "Technical SEO", "Robots & sitemap", "🟢 Thấp", True, "Thêm dòng 'Sitemap: https://rootytrip.com/sitemap_index.xml'."),
    ("T04", "Sitemap XML tồn tại và đọc được", "Technical SEO", "Robots & sitemap", "🔴 Cao", True, "Bật sitemap trong plugin SEO; gửi lên Search Console."),
    ("T05", "Sitemap chỉ chứa URL trả mã 200 (không redirect/404)", "Technical SEO", "Robots & sitemap", "🟡 Vừa", True, "Kiểm 25 URL mẫu trong sitemap. URL lỗi/redirect → loại khỏi sitemap hoặc sửa."),
    ("T28", "Trang chủ không có meta robots noindex/nofollow", "Technical SEO", "Crawl & index", "🔴 Cao", True, "WordPress → Cài đặt → Đọc: bỏ tick 'Ngăn chặn công cụ tìm kiếm'; kiểm plugin SEO."),
    ("T10", "Trang không tồn tại trả đúng mã 404 (không soft-404)", "Technical SEO", "Mã lỗi & redirect", "🟡 Vừa", True, "Thử một URL ngẫu nhiên. Trả 200 → sửa theme/plugin để trả 404."),
    ("T11", "Trang chủ có canonical tự trỏ", "Technical SEO", "Crawl & index", "🟡 Vừa", True, "Plugin SEO tự thêm; kiểm không bị trỏ sang URL khác."),
    ("T12", "Không còn trang lỗi 4xx/5xx được link nội bộ trỏ tới", "Technical SEO", "Mã lỗi & redirect", "🔴 Cao", True, "Từ báo cáo crawl. Sửa link hoặc 301 (xem tab Danh sách lỗi)."),
    ("T13", "Không còn link nội bộ trỏ vào URL đã redirect 301/302", "Technical SEO", "Mã lỗi & redirect", "🟡 Vừa", True, "Từ báo cáo crawl. Sửa link trỏ thẳng URL đích."),
    ("T14", "Không có chuỗi/vòng lặp redirect", "Technical SEO", "Mã lỗi & redirect", "🟡 Vừa", True, "Từ báo cáo crawl: A → B → C phải sửa thành A → C; vòng lặp A → B → A phải gỡ."),
    ("T16", "Canonical không trỏ lệch sang URL khác", "Technical SEO", "Crawl & index", "🟡 Vừa", True, "Từ báo cáo crawl. Trang chính phải canonical tự trỏ."),
    ("T06", "http:// chuyển 301 sang https:// (SSL)", "Technical SEO", "HTTPS & bảo mật", "🔴 Cao", True, "Bật chuyển hướng HTTPS ở hosting/Cloudflare (Always Use HTTPS)."),
    ("T07", "www và không-www về một bản duy nhất (301)", "Technical SEO", "HTTPS & bảo mật", "🟡 Vừa", True, "Trỏ DNS cho bản phụ và 301 về bản chính."),
    ("T08", "Bật HSTS", "Technical SEO", "HTTPS & bảo mật", "🟢 Thấp", True, "Thêm header Strict-Transport-Security (Cloudflare → SSL/TLS → Edge Certificates → HSTS)."),
    ("T09", "Không có nội dung http:// lẫn trong trang https (mixed content)", "Technical SEO", "HTTPS & bảo mật", "🟡 Vừa", True, "Đổi link ảnh/script sang https (plugin Better Search Replace)."),
    ("T17", "Thời gian phản hồi máy chủ trang chủ < 350ms", "Technical SEO", "Tốc độ & CWV", "🟡 Vừa", True, "Đo 3 lần lấy trung vị. Chậm → cache trang (LiteSpeed/WP Rocket), CDN, nâng hosting."),
    ("T18", "Bật nén gzip/brotli", "Technical SEO", "Tốc độ & CWV", "🟢 Thấp", True, "Bật ở hosting hoặc Cloudflare."),
    ("T19", "Core Web Vitals MOBILE đạt (LCP ≤ 2,5s · INP ≤ 200ms · CLS ≤ 0,1)", "Technical SEO", "Tốc độ & CWV", "🔴 Cao", True, "PageSpeed Insights (dữ liệu người dùng thật nếu có). Chưa đạt → ảnh WebP, bỏ plugin nặng, trì hoãn JS, cache."),
    ("T27", "Core Web Vitals DESKTOP đạt (LCP ≤ 2,5s · INP ≤ 200ms · CLS ≤ 0,1)", "Technical SEO", "Tốc độ & CWV", "🟡 Vừa", True, "PageSpeed Insights chế độ máy tính."),
    ("M03", "Search Console: báo cáo Core Web Vitals không có URL 'Kém'", "Technical SEO", "Tốc độ & CWV", "🟡 Vừa", False, "GSC → Trải nghiệm → Chỉ số quan trọng về trang web (cả di động và máy tính)."),
    ("T20", "Thân thiện di động: có meta viewport", "Technical SEO", "Mobile", "🔴 Cao", True, "Theme phải có <meta name=viewport content='width=device-width, initial-scale=1'>."),
    ("T23", "JSON-LD hợp lệ (không lỗi cú pháp) trên trang mẫu", "Technical SEO", "Schema", "🟡 Vừa", True, "Kiểm trang chủ + 3 trang trong sitemap. Lỗi → sửa plugin/đoạn chèn tay."),
    ("M07", "Rich Results Test trang tour không lỗi (Product/TouristTrip + giá)", "Technical SEO", "Schema", "🟡 Vừa", False, "search.google.com/test/rich-results với 2–3 trang tour."),
    ("T21", "Thẻ <html lang> đúng ngôn ngữ", "Technical SEO", "Đa ngôn ngữ", "🟢 Thấp", True, "Bản tiếng Việt lang='vi', bản /en/ lang='en'…"),
    ("T22", "hreflang giữa các bản ngôn ngữ + x-default", "Technical SEO", "Đa ngôn ngữ", "🟡 Vừa", True, "Site có /en/, /ja/ → mỗi trang khai báo link rel=alternate hreflang (WPML/Polylang/TranslatePress)."),
    ("T25", "Bot tìm nguồn của AI được phép vào (OAI-SearchBot, PerplexityBot, Claude-SearchBot…)", "Technical SEO", "Bot AI", "🟡 Vừa", True, "Theo robots.txt. Muốn được ChatGPT/Perplexity trích dẫn thì không chặn nhóm này."),
    ("T26", "Bot chạy khi người dùng hỏi được phép vào (ChatGPT-User, Perplexity-User, Claude-User)", "Technical SEO", "Bot AI", "🟡 Vừa", True, "Theo robots.txt."),
    ("M04", "Cloudflare/tường lửa không chặn Googlebot và bot AI", "Technical SEO", "Bot AI", "🟡 Vừa", False, "Cloudflare → Security → Bots / WAF events."),
    ("M01", "Search Console: không có lỗi lập chỉ mục tăng bất thường", "Technical SEO", "Crawl & index", "🔴 Cao", False, "GSC → Trang → 'Lý do trang không được lập chỉ mục'. Ghi số liệu vào Chi tiết."),
    ("M02", "Search Console: sitemap đã gửi, trạng thái Thành công", "Technical SEO", "Robots & sitemap", "🟡 Vừa", False, "GSC → Sơ đồ trang web."),
    ("M05", "Trang tag, phân trang, tìm kiếm nội bộ: noindex hoặc canonical hợp lý", "Technical SEO", "Crawl & index", "🟢 Thấp", False, "Trang tag mỏng → noindex,follow. Phân trang /page/N/ → title riêng, canonical tự trỏ."),
    ("M06", "Rà các trang đang noindex là có chủ đích", "Technical SEO", "Crawl & index", "🟡 Vừa", False, "Lọc noindex trong file crawl CSV; trang tour/bài lõi không được noindex."),
    ("M10", "Đọc log máy chủ 30 ngày: bot vào trang tiền, không phí lượt vào trang rác", "Technical SEO", "Log & giám sát", "🟢 Thấp", False, "Xuất access log, chạy /rooty-ky-thuat đọc log (khoảng tháng 7)."),
    # ===== 2. SILO
    ("S01", "Trang danh mục (tour, combo, vé) nằm ngay tầng 1 — 1 click từ trang chủ", "Silo", "Phân cấp", "🟡 Vừa", True, "Từ crawl: trang danh mục phải có link trực tiếp từ trang chủ/menu."),
    ("T15", "Trang quan trọng nằm trong 3 click từ trang chủ", "Silo", "Phân cấp", "🟡 Vừa", True, "Từ crawl. Trang sâu → đưa vào danh mục/trang Pillar hoặc thêm link từ bài cùng cụm."),
    ("S02", "Có breadcrumb (BreadcrumbList) trên trang tour và bài viết", "Silo", "Phân cấp", "🟡 Vừa", True, "Bật breadcrumb trong Rank Math/Yoast và hiển thị trong theme."),
    ("S03", "URL phản ánh phân cấp, ngắn, không dấu, không ngày tháng", "Silo", "Phân cấp", "🟢 Thấp", False, "VD /tour-phu-quoc-tron-goi/3n2d/. Không đổi URL đang có traffic; nếu đổi phải 301."),
    ("S04", "≥ 80% trang đích đã gán cụm chủ đề (topical map)", "Silo", "Topical map & phễu", "🟡 Vừa", True, "Tab B3 · gán cột Cụm chủ đề cho Trang đích."),
    ("S05", "Mỗi cụm chủ đề có đúng 1 trang Pillar", "Silo", "Topical map & phễu", "🟡 Vừa", True, "Tab B3 · cột Vai trò silo."),
    ("S06", "Đủ nội dung cho cả 3 tầng phễu TOFU – MOFU – BOFU", "Silo", "Topical map & phễu", "🟡 Vừa", True, "TOFU = ý định Thông tin · MOFU = Cân nhắc · BOFU = Mua. Mỗi tầng cần từ khoá đã có trang đích (tab B2/B3)."),
    ("S07", "Không có trang mồ côi (orphan pages)", "Silo", "Liên kết nội bộ", "🟡 Vừa", True, "Từ crawl đầy đủ: trang có trong sitemap nhưng không có link nội bộ nào trỏ tới → gắn link hoặc xử lý ở B5 · Danh sách lỗi."),
    ("S08", "Mọi trang tour/sản phẩm nhận ≥ 5 link nội bộ", "Silo", "Liên kết nội bộ", "🟡 Vừa", True, "Từ crawl. Thêm link từ bài cẩm nang cùng cụm về trang tour (tab B9)."),
    ("S09", "Không có trang nội dung chỉ nhận ≤ 1 link nội bộ", "Silo", "Liên kết nội bộ", "🟢 Thấp", True, "Từ crawl. Lập kế hoạch link theo cụm (tab B9)."),
    # ===== 3. UX/UI
    ("U01", "Menu logic theo cụm (Tour đảo · Tour trong ngày · Combo · Vé · Cẩm nang · Về Rooty)", "UX/UI", "Điều hướng", "🟡 Vừa", False, "Mở web trên máy tính & điện thoại: khách tìm được tour cần trong ≤ 2 lần bấm?"),
    ("U02", "Có thanh tìm kiếm trên website", "UX/UI", "Điều hướng", "🟢 Thấp", True, "Kiểm trang chủ có ô tìm kiếm."),
    ("U03", "Breadcrumb hiển thị cho người đọc (không chỉ trong schema)", "UX/UI", "Điều hướng", "🟢 Thấp", True, "Kiểm trang tour/bài viết có thanh 'Trang chủ › Danh mục › Trang'."),
    ("U04", "Trang tour có nút liên hệ/đặt (Zalo, gọi, Messenger)", "UX/UI", "CTA & chuyển đổi", "🔴 Cao", True, "Kiểm trang tour mẫu có link zalo.me / tel: / m.me. Nút nên cố định ở cuối màn hình di động."),
    ("U05", "Đã cài GA4 / Google Tag Manager", "UX/UI", "Hành vi người dùng (GA4)", "🔴 Cao", True, "Kiểm mã gtag G-… hoặc GTM-… trên trang."),
    ("U06", "GA4: tỷ lệ tương tác & thời gian trên trang của trang tour/bài lõi ở mức tốt", "UX/UI", "Hành vi người dùng (GA4)", "🟡 Vừa", False, "GA4 → Báo cáo → Tương tác → Trang và màn hình: tỷ lệ tương tác (≈ ngược với tỷ lệ thoát), thời gian tương tác TB. Ghi 5 trang tệ nhất."),
    ("U07", "GA4: tìm điểm rớt trên phễu xem trang tour → bấm Zalo/gọi → đặt", "UX/UI", "Hành vi người dùng (GA4)", "🟡 Vừa", False, "GA4 → Khám phá → Khám phá phễu. Cần sự kiện bấm Zalo/gọi/gửi form."),
    ("M09", "Đặt thử tour trên điện thoại: nút hiện ngay, không popup che nội dung", "UX/UI", "Di động", "🔴 Cao", False, "Tự làm trên điện thoại thật, cả Android và iPhone."),
    ("U08", "Di động: chữ ≥ 16px, nút bấm đủ lớn & cách nhau, ảnh không tràn màn hình", "UX/UI", "Di động", "🟡 Vừa", False, "Xem trên điện thoại hoặc Chrome DevTools chế độ điện thoại; PageSpeed Insights mục Khả năng truy cập."),
    # ===== 4. ONSITE
    ("O01", "Title không trùng giữa các trang", "Onsite", "Thẻ meta & heading", "🟡 Vừa", True, "Từ crawl (bỏ qua trang phân trang). Viết title riêng; trùng chủ đề → cân nhắc gộp."),
    ("O02", "Title dài 20–65 ký tự (≥ 90% trang)", "Onsite", "Thẻ meta & heading", "🟢 Thấp", True, "Từ crawl."),
    ("O03", "Có meta description 70–170 ký tự (≥ 90% trang)", "Onsite", "Thẻ meta & heading", "🟡 Vừa", True, "Từ crawl. Viết meta chứa câu trả lời ngắn + lời mời."),
    ("O04", "Mỗi trang đúng 1 thẻ H1", "Onsite", "Thẻ meta & heading", "🟡 Vừa", True, "Từ crawl. Logo/tiêu đề phụ không dùng H1."),
    ("O05", "H2/H3 là câu hỏi khách thật sự hỏi, theo từ khoá mục tiêu", "Onsite", "Thẻ meta & heading", "🟡 Vừa", True, "Từ GEO audit (tỷ lệ H2 dạng câu hỏi)."),
    ("O12", "Đoạn mở đầu trả lời thẳng — không bị khối tác giả/ngày chen giữa H1 và nội dung", "Onsite", "Chất lượng nội dung", "🔴 Cao", True, "Từ GEO audit. Sửa template bài viết."),
    ("O06", "Không có trang nội dung mỏng (< 300 từ)", "Onsite", "Chất lượng nội dung", "🟢 Thấp", True, "Từ crawl. Bổ sung, gộp hoặc noindex."),
    ("O07", "Không trùng lặp nội dung (H1 trùng giữa các trang)", "Onsite", "Chất lượng nội dung", "🟡 Vừa", True, "Từ crawl. H1 trùng thường là 2 bài cùng chủ đề → gộp + 301."),
    ("O08", "Nội dung đáp ứng đúng ý định tìm kiếm & đủ độ sâu", "Onsite", "Chất lượng nội dung", "🟡 Vừa", False, "Google từ khoá chính, so loại trang top 3 với trang của Rooty (bài viết hay trang bán, độ dài, bảng giá…)."),
    ("O09", "Ảnh có thẻ alt (≥ 90% ảnh nội dung)", "Onsite", "Hình ảnh & media", "🟢 Thấp", True, "Kiểm ảnh trên trang chủ + trang tour + bài viết mẫu."),
    ("O10", "Ảnh dùng định dạng hiện đại (WebP/AVIF)", "Onsite", "Hình ảnh & media", "🟢 Thấp", True, "Plugin tối ưu ảnh (ShortPixel/Imagify/LiteSpeed) chuyển WebP."),
    ("O11", "Ảnh dung lượng ≤ 200KB", "Onsite", "Hình ảnh & media", "🟢 Thấp", True, "Kiểm 20 ảnh mẫu. Nén ảnh trước khi tải lên."),
    # ===== 5. ENTITY
    ("E01", "NAP trên website: có tên, hotline, địa chỉ ở chân trang và trang liên hệ, giống nhau", "Entity", "NAP", "🔴 Cao", True, "Kiểm số điện thoại xuất hiện trên trang chủ và trang liên hệ."),
    ("E02", "NAP khớp trên mọi hồ sơ (GBP, Facebook, OTA…)", "Entity", "NAP", "🔴 Cao", True, "Từ bảng Hồ sơ thương hiệu (tab B8)."),
    ("E05", "Google Business Profile đã xác minh, đầy đủ, khớp NAP", "Entity", "NAP", "🔴 Cao", True, "Từ bảng Hồ sơ thương hiệu (tab B8)."),
    ("E03", "Schema Organization / TravelAgency / LocalBusiness đủ name, url, logo, telephone, address", "Entity", "Schema thực thể", "🟡 Vừa", True, "Kiểm JSON-LD trang chủ. Cấu hình trong Rank Math → Local SEO / Knowledge Graph."),
    ("T24", "Schema Organization có sameAs trỏ các hồ sơ thương hiệu", "Entity", "Schema thực thể", "🟡 Vừa", True, "Thêm URL Facebook, TikTok, YouTube, GBP… vào sameAs (xem tab B8)."),
    ("E04", "Bài viết có schema tác giả (Person) — tác giả thật", "Entity", "Schema thực thể", "🟢 Thấp", True, "Kiểm bài viết mẫu có author là Person."),
    ("E06", "Phủ sóng mạng xã hội: ≥ 5 hồ sơ chính đã có", "Entity", "Social & citation", "🟡 Vừa", True, "Từ bảng Hồ sơ thương hiệu (tab B8)."),
    ("E07", "Có báo chí / citation uy tín nhắc tới Rooty (≥ 5)", "Entity", "Social & citation", "🟡 Vừa", True, "Từ bảng Liên kết (tab B9, loại Báo chí / Hồ sơ/citation)."),
    ("E08", "Google 'Rooty Trip' hiện bảng tri thức (Knowledge Panel) / hồ sơ GBP", "Entity", "Social & citation", "🟢 Thấp", False, "Tìm 'Rooty Trip' và 'Rooty Trip Phú Quốc' ở chế độ ẩn danh, chụp lại kết quả."),
]

TABLES = {
    # ---------------- 1 · DISCOVERY
    "nguondl": {"name": "Nguồn dữ liệu khách", "fields": [
        F("Nguồn"), F("Loại", "select", DATA_SOURCES), F("Cách thu thập", "long"), F("Cỡ mẫu", "num"),
        F("Thời gian"), F("Phát hiện chính", "long"), F("Áp dụng cho nhóm"), F("Link file", "url"),
        F("Trạng thái", "select", ["Kế hoạch", "Đang thu", "Đã phân tích"]), F("Ghi chú", "long")]},
    "khach": {"name": "Khách hàng", "fields": [
        F("Nhóm khách"), F("Tên đại diện"), F("Tỷ trọng khách %", "dec"),
        # nhân khẩu học
        F("Độ tuổi"), F("Giới tính", "select", ["Nữ", "Nam", "Cả hai"]), F("Nghề nghiệp"), F("Thu nhập"),
        F("Nơi sống"), F("Học vấn"),
        # tâm lý & lối sống
        F("Tâm lý & lối sống", "long"), F("Sở thích", "long"),
        # nhu cầu & động cơ
        F("Nhu cầu & động cơ", "long"), F("Mục tiêu chuyến đi", "long"),
        # điểm đau
        F("Điểm đau", "long"), F("Câu hỏi hay hỏi", "long"),
        # hành vi tiêu dùng
        F("Kênh tìm thông tin", "long"), F("Mua online/offline", "select", ["Online", "Offline", "Cả hai"]),
        F("Yếu tố quyết định", "long"), F("Ngân sách / chuyến"), F("Thời điểm đi"), F("Đặt trước bao lâu"),
        F("Tour phù hợp"),
        F("Nguồn dữ liệu", "long"), F("Xác nhận", "select", ["Giả định", "Đã xác nhận"]), F("Ghi chú", "long")]},
    "hanhtrinh": {"name": "Hành trình khách", "fields": [
        F("Câu hỏi / nhu cầu"), F("Giai đoạn", "select", JOURNEY), F("Nhóm khách"),
        F("Hành động của khách", "long"), F("Điểm chạm", "long"), F("Cảm xúc", "select", EMOTION),
        F("Rào cản", "long"), F("Cơ hội cho Rooty", "long"),
        F("Loại nội dung", "select", CONTENT_TYPES), F("Từ khoá ví dụ"), F("Trang đáp ứng", "url"),
        F("Chỉ số đo"), F("Ghi chú", "long")]},
    "tukhoagoc": {"name": "Từ khoá gốc", "fields": [
        F("Từ khoá gốc"), F("Loại", "select", SEED_TYPES), F("Sản phẩm / dịch vụ"), F("Cụm dự kiến"),
        F("Mở rộng", "select", ["Chưa", "Đã mở rộng"]), F("Số từ khoá tìm được", "num"), F("Ghi chú", "long")]},
    "tukhoa": {"name": "Từ khoá", "fields": [
        F("Từ khoá"), F("Cụm chủ đề"), F("Nhóm URL"), F("Vai trò", "select", ["Từ khoá chính", "Từ khoá phụ"]),
        F("Ý định", "select", INTENT), F("Giai đoạn", "select", JOURNEY),
        F("Lượng tìm", "num"), F("Độ khó", "num"), F("CPC", "num"), F("Cạnh tranh"),
        F("Vị trí", "dec"), F("Lượt nhấp", "num"), F("Hiển thị", "num"),
        F("Trang đích", "url"), F("Từ khoá gốc"), F("Từ khoá cha"),
        F("Ưu tiên", "select", PRIORITY), F("Nguồn", "select", ["Search Console", "Keyword Planner", "Ahrefs/Semrush", "Keywordtool.io", "Công cụ từ khoá", "Gợi ý Google", "Sale/CSKH", "Đối thủ"]),
        F("Trạng thái", "select", ["Mới", "Đã gán trang", "Cần viết", "Đang viết", "Bỏ"]), F("Ghi chú", "long")]},
    "trang": {"name": "Trang đích", "fields": [
        F("URL", "url"), F("Tiêu đề"), F("H1"), F("Cụm chủ đề"), F("Vai trò silo", "select", SILO_ROLE),
        F("Loại trang", "select", PAGE_KIND), F("Từ khoá chính"),
        F("Nội dung", "select", ["Tốt", "Cần sửa", "Cần viết", "Gộp", "Xoá"]),
        F("Số từ", "num"), F("Độ sâu", "num"), F("Link vào", "num"),
        # Bước 7 · onpage 5 hạng mục
        F("Title", "select", CHECK), F("Meta", "select", CHECK), F("Heading", "select", CHECK),
        F("URL chuẩn", "select", CHECK), F("Hình ảnh", "select", CHECK),
        F("Gợi ý Title"), F("Gợi ý Meta", "long"), F("Chi tiết onpage", "long"), F("Lần chấm onpage", "date"),
        # Bước 10 · số liệu & content audit
        F("GSC lượt nhấp", "num"), F("GSC hiển thị", "num"), F("GSC CTR %", "dec"), F("GSC vị trí", "dec"),
        F("GA4 phiên", "num"), F("GA4 tương tác %", "dec"), F("GA4 chuyển đổi", "num"), F("Kỳ số liệu"),
        F("Đề xuất audit", "select", ["Giữ", "Cập nhật / viết lại", "Gộp", "Xoá / 301", "Noindex", "Theo dõi"]), F("Lý do đề xuất", "long"),
        F("Quyết định", "select", ["Giữ", "Cập nhật / viết lại", "Gộp", "Xoá / 301", "Noindex", "Chưa quyết"]),
        F("Điểm onpage", "num"), F("Onpage", "select", ["Chưa làm", "Đang làm", "Xong"]),
        # GEO · AI Search
        F("Điểm GEO", "num"), F("Qua cửa chặn GEO", "select", ["Đạt", "Chưa đạt"]), F("Chấm GEO", "long"), F("Lần chấm GEO", "date"),
        F("Ghi chú", "long")]},
    "doithu": {"name": "Đối thủ", "fields": [
        F("Đối thủ"), F("Website", "url"), F("Loại", "select", ["Công ty tour", "OTA", "Blog du lịch", "Báo", "Khác"]),
        F("Mạnh ở cụm"), F("Chạy Google Ads", "select", ["Có", "Không", "Chưa kiểm"]),
        # chỉ số (từ Ahrefs/Semrush nếu có)
        F("Số từ khoá organic", "num"), F("Traffic ước tính", "num"), F("DR/DA", "num"), F("Số domain trỏ về", "num"),
        F("Top từ khoá traffic", "long"),
        # điểm mạnh
        F("Mạnh: nội dung", "long"), F("Mạnh: backlink & uy tín", "long"), F("Mạnh: UX/UI & tốc độ", "long"),
        F("Mạnh: thương hiệu, giá, chính sách", "long"),
        # điểm yếu
        F("Yếu: khoảng trống nội dung", "long"), F("Yếu: bài cũ, heading/title chưa tối ưu", "long"),
        F("Yếu: chuyển đổi & chăm sóc khách", "long"),
        F("Khoảng trống Rooty thắng được", "long"), F("Chỉ số kỹ thuật", "long"), F("Ngày soi", "date"),
        F("Trạng thái", "select", ["Cần phân tích", "Đang phân tích", "Đã phân tích"]), F("Ghi chú", "long")]},
    "dtkw": {"name": "Từ khoá đối thủ", "fields": [
        F("Từ khoá"), F("Đối thủ"), F("Vị trí đối thủ", "dec"), F("Vị trí Rooty", "dec"), F("Lượng tìm", "num"),
        F("Traffic đối thủ", "num"), F("URL đối thủ", "url"),
        F("Phân loại", "select", ["Gap — Rooty chưa có", "Common — đối thủ hơn", "Common — Rooty hơn"]),
        F("Cơ hội", "select", PRIORITY), F("Đã thêm vào Từ khoá", "select", ["Chưa", "Đã thêm"]), F("Ghi chú", "long")]},
    # ---------------- 2 · IMPROVING
    "kythuat": {"name": "Checklist audit", "fields": [
        F("Mục kiểm"), F("Mã"), F("Hạng mục", "select", AUDIT_AREAS), F("Nhóm", "select", TECH_GROUPS),
        F("Mức độ", "select", ["🔴 Cao", "🟡 Vừa", "🟢 Thấp"]),
        F("Kết quả", "select", ["Đạt", "Chưa đạt", "Chưa kiểm", "Không áp dụng"]),
        F("Chi tiết kết quả", "long"), F("Cách kiểm / cách sửa", "long"),
        F("Kiểm tự động", "select", ["Có", "Không"]), F("Lần kiểm", "date"),
        F("Người sửa"), F("Hạn", "date"), F("Ghi chú", "long")]},
    "audit": {"name": "Audit", "fields": [
        F("Vấn đề"), F("Hạng mục", "select", ["Kỹ thuật", "Silo", "UX/UI", "Onsite", "Entity", "GEO"]),
        F("Mức độ", "select", ["🔴 Cao", "🟡 Vừa", "🟢 Thấp"]), F("Số trang", "num"), F("URL ví dụ", "long"),
        F("Cách sửa", "long"), F("Người sửa"), F("Hạn", "date"),
        F("Trạng thái", "select", ["Mới", "Đang sửa", "Đã sửa", "Bỏ qua"]), F("Nguồn"), F("Ghi chú", "long")]},
    # ---------------- 3 · CREATE & OPTIMIZE (Content = bảng Bài viết, Onpage = cột trong Trang đích)
    "sualoi": {"name": "Sửa lỗi từng trang", "fields": [
        F("Lỗi trên trang"), F("Loại lỗi"), F("URL", "url"), F("Ngôn ngữ"), F("Chi tiết lỗi", "long"), F("Cần sửa gì", "long"), F("Mô tả loại lỗi", "long"),
        F("Mức độ", "select", ["🔴 Cao", "🟡 Vừa", "🟢 Thấp"]),
        F("Trạng thái", "select", ["Mới", "Đã xác nhận", "Đang sửa", "Đã sửa", "Sửa chưa đạt", "Tái phát", "Hết lỗi (quét lại)", "Không phải lỗi", "Bỏ qua"]),
        F("Người sửa"), F("Hạn", "date"), F("Đã sửa gì", "long"),
        F("Ngày phát hiện", "date"), F("Ngày sửa", "date"), F("Đợt quét"), F("Kiểm lại", "long"), F("Lần kiểm lại", "date"),
        F("Nhấp trước", "num"), F("Hiển thị trước", "num"), F("Vị trí trước", "dec"), F("Kỳ số liệu trước"),
        F("Nhấp sau", "num"), F("Hiển thị sau", "num"), F("Vị trí sau", "dec"), F("Kỳ số liệu sau"),
        F("Hiệu quả", "select", ["Chờ đo", "Tốt lên", "Không đổi", "Giảm", "Chưa có số liệu"]), F("Ghi chú", "long")]},
    "giadukien": {"name": "Giá & dữ kiện", "fields": [
        F("Dữ kiện"), F("Loại", "select", ["Giá tour/combo/vé", "Giá vé tham quan", "Giờ mở cửa / lịch", "Khoảng cách / thời gian", "Chính sách", "Khác"]),
        F("Sản phẩm / địa điểm"), F("Giá trị"), F("Giá cũ"), F("Áp dụng từ", "date"), F("Áp dụng đến", "date"),
        F("Nguồn", "url"), F("Nguồn từ"), F("Ngày kiểm", "date"), F("Kiểm lại sau (ngày)", "num"),
        F("Trạng thái", "select", ["Đúng", "Đã đổi — dò lại bài", "Có bài cần sửa", "Cần kiểm lại", "Ngừng bán"]),
        F("Từ khoá tìm trong bài", "long"), F("Bài đang dùng", "long"), F("Số bài ghi khác giá", "num"), F("Lần dò bài", "date"),
        F("Lịch sử", "long"), F("Ghi chú", "long")]},
    "kiemweb": {"name": "Kiểm nhiều website", "fields": [
        F("Website"), F("Nhóm"), F("Loại kiểm", "select", ["Toàn site", "Một trang"]),
        F("Trạng thái", "select", ["Đang chờ", "Đang kiểm", "Xong", "Lỗi"]), F("Lần kiểm", "date"),
        F("Điểm %", "num"), F("Đạt", "num"), F("Chưa đạt", "num"), F("Chưa kiểm", "num"),
        F("Lỗi cần sửa", "long"), F("Chi tiết", "long"), F("Ghi chú", "long")]},
    "thuattoan": {"name": "Cập nhật thuật toán", "fields": [
        F("Tên đợt"), F("Loại", "select", ["Core update", "Spam update", "Discover update", "Reviews update", "Helpful content", "Sự cố hệ thống", "Khác"]),
        F("Bắt đầu", "date"), F("Kết thúc", "date"), F("Trạng thái", "select", ["Đang triển khai", "Đã xong"]),
        F("Nguồn", "url"), F("Thông báo của Google", "long"),
        F("Ảnh hưởng tới Rooty", "select", ["Đang triển khai", "Chưa có số liệu", "Không đáng kể", "Tăng", "Giảm"]),
        F("Lượt nhấp/ngày trước", "dec"), F("Lượt nhấp/ngày sau", "dec"), F("Thay đổi lượt nhấp %", "dec"), F("Thay đổi hiển thị %", "dec"),
        F("Chi tiết ảnh hưởng", "long"), F("Việc cần làm", "long"), F("Đã review", "select", ["Chưa", "Đã"]), F("Kết luận", "long")]},
    "tinseo": {"name": "Tin Google Search Central", "fields": [
        F("Tiêu đề"), F("Ngày", "date"), F("Link", "url"), F("Tóm tắt", "long"),
        F("Mức liên quan", "select", ["Cao", "Vừa", "Thấp"]), F("Đã đọc", "select", ["Chưa", "Đã"]), F("Việc cần làm cho Rooty", "long")]},
    "chinhsach": {"name": "Chính sách spam Google", "fields": [
        F("Chính sách"), F("Tên gốc"), F("Mã"), F("Nhóm", "select", ["Chính sách spam", "Thao túng khác"]),
        F("Nghĩa là gì", "long"), F("Rủi ro với Rooty", "long"), F("Cách kiểm", "long"),
        F("Trạng thái", "select", ["Chưa kiểm", "An toàn", "Có rủi ro", "Vi phạm — cần sửa"]),
        F("Kết quả tự kiểm", "long"), F("Lần kiểm", "date"), F("Nguồn", "url"), F("Ghi chú", "long")]},
    "thucthe": {"name": "Thực thể", "fields": [
        F("Thực thể"), F("Loại", "select", ["Thương hiệu", "Điểm đến", "Tour/sản phẩm", "Người", "Đối tác"]),
        F("Thuộc tính", "long"), F("Nguồn", "url"), F("Ngày kiểm", "date"), F("Trang dùng", "long"),
        F("Schema"), F("Ghi chú", "long")]},
    "brand": {"name": "Thông tin thương hiệu", "fields": [
        F("Tên thương hiệu"), F("Tên pháp lý"), F("Website", "url"), F("Hotline chính"), F("Email"),
        F("Địa chỉ"), F("Thành phố"), F("Tỉnh/thành"), F("Giờ mở cửa"), F("Logo URL", "url"),
        F("Mô tả ngắn", "long"), F("Năm thành lập"), F("Giấy phép lữ hành"), F("Wikidata URL", "url"), F("Ghi chú", "long")]},
    "hoso": {"name": "Hồ sơ thương hiệu", "fields": [
        F("Nền tảng"), F("Nhóm", "select", PROFILE_GROUPS), F("URL", "url"), F("Tên hiển thị"), F("Địa chỉ"), F("Hotline"),
        F("Khớp NAP", "select", ["Khớp", "Lệch", "Chưa kiểm"]), F("Trong sameAs", "select", ["Có", "Chưa"]),
        F("Web trỏ tới hồ sơ", "select", ["Có", "Chưa"]), F("Hồ sơ trỏ về web", "select", ["Có", "Chưa", "Chưa kiểm"]),
        F("Đã xác minh", "select", ["Có", "Chưa", "Không áp dụng"]),
        F("Số đánh giá", "num"), F("Điểm", "dec"),
        F("Trạng thái", "select", ["Chưa có", "Đã có", "Cần sửa"]), F("Ghi chú", "long")]},
    "gbp": {"name": "Lịch đăng GBP", "fields": [
        F("Chủ đề"), F("STT", "num"), F("Ngày đăng", "date"), F("Loại bài", "select", ["Cập nhật", "Ưu đãi", "Sự kiện"]),
        F("Link trong bài GBP", "url"), F("Bài blog", "url"), F("Trang tour", "url"), F("Giá từ"), F("Nguồn giá"),
        F("Blog đã link sang tour", "select", ["Có", "CHƯA – thêm link"]),
        F("Trạng thái", "select", ["Chưa soạn", "Đã soạn", "Đã duyệt", "Đã đăng", "Bỏ"]),
        F("Nội dung bài", "long"), F("Ảnh"), F("Người đăng"), F("Link bài đã đăng", "url"),
        F("Lượt xem", "num"), F("Lượt bấm", "num"), F("Ghi chú", "long")]},
    "hesinhthai": {"name": "Hệ sinh thái Google", "fields": [
        F("Việc"), F("Loại", "select", ["Nền tảng", "Ghim My Maps", "Link nội bộ", "Video YouTube", "Tài liệu Google"]),
        F("Nền tảng", "select", ["Google Business Profile", "YouTube", "Google My Maps", "Google Sites", "Google Docs / Sheets / Slides / Drive",
                                  "Blogger", "Google Calendar / Groups", "Công cụ ép index / bắn link", "Website"]),
        F("Quyết định", "select", ["Làm", "Không ưu tiên", "Bỏ"]),
        F("Trạng thái", "select", ["Chưa làm", "Đang làm", "Xong", "Bỏ"]),
        F("Lớp"), F("Tìm địa điểm"), F("Từ URL", "url"), F("Đến URL", "url"), F("Link", "url"), F("URL tài sản", "url"),
        F("Lý do", "long"), F("Người làm"), F("Hạn", "date"), F("Ghi chú", "long")]},
    # ---------------- 4 · PROMOTION
    "lienket": {"name": "Liên kết", "fields": [
        F("Anchor"), F("Loại", "select", ["Nội bộ", "Backlink", "Báo chí", "Hồ sơ/citation", "Guest post"]),
        F("Từ URL", "url"), F("Đến URL", "url"), F("Thuộc tính", "select", ["Dofollow", "Nofollow"]),
        F("Chi phí", "num"), F("Trạng thái", "select", ["Kế hoạch", "Đang liên hệ", "Đã gắn", "Đang live", "Mất link", "Bỏ"]),
        F("Ngày", "date"),
        # Bước 9
        F("Chiến lược", "select", ["Liên kết nội bộ", "Guest post", "Digital PR / báo chí", "Broken link", "Linkable asset", "Hồ sơ / citation", "Đối tác / khách sạn", "Khác"]),
        F("Domain nguồn"), F("Uy tín (DR/DA)", "num"), F("Liên quan chủ đề", "select", PRIORITY),
        F("Vị trí đặt", "select", ["Trong nội dung", "Sidebar", "Footer", "Menu/header", "Hồ sơ/bio"]),
        F("Điểm chất lượng", "num"), F("Câu gắn link", "long"), F("Kiểm lần cuối", "date"), F("Kết quả kiểm", "long"),
        F("Ghi chú", "long")]},
    # ---------------- 5 · EVALUATE
    "danhgia": {"name": "Đánh giá tháng", "fields": [
        F("Tháng"), F("Lượt nhấp", "num"), F("Hiển thị", "num"), F("CTR %", "dec"), F("Vị trí TB", "dec"),
        F("Phiên organic", "num"), F("Người dùng organic", "num"), F("Tỷ lệ tương tác %", "dec"),
        F("Thời gian tương tác TB (giây)", "num"), F("Chuyển đổi organic", "num"), F("Tỷ lệ chuyển đổi %", "dec"),
        F("Tỷ lệ thoát %", "dec"), F("Phiên (mọi kênh)", "num"),
        F("Khách đăng ký sales@", "num"), F("Đặt dịch vụ / tư vấn / đơn online / email khách"), F("Tỷ lệ đăng ký %", "dec"),
        F("Referral AI", "num"), F("Trang lỗi index", "num"),
        F("Từ khoá top 3", "num"), F("Từ khoá top 10", "num"), F("Nguồn số liệu"), F("Nhận xét", "long"), F("Việc tháng sau", "long")]},
    "cannib": {"name": "Xung đột từ khoá", "fields": [
        F("Từ khoá"), F("Số trang", "num"), F("Các URL", "long"), F("Hiển thị", "num"), F("Lượt nhấp", "num"),
        F("Trang nên giữ", "url"), F("Cách xử lý", "select", ["Gộp + 301", "Đổi từ khoá trang phụ", "Canonical", "Liên kết nội bộ về trang chính", "Bỏ qua"]),
        F("Trạng thái", "select", ["Mới", "Đang xử lý", "Đã xử lý"]), F("Ghi chú", "long")]},
    "changelog": {"name": "Nhật ký thay đổi", "fields": [
        F("Thay đổi", "long"), F("Ngày", "date"), F("URL", "url"),
        F("Loại", "select", ["Nội dung", "Onpage", "Kỹ thuật", "Liên kết", "Gộp/Xoá", "Khác"]), F("Người làm"),
        F("Lượt nhấp trước", "num"), F("Vị trí trước", "dec"), F("Lượt nhấp sau", "num"), F("Vị trí sau", "dec"),
        F("Kết quả", "select", ["Chờ đo", "Tốt lên", "Không đổi", "Giảm"]), F("Ghi chú", "long")]},
    "lichreview": {"name": "Lịch review", "fields": [
        F("Việc"), F("Tần suất", "select", ["Hàng tuần", "Hàng tháng", "Hàng quý"]), F("Hạng mục"),
        F("Lần làm gần nhất", "date"), F("Người làm"), F("Tab liên quan"), F("Cách làm", "long"), F("Ghi chú", "long")]},
    # ---------------- GEO · AI Search (Checklist GEO của GTV — 6 điểm chạm, 32 việc)
    "geo": {"name": "Checklist GEO", "fields": [
        F("Việc"), F("Số", "num"), F("Điểm chạm", "select", GEO_POINTS), F("Thời điểm"), F("Tiêu chí đạt", "long"),
        F("Mức", "select", ["Bắt buộc", "Tuỳ chọn"]), F("Cửa chặn", "select", ["Có", "Không"]),
        F("Bằng chứng", "select", ["A", "B", "C", "D"]), F("Làm bằng"), F("Đo ở đâu"),
        F("Trạng thái", "select", GEO_STATUS), F("Kết quả tự kiểm", "long"), F("Lần kiểm", "date"),
        F("Người làm"), F("Hạn", "date"), F("Ghi chú", "long")]},
    "cauhoiai": {"name": "Bộ câu hỏi AI", "fields": [
        F("Câu hỏi"), F("Mã câu"), F("Nhóm", "select", ["Sát lúc mua", "Đang cân nhắc", "Mới tìm hiểu", "Gắn tên thương hiệu"]),
        F("Chủ đề"), F("Trang Rooty trả lời", "url"), F("Ngày thêm", "date"), F("Ghi chú", "long")]},
    "aihien": {"name": "Đo hiện diện AI", "fields": [
        F("Câu hỏi"), F("Mã câu"), F("Chủ đề"), F("Máy AI", "select", AI_ENGINES), F("Phiên bản mô hình"),
        F("Ngày chạy", "date"), F("Lần chạy", "num"), F("Câu trả lời", "long"),
        F("Nhắc tên Rooty", "select", ["Có", "Không"]), F("Trích link Rooty", "select", ["Có", "Không"]),
        F("Thứ tự Rooty", "num"), F("URL được trích", "long"),
        F("Thông tin đúng", "select", ["Đúng", "Một phần", "Sai", "Không nhắc"]), F("Lỗi sai", "long"),
        F("Đối thủ xuất hiện", "long"), F("Ghi chú", "long")]},
}

_LARK_TYPE = {"text": 1, "long": 1, "url": 1, "select": 3, "num": 2, "dec": 2, "date": 5}


def lark_fields(key):
    out = []
    for f in TABLES[key]["fields"]:
        prop = None
        if f["k"] == "select":
            prop = {"options": [{"name": o} for o in f["o"]]}
        elif f["k"] == "num":
            prop = {"formatter": "0"}
        elif f["k"] == "dec":
            prop = {"formatter": "0.0"}
        elif f["k"] == "date":
            prop = {"date_formatter": "yyyy/MM/dd"}
        out.append((f["n"], _LARK_TYPE[f["k"]], prop))
    return out


def primary(key):
    return TABLES[key]["fields"][0]["n"]


# ------------------------------------------------------------------ dữ liệu mẫu

SEEDS = {
    "nguondl": [
        {"Nguồn": "Phỏng vấn sale & CSKH", "Loại": "Phỏng vấn sale/CSKH", "Trạng thái": "Kế hoạch", "Cỡ mẫu": 3,
         "Cách thu thập": "30 phút/người theo kịch bản trong quy-trinh/mau-khao-sat-khach.md (phần A). Hỏi: khách là ai, hỏi gì nhiều nhất, vì sao chốt/không chốt, khách chê gì."},
        {"Nguồn": "Phỏng vấn hướng dẫn viên", "Loại": "Phỏng vấn HDV", "Trạng thái": "Kế hoạch", "Cỡ mẫu": 3,
         "Cách thu thập": "Hỏi 2–3 HDV: nhóm khách nào hay đi tour nào, khách hào hứng/lo lắng ở điểm nào trong tour, khách hỏi gì trên xe, điều gì khiến khách khen/chê."},
        {"Nguồn": "Tin nhắn Zalo OA / Fanpage 1 tháng gần nhất", "Loại": "Tin nhắn Zalo/Fanpage", "Trạng thái": "Kế hoạch", "Cỡ mẫu": 100,
         "Cách thu thập": "Xuất hoặc đọc 100 hội thoại gần nhất. Ghi lại: câu hỏi đầu tiên của khách, số người đi, có trẻ em không, ngân sách, lý do không chốt. Có thể dán (đã ẩn tên, SĐT) cho Claude tổng hợp."},
        {"Nguồn": "Đánh giá Google, Tripadvisor, Facebook", "Loại": "Đánh giá Google/Tripadvisor", "Trạng thái": "Kế hoạch", "Cỡ mẫu": 50,
         "Cách thu thập": "Đọc 50 đánh giá gần nhất của Rooty và 50 của 2 đối thủ. Ghi: khen gì, chê gì, ai viết (gia đình/cặp đôi…), nhắc tour nào."},
        {"Nguồn": "Dữ liệu đặt tour 12 tháng", "Loại": "Dữ liệu đặt tour/CRM", "Trạng thái": "Kế hoạch",
         "Cách thu thập": "Xuất danh sách booking (bỏ tên, SĐT): ngày đặt, ngày đi, số người, người lớn/trẻ em, tour/combo, giá trị, kênh đến. Tính: tỷ trọng từng nhóm khách, đặt trước bao lâu, tháng cao điểm."},
        {"Nguồn": "Khảo sát khách sau tour", "Loại": "Khảo sát khách", "Trạng thái": "Kế hoạch", "Cỡ mẫu": 50,
         "Cách thu thập": "Google Form theo phần B của mẫu khảo sát, gửi qua Zalo 24h sau tour cùng ảnh phó nháy chụp. Mục tiêu ≥ 50 phản hồi."},
        {"Nguồn": "GA4 — nhân khẩu học & thiết bị", "Loại": "GA4", "Trạng thái": "Kế hoạch",
         "Cách thu thập": "GA4 → Báo cáo → Người dùng → Thuộc tính người dùng (tuổi, giới tính, thành phố) và Công nghệ (thiết bị). Cần bật Google Signals."},
        {"Nguồn": "Search Console — câu hỏi khách tìm", "Loại": "Search Console", "Trạng thái": "Kế hoạch",
         "Cách thu thập": "Hiệu suất → Truy vấn: lọc truy vấn chứa 'không', 'bao nhiêu', 'nên', 'có', 'ở đâu' → đó là câu hỏi thật ở từng giai đoạn hành trình."},
        {"Nguồn": "Nhóm Facebook & TikTok du lịch Phú Quốc", "Loại": "Mạng xã hội/nhóm du lịch", "Trạng thái": "Kế hoạch",
         "Cách thu thập": "Đọc 30 bài hỏi đáp gần nhất trong các nhóm 'Phú Quốc', 'Review du lịch'; bình luận dưới video TikTok tour đảo. Ghi câu hỏi, nỗi lo, cách người ta so sánh."},
    ],
    "khach": [
        {"Nhóm khách": "Gia đình có trẻ nhỏ", "Tên đại diện": "Chị Hạnh, 36 tuổi, Hà Nội", "Độ tuổi": "30–45", "Giới tính": "Nữ",
         "Nghề nghiệp": "Nhân viên văn phòng, kế toán, giáo viên", "Thu nhập": "Hộ gia đình 30–60 triệu/tháng", "Nơi sống": "Hà Nội, TP.HCM", "Học vấn": "Đại học",
         "Tâm lý & lối sống": "Cẩn thận, lên kế hoạch kỹ, đặt sự an toàn và thoải mái của con lên đầu. Thích đi theo lịch cố định, ngại phát sinh.",
         "Sở thích": "Nghỉ dưỡng resort có hồ bơi, khu vui chơi cho trẻ (VinWonders, Safari), ăn hải sản.",
         "Nhu cầu & động cơ": "Kỳ nghỉ hè/lễ cho cả nhà, con được vui chơi, bố mẹ được nghỉ ngơi, không phải lo khâu tổ chức.",
         "Mục tiêu chuyến đi": "Cả nhà vui, con an toàn, có ảnh đẹp gia đình.",
         "Điểm đau": "Sợ tour đi nhiều, con mệt; say sóng khi đi cano; nắng gắt; đồ ăn không hợp trẻ; không biết chính sách vé trẻ em; sợ bị 'chặt chém'.",
         "Câu hỏi hay hỏi": "Trẻ em bao nhiêu tuổi thì tính vé? Tour 4 đảo có hợp bé 4–5 tuổi không? Có áo phao trẻ em không? Có đón tận khách sạn không?",
         "Kênh tìm thông tin": "Google, nhóm Facebook mẹ bỉm/du lịch gia đình, TikTok, hỏi bạn bè đã đi.",
         "Mua online/offline": "Online", "Yếu tố quyết định": "Đánh giá của gia đình khác, chính sách trẻ em rõ ràng, đón tiễn tận nơi, tư vấn nhanh qua Zalo.",
         "Ngân sách / chuyến": "15–30 triệu cho cả nhà (3N2Đ)", "Thời điểm đi": "Hè (6–8), lễ 30/4, Tết", "Đặt trước bao lâu": "3–6 tuần",
         "Tour phù hợp": "Combo nghỉ dưỡng, tour Nam đảo nhẹ nhàng, VinWonders/Safari", "Xác nhận": "Giả định",
         "Nguồn dữ liệu": "Giả định ban đầu — cần đối chiếu dữ liệu đặt tour, tin nhắn Zalo, phỏng vấn sale."},
        {"Nhóm khách": "Cặp đôi / trăng mật", "Tên đại diện": "Minh & Vy, 28 tuổi, TP.HCM", "Độ tuổi": "24–35", "Giới tính": "Cả hai",
         "Nghề nghiệp": "Nhân viên văn phòng, kinh doanh tự do", "Thu nhập": "15–35 triệu/người/tháng", "Nơi sống": "TP.HCM, Hà Nội, Đà Nẵng", "Học vấn": "Đại học",
         "Tâm lý & lối sống": "Thích trải nghiệm mới, coi trọng hình ảnh và khoảnh khắc riêng tư; hay xem review và lưu địa điểm trên TikTok/Instagram.",
         "Sở thích": "Ngắm hoàng hôn, chụp ảnh, lặn ngắm san hô, quán cà phê view biển, resort đẹp.",
         "Nhu cầu & động cơ": "Kỷ niệm (trăng mật, kỷ niệm ngày cưới, sinh nhật), có ảnh đẹp đăng mạng xã hội, trải nghiệm lãng mạn.",
         "Mục tiêu chuyến đi": "Ảnh đẹp, trải nghiệm riêng tư, không bị đông đúc.",
         "Điểm đau": "Tour ghép đông người, mất không khí riêng; ảnh tự chụp không đẹp; lo giá không xứng; điểm check-in quá đông giờ đẹp.",
         "Câu hỏi hay hỏi": "Chỗ ngắm hoàng hôn đẹp nhất? Trong tour có người chụp ảnh không? Tour riêng giá bao nhiêu? Mấy giờ đến Cầu Hôn là đẹp?",
         "Kênh tìm thông tin": "TikTok, Instagram, Google, review blog cá nhân.", "Mua online/offline": "Online",
         "Yếu tố quyết định": "Ảnh thật của khách trước, có phó nháy, tour riêng/nhóm nhỏ, phản hồi nhanh.",
         "Ngân sách / chuyến": "10–25 triệu cho 2 người (3N2Đ)", "Thời điểm đi": "Mùa khô (11–4), sau cưới", "Đặt trước bao lâu": "2–4 tuần",
         "Tour phù hợp": "Tour có phó nháy, tour riêng, combo resort, câu mực đêm", "Xác nhận": "Giả định",
         "Nguồn dữ liệu": "Giả định ban đầu — cần đối chiếu đánh giá và tin nhắn."},
        {"Nhóm khách": "Nhóm bạn trẻ", "Tên đại diện": "Nhóm của Huy, 23 tuổi, 6 người", "Độ tuổi": "18–28", "Giới tính": "Cả hai",
         "Nghề nghiệp": "Sinh viên, mới đi làm", "Thu nhập": "5–15 triệu/tháng", "Nơi sống": "TP.HCM, Hà Nội, miền Tây", "Học vấn": "Đang học/Đại học",
         "Tâm lý & lối sống": "Nhạy cảm về giá, thích vui, năng động, quyết định theo nhóm, hay so sánh tự túc với đi tour.",
         "Sở thích": "Cano 4 đảo, câu mực đêm, Grand World, chợ đêm, quay video TikTok.",
         "Nhu cầu & động cơ": "Đi chơi cùng bạn bè, nhiều hoạt động trong ít ngày, chi phí hợp lý.",
         "Mục tiêu chuyến đi": "Vui, nhiều trải nghiệm, rẻ.",
         "Điểm đau": "Ngân sách eo hẹp; chia tiền phức tạp; sợ tour nhàm; không chắc đi tour có rẻ hơn tự túc.",
         "Câu hỏi hay hỏi": "Đi Phú Quốc 3 ngày hết bao nhiêu tiền? Tour 4 đảo bao nhiêu một người? Có giảm giá nhóm không? Tự túc hay đi tour?",
         "Kênh tìm thông tin": "TikTok, Google, nhóm Facebook, review YouTube.", "Mua online/offline": "Online",
         "Yếu tố quyết định": "Giá/người, ưu đãi nhóm, video thực tế, lịch trình nhiều hoạt động.",
         "Ngân sách / chuyến": "3–6 triệu/người", "Thời điểm đi": "Hè, lễ, cuối tuần dài", "Đặt trước bao lâu": "1–3 tuần",
         "Tour phù hợp": "Tour cano 4 đảo, câu mực đêm, tour ghép", "Xác nhận": "Giả định",
         "Nguồn dữ liệu": "Giả định ban đầu — cần đối chiếu dữ liệu đặt tour."},
        {"Nhóm khách": "Khách đoàn công ty", "Tên đại diện": "Anh Tuấn, trưởng phòng hành chính", "Độ tuổi": "30–50", "Giới tính": "Cả hai",
         "Nghề nghiệp": "Hành chính, nhân sự, công đoàn doanh nghiệp", "Thu nhập": "Ngân sách công ty", "Nơi sống": "TP.HCM, Hà Nội, các tỉnh miền Tây", "Học vấn": "Đại học",
         "Tâm lý & lối sống": "Chịu trách nhiệm trước sếp và đồng nghiệp, ưu tiên an toàn, đúng giờ, giấy tờ rõ ràng; ít thời gian so sánh.",
         "Sở thích": "Team building, gala dinner, tour đảo, nghỉ dưỡng.",
         "Nhu cầu & động cơ": "Tổ chức du lịch công ty suôn sẻ, nhân viên hài lòng, đúng ngân sách.",
         "Mục tiêu chuyến đi": "Không sự cố, mọi người vui, chứng từ đầy đủ.",
         "Điểm đau": "Sợ nhà cung cấp không đủ năng lực, phát sinh chi phí, thiếu hoá đơn VAT, lịch trình trễ.",
         "Câu hỏi hay hỏi": "Có xuất hoá đơn VAT không? Có tổ chức gala/team building? Giá đoàn 50 người? Có hợp đồng không?",
         "Kênh tìm thông tin": "Google, giới thiệu, đối tác cũ.", "Mua online/offline": "Cả hai",
         "Yếu tố quyết định": "Uy tín (giấy phép, khách đoàn đã làm), báo giá chi tiết, hợp đồng, người phụ trách riêng.",
         "Ngân sách / chuyến": "Theo đoàn", "Thời điểm đi": "Quý 2–3, cuối năm", "Đặt trước bao lâu": "1–3 tháng",
         "Tour phù hợp": "Tour đoàn theo yêu cầu, combo + gala", "Xác nhận": "Giả định",
         "Nguồn dữ liệu": "Giả định ban đầu — cần hỏi sale phụ trách khách đoàn."},
    ],
    "hanhtrinh": [
        # Nhận thức
        {"Câu hỏi / nhu cầu": "Phú Quốc có gì đẹp, có đáng đi không?", "Giai đoạn": "Nhận thức", "Nhóm khách": "Tất cả",
         "Hành động của khách": "Lướt TikTok/Instagram thấy video biển đảo, lưu lại; tìm Google 'Phú Quốc có gì'.",
         "Điểm chạm": "TikTok, Instagram, Google tìm kiếm, AI (ChatGPT/AI Overview), bạn bè chia sẻ", "Cảm xúc": "😀 Hào hứng",
         "Rào cản": "Chưa biết đi mùa nào, chi phí bao nhiêu.", "Cơ hội cho Rooty": "Video tour thật do phó nháy quay; cẩm nang điểm đến trả lời thẳng, được AI trích dẫn.",
         "Loại nội dung": "Cẩm nang điểm đến", "Từ khoá ví dụ": "địa điểm du lịch phú quốc, phú quốc có gì chơi", "Chỉ số đo": "Hiển thị & lượt nhấp bài cẩm nang, lượt xem video"},
        {"Câu hỏi / nhu cầu": "Tháng mấy đi Phú Quốc đẹp, có nên đi mùa mưa?", "Giai đoạn": "Nhận thức", "Nhóm khách": "Tất cả",
         "Hành động của khách": "Hỏi Google/ChatGPT về thời tiết, mùa du lịch.", "Điểm chạm": "Google, AI, blog du lịch", "Cảm xúc": "😐 Phân vân",
         "Rào cản": "Sợ mưa bão, biển động.", "Cơ hội cho Rooty": "Bài thời điểm đẹp có dữ liệu thật từ HDV (tháng nào biển êm, tour nào vẫn đi được mùa mưa).",
         "Loại nội dung": "Cẩm nang điểm đến", "Từ khoá ví dụ": "tháng mấy đi phú quốc đẹp, phú quốc mùa mưa", "Chỉ số đo": "Lượt nhấp bài"},
        # Cân nhắc
        {"Câu hỏi / nhu cầu": "Đi mấy ngày, lịch trình thế nào, hết bao nhiêu tiền?", "Giai đoạn": "Cân nhắc", "Nhóm khách": "Tất cả",
         "Hành động của khách": "Đọc 3–5 bài lịch trình, tính chi phí, so sánh tự túc với đi tour.", "Điểm chạm": "Google, blog, YouTube, nhóm Facebook", "Cảm xúc": "😐 Phân vân",
         "Rào cản": "Quá nhiều thông tin trái chiều; không chắc chi phí thật.", "Cơ hội cho Rooty": "Bảng chi phí thực tế từ booking khách Rooty; lịch trình mẫu gắn tour tương ứng.",
         "Loại nội dung": "Lịch trình", "Từ khoá ví dụ": "lịch trình phú quốc 3 ngày 2 đêm, chi phí du lịch phú quốc", "Chỉ số đo": "Lượt nhấp, tỷ lệ bấm sang trang tour"},
        {"Câu hỏi / nhu cầu": "Nên đi tour nào, 3 đảo hay 4 đảo, bên nào uy tín?", "Giai đoạn": "Cân nhắc", "Nhóm khách": "Tất cả",
         "Hành động của khách": "So sánh các công ty tour, đọc đánh giá Google/Tripadvisor, hỏi trong nhóm Facebook.", "Điểm chạm": "Google, Google Maps, Tripadvisor, nhóm Facebook, AI", "Cảm xúc": "😟 Lo lắng",
         "Rào cản": "Sợ chọn nhầm bên kém, bị lừa đảo, tour khác quảng cáo.", "Cơ hội cho Rooty": "Bài so sánh trung thực; đánh giá thật nhiều trên GBP; thông tin thương hiệu nhất quán để AI nhắc tên Rooty.",
         "Loại nội dung": "So sánh", "Từ khoá ví dụ": "nên đi tour 3 đảo hay 4 đảo, công ty tour phú quốc uy tín", "Chỉ số đo": "Số đánh giá GBP, tỷ lệ được AI nhắc tên"},
        # Quyết định
        {"Câu hỏi / nhu cầu": "Giá tour bao nhiêu, bao gồm gì, chính sách huỷ, đặt thế nào?", "Giai đoạn": "Quyết định", "Nhóm khách": "Tất cả",
         "Hành động của khách": "Vào trang tour, xem giá, nhắn Zalo/gọi hotline để hỏi chỗ trống và chốt.", "Điểm chạm": "Website trang tour, Zalo OA, hotline, Messenger", "Cảm xúc": "😟 Lo lắng",
         "Rào cản": "Giá không rõ, thiếu chính sách huỷ, phản hồi chậm, phải chuyển khoản trước.", "Cơ hội cho Rooty": "Trang tour có bảng giá, bao gồm/không bao gồm, chính sách huỷ; nút Zalo nổi trên di động; trả lời trong 5 phút.",
         "Loại nội dung": "Trang tour/combo", "Từ khoá ví dụ": "tour 4 đảo phú quốc giá, đặt tour phú quốc", "Chỉ số đo": "Lượt bấm Zalo/gọi (GA4), tỷ lệ chốt"},
        {"Câu hỏi / nhu cầu": "Trẻ em tính vé thế nào, có đón tận khách sạn không?", "Giai đoạn": "Quyết định", "Nhóm khách": "Gia đình có trẻ nhỏ",
         "Hành động của khách": "Hỏi kỹ chi tiết trước khi chuyển tiền.", "Điểm chạm": "Zalo OA, trang FAQ, trang tour", "Cảm xúc": "😟 Lo lắng",
         "Rào cản": "Thông tin trẻ em không có sẵn trên web.", "Cơ hội cho Rooty": "Mục 'Đi cùng trẻ nhỏ' trên mỗi trang tour + trang FAQ.",
         "Loại nội dung": "FAQ", "Từ khoá ví dụ": "tour phú quốc cho trẻ em, trẻ em đi tour 4 đảo", "Chỉ số đo": "Số câu hỏi lặp lại trên Zalo giảm"},
        # Sử dụng & giữ chân
        {"Câu hỏi / nhu cầu": "Hôm nay mấy giờ đón, cần mang gì, thời tiết có đi được không?", "Giai đoạn": "Sử dụng & giữ chân", "Nhóm khách": "Tất cả",
         "Hành động của khách": "Nhận xác nhận, chờ xe đón, đi tour cùng HDV.", "Điểm chạm": "Zalo nhắc lịch, tài xế, HDV, phó nháy, tàu/cano", "Cảm xúc": "😀 Hào hứng",
         "Rào cản": "Đón trễ, thông tin thay đổi phút chót, HDV thiếu nhiệt tình.", "Cơ hội cho Rooty": "Tin nhắc lịch tự động tối hôm trước; HDV bản địa kể chuyện; phó nháy chụp ảnh — điểm khác biệt chính.",
         "Loại nội dung": "FAQ", "Từ khoá ví dụ": "đi tour 4 đảo cần mang gì", "Chỉ số đo": "Đánh giá sau tour, khiếu nại"},
        {"Câu hỏi / nhu cầu": "Khi nào nhận ảnh, có ăn tối/đi chơi thêm gì không?", "Giai đoạn": "Sử dụng & giữ chân", "Nhóm khách": "Cặp đôi / trăng mật",
         "Hành động của khách": "Chờ ảnh phó nháy, hỏi gợi ý buổi tối.", "Điểm chạm": "Zalo, HDV", "Cảm xúc": "🙂 Hài lòng",
         "Rào cản": "Nhận ảnh chậm.", "Cơ hội cho Rooty": "Gửi ảnh trong 24h kèm gợi ý tour tối (câu mực, chợ đêm) — bán thêm.",
         "Loại nội dung": "Cẩm nang điểm đến", "Từ khoá ví dụ": "phú quốc buổi tối đi đâu", "Chỉ số đo": "Tỷ lệ mua thêm tour"},
        # Trung thành & giới thiệu
        {"Câu hỏi / nhu cầu": "Chia sẻ ảnh, đánh giá, giới thiệu bạn bè, lần sau đi đâu?", "Giai đoạn": "Trung thành & giới thiệu", "Nhóm khách": "Tất cả",
         "Hành động của khách": "Đăng ảnh, viết đánh giá nếu được nhắc, giới thiệu khi bạn bè hỏi.", "Điểm chạm": "Google Maps (đánh giá), Facebook, TikTok, Zalo", "Cảm xúc": "🙂 Hài lòng",
         "Rào cản": "Quên đánh giá; không có lý do quay lại.", "Cơ hội cho Rooty": "Tin cảm ơn + link đánh giá Google 24h sau tour; mã giới thiệu bạn bè; gợi ý tour miền Tây/Kiên Giang cho chuyến sau.",
         "Loại nội dung": "Trang thương hiệu", "Từ khoá ví dụ": "rooty trip đánh giá, rooty trip có uy tín không", "Chỉ số đo": "Số đánh giá mới/tháng, khách quay lại, khách giới thiệu"},
        {"Câu hỏi / nhu cầu": "Công ty có tổ chức lại cho đoàn năm sau không, giá có ưu đãi không?", "Giai đoạn": "Trung thành & giới thiệu", "Nhóm khách": "Khách đoàn công ty",
         "Hành động của khách": "Đánh giá nhà cung cấp cuối năm, quyết định ký lại.", "Điểm chạm": "Sale phụ trách đoàn, email, báo cáo tổng kết chuyến đi", "Cảm xúc": "🙂 Hài lòng",
         "Rào cản": "Không có người chăm sóc sau chuyến.", "Cơ hội cho Rooty": "Gửi album + báo cáo chuyến đi; ưu đãi ký lại; xin thư giới thiệu/logo đối tác.",
         "Loại nội dung": "Trang thương hiệu", "Từ khoá ví dụ": "tour đoàn công ty phú quốc", "Chỉ số đo": "Tỷ lệ đoàn ký lại"},
    ],
    "hoso": [{"Nền tảng": n, "Nhóm": g, "Khớp NAP": "Chưa kiểm", "Trong sameAs": "Chưa", "Web trỏ tới hồ sơ": "Chưa",
              "Hồ sơ trỏ về web": "Chưa kiểm", "Đã xác minh": "Chưa", "Trạng thái": "Chưa có"} for n, g in PROFILES],
    "brand": [{"Tên thương hiệu": "Rooty Trip", "Website": "https://rootytrip.com",
               "Ghi chú": "Bấm «Lấy từ website» để điền từ schema trang chủ, rồi kiểm lại từng ô — đây là NAP gốc để so mọi hồ sơ."}],
    "thucthe": [
        {"Thực thể": "Rooty Trip", "Loại": "Thương hiệu", "Schema": "Organization / TravelAgency",
         "Thuộc tính": "Website: https://rootytrip.com\nLĩnh vực: tour trong ngày, tour trọn gói, combo nghỉ dưỡng, vé tham quan Phú Quốc\nĐiểm khác biệt: HDV bản địa, phó nháy chụp ảnh\nĐịa chỉ: (cần điền)\nHotline: (cần điền)\nNăm thành lập: (cần điền)",
         "Nguồn": "https://rootytrip.com", "Trang dùng": "Trang chủ, Giới thiệu"},
        {"Thực thể": "Thị trấn Hoàng Hôn (Địa Trung Hải Phú Quốc)", "Loại": "Điểm đến", "Schema": "TouristAttraction",
         "Thuộc tính": "Vị trí: mũi Ông Bốn, phường An Thới, Nam đảo\nCách Dương Đông: 29,7 km (~42 phút)\nCách sân bay: 19,6 km (~27 phút)\nChủ đầu tư: Sun Group (Sun Premier Village Primavera)",
         "Nguồn": "https://rootytrip.com/dia-trung-hai-phu-quoc/", "Trang dùng": "/dia-trung-hai-phu-quoc/"},
    ],
}


SEEDS["tukhoagoc"] = [
    {"Từ khoá gốc": k, "Loại": t, "Sản phẩm / dịch vụ": p, "Cụm dự kiến": c, "Mở rộng": "Chưa"} for k, t, p, c in [
        ("tour 4 đảo phú quốc", "Tên sản phẩm", "Tour cano 4 đảo", "Tour đảo"),
        ("tour 3 đảo phú quốc", "Tên sản phẩm", "Tour cano 3 đảo", "Tour đảo"),
        ("tour hòn thơm", "Tên sản phẩm", "Tour đảo Hòn Thơm + cáp treo", "Tour đảo"),
        ("tour câu mực phú quốc", "Tên sản phẩm", "Tour câu mực đêm", "Tour trong ngày"),
        ("tour nam đảo phú quốc", "Tên sản phẩm", "Tour Nam đảo trong ngày", "Tour trong ngày"),
        ("tour bắc đảo phú quốc", "Tên sản phẩm", "Tour Bắc đảo trong ngày", "Tour trong ngày"),
        ("tour phú quốc trọn gói", "Tên sản phẩm", "Tour trọn gói", "Tour trọn gói"),
        ("combo phú quốc", "Tên sản phẩm", "Combo nghỉ dưỡng", "Combo & khách sạn"),
        ("vé vinwonders phú quốc", "Tên sản phẩm", "Vé VinWonders", "Vé tham quan"),
        ("vé cáp treo hòn thơm", "Tên sản phẩm", "Vé cáp treo Hòn Thơm", "Vé tham quan"),
        ("rooty trip", "Thương hiệu", "Thương hiệu Rooty Trip", "Thương hiệu"),
        ("tour phú quốc có hướng dẫn viên", "Tính năng / đặc điểm", "HDV bản địa", "Tour trọn gói"),
        ("tour phú quốc có chụp ảnh", "Tính năng / đặc điểm", "Phó nháy trong tour", "Tour đảo"),
        ("tour phú quốc cho gia đình", "Nhu cầu cốt lõi", "Tour gia đình có trẻ nhỏ", "Tour trọn gói"),
        ("du lịch phú quốc", "Nhu cầu cốt lõi", "Toàn bộ", "Lên kế hoạch"),
        ("lịch trình phú quốc", "Nhu cầu cốt lõi", "Tour trọn gói, combo", "Lên kế hoạch"),
        ("chi phí du lịch phú quốc", "Nhu cầu cốt lõi", "Tour trọn gói, combo", "Lên kế hoạch"),
        ("địa điểm du lịch phú quốc", "Địa điểm", "Tour Nam/Bắc đảo", "Điểm đến"),
        ("ăn gì ở phú quốc", "Nhu cầu cốt lõi", "Tour ẩm thực, tour đêm", "Ẩm thực"),
        ("du lịch kiên giang", "Địa điểm", "Tour miền Tây/Kiên Giang", "Điểm đến"),
    ]]
SEEDS["doithu"] = [
    {"Đối thủ": "Klook", "Website": "https://www.klook.com/vi/", "Loại": "OTA", "Trạng thái": "Cần phân tích", "Chạy Google Ads": "Chưa kiểm"},
    {"Đối thủ": "Traveloka", "Website": "https://www.traveloka.com/vi-vn/", "Loại": "OTA", "Trạng thái": "Cần phân tích", "Chạy Google Ads": "Chưa kiểm"},
]

SEEDS["lichreview"] = [
    {"Việc": v, "Tần suất": t, "Hạng mục": h, "Tab liên quan": tab, "Cách làm": how} for v, t, h, tab, how in [
        ("Xem biến động traffic 7 ngày", "Hàng tuần", "Theo dõi", "danhgia", "GSC → Hiệu suất → so 7 ngày gần nhất với 7 ngày trước → xuất Ngày (Dates.csv) → Nhập CSV ở B10. Giảm > 20% → tìm trang/từ khoá giảm."),
        ("Kiểm lỗi lập chỉ mục mới", "Hàng tuần", "Theo dõi", "kythuat", "GSC → Trang → Lý do không lập chỉ mục: có lỗi mới (404, chặn robots, máy chủ) không? Ghi số trang lỗi vào dòng tháng ở B10."),
        ("Kiểm backlink mất", "Hàng tuần", "Theo dõi", "link", "B9 → Kiểm backlink còn sống."),
        ("Nhập số liệu tháng GSC + GA4", "Hàng tháng", "Theo dõi", "danhgia", "Đầu tháng: xuất GSC (Ngày, Trang, Truy vấn) và GA4 (Trang đích — kênh Organic Search) cho tháng trước → Nhập CSV ở B10; điền các số GA4 tổng vào dòng tháng."),
        ("Chạy crawl + Kiểm tự động", "Hàng tháng", "Kỹ thuật", "kythuat", "B5 → Chạy crawl → Kiểm tự động."),
        ("Báo cáo tháng", "Hàng tháng", "Theo dõi", "danhgia", "Chạy /rooty-bao-cao, dán nhận xét + việc tháng sau vào dòng tháng ở B10."),
        ("Cập nhật bài giá / lịch trình / mùa vụ", "Hàng tháng", "Nội dung", "content", "Bài có giá, lịch show, mùa vụ: kiểm lại thông tin, sửa thật (không chỉ đổi năm)."),
        ("Audit kỹ thuật toàn diện", "Hàng quý", "Kỹ thuật", "kythuat", "B5: tốc độ (Core Web Vitals mobile/desktop), uptime hosting, lỗi mobile, cấu trúc URL, 16 mục kiểm tay."),
        ("Audit nội dung: giữ / cập nhật / gộp / xoá", "Hàng quý", "Nội dung", "danhgia", "Nhập GSC Trang (3 tháng) + GA4 Trang đích → B10 · Phân loại content audit → duyệt cột Quyết định → tạo việc cập nhật."),
        ("Kiểm xung đột từ khoá", "Hàng quý", "Nội dung", "danhgia", "Xuất GSC Truy vấn × Trang (Search Analytics for Sheets / Looker Studio) → Nhập CSV ở B10."),
        ("Đo lại hiệu quả các thay đổi", "Hàng quý", "Theo dõi", "danhgia", "B10 → Nhật ký thay đổi → Đo lại (sau ≥ 4 tuần kể từ ngày sửa)."),
        ("Đo hiện diện AI", "Hàng quý", "Theo dõi", "kehoach", "/rooty-do-hien-dien-ai với đúng bộ câu hỏi tháng 1."),
        ("Lập kế hoạch quý tiếp theo + review KPI", "Hàng quý", "Kế hoạch", "kehoach", "Từ kết quả audit: danh sách việc cụ thể cho quý sau, người làm, hạn; so KPI quý với mục tiêu."),
    ]]

SEEDS["kythuat"] = [
    {"Mục kiểm": m, "Mã": c, "Hạng mục": a, "Nhóm": g, "Mức độ": lv, "Kết quả": "Chưa kiểm",
     "Kiểm tự động": "Có" if auto else "Không", "Cách kiểm / cách sửa": how}
    for c, m, a, g, lv, auto, how in TECH_CHECKLIST]


# GEO · nơi đo trong app cho từng việc của checklist GTV (mã B5 = Checklist audit; "bài" = chấm GEO từng bài; "AI" = đo hiện diện)
GEO_WHERE = {
    1: "B10 (GSC: trang có hiển thị/top 10) · thủ công", 2: "B5: T25, T26, M04", 3: "Tab GEO · Bộ câu hỏi AI + Đo hiện diện",
    4: "Thủ công (đọc AI Overview theo nhóm từ khoá)", 5: "Thủ công · CLAUDE.md «5 điều không hứa»", 6: "B5: T17",
    7: "B5: T11, T16, M06", 8: "Chấm GEO từng bài (#8) + B5: O12", 9: "Thủ công (site:rootytrip.com + câu hỏi)",
    10: "Thủ công (trang Giới thiệu, Bảng giá, FAQ, Chính sách)", 11: "B5: E01, E02 · B8", 12: "B5: E03, T24 · B8",
    13: "Chấm GEO từng bài (#13) + B5: E04", 26: "B9 · Liên kết", 27: "B9 · Liên kết (Báo chí/PR)", 28: "B3 · Topical map + B9",
    29: "B9 · Liên kết", 30: "Tab GEO · Đo hiện diện (≥ 3 lần/câu/máy)", 31: "Tab GEO · Đo hiện diện (theo chủ đề, theo máy)",
    32: "Thủ công · quy tắc báo cáo",
}
GEO_TECH = {2: ["T25", "T26", "M04"], 6: ["T17"], 7: ["T11", "T16", "M06"], 11: ["E01", "E02"], 12: ["E03", "T24"], 13: ["E04"]}
GEO_AUTO_PAGE = {8, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24}


def _geo_seed():
    import json as _j
    d = _j.loads((Path(os.path.dirname(os.path.abspath(__file__))) / "geo_checklist.json").read_text(encoding="utf-8"))
    names = {p.split(" · ")[0]: p for p in GEO_POINTS}
    out = []
    for it in d["items"]:
        n = it["n"]
        where = GEO_WHERE.get(n) or ("Chấm GEO từng bài" if n in GEO_AUTO_PAGE else "Kiểm tay khi duyệt bài (Cổng 4)")
        out.append({"Việc": it["viec"], "Số": n, "Điểm chạm": names[it["g"]], "Thời điểm": it["khi"], "Tiêu chí đạt": it["tieuchi"],
                    "Mức": it["muc"], "Cửa chặn": it["chan"], "Bằng chứng": it["bc"], "Làm bằng": it["lam"], "Đo ở đâu": where,
                    "Trạng thái": "Chưa làm"})
    return out


SEEDS["geo"] = _geo_seed()


def _cauhoi_seed():
    f = Path(os.path.dirname(os.path.abspath(__file__))).parent / "01-prompts" / "bo-cau-hoi-ai.csv"
    if not f.exists():
        return []
    group = {"sat-luc-mua": "Sát lúc mua", "can-nhac": "Đang cân nhắc", "dang-can-nhac": "Đang cân nhắc",
             "tim-hieu": "Mới tìm hiểu", "moi-tim-hieu": "Mới tìm hiểu", "thuong-hieu": "Gắn tên thương hiệu"}
    with f.open(encoding="utf-8-sig") as fh:
        return [{"Câu hỏi": r["cau_hoi"], "Mã câu": r["id"], "Nhóm": group.get(r["nhom"], "Mới tìm hiểu"), "Chủ đề": r["chu_de"]}
                for r in csv.DictReader(fh) if r.get("cau_hoi")]


SEEDS["cauhoiai"] = _cauhoi_seed()


def _policy_seed():
    import sys as _s
    _s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import algo
    return algo.policy_seed()


SEEDS["chinhsach"] = _policy_seed()


def _gbp_seed():
    """Lịch đăng bài Google Maps — nghien-cuu/lich-dang-gbp.csv (xem nghien-cuu/google-maps-huong-dan.md)."""
    import time as _t
    f = Path(os.path.dirname(os.path.abspath(__file__))).parent / "nghien-cuu" / "lich-dang-gbp.csv"
    if not f.exists():
        return []
    with f.open(encoding="utf-8-sig") as fh:
        return [{"Chủ đề": r["chu_de"], "STT": int(r["stt"]),
                 "Ngày đăng": int(_t.mktime(_t.strptime(r["ngay_dang"], "%d/%m/%Y")) * 1000),
                 "Loại bài": r["loai_bai_gbp"], "Link trong bài GBP": r["link_trong_bai_gbp"], "Bài blog": r["bai_blog"],
                 "Trang tour": r["trang_tour"], "Giá từ": r["gia_tu"], "Nguồn giá": r["nguon_gia"],
                 "Blog đã link sang tour": r["blog_da_link_sang_tour"], "Trạng thái": r["trang_thai"]}
                for r in csv.DictReader(fh) if r.get("chu_de")]



SEEDS["gbp"] = _gbp_seed()


def _hesinhthai_seed():
    """Hệ sinh thái Google — nghien-cuu/he-sinh-thai-google-viec.csv (xem nghien-cuu/he-sinh-thai-google.md)."""
    f = Path(os.path.dirname(os.path.abspath(__file__))).parent / "nghien-cuu" / "he-sinh-thai-google-viec.csv"
    if not f.exists():
        return []
    with f.open(encoding="utf-8-sig") as fh:
        return [{k: v for k, v in r.items() if v} for r in csv.DictReader(fh) if r.get("Việc")]


SEEDS["hesinhthai"] = _hesinhthai_seed()


# ------------------------------------------------------------------ nạp từ crawl

def latest(pattern):
    files = glob.glob(pattern)
    return max(files, key=os.path.getmtime) if files else None


def _kind(path: str) -> str:
    p = path.strip("/")
    if p == "":
        return "Trang chủ"
    if re.match(r"^(en|ja|ko|zh|ru)(/|$)", p):
        return "Ngôn ngữ khác"
    if p.startswith(("san-pham/", "product/")):
        return "Trang tour/sản phẩm"
    if p.startswith(("tu-khoa-san-pham/", "tag/", "danh-muc", "category/", "author/")):
        return "Trang tag"
    if re.match(r"^(gioi-thieu|lien-he|chinh-sach|dieu-khoan|ve-chung-toi|faq)", p):
        return "Trang thương hiệu"
    if re.match(r"^(tour-|combo-|ve-|khach-san)", p):
        return "Danh mục"
    return "Bài viết"


def crawl_rows(reports_dir: Path):
    f = latest(str(reports_dir / "crawl-*.csv"))
    if not f:
        raise FileNotFoundError("Chưa có báo cáo crawl. Chạy: python -X utf8 scripts/crawl_site.py https://rootytrip.com --max-pages 1200")
    with open(f, encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh)), os.path.basename(f)


def crawl_complete(reports_dir: Path) -> bool:
    """Báo cáo crawl mới nhất có quét hết site không (dòng cảnh báo «Chưa crawl hết» trong file .md cùng tên)."""
    f = latest(str(reports_dir / "crawl-*.csv"))
    if not f:
        return False
    md = Path(f[:-4] + ".md")
    return md.exists() and "Chưa crawl hết" not in md.read_text(encoding="utf-8")


def _int(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def crawl_pages(rows):
    return [r for r in rows if r.get("status") == "200" and r.get("title") is not None
            and not re.search(r"/page/\d+/?$", r["url"]) and "?" not in r["url"]]


def trang_from_crawl(rows, existing_urls: set):
    """Biến các dòng crawl (trang 200) thành bản ghi Trang đích, chấm nhanh onpage (Title, Meta, Heading, URL)."""
    import onpage
    out = []
    for r in crawl_pages(rows):
        url = r["url"]
        if url in existing_urls:
            continue
        path = re.sub(r"^https?://[^/]+", "", url)
        res, score = onpage.quick(r, None)
        out.append({
            "URL": url, "Tiêu đề": r.get("title", ""), "H1": r.get("h1", ""), "Loại trang": _kind(path), "Vai trò silo": "Khác",
            "Số từ": _int(r.get("words")), "Độ sâu": _int(r.get("depth")), "Link vào": _int(r.get("inlinks")),
            **res, "Điểm onpage": score, "Onpage": "Chưa làm",
        })
    return out


def audit_from_reports(rows, src_name, reports_dir: Path, existing: set):
    """Gom lỗi theo loại từ CSV crawl + bảng tổng hợp của GEO audit mới nhất."""
    ok200 = [r for r in rows if r.get("status") == "200" and r.get("title") is not None]
    is_page = lambda u: re.search(r"/page/\d+/?$", u)

    def sample(rs, n=6, key="url"):
        return "\n".join(r[key] for r in rs[:n])

    titles = {}
    for r in ok200:
        titles.setdefault(r.get("title", ""), []).append(r)
    dup = [rs for t, rs in titles.items() if t and len(rs) > 1]
    dup_real = [rs for rs in dup if sum(not is_page(r["url"]) for r in rs) > 1]
    dup_paging = [rs for rs in dup if rs not in dup_real]

    items = [
        ("Trang lỗi 4xx/5xx còn được link nội bộ trỏ tới", "Kỹ thuật", "🔴 Cao",
         [r for r in rows if r.get("status") not in ("200", "301", "302", "307", "308")],
         "Sửa link đang trỏ tới (xem cột URL), hoặc 301 về trang thay thế gần nghĩa nhất. Link dạng ?post_type=product&p=… là sản phẩm đã xoá."),
        ("Link nội bộ trỏ vào URL đã redirect", "Kỹ thuật", "🟡 Vừa",
         [r for r in rows if r.get("status") in ("301", "302", "307", "308")],
         "Sửa link trong bài/menu trỏ thẳng về URL đích (ghi ở cột note của file crawl) để không qua redirect."),
        ("Canonical trỏ sang URL khác", "Kỹ thuật", "🟡 Vừa",
         [r for r in ok200 if r.get("canonical_self") == "False"],
         "Kiểm từng trang: nếu là trang chính thì canonical tự trỏ; nếu là bản trùng thì giữ canonical và bỏ link nội bộ tới nó."),
        ("Trang đang noindex", "Kỹ thuật", "🟢 Thấp",
         [r for r in ok200 if r.get("noindex") == "True"],
         "Xác nhận noindex là có chủ đích (trang tag, giỏ hàng…). Trang tour/bài lõi không được noindex."),
        ("Title trùng giữa các trang khác nhau", "Onsite", "🟡 Vừa",
         [rs[0] | {"url": " | ".join(x["url"] for x in rs[:3])} for rs in dup_real],
         "Viết title riêng cho từng trang; nếu 2 trang cùng chủ đề → cân nhắc gộp (tranh từ khoá)."),
        ("Trang phân trang dùng chung title với trang danh mục", "Onsite", "🟢 Thấp",
         [rs[0] for rs in dup_paging],
         "Sửa theme/plugin SEO: thêm « – Trang N » vào title và meta của /page/N/."),
        ("Thiếu meta description", "Onsite", "🟡 Vừa",
         [r for r in ok200 if not r.get("meta_description") and not is_page(r["url"])],
         "Viết meta 140–160 ký tự chứa câu trả lời ngắn + lời mời đặt tour."),
        ("H1 không phải đúng 1 thẻ", "Onsite", "🟡 Vừa",
         [r for r in ok200 if r.get("h1_count") not in ("1", None) and not is_page(r["url"])],
         "Mỗi trang đúng 1 H1 chứa thực thể chính; logo/tiêu đề phụ không dùng H1."),
        ("Trang mỏng (< 300 từ)", "Onsite", "🟢 Thấp",
         [r for r in ok200 if (_int(r.get("words")) or 0) < 300 and not is_page(r["url"])],
         "Trang tag/sản phẩm mỏng: bổ sung nội dung hoặc noindex trang tag. Bài mỏng: cập nhật hoặc gộp."),
        ("Trang sâu hơn 3 click từ trang chủ", "Silo", "🟡 Vừa",
         [r for r in ok200 if (_int(r.get("depth")) or 0) > 3],
         "Đưa vào menu/danh mục/trang trụ của cụm, hoặc thêm link từ bài cùng cụm."),
        ("Trang chỉ có ≤ 1 link nội bộ trỏ vào", "Silo", "🟡 Vừa",
         [r for r in ok200 if (_int(r.get("inlinks")) or 0) <= 1 and r["url"].rstrip("/").count("/") > 2],
         "Lập kế hoạch link nội bộ theo cụm (tab B9) — ưu tiên trang tour/sản phẩm."),
    ]
    out = []
    for name, cat, lvl, rs, fix in items:
        if not rs or name in existing:
            continue
        out.append({"Vấn đề": name, "Hạng mục": cat, "Mức độ": lvl, "Số trang": len(rs),
                    "URL ví dụ": sample(rs), "Cách sửa": fix, "Trạng thái": "Mới", "Nguồn": src_name})

    # GEO audit: đọc bảng "Tổng hợp lỗi theo tần suất"
    g = latest(str(reports_dir / "geo-audit-*.md"))
    if g:
        txt = Path(g).read_text(encoding="utf-8")
        sec = txt.split("## 2.", 1)[-1].split("## 3.", 1)[0]
        geo_fix = {
            "Khối meta chen giữa H1 và câu trả lời": ("GEO", "🔴 Cao", "Sửa template bài viết: chuyển khối chuyên mục/tác giả/ngày/lượt xem xuống dưới đoạn mở đầu."),
            "Ít H2 dạng câu hỏi khách thật sự hỏi AI": ("GEO", "🟡 Vừa", "Khi cập nhật bài, đổi H2 thành câu khách hỏi thật; câu đầu sau H2 là câu trả lời."),
            "JSON-LD lỗi cú pháp": ("Entity", "🟡 Vừa", "Sửa đoạn JSON-LD/plugin schema; kiểm bằng Rich Results Test."),
            "N/N ảnh thiếu alt": ("Onsite", "🟢 Thấp", "Bổ sung alt mô tả cụ thể cho ảnh nội dung."),
        }
        for m in re.finditer(r"^\| (.+?) \| (\d+)/(\d+) \|$", sec, re.M):
            name = m.group(1).strip()
            cat, lvl, fix = geo_fix.get(name, ("GEO", "🟡 Vừa", "Xem báo cáo GEO audit."))
            label = "Trang chủ nhiều ảnh thiếu alt" if name.startswith("N/N") else name
            if label in existing:
                continue
            out.append({"Vấn đề": label, "Hạng mục": cat, "Mức độ": lvl, "Số trang": int(m.group(2)),
                        "URL ví dụ": f"Mẫu {m.group(2)}/{m.group(3)} trang quét", "Cách sửa": fix,
                        "Trạng thái": "Mới", "Nguồn": os.path.basename(g)})
    return out
