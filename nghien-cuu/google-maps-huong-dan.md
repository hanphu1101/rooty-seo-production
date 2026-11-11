# SEO Google Maps cho Rooty Trip — hướng dẫn & kế hoạch đăng bài

Soạn 11/11/2026 · theo `quy-trinh/08-local-seo-danh-gia.md` (công đoạn R3) · lịch đăng chi tiết: `nghien-cuu/lich-dang-gbp.csv`

> AI chỉ soạn. Người phụ trách GBP đăng nhập và tự đăng — không đưa mật khẩu GBP cho AI.

## 1. Google xếp hạng trên Maps dựa vào gì?

Google công bố 3 yếu tố xếp hạng địa phương: **mức liên quan** (hồ sơ khớp với điều khách tìm), **khoảng cách** (từ khách tới doanh nghiệp) và **mức nổi bật** (đánh giá, mức độ được nhắc trên web, thứ hạng website). Khoảng cách không đổi được, nên Rooty làm hai việc còn lại:

| Yếu tố | Rooty làm gì |
|---|---|
| Liên quan | Đúng danh mục, mô tả rõ dịch vụ, mục Sản phẩm liệt kê từng tour kèm link, bài đăng đều nói về tour/điểm đến cụ thể |
| Nổi bật | Đánh giá thật đều đặn + trả lời hết; NAP khớp mọi nơi; bài blog trên rootytrip.com lên top |

Không làm: nhồi từ khoá vào tên hồ sơ ("Rooty Trip – Tour Phú Quốc Giá Rẻ"), mua đánh giá, đổi quà lấy 5 sao. Cả ba vi phạm chính sách Google và có thể bị khoá hồ sơ.

## 2. Chuẩn hoá hồ sơ (làm một lần, tháng 11/2026)

- [ ] **Chủ sở hữu** là email công ty, có ít nhất 2 quản lý (không để 1 nhân viên giữ duy nhất).
- [ ] **Tên:** `Rooty Trip` — đúng như trên website và biển hiệu.
- [ ] **Danh mục chính:** Công ty lữ hành (Tour operator). **Phụ:** Đại lý du lịch (Travel agency) — chỉ thêm danh mục đúng việc đang làm.
- [ ] **Địa chỉ · hotline · giờ làm · website:** giống hệt chân trang rootytrip.com. ⚠️ `00-context/brand.md` còn trống địa chỉ, hotline, năm thành lập — điền ở đó trước, rồi đối chiếu GBP theo đúng bản đó.
- [ ] **Mô tả (≤ 750 ký tự):** nêu làm gì, cho ai, khác biệt. Bản nháp ở mục 5.
- [ ] **Sản phẩm:** mỗi tour/combo chủ lực một mục — tên, giá từ, ảnh, nút link về đúng trang sản phẩm. Danh sách ở mục 6.
- [ ] **Ảnh thật ≥ 20:** văn phòng, đội HDV, khách trong tour, cano/tàu, ảnh phó nháy chụp. Thêm ảnh mới mỗi tháng. Không dùng ảnh mua hay ảnh lấy từ web khác.
- [ ] **Link đặt tour / website:** gắn UTM để đo trong GA4: `?utm_source=google&utm_medium=organic&utm_campaign=gbp`.
- [ ] **Hỏi & Đáp:** [CẦN KIỂM CHỨNG] Google đã thông báo thu hẹp tính năng Hỏi & Đáp trên một số hồ sơ. Mở GBP xem còn mục này không; còn thì tự đăng 5–10 câu khách hay hỏi.

## 3. Đăng bài GBP — hệ sinh thái liên kết về website

**Nhịp:** 2 bài/tuần, **thứ Ba** và **thứ Sáu** (8 bài/tháng). Đều đặn quan trọng hơn dồn nhiều bài một ngày.

**Cách mỗi bài nối các trang trên web với nhau:**

```
Bài đăng GBP ──link (có UTM)──▶ Bài blog cẩm nang ──link──▶ Trang tour/combo
       └──── nhắc tên tour + giá từ ──────────────────────────────┘
```

1. Bài GBP kể một điểm đến/kinh nghiệm, nút **Tìm hiểu thêm** dẫn về **bài blog** cùng chủ đề.
2. Trong thân bài GBP nhắc tên **tour/combo** liên quan và **giá từ**.
3. Bài blog đó phải có link chữ sang trang tour. Em đã đối chiếu bản đồ link nội bộ (crawl 08/11/2026): **10/24 bài blog trong lịch chưa link sang tour đi kèm** — cột `blog_da_link_sang_tour` ghi "CHƯA – thêm link". Sửa các bài này **trước ngày đăng** bài GBP tương ứng, nếu không khách vào blog sẽ không đi tiếp được tới trang đặt tour.
4. Bài loại **Ưu đãi** cho nút **Đặt trước** dẫn thẳng về trang tour.

**Ba loại bài GBP dùng:**

| Loại | Khi nào | Nút |
|---|---|---|
| Cập nhật | Kinh nghiệm, điểm đến, mẹo HDV | Tìm hiểu thêm → bài blog |
| Ưu đãi | Có giá/khuyến mãi thật, có hạn | Đặt trước → trang tour |
| Sự kiện | Show, pháo hoa, lễ Tết — có ngày cụ thể | Tìm hiểu thêm → bài blog |

**Khuôn một bài (≈ 600–900 ký tự):**

1. Câu đầu trả lời thẳng: điểm đến là gì / có gì / khi nào đẹp.
2. 2–3 câu kinh nghiệm riêng của HDV Rooty (giờ đẹp, chỗ ít đông, mẹo chụp ảnh) — đây là thứ đối thủ không có.
3. Một câu nhắc tour: "Tour … của Rooty Trip, giá từ … (cập nhật …/2026)".
4. Lời mời: xem cẩm nang đầy đủ / đặt tour.
5. Ảnh: ảnh thật do đội phó nháy chụp, ngang, không chèn chữ kín ảnh.

**Luật dữ kiện** (giống dây chuyền bài viết): giá lấy từ bảng Lark «Giá & dữ kiện» (lần kiểm 09/11/2026), kiểm lại trước khi đăng. Giờ diễn, lịch pháo hoa, giờ mở cửa dịp lễ chưa có nguồn thì ghi `[CẦN KIỂM CHỨNG]` và hỏi trước khi đăng — không đoán.

## 4. Lịch 12 tuần (17/11/2026 → 05/02/2027)

Đầy đủ link, UTM, giá trong `nghien-cuu/lich-dang-gbp.csv` (mở bằng Excel được).

| # | Ngày | Loại | Chủ đề | Blog đã link sang tour? |
|---|---|---|---|---|
| 1 | 17/11 | Cập nhật | Mùa khô Phú Quốc – đi tháng nào đẹp | CHƯA |
| 2 | 20/11 | Cập nhật | Cáp treo Hòn Thơm – trải nghiệm thật | CHƯA |
| 3 | 24/11 | Ưu đãi | Hòn Thơm có gì – vé cáp treo | Có |
| 4 | 27/11 | Cập nhật | Lặn ngắm san hô 3 đảo | Có |
| 5 | 01/12 | Cập nhật | Rạch Vẹm – săn sao biển Bắc đảo | Có |
| 6 | 04/12 | Sự kiện | Show Symphony of the Sea – giờ diễn & mẹo | Có |
| 7 | 08/12 | Cập nhật | Cầu Hôn Sunset Town – giờ đẹp ngắm hoàng hôn | CHƯA |
| 8 | 11/12 | Cập nhật | Câu mực đêm | Có |
| 9 | 15/12 | Cập nhật | Grand World có gì | Có |
| 10 | 18/12 | Ưu đãi | VinWonders mùa Giáng sinh | Có |
| 11 | 22/12 | Cập nhật | Vinpearl Safari – kinh nghiệm A-Z | Có |
| 12 | 25/12 | Sự kiện | Pháo hoa năm mới Địa Trung Hải [CẦN KIỂM CHỨNG lịch bắn] | CHƯA |
| 13 | 29/12 | Cập nhật | Phú Quốc về đêm – du thuyền hoàng hôn | CHƯA |
| 14 | 01/01 | Cập nhật | Lịch trình 3N2Đ đầu năm | Có |
| 15 | 05/01 | Cập nhật | Nam đảo có gì chơi | Có |
| 16 | 08/01 | Cập nhật | Bãi Sao – tắm biển bằng tàu gỗ | Có |
| 17 | 12/01 | Ưu đãi | Chi phí đi Phú Quốc – combo 4 sao | CHƯA |
| 18 | 15/01 | Cập nhật | Đặc sản Phú Quốc mua làm quà | Có |
| 19 | 19/01 | Cập nhật | Vinpearl Phú Quốc – lịch trình A-Z | CHƯA |
| 20 | 22/01 | Ưu đãi | 22 góc check-in Địa Trung Hải | CHƯA |
| 21 | 26/01 | Cập nhật | Bản đồ du lịch 4 cụm | Có |
| 22 | 29/01 | Cập nhật | Trò chơi trên biển – Seawalker | Có |
| 23 | 02/02 | Ưu đãi | Phú Quốc tự túc dịp Tết | CHƯA |
| 24 | 05/02 | Sự kiện | Đi lễ Dinh Cậu đầu năm (Tết Đinh Mùi 06/02/2027) [CẦN KIỂM CHỨNG giờ mở cửa dịp Tết] | CHƯA |

Trước khi viết câu "tour có ghé X", mở trang tour kiểm lịch trình — một số cặp blog/tour ở trên là gợi ý chủ đề gần nhau, không phải tour nào cũng đi qua điểm trong bài blog.

## 5. Bản nháp mô tả hồ sơ (≈ 600 ký tự — điền ✏️ rồi mới dán)

> Rooty Trip là công ty lữ hành tại Phú Quốc, tổ chức tour trong ngày, tour trọn gói, combo nghỉ dưỡng và bán vé tham quan trên đảo. Khách đi cùng hướng dẫn viên người địa phương và đội phó nháy chụp ảnh suốt hành trình. Một số tour tiêu biểu: tour cano 4 đảo kèm cáp treo Hòn Thơm, tour Nam đảo, tour Rạch Vẹm khám phá Bắc đảo, tour VinWonders – Safari và combo 3N2Đ tại Grand World. Tư vấn viên hỗ trợ lên lịch trình theo nhu cầu gia đình, cặp đôi hay nhóm bạn. ✏️ Hoạt động từ năm … · giấy phép lữ hành số …

## 6. Mục Sản phẩm trên GBP — 10 sản phẩm nên đưa lên trước

Giá theo Lark «Giá & dữ kiện», kiểm 09/11/2026.

| Sản phẩm | Giá từ | Link |
|---|---|---|
| Tour 4 đảo Phú Quốc và cáp treo Hòn Thơm 1 ngày | 1.550.000đ | https://rootytrip.com/san-pham/tour-cano-4-dao-cap-treo-1-ngay/ |
| Tour 3 đảo Phú Quốc | 800.000đ | https://rootytrip.com/san-pham/tour-cano-3-dao-phu-quoc/ |
| Tour Nam đảo Phú Quốc 1 ngày | 970.000đ | https://rootytrip.com/san-pham/tour-nam-dao-phu-quoc-1-ngay/ |
| Tour Rạch Vẹm khám phá Bắc đảo 1 ngày | 950.000đ | https://rootytrip.com/san-pham/tour-rach-vem-kham-pha-bac-dao-phu-quoc/ |
| Tour Safari – VinWonders 1 ngày | 2.150.000đ | https://rootytrip.com/san-pham/tour-safari-vinwonders-phu-quoc/ |
| Tour chiều tối Nam đảo + Show Symphony of the Sea | 1.150.000đ | https://rootytrip.com/san-pham/tour-nam-dao-symphony-of-the-sea/ |
| Tour Phú Quốc 3N2Đ cho khách lần đầu đến đảo | 3.699.000đ | https://rootytrip.com/san-pham/tour-phu-quoc-3n2d-cho-nguoi-lan-dau/ |
| Combo Phú Quốc 3N2Đ Wyndham Garden Grand World 4★ | 2.700.000đ | https://rootytrip.com/san-pham/combo-phu-quoc-3n2d-4-sao-wyndham-graden/ |
| Vé cáp treo Hòn Thơm | 850.000đ | https://rootytrip.com/san-pham/ve-cap-treo-hon-thom/ |
| Chụp ảnh máy cơ cùng HDV Rooty Trip | 500.000đ | https://rootytrip.com/san-pham/dich-vu-chup-anh-may-co-cung-hdv-rooty-trip/ |

## 7. Đánh giá — việc hằng tuần

- Trả lời **mọi** đánh giá trong 48 giờ. Nhắc tên tour khách đi, cảm ơn chi tiết cụ thể khách kể; đánh giá xấu thì xin lỗi, nói cách đã xử lý, mời liên hệ trực tiếp. Không dán một mẫu cho mọi đánh giá.
- Xin đánh giá: HDV nhắc cuối tour + gửi mã QR; CSKH nhắn Zalo sau 24 giờ kèm link đánh giá và ảnh phó nháy chụp.
- Theo dõi mỗi tháng: số đánh giá mới, điểm trung bình, tỷ lệ đã trả lời → đưa vào báo cáo tháng (`/rooty-bao-cao`).

## 8. Đối chiếu quy trình 7 bước SEO Google Maps phổ biến

Quy trình 7 bước hay được chia sẻ (tạo & xác minh → NAP → ảnh & GeoTag → citation → đánh giá → Google Posts → website & schema) khớp với tài liệu này. Bốn điểm Rooty làm khác:

| Bước | Rooty làm | Ghi chú |
|---|---|---|
| 1 · Tạo & xác minh, tên không nhồi từ khoá | Mục 2 | Giữ nguyên |
| 2 · NAP, danh mục chính + 3–5 phụ, giờ mở cửa | Mục 2 | Danh mục phụ chỉ thêm khi đúng việc đang làm. Thêm cho đủ 5 danh mục mà không đúng thì hại nhiều hơn lợi |
| 3 · Ảnh thật + **GeoTag** | Mục 2: ảnh thật, thêm mỗi tháng | **Bỏ GeoTag.** Google xoá dữ liệu GPS (EXIF) khi ảnh tải lên. Đại diện Google đã nói nhiều lần rằng toạ độ trong ảnh không ảnh hưởng xếp hạng. Đặt tên file không dấu thì vô hại, nhưng đừng tốn công |
| 4 · Citation | App tab **B8 · Entity** (19 hồ sơ, nút Kiểm NAP); `quy-trinh/08` mục R4 | Ưu tiên nơi khách thật xem: Tripadvisor, Klook, Traveloka, Facebook, danh bạ du lịch. Không rải hàng trăm trang vàng kém chất lượng |
| 5 · Đánh giá | Mục 7 | **Không xin "5 sao".** Chính sách Google cấm xin chọn lọc đánh giá tốt (review gating). Câu đúng: "Anh/chị để lại cảm nhận thật giúp Rooty nhé". Trả lời đánh giá có thể nhắc tên tour cho tự nhiên, không chèn từ khoá |
| 6 · Google Posts | Mục 3–4, lịch 24 bài | Thêm: mỗi bài dẫn về blog, blog dẫn sang tour |
| 7 · Website & schema LocalBusiness, nhúng bản đồ | Kiểm ngày 11/11/2026, xem dưới | Còn 2 việc cần sửa |

**Kết quả kiểm bước 7 trên rootytrip.com (11/11/2026):**

- ✅ Title trang chủ có tên địa phương: "Rooty Trip Phú Quốc - Tour, Combo & Vé Tham Quan".
- ✅ Trang chủ có schema `TravelAgency` (một loại LocalBusiness), có địa chỉ 191 Trần Hưng Đạo, Khu phố Cửa Lấp, Đặc khu Phú Quốc, An Giang, và điện thoại +84 886-068-886.
- ⚠️ **Tên thực thể lệch nhau:** cùng trang chủ có schema `Organization` tên "Rooty Trip" và `TravelAgency` tên "Rooty Trip Phú Quốc". Nên thống nhất một tên, trùng đúng tên trên GBP, và dùng chung `@id` để Google hiểu đây là một doanh nghiệp. JSON-LD gợi ý lấy ở app tab B8 → Sinh JSON-LD.
- ⚠️ **Bản đồ ở trang Liên hệ nhúng theo địa chỉ** (`maps?q=191 Trần Hưng Đạo…`). Kiểu này chỉ hiện một chấm trên bản đồ, không mở ra hồ sơ GBP có đánh giá. Nên thay bằng mã nhúng lấy từ chính hồ sơ Rooty Trip trên Google Maps (Chia sẻ → Nhúng bản đồ).
- ℹ️ Trang Liên hệ có **2 địa chỉ** (191 Trần Hưng Đạo và 132 Ngô Tất Tố). Nếu 132 Ngô Tất Tố là văn phòng thật có đón khách thì có thể làm hồ sơ GBP riêng. Nếu không thì GBP chỉ dùng địa chỉ trụ sở. Hai địa chỉ này cũng nên được điền vào `00-context/brand.md` sau khi chị xác nhận.

## 9. Đo hiệu quả

- GA4: lọc `utm_campaign=gbp-post` (bài đăng) và `gbp` (nút website) để xem lượt vào, lượt đặt tour.
- GBP → Hiệu suất: lượt xem hồ sơ, lượt gọi, lượt bấm website, lượt chỉ đường — chụp số đầu mỗi tháng.
- Sau 12 tuần (đầu tháng 2/2027) so với số tháng 11/2026, giữ chủ đề kéo được nhiều lượt bấm, thay chủ đề yếu.
