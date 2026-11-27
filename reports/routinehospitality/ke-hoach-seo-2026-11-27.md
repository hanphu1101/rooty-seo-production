# Kế hoạch SEO routinehospitality.vn · lập ngày 27/11/2026

Người lập: Claude (em), theo yêu cầu chị Hân. Khung: `quy-trinh/00-tong-quan.md` + `quy-trinh/cong-doan.json` (33 công đoạn, 5 pha), co lại cho **web khách sạn mới** thay vì web tour đã có nhiều bài.

**Nguồn dữ liệu dùng trong bản này**
- Google Sheet «KEY KS ROUTINE» (tab duy nhất, gid 1654902300): xuất từ Google Keyword Planner, kỳ 01/11/2025 – 31/10/2026, 2.443 từ khoá. Bảng phân cụm đầy đủ (mỗi từ khoá 1 cụm + trang gợi ý): [`tu-khoa-phan-cum-2026-11-27.csv`](tu-khoa-phan-cum-2026-11-27.csv).
- Khảo sát trực tiếp routinehospitality.vn ngày 27/11/2026 (HTML thật, robots.txt, sitemap.xml, header HTTP).
- Search Console theo ngày đã nạp vào app: `reports/web/routinehospitality.vn/du-lieu/gsc-daily.json` (22/10 – 14/11/2026).
- Không ghi gì vào Google Sheet (sheet là dữ liệu từ khoá, không phải mẫu kế hoạch).

**Theo dõi hằng ngày (không cần Claude):** app SEO Automation → chọn web «Routine Hospitality» → tab **Kế hoạch**. 41 việc (RH01–RH37 + 4 việc lặp RH-L1…L4) đã nạp vào bảng «Việc SEO» của Base Routine; mỗi việc có người làm, hạn, đầu ra, «Xong khi». Người làm tự đổi trạng thái, ghi link kết quả, ghi chú; app tự báo việc tháng này và việc trễ (dự án bắt đầu 12/2026, ô «Bắt đầu dự án» trong bảng «Danh sách website»). Bản CSV cùng nội dung: [`viec-seo-2026-11-27.csv`](viec-seo-2026-11-27.csv).

---

## 1. Tóm tắt 5 dòng

1. Web còn rất mới: Search Console ghi nhận **8 lượt nhấp, 318 lượt hiển thị** trong 24 ngày (22/10 – 14/11/2026), lượt hiển thị đầu tiên ngày 02/11/2026. Chưa có số nền đủ để đặt KPI → tháng 1 phải dựng đo lường trước.
2. **86% lượng tìm trong sheet (317.600/370.140 lượt/tháng) là tên khách sạn khác** (JW Marriott, Mường Thanh, Novotel…). Không nhắm được trực tiếp.
3. Tên khách sạn của Routine gần như vắng mặt trong sheet: chỉ **Praha Hotel (7 từ khoá, tổng 2.560)** và **Times Corner (1 từ khoá, 140)**. PITO, Routine, Calista, Wyndham, Lyn, Casepia, Duo, Daystar: **không có từ khoá nào** → phải chạy lại Keyword Planner với tên các khách sạn này.
4. Phần nhắm được thật là **trang khu vực** (Nam đảo 390, Dương Đông 320, Địa Trung Hải 260, An Thới 210, Bắc đảo 170, Bãi Khem 170, gần chợ đêm 170, Grand World 140…) và **trang từng khách sạn** — web đã có khung cho cả hai, nhưng nội dung còn mỏng (trang khách sạn PITO ~350 chữ, trang Nam đảo ~250 chữ).
5. Cơ hội lưu lượng sớm nằm ở bài cẩm nang ít cạnh tranh gắn với khách sạn: **cảng An Thới (6.600/tháng, cạnh tranh quảng cáo Thấp)**, Phu Quoc Express (2.400), Grand World giá vé (210), làng chài Rạch Vẹm (210).

---

## 2. Hiện trạng website (kiểm ngày 27/11/2026)

| Hạng mục | Thấy gì | Đánh giá |
|---|---|---|
| Doanh nghiệp | Chuỗi khách sạn tại Phú Quốc. Pháp nhân: Công ty TNHH Khách sạn Hòn Thơm Phú Quốc, MST 1702375019, văn phòng Căn M6-32 Santo Port, Hòn Thơm. Hotline/Zalo (+84) 915 919 328, email pito@routinehospitality.vn | Đủ NAP gốc cho trang Liên hệ |
| Khách sạn | 12 trang `/hotel/…`: PITO Hòn Thơm, Routine Hotel Hòn Thơm, Calista (khai trương 20/12/2026 theo web), Wyndham Garden Grandworld, Wyndham Grand, Times Corner Sorrento, Times Corner Amalfi, Praha, Daystar, Lyn Hotel 2, Casepia Sorrento, Duo by Casepia | Quan hệ của Routine với Wyndham (quản lý? đại lý?) **[CẦN KIỂM CHỨNG]** — ảnh hưởng việc có được làm GBP/trang thương hiệu hay không |
| Nền tảng | Next.js (header `x-powered-by: Next.js`), chạy trên Render, qua Cloudflare. Mã nguồn: `C:\HAN\code web ks routine\rt-hospitality-webapp` (GitHub xhai2k/rt-hospitality-webapp) | Không phải WordPress → mọi sửa kỹ thuật/onpage là **sửa code**, cần dev |
| HTML | Nội dung có sẵn trong HTML (SSR), mỗi trang có title riêng, meta description, canonical tự trỏ, hreflang vi/en/x-default | Tốt cho Google và bot AI |
| Chuyển hướng | http:// và www → 301 về https://routinehospitality.vn/ | Đạt |
| robots.txt | Cho phép tất cả, chặn trang đặt phòng/tài khoản/API; khai sitemap | Đạt |
| sitemap.xml | 1 file, 39 thẻ `<loc>`, có hreflang; chỉ 2 URL có `lastmod`; không có sitemap index | Thêm `lastmod` cho mọi URL |
| Trang chủ | Title «Routine Hospitality — Khách sạn tại Phú Quốc», 1 H1 «Tự do & thoải mái, giữa lòng Phú Quốc», **không có JSON-LD** | H1 không chứa «khách sạn Phú Quốc»; thiếu schema thực thể |
| Trang khách sạn | Có schema `Hotel`. H1 = «Chào mừng quý khách đến với PITO Hòn Thơm» (mẫu chung), ~350 chữ, 6/12 ảnh thiếu alt (PITO) | H1 nên là tên khách sạn + khu vực; nội dung mỏng |
| Trang khu vực | `/khach-san/nam-dao`, `bac-dao`, `trung-tam`, `hon-thom`, `sunset-town` — Nam đảo ~250 chữ | Đúng hướng, cần viết dày |
| Cẩm nang | `/cam-nang/cap-treo-hon-thom` (~1.500 chữ, H2 dạng câu hỏi, có FAQPage), `/diem-den/hon-thom-santo-port` | Tốt; FAQPage Google hầu như không còn hiển thị → không ưu tiên |
| Tour/combo | 6 trang tour + 2 combo, có schema `Product` | Là mảng phụ; không để ăn thịt từ khoá khách sạn |
| Nội dung tạm | «Ưu đãi mẫu · Chờ Routine xác nhận», ảnh `/home/hotel-sample.jpg`, Calista «Ảnh đang cập nhật» | Phải thay trước khi đẩy SEO |
| Đo lường | GSC có dữ liệu (app đọc được). GA4 property 560433112 **chưa cấp quyền** cho tài khoản dịch vụ (memory 17/11/2026). Sự kiện chuyển đổi (Zalo, gọi, đặt phòng) **[CẦN KIỂM CHỨNG]** | Việc số 1 của tháng 1 |
| Blog | `/blog` trả 404; cẩm nang nằm ở `/cam-nang/` và `/diem-den/` | Giữ 2 thư mục này, không tạo `/blog` song song |

---

## 3. Từ khoá → chủ đề → trang đích

Chi tiết từng từ khoá: [`tu-khoa-phan-cum-2026-11-27.csv`](tu-khoa-phan-cum-2026-11-27.csv). Số lượng tìm là trung bình tháng theo Keyword Planner; cột «cạnh tranh» là **cạnh tranh quảng cáo**, không phải độ khó lên top tự nhiên.

### 3.1 Tổng quan sheet

| Nhóm | Số từ khoá | Lượt tìm/tháng | Tỷ trọng |
|---|---|---|---|
| Tên khách sạn khác (đối thủ) | 1.759 | 317.600 | 85,8% |
| «khách sạn phú quốc» và biến thể (tiếng Việt) | 54 | 16.090 | 4,3% |
| Du lịch không phải lưu trú (cảng, tàu, điểm đến) | 58 | 12.220 | 3,3% |
| Hạng sao / giá / loại hình | 255 | 9.230 | 2,5% |
| Khu vực | 186 | 6.830 | 1,8% |
| «resort/hotel phú quốc» | 8 | 2.780 | 0,8% |
| Tên khách sạn Routine | 8 | 2.700 | 0,7% |
| Đặt phòng (đặt phòng, booking, agoda) | 76 | 2.130 | 0,6% |
| Thông tin («nên ở khách sạn nào») | 39 | 560 | 0,2% |

1.501/2.443 từ khoá (61%) có lượng tìm 0 hoặc 10. Ba từ khoá đang có trong tài khoản Google Ads (cột «In account?» = Y): khách sạn nam đảo phú quốc, khách sạn an thới phú quốc, khách sạn an thới.

**Mùa vụ** (nhóm từ khoá chung, bỏ tên đối thủ): cao nhất tháng 6/2026 (46.520) và 12/2025 (43.510), thấp nhất 9–10/2026 (~27.000). → Trang phải chín trước **tháng 6/2027** nghĩa là xong nội dung **trước giữa tháng 3/2027** (nguyên tắc ~100 ngày).

### 3.2 Bản đồ chủ đề đề xuất (chốt ở công đoạn ◇10)

| Cụm | Từ khoá chính (lượt/tháng) | Trang đích | Có sẵn? | Ưu tiên |
|---|---|---|---|---|
| Trụ: khách sạn Phú Quốc | khách sạn phú quốc (6.600), khách sạn ở phú quốc (880), resort phú quốc (1.900), hotel phú quốc (390) | `/khach-san` (+ trang chủ nhắm thương hiệu) | Có, mỏng | Trung bình — đối thủ là OTA, lâu mới lên |
| Nam đảo | khách sạn nam đảo phú quốc (390), khách sạn ở nam đảo (140) | `/khach-san/nam-dao` | Có, mỏng | **Cao** |
| Sunset Town / Địa Trung Hải / An Thới | khách sạn địa trung hải phú quốc (260), khách sạn an thới phú quốc (210), khách sạn an thới (110), nhà nghỉ an thới (70) | `/khach-san/sunset-town` (6 khách sạn của Routine ở đây) | Có | **Cao** |
| Hòn Thơm | khách sạn hòn thơm phú quốc (50), khách sạn ở hòn thơm (30) | `/khach-san/hon-thom` | Có | Cao (ít tìm nhưng Routine gần như độc quyền: PITO + Routine Hotel) |
| Dương Đông / trung tâm / chợ đêm | khách sạn dương đông (320), khách sạn trung tâm (210), gần chợ đêm (170 + 170) | `/khach-san/trung-tam` | Có | Trung bình (chỉ có Daystar) |
| Bắc đảo / Grand World / Gành Dầu | khách sạn bắc đảo (170), khách sạn grand world (140), gần vinwonder (110), khách sạn gành dầu (40) | `/khach-san/bac-dao` | Có | Trung bình — phụ thuộc quan hệ với Wyndham **[CẦN KIỂM CHỨNG]** |
| Bãi Khem / Bãi Sao | khách sạn bãi khem (170), gần bãi khem (90), gần bãi sao (40) | Gộp vào `/khach-san/nam-dao` (mục H2 riêng), không tạo trang mới đến khi có khách sạn ở đó | — | Thấp |
| Tên từng khách sạn | praha hotel phú quốc (1.900), khách sạn praha (320), times corner hotel (140); các tên khác **chưa có số** | `/hotel/<slug>` | Có (12 trang) | **Cao** |
| Hạng sao | khách sạn 3/4/5 sao phú quốc (720 mỗi từ) | Chỉ làm nếu khách sạn có hạng sao chính thức **[CẦN KIỂM CHỨNG]** → bộ lọc trên `/khach-san` | Chưa | Treo |
| Giá rẻ / nhà nghỉ | nhà nghỉ phú quốc (1.000), khách sạn phú quốc giá rẻ (140) | Chỉ nhắm nếu giá Routine thật sự ở phân khúc này (web ghi Routine Hotel từ 300.000đ/đêm) | Chưa | Thấp |
| Cẩm nang gắn khách sạn | cảng an thới (6.600), phu quoc express (2.400), grand world phú quốc giá vé (210), làng chài rạch vẹm (210), cáp treo hòn thơm (đã có bài), «đi phú quốc nên ở khách sạn nào» (30 + biến thể) | `/cam-nang/<slug>`, `/diem-den/<slug>`, mỗi bài link về trang khu vực + khách sạn gần nhất | 1–2 bài có | **Cao** (traffic sớm) |
| Đặt phòng | đặt phòng phú quốc (210), đặt phòng khách sạn phú quốc (110), booking phú quốc (170) | Không làm trang riêng; nhắm bằng title/meta trang `/khach-san` | — | Thấp |

**Không làm:** trang so sánh với khách sạn đối thủ theo tên (JW Marriott, Mường Thanh…) — không có cách chấm công khai, dễ thành nội dung mỏng.

---

## 4. Lộ trình 10 tháng

T1 = tháng 12/2026 → T10 = tháng 9/2027. Tháng 1–3 chia theo tuần, từ tháng 4 theo tháng. Mã công đoạn theo `quy-trinh/cong-doan.json`.

**Người làm (vai trò, cần chị điền tên):**
- **Chị Hân** — trưởng SEO, duyệt cổng 4, quyết định ở các cửa ◇.
- **Dev** — người giữ repo `rt-hospitality-webapp` **[CẦN KIỂM CHỨNG tên]**: mọi sửa code, schema, sitemap.
- **QL KS** — quản lý/lễ tân từng khách sạn: ảnh thật, thông tin phòng, GBP, xin đánh giá.
- **CSKH** — người trực Zalo/hotline/pito@: câu hỏi khách hay hỏi, nguồn đặt phòng.
- **AI** — Claude: nghiên cứu, soạn nháp qua dây chuyền 6 trạm, audit, báo cáo.

### Tháng 1 · 12/2026 — Pha 1: đo lường, nền tảng, sửa lỗi

| Tuần | Việc (mã) | Người | Xong khi (kiểm được) |
|---|---|---|---|
| T1·W1 (1–7/12) | **Đo lường** (01, SOP 11): cấp quyền GA4 560433112 cho tài khoản dịch vụ; xác minh GSC dạng domain property; đặt sự kiện chuyển đổi: bấm Zalo, gọi, WhatsApp, gửi đặt phòng thành công | Chị Hân + Dev | App SEO tab GA4 đọc được số Routine; GA4 → Key events có ≥ 4 sự kiện và mỗi sự kiện đã ghi ≥ 1 lượt thử |
| T1·W1 | **Lấy số nền** GSC 3 tháng (từ khi có dữ liệu) + GA4 | AI | File `reports/web/routinehospitality.vn/du-lieu/so-nen-2026-12.md` có clicks, impressions, CTR, vị trí, phiên organic, chuyển đổi — mỗi số ghi khoảng ngày |
| T1·W1 | **Chạy lại Keyword Planner** với tên 12 khách sạn + «routine hospitality» + Santo Port, Sunset Town, Hòn Thơm | Chị Hân | Sheet có thêm tab mới; mỗi khách sạn có ≥ 1 dòng (hoặc ghi rõ «không có lượng tìm») |
| T1·W1 | **Họp khởi động** (12): chốt người làm, quan hệ với Wyndham, hạng sao từng khách sạn, ai trả lời đánh giá | Chị Hân | Biên bản có tên người phụ trách + hạn cho Dev, QL KS, CSKH; 3 điểm [CẦN KIỂM CHỨNG] ở mục 2 đã có câu trả lời |
| T1·W2 (8–14/12) | **Rà soát toàn site** (05): `python -X utf8 scripts/crawl_site.py https://routinehospitality.vn --max-pages 300` + `scripts/geo_audit.py` | AI | Có `reports/web/routinehospitality.vn/crawl-<ngày>.csv` + báo cáo geo-audit; lỗi nạp vào B5 (chọn web Routine) |
| T1·W2 | **Đối thủ theo loại trang** (02): top 10 Google cho «khách sạn nam đảo phú quốc», «khách sạn an thới phú quốc», «khách sạn địa trung hải phú quốc», «praha hotel phú quốc», «cảng an thới» | AI | Báo cáo ≥ 5 đối thủ, mỗi loại trang (khu vực, khách sạn, cẩm nang) ≥ 1 đối thủ + danh sách khoảng trống |
| T1·W2–W3 | **Sửa lỗi kỹ thuật** (R1), thứ tự: (1) gỡ nội dung tạm «Ưu đãi mẫu», ảnh `hotel-sample.jpg`; (2) H1 trang khách sạn = «<Tên> – khách sạn <loại> tại <khu vực>, Phú Quốc»; (3) alt cho ảnh nội dung; (4) `lastmod` cho mọi URL trong sitemap; (5) JSON-LD trang chủ: `Organization` (hoặc `LodgingBusiness` cấp chuỗi) có tên, logo, địa chỉ, điện thoại, `sameAs` | Dev (AI soạn đặc tả) | Nhật ký thay đổi B11 mỗi dòng có «Phép kiểm», ví dụ: `KHÔNG: Ưu đãi mẫu` (trang chủ) · `KHÔNG: Chào mừng quý khách đến với` (trang khách sạn) · `CÓ: application/ld+json` (trang chủ); nút «Thanh tra» chấm Đạt hết; validator.schema.org không lỗi |
| T1·W3 (15–21/12) | **Gom từ khoá → trang đích** (04): từ file phân cụm, gán đúng 1 URL cho mỗi cụm, tạo `nghien-cuu/routinehospitality/tu-khoa-chu-de.csv` | AI, chị Hân duyệt | 100% từ khoá ngoài nhóm «đối thủ» có cụm + URL đích; không 2 URL cùng nhắm 1 từ khoá chính |
| T1·W3 | **GBP từng khách sạn** (R3) — kiểm kê: khách sạn nào đã có hồ sơ, ai là chủ sở hữu, NAP có khớp trang `/hotel/<slug>` không | QL KS + AI | Bảng `nghien-cuu/routinehospitality/ho-so-thuong-hieu.csv` có 12 dòng: url GBP, chủ sở hữu, tên/địa chỉ/điện thoại, số đánh giá, điểm, ngày kiểm |
| T1·W3 | **Calista khai trương 20/12/2026**: ảnh thật, giá thật lên trang `/hotel/calista`; tạo/nhận GBP | QL KS Calista + Dev | Trang không còn «Ảnh đang cập nhật»; GBP Calista đã gửi xác minh |
| T1·W4 (22–31/12) | **Nền marketing** (03): chân dung khách (cặp đôi, gia đình, nhóm bạn, khách công tác…), lý do chọn từng khách sạn; giọng văn Routine | AI soạn, chị Hân chốt | File `00-context/routinehospitality/brand.md` + `giong-van.md` được chị duyệt |
| T1·W4 | **GEO số nền** (14): bộ 20 câu hỏi cố định («khách sạn ở Hòn Thơm», «nên ở đâu khi đi cáp treo Hòn Thơm», «khách sạn gần cảng An Thới»…), mỗi câu chạy 3 lần trên ChatGPT/Gemini/Perplexity | AI | File CSV kết quả có tỷ lệ nhắc tên Routine/từng khách sạn theo câu; dán nhãn «tham khảo xu hướng» |
| T1·W4 | **Chiến lược + KPI** (01, 08) — đặt KPI theo quý từ số nền | AI đề xuất, chị Hân duyệt | Bảng KPI có con số cho Q1–Q3/2027: lượt nhấp organic, lượt chuyển đổi organic, số từ khoá khu vực vào top 10 |

### Tháng 2 · 01/2027 — Pha 2: cấu trúc + trang đích

| Tuần | Việc (mã) | Người | Xong khi |
|---|---|---|---|
| T2·W1 (1–7/1) | **Chốt bản đồ chủ đề** (◇10) từ mục 3.2 | Chị Hân | `nghien-cuu/routinehospitality/topical-map.md` có mọi node: URL, loại trang, từ khoá chính, trạng thái; chị ghi «chốt» |
| T2·W1–W2 | **Cấu trúc + mẫu trang** (11): mẫu trang khu vực và trang khách sạn (thứ tự: H1 + đoạn trả lời 2–3 câu → bảng nhanh: khu vực, giá từ, số phòng, khoảng cách tới điểm chính → nút đặt/Zalo → hạng phòng → ảnh thật → tiện ích → chính sách → đánh giá thật → FAQ → khách sạn lân cận); breadcrumb mọi trang | AI soạn wireframe, Dev làm | Wireframe được duyệt; mọi trang khách sạn/khu vực ≤ 3 nhấp từ trang chủ (kiểm bằng crawl, cột depth) |
| T2·W2–W4 | **Trang nhận diện** (13): Giới thiệu (Routine là ai, vận hành những khách sạn nào, năm thành lập **[CẦN KIỂM CHỨNG]**), Liên hệ từng khách sạn, FAQ đặt phòng, chính sách huỷ (đã có ~1.200 chữ) | AI + CSKH | Đủ 4 trang; NAP trên trang khớp NAP gốc + GBP từng khách sạn |
| T2·W2–W4 | **Trang khu vực đợt 1** (15): Nam đảo, Sunset Town/An Thới, Hòn Thơm — mỗi trang ≥ 800 chữ, H2 = câu hỏi thật («Ở Sunset Town Phú Quốc có gì?», «Từ An Thới đi cáp treo Hòn Thơm bao xa?»), khoảng cách/giá có nguồn | AI qua dây chuyền 6 trạm, QL KS góp kinh nghiệm thật | Mỗi trang qua cổng 1–3 + chị duyệt cổng 4 và đã đăng; không còn [CẦN KIỂM CHỨNG] trên trang |
| T2·W3–W4 | **Cẩm nang traffic sớm** (09): cảng An Thới, Phu Quoc Express | AI | 2 bài qua cổng 4 và đăng; mỗi bài link về `/khach-san/sunset-town` |

### Tháng 3 · 02/2027 — trang đích còn lại + onpage

| Tuần | Việc | Người | Xong khi |
|---|---|---|---|
| T3·W1–W2 | **Trang khách sạn đợt 1** (15): Praha (có lượng tìm thật), PITO, Routine Hotel, Calista, Times Corner ×2 — mỗi trang ≥ 600 chữ, có hạng phòng, giá từ theo hệ thống đặt phòng, ảnh thật có alt | AI + QL KS | 6 trang đăng lại; Phép kiểm B11 `CÓ: <tên khách sạn>` trong H1; quét giá cũ = 0 |
| T3·W1–W2 | **Trang khu vực đợt 2**: Trung tâm/Dương Đông, Bắc đảo | AI | 2 trang qua cổng 4 và đăng |
| T3·W3–W4 | **Onpage trang đích** (R2) — 10–15 ngày sau khi đăng: title ≤ 60 ký tự bắt đầu bằng từ khoá chính, meta 140–160 ký tự, alt, schema `Hotel` đủ `address`, `telephone`, `priceRange`, `image` (không `aggregateRating` tự chấm) | AI + Dev | Checklist SOP 06 PASS 100% cho mọi trang đích; validator.schema.org không lỗi |
| T3·W3–W4 | **Trang khách sạn đợt 2**: Lyn Hotel 2, Casepia, Duo, Daystar, Wyndham ×2 (tuỳ kết luận họp khởi động) | AI + QL KS | 6 trang đăng lại |
| T3·W4 | **Kế hoạch traffic** (17): lượng tìm × CTR theo vị trí mục tiêu (vị trí 1 ≈ 25–30%, 3 ≈ 10%, 5 ≈ 5–6%, 10 ≈ 2% — ước lượng) | AI | Bảng dự báo ≥ 120% KPI; thiếu thì thêm chủ đề vào map |

> **Mốc cứng:** mọi trang khu vực + khách sạn xong onpage **trước 15/3/2027** để kịp chín cho đỉnh tìm kiếm tháng 6/2027.

### Tháng 4–10 · 03/2027 – 09/2027

| Tháng | Việc (mã) | Người | Xong khi |
|---|---|---|---|
| T4 · 3/2027 | Liên kết nội bộ theo cụm (18): cẩm nang → trang khu vực → trang khách sạn; mỗi trang khách sạn link 2–3 khách sạn cùng khu | AI + Dev | Crawl lại: mọi bài cẩm nang có ≥ 3 link nội bộ đúng cụm; trang mồ côi = 0; link tự trỏ = 0 |
| T4 · 3/2027 | Cẩm nang mở rộng (19), 4 bài/tháng theo hành trình khách: Grand World giá vé, làng chài Rạch Vẹm, «đi Phú Quốc nên ở khu nào», Sunset Town chơi gì, Bãi Khem… | AI, chị duyệt | Bài trong map đã đăng; mỗi bài link về ≥ 1 trang khu vực |
| T4–T5 · 3–4/2027 | Hồ sơ OTA & đánh giá (R4): Booking, Agoda, Traveloka, Tripadvisor, Facebook từng khách sạn — tên, địa chỉ, điện thoại khớp NAP gốc, link về trang `/hotel/<slug>` | QL KS | `ho-so-thuong-hieu.csv` mỗi khách sạn có ≥ 4 nền tảng, cột NAP khớp = có |
| T5 · 4/2027 | Nền offsite (20): Facebook/Instagram/TikTok/YouTube Routine, citation danh bạ; `sameAs` trong schema trang chủ | Chị Hân + AI | Danh sách hồ sơ + citation, mỗi dòng có link kiểm được |
| T5 · 4/2027 | GEO đợt 1 (21): chấm 10 trang traffic cao nhất theo cổng 2; đo lại bộ câu hỏi | AI | Báo cáo có số so với số nền tháng 12/2026 |
| T6 · 5/2027 | ◇22 Thứ hạng ban đầu: so vị trí trang khu vực/khách sạn với dự kiến | Chị Hân | Có quyết định điều chỉnh ghi lại, dựa trên số GSC |
| T6 · 5/2027 | Điều chỉnh bài top 10–30 (23) | AI | Mỗi trang top 10–30 có quyết định giữ/sửa/viết lại; bài sửa có dòng B11 |
| T7 · 6/2027 | ◇25 Cửa offsite — có cần đầu tư link? PR với báo du lịch/địa phương (khai trương, Santo Port…) chỉ khi qua cửa | Chị Hân | Quyết định có/không + ngân sách được duyệt |
| T7 · 6/2027 | Đo GEO giữa kỳ (24) — đúng bộ câu hỏi tháng 12 | AI | Bảng so sánh với số nền |
| T7–T8 · 6–7/2027 | Đọc log Cloudflare/Render (27) + kỹ thuật nâng cao (29): độ sâu click, tốc độ (LCP < 2,5 s, INP < 200 ms, CLS < 0,1 trên di động) | Dev + AI | Googlebot và bot AI vào được trang chính; lỗi Cao = 0 |
| T8 · 7/2027 | GEO đợt 2 (28): viết bổ sung câu hỏi con | AI | Bài bổ sung đăng + gắn link vào bài mẹ |
| T9 · 8/2027 | ◇30 Đạt KPI Q3? + review quản lý (31) | Chị Hân | Bảng đối chiếu KPI + biên bản có người làm và hạn |
| T10 · 9/2027 | Báo cáo kép SEO + AI (32), bàn giao duy trì (33) | AI + chị Hân | Báo cáo so với số nền tháng 12/2026; bộ bàn giao đủ tài khoản, danh sách link, bộ câu hỏi AI, lịch đo |

### Việc lặp lại

| Nhịp | Việc | Người | Xong khi |
|---|---|---|---|
| Tuần | GSC: lỗi lập chỉ mục, truy vấn mới (app SEO, chọn web Routine) | AI | Ghi chú tuần trong Lark Base Routine |
| Tuần | 1–2 bài đăng GBP mỗi khách sạn có GBP; trả lời mọi đánh giá trong 48 giờ | QL KS | Tỷ lệ phản hồi đánh giá = 100% (kiểm trong GBP) |
| Tuần | Xin đánh giá sau lưu trú: QR ở quầy lễ tân + tin Zalo 24 giờ sau trả phòng; không mua/đổi quà lấy đánh giá | QL KS + CSKH | Số đánh giá Google mới/tháng mỗi khách sạn ghi vào `ho-so-thuong-hieu.csv` |
| Tháng | Báo cáo tháng (`rooty-bao-cao`, chọn web Routine); cập nhật giá phòng/ưu đãi trên trang | AI | `reports/routinehospitality/bao-cao-<YYYY-MM>.md`; 5 con số ngẫu nhiên khớp nguồn |
| Quý | Đo hiện diện AI, rà KPI | AI + chị Hân | Bảng so sánh với quý trước |

---

## 5. Rủi ro và cách xử lý

| Rủi ro | Dấu hiệu | Xử lý |
|---|---|---|
| OTA (Agoda, Booking, Traveloka) chiếm hết top cho «khách sạn phú quốc» | Sau 3 tháng `/khach-san` vẫn ngoài top 30 | Không đổ thêm công vào head term; dồn vào trang khu vực + tên khách sạn + cẩm nang |
| Trang chính thức của Wyndham chiếm từ khoá thương hiệu Wyndham | GSC không có hiển thị cho «wyndham garden grandworld» | Trang Wyndham trên Routine tập trung ưu đãi đặt trực tiếp/combo; không cạnh tranh thương hiệu |
| Trang tour/combo ăn thịt từ khoá khách sạn | Hai URL cùng hiện cho một truy vấn trong GSC | Một từ khoá chính = một URL (công đoạn 04) |
| Dev chậm → sửa onpage trễ (web không có trình soạn kiểu WordPress) | Việc R1/R2 quá 2 tuần chưa đóng | Gom thay đổi theo đợt, AI soạn đặc tả sẵn; hoặc làm trong session code ở repo `rt-hospitality-webapp` |
| Nội dung mỏng/trùng giữa 12 trang khách sạn | Crawl: số chữ < 400, title/H1 giống mẫu | Mỗi trang ≥ 600 chữ thông tin riêng (vị trí, hạng phòng, ảnh thật, kinh nghiệm lễ tân) |

## 6. Cần chị trả lời trước khi bắt đầu T1

1. Routine quản lý hay chỉ phân phối Wyndham Garden Grandworld và Wyndham Grand? (quyết định có làm GBP/trang riêng không)
2. Hạng sao chính thức của từng khách sạn? (quyết định có nhắm «khách sạn 3/4/5 sao phú quốc» không)
3. Tên Dev và QL KS từng khách sạn để điền cột «Người».
4. Ngày bắt đầu dự án: em đang đặt T1 = 12/2026. Nếu chị muốn khác, lịch dời theo.
5. Có muốn em ghi kế hoạch này thành một tab mới trong Google Sheet «KEY KS ROUTINE» không? (em chưa ghi gì vào sheet)
