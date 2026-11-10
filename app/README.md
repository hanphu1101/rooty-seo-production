# Trang làm SEO — 10 bước, lưu trên Lark Base

Trang web chạy trên máy để **làm và theo dõi toàn bộ SEO** của rootytrip.com theo 10 bước, 5 giai đoạn. Mỗi tab = một bước, gồm **hướng dẫn chi tiết** (mục tiêu · cách làm · đạt khi · lệnh cho Claude) và **bảng dữ liệu** để làm việc ngay trên trang (thêm, sửa, xoá, lọc, tìm).

```bash
python -X utf8 app/server.py      # → http://localhost:8010
```

## Các tab

| Giai đoạn | Tab | Bảng Lark | Làm gì trên trang |
|---|---|---|---|
| — | **🩺 Chẩn đoán rớt top** | (dùng các bảng khác) | Một nút chạy 4 bước: GSC tìm ngày rớt → đối chiếu core/spam update chính thức → quét toàn bộ bài blog mọi ngôn ngữ qua WordPress REST API tìm 8 loại lỗi (ĐÃ KIỂM / NGHI VẤN) + GEO + chính sách spam → thứ tự sửa. Lỗi tự nạp vào B5 · Sửa lỗi từng trang; báo cáo lưu `reports/chan-doan-rot-top-*.md`. Gõ một câu với Claude Code: skill `/rooty-chan-doan` |
| — | **Tổng quan** | — | Thẻ tiến độ của cả 10 bước + nhật ký; bấm thẻ để mở bước |
| 1 · Discovery | **B1 · Khách hàng & hành trình** | Nguồn dữ liệu khách, Khách hàng, Hành trình khách | ① 9 nguồn dữ liệu cần thu (kèm mẫu khảo sát `quy-trinh/mau-khao-sat-khach.md`) · ② thẻ chân dung đủ 5 phần (nhân khẩu học, tâm lý & lối sống, nhu cầu & động cơ, điểm đau, hành vi tiêu dùng) · ③ bản đồ hành trình 5 giai đoạn × điểm chạm, cảm xúc, rào cản, cơ hội — lọc theo nhóm khách |
| | **B2 · Từ khoá** | Từ khoá gốc, Từ khoá | ① 20 seed mẫu (tên sản phẩm, thương hiệu, tính năng, nhu cầu, địa điểm) + nút **Mở rộng bằng gợi ý Google** (chạy nền) · ② link công cụ (Keyword Planner, GSC, Ahrefs/Semrush, Keywordtool.io) · ③ Nhập CSV mọi công cụ (kể cả file UTF-16 của Keyword Planner), tự đoán ý định Informational/Navigational/Commercial/Transactional, Xuất CSV |
| | **B3 · Cụm chủ đề & silo** | Từ khoá (cột Nhóm URL, Cụm), Trang đích | Bảng cụm: mỗi nhóm URL = 1 bài, tổng lượng tìm, gợi ý Pillar (3.000–5.000 từ) / Cluster (1.000–2.000 từ). Nút **Gợi ý gom nhóm tự động**, **Tạo bài cho nhóm chưa có trang** (đưa vào B6), **Xuất CSV** cho Excel/Sheets |
| | **B4 · Đối thủ** | Đối thủ, Từ khoá đối thủ | Điểm mạnh (nội dung, backlink, UX/tốc độ, thương hiệu/giá) & điểm yếu (content gap, bài cũ, chuyển đổi); nút **Soi website** (tốc độ, title/meta, H1, schema, hreflang, sitemap). Nhập CSV organic keywords từ Ahrefs/Semrush → **Phân loại Common/Gap** → **Chuyển Gap sang Từ khoá** |
| 2 · Improving | **B5 · Audit 5 hạng mục** | Checklist audit | 74 mục chia 5 hạng mục **Technical SEO · Silo · UX/UI · Onsite · Entity**, mỗi hạng mục có thẻ điểm %. Nút **Kiểm tự động** chấm 58 mục (robots, sitemap, meta robots, 404/5xx, redirect, SSL/HSTS, CWV mobile + desktop, schema, hreflang, bot AI · tầng danh mục, breadcrumb, cụm/Pillar, phễu TOFU–MOFU–BOFU, trang mồ côi, link nội bộ · ô tìm kiếm, CTA Zalo/gọi, GA4/GTM · title, meta, H1, H2, trang mỏng, trùng lặp, ảnh alt/WebP/dung lượng · NAP trên web, schema Organization, Person, hồ sơ & citation). Nút **Chạy crawl** quét toàn site |
| | **B5 · Danh sách lỗi & sửa** | Audit, Sửa lỗi từng trang | Lỗi gom từ crawl + GEO audit; mỗi lần crawl lại tự thêm lỗi mới, đóng lỗi đã hết, mở lại lỗi tái phát (chỉ tự đóng khi crawl quét hết site). **Sửa lỗi từng trang**: nhập báo cáo lỗi .xlsx (mỗi tab một loại lỗi, có cột URL / Các URL) → mỗi lỗi × trang một dòng, trạng thái Mới → Đã xác nhận → Đang sửa → Đã sửa (+ Sửa chưa đạt, Tái phát, Hết lỗi, Không phải lỗi, Bỏ qua); đánh dấu Đã sửa tự ghi ngày sửa + chụp lượt nhấp/vị trí GSC làm mốc trước; **Kiểm lại trang** (máy tự kiểm link tự thân, đổi năm giả); **Đo hiệu quả** sau ≥ 4 tuần, so nhóm đã sửa với nhóm chưa sửa (đối chứng) theo từng loại lỗi; nhập đợt quét mới tự đóng lỗi đã hết và đánh dấu tái phát |
| | **B5 · Kiểm nhiều website** | Kiểm nhiều website | Dán tối đa 50 địa chỉ/lần, kiểm song song 4 cái: tên miền → 34 mục tự động như B5 (robots, sitemap, HTTPS/HSTS, tốc độ, bot AI, canonical, hreflang, schema, NAP, ảnh…); link bài → chấm GEO + onpage. Ra điểm %, “Lỗi cần sửa” xếp 🔴 trước, lọc theo nhóm (công ty / đối thủ / khách), Kiểm lại, Xuất CSV |
| 3 · Create & Optimize | **B6 · Content** | Bài viết | Kanban 6 trạm, chấm 4 cổng QC, khoá chuyển trạm khi chưa PASS. Mỗi bài có: ① **Search Intent** (Thông tin/Điều hướng/Cân nhắc/Mua + định dạng phù hợp, nút suy ý định từ nhóm từ khoá B3) · ② **Phân tích SERP** (mở Google đúng từ khoá, ghi loại trang top 10, tick Featured Snippet/PAA/Local Pack/Video/AI Overview, nút lấy câu hỏi thật từ gợi ý Google) · ③ **Chấm bài đã đăng** theo intent (trả lời đầu bài, H1/H2/H3, bullet, bảng, ảnh, video, giá + nút đặt, schema…) ra điểm /100 · ④ **Chấm GEO** theo checklist GTV |
| | **B6 · Giá & dữ kiện** | Giá & dữ kiện | Một nguồn sự thật cho giá/giờ/lịch, có nguồn + ngày kiểm + hạn kiểm lại. **Lấy giá từ trang sản phẩm Rooty** (schema Offer) — chạy lại là tự phát hiện đổi giá, lưu giá cũ + lịch sử. Sửa tay «Giá trị» cũng tự ghi lịch sử. **Dò bài đang ghi giá**: đọc toàn blog, con số tiền đứng ngay sau tên sản phẩm (cùng câu, ≤ 15 chữ) mà khác giá hiện tại → việc «Giá cũ» ở B5 · Sửa lỗi từng trang (đổi số nào thành số nào, ở câu nào), có «Kiểm lại trang» |
| | **B7 · Onpage** | Trang đích (cột onpage) | 5 hạng mục, mỗi hạng mục 1 thẻ điểm: **Title** (50–60 ký tự, từ khoá gần đầu, "\| Rooty Trip" ở cuối) · **Meta** (120–160, có từ khoá, có lời kêu gọi) · **Heading** (1 H1 chứa từ khoá ≈ Title, H2/H3 chứa từ khoá phụ) · **URL** (ngắn, không dấu, gạch ngang, có từ khoá, không từ thừa/ngày tháng) · **Hình ảnh** (tên file, alt, WebP, ≤ 200KB). Nút chấm nhanh mọi trang từ crawl, chấm chi tiết 40 trang quan trọng (chạy nền), chấm từng trang; kèm gợi ý Title/Meta |
| | **B8 · Entity** | Thông tin thương hiệu, Hồ sơ thương hiệu, Thực thể | ① **NAP gốc** (nút lấy từ schema trang chủ) · ② 19 hồ sơ chia nhóm Mạng xã hội / Xác thực bên thứ ba (GBP, Bing Places, Apple, Wikidata) / Danh bạ & citation / OTA & đánh giá; nút **Quét liên kết chéo** (web có link tới hồ sơ? có trong sameAs? link có đúng là hồ sơ không, link trên web và sameAs có khớp?) và **Kiểm NAP** từng hồ sơ · ③ **Sinh JSON-LD** TravelAgency + Organization + WebSite + WebPage, liệt kê chỗ schema trang chủ còn thiếu · ④ Thực thể & dữ kiện |
| | **GEO · AI Search** | Checklist GEO, Bộ câu hỏi AI, Đo hiện diện AI (+ cột Điểm GEO trong Trang đích và Bài viết) | Theo **Checklist GEO của GTV** (32 việc, 6 điểm chạm G0–G5, 🔒 cửa chặn). ① Thẻ tiến độ từng điểm chạm + nút **Tự kiểm từ dữ liệu** (17 việc tự lấy kết quả từ B5, chấm bài, GSC, đo AI) · ② **Chấm GEO từng bài** (#8, #13–20, #22, #24: mở đầu = câu trả lời, H2 = câu hỏi thật, câu đầu sau H2 trả lời 40–50 từ, đoạn tự đứng, mật độ dữ kiện, trích nguồn, thông tin riêng Rooty, tác giả, độ mới, AggregateRating) — chấm 30 bài chạy nền, hoặc từng bài ở B6 · ③ **Đo hiện diện AI**: dán câu trả lời của ChatGPT/Gemini/AI Overview/Perplexity → tự ghi nhắc tên, trích link, thứ tự, đối thủ, số hotline sai; tổng hợp theo máy AI và theo chủ đề, đếm đủ 3 lần/câu/máy, cảnh báo tập trung > 70% |
| 4 · Promotion | **B9 · Link building** | Liên kết | ⓪ **Kế hoạch link cho một trang cần lên top** (silo kim tự tháp): chọn trang + từ khoá → trang đích ở đỉnh, danh mục + bài trụ ở giữa, bài vệ tinh cùng chủ đề ở đáy; liệt kê link nào đã có, link nào thiếu, link chỉ bằng “Đặt ngay!”/ảnh (cần thêm link chữ), anchor theo tỉ lệ an toàn (chính xác ~15% · biến thể ~55% · thương hiệu ~10% · mô tả ~20%, xoay vòng không lặp) + câu đặt link; việc thiếu tự vào bảng Liên kết · ① **Internal link**: crawl ghi bản đồ link nội bộ (`reports/crawl-*.links.tsv`: từ → đến, anchor, rel, vị trí nội dung/menu/footer); thống kê anchor chung chung, trang tour/danh mục/Pillar ít link; nút **Gợi ý link nội bộ** tìm câu trong bài blog đã nhắc tới trang đích mà chưa gắn link (kèm anchor + câu) · ② **Backlink**: chiến lược (Guest post, PR, Broken link, Linkable asset…), DR/DA, liên quan, vị trí → điểm chất lượng; nút **Kiểm backlink còn sống** (còn link? dofollow? trong nội dung?); phân bổ anchor + cảnh báo anchor từ khoá > 30% · ③ **Tìm link gãy** trên trang của site khác, lưu thành cơ hội |
| 5 · Evaluate | **B10 · Review** | Đánh giá tháng, Xung đột từ khoá, Nhật ký thay đổi, Lịch review (+ cột số liệu trong Trang đích) | ① **Nhập CSV** GSC/GA4 — tự nhận file Ngày / Trang / Truy vấn / Truy vấn × Trang / GA4 Trang đích · ② KPI tháng so tháng trước (lượt nhấp, hiển thị, CTR, vị trí, phiên, tương tác, thời gian, tỷ lệ chuyển đổi) + **cảnh báo tuần** (giảm ≥ 20%) + biểu đồ · ③ **Xung đột từ khoá** · ④ **Content audit** tự đề xuất Giữ / Cập nhật / Gộp / Xoá-301 / Noindex kèm lý do → cột Quyết định → tạo việc sang B6 · ⑤ **Change log** đo trước/sau · ⑥ **Lịch review** tuần/tháng/quý, báo việc quá hạn |
| | **B10 · Thuật toán Google** | Cập nhật thuật toán, Tin Google Search Central, Chính sách spam Google | Tự lấy (mỗi 24 giờ khi mở app, hoặc bấm nút) các đợt core/spam update từ **Google Search Status Dashboard** và tin từ **blog Search Central** — chỉ nguồn chính thức. Đo ảnh hưởng mỗi đợt lên Rooty bằng GSC theo ngày (14 ngày trước vs 14 ngày sau), kèm việc cần làm theo loại đợt; banner khi có đợt đang triển khai. Checklist **19 chính sách spam** của Google với rủi ro cụ thể cho Rooty, nút **Tự kiểm** từ dữ liệu app (lỗi từng trang, GEO, backlink trả tiền); danh sách “lên top nhanh mà không vi phạm” |
| Quản lý | **Kế hoạch 10 tháng** | Việc SEO | 37 công đoạn theo pha, việc trễ/đang trong hạn, mở SOP, copy lệnh |

Các bảng nối với nhau qua **URL trang đích**: cột "Trang đích" (Từ khoá), "Từ/Đến URL" (Liên kết), "Trang đáp ứng" (Hành trình), "Link bài" (Bài viết) đều gợi ý từ danh sách URL trong bảng Trang đích.

## Nạp dữ liệu có sẵn
- **B5 → "Chạy crawl"**: quét toàn site ngay trên trang (5–8 phút, chạy nền), xong tự cập nhật Trang đích, Audit và các mục T12–T16. Vẫn chạy được bằng lệnh: `python -X utf8 scripts/crawl_site.py https://rootytrip.com --max-pages 1500`
- **B5 → "Kiểm tự động"**: chấm 26 mục Technical SEO (~40 giây). Lần đầu tự nạp checklist.
- **B3 / B7 → "Nạp trang từ crawl"**: đọc `reports/crawl-*.csv` mới nhất.
- **B5 → "Nạp lỗi từ báo cáo"**: gom lỗi từ crawl + `reports/geo-audit-*.md` mới nhất.
- **B1, B8 → "Nạp dữ liệu mẫu"** (hiện khi bảng trống): 9 nguồn dữ liệu cần thu, 4 chân dung giả định (cần xác nhận bằng dữ liệu thật), 10 ghi nhận hành trình qua 5 giai đoạn, 11 nền tảng hồ sơ, 2 thực thể.
- **B2 → "Nhập CSV"**: file xuất Search Console (Truy vấn) hoặc Keyword Planner/Ahrefs/Semrush.
- Nạp lại nhiều lần không bị trùng (bỏ qua dòng đã có).

## Nối Lark Base (làm một lần, ~10 phút)

1. **Tạo Base** trong Lark **Drive** (không tạo trong Wiki). Mã Base là phần sau `/base/` trên thanh địa chỉ, trước dấu `?`.
2. **Tạo app**: https://open.larksuite.com/app → Create Custom App → lấy **App ID**, **App Secret** (Credentials & Basic Info).
3. **Cấp quyền**: Permissions & Scopes → `bitable:app` → Version Management & Release → phát hành (có thể cần admin duyệt).
4. **Cho app vào Base**: mở Base → **…** → **Add Document App** → chọn app, quyền **có thể quản lý**.
5. **Điền `.env`**: copy `.env.example` → `.env` (thư mục `rooty-seo-production`), tự điền App ID, App Secret, mã Base, `PROJECT_START`.
6. **Chạy lại server** → bấm **Khởi tạo bảng Lark** → trang tự tạo **30 bảng** (thêm Giá & dữ kiện, Kiểm nhiều website, Cập nhật thuật toán, Tin Google Search Central, Chính sách spam Google, Sửa lỗi từng trang, Thông tin thương hiệu, Xung đột từ khoá, Nhật ký thay đổi, Lịch review, Checklist GEO, Bộ câu hỏi AI, Đo hiện diện AI): Bài viết · Việc SEO · Nhật ký · Nguồn dữ liệu khách · Khách hàng · Hành trình khách · Từ khoá gốc · Từ khoá · Trang đích · Đối thủ · Từ khoá đối thủ · Checklist audit · Audit · Thực thể · Hồ sơ thương hiệu · Liên kết · Đánh giá tháng.
7. Đã làm ở chế độ demo trên máy? Bấm **Chuyển dữ liệu máy → Lark** (góc trên): chép mọi bảng trong `app/demo-data.json` lên Lark, chỉ ghi vào bảng Lark còn trống nên bấm lại không bị nhân đôi. Chưa có gì thì bấm các nút nạp dữ liệu ở B3, B5, B1, B8 và "Nạp công đoạn" ở Kế hoạch.

Sau đó mọi thao tác trên trang ghi thẳng vào Lark. Team có thể mở Base để xem, lọc, làm dashboard, hoặc gắn automation (VD báo vào group chat khi có vấn đề 🔴 mới hoặc bài "Chờ duyệt"). Muốn nối bảng bằng trường "Liên kết hai chiều" của Lark thì thêm cột mới trong Lark — đừng đổi tên cột có sẵn.

## Lỗi hay gặp

| Thông báo | Cách sửa |
|---|---|
| `Sai App ID/App Secret?` | Kiểm lại `.env`, không có dấu cách thừa |
| `Lark lỗi 91403` / Forbidden | App chưa được thêm vào Base (bước 4) hoặc chỉ có quyền xem |
| `Lark lỗi 99991672` / thiếu quyền | Chưa thêm `bitable:app` hoặc chưa phát hành phiên bản |
| `Chưa có bảng «…»` | Bấm **Khởi tạo bảng Lark** (bấm lại an toàn — chỉ tạo bảng/cột còn thiếu) |
| `Chưa có báo cáo crawl` | Chạy `scripts/crawl_site.py` trước |
| Dùng Feishu | `LARK_DOMAIN=https://open.feishu.cn` |

## Lưu ý
- Đừng đổi tên bảng/cột trong Lark — trang tìm theo đúng tên. Thêm cột mới thì thoải mái.
- `.env` và `app/demo-data.json` nằm trong `.gitignore`.
- AI không tự sửa website, không tự đăng bài, không gửi gì ra ngoài — chỉ soạn và phân tích.
