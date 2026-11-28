# Kế hoạch xử lý 293 lỗi «Mới» · 28/11/2026

Nguồn: file `danh-sach-293-loi-moi-can-sua-claude.csv`, khớp với các dòng «Mới» trong app (B5 · Sửa lỗi từng trang): Tác giả 174 · Thiếu trải nghiệm 80 · Lạc chủ đề 19 · Trùng từ khóa 12 · Thương mại 7 · Đổi năm giả 1.

Số liệu GSC: truy vấn × trang, 90 ngày 22/8–20/11/2026. «A 11.9/862» nghĩa là trang A ở vị trí trung bình 11,9 với 862 lượt hiển thị cho truy vấn đó. Kiểm trạng thái URL (200/301, index, canonical) ngày 28/11/2026.

## 0. Đã đóng ngay khi quét lại (28/11)

- **6 bài «Thiếu trải nghiệm» → Hết lỗi (quét lại).** Đó là /canh-dep-o-phu-quoc/, /rach-vem-phu-quoc/, /dia-trung-hai-phu-quoc/, /cho-duong-dong-phu-quoc/, /bai-sao-phu-quoc/, /cafe-phu-quoc/. Các bài này đã có đoạn kinh nghiệm thật của anh Nguyên (phiếu đợt 2, 23/11) nhưng dòng còn ghi «Mới» vì lần quét gần nhất là 09/11.
- **/nha-thung-nuoc-mam-phu-quoc/ (Thiếu trải nghiệm) → Không phải lỗi.** Bài đã gộp và 301 sang /bi-mat-nuoc-mam-truyen-thong-phu-quoc/.
- **/ru/bun-quay/ (Lạc chủ đề) → Không phải lỗi.** Tiêu đề có «Фукуок» (Phú Quốc, chữ Nga), nhưng máy quét chỉ dò chữ Latin nên bắt nhầm.
- **/en/phu-quoc-motorbike-rental-services/ vẫn «Mới».** Máy quét nhận chữ «we rented…», nhưng đó là lời khách trích từ chỗ thuê xe khác, không phải trải nghiệm của Rooty.

## 1. «Thiếu trải nghiệm» (73 bài còn lại) và «Tác giả»: KHÔNG viết trải nghiệm bịa

Prompt đề nghị AI tự viết 2–3 đoạn «trải nghiệm thực tế độc quyền», cài sẵn cụm «HDV của Rooty Trip», «đoàn khách», «chúng tôi đã». Em không làm theo cách này, vì 3 lý do:

- Trái luật 4 của dự án («không bịa dữ kiện»). Trải nghiệm AI tự viết là trải nghiệm giả, dù không có con số giá nào.
- Trái luật học được 18/11: không lặp nhãn và cụm cố định giữa các bài. Cài sẵn «HDV của Rooty Trip / chúng tôi đã» chỉ là nhồi chữ để lừa máy quét.
- Google gọi đây là nội dung giả trải nghiệm (thiếu chữ E đầu tiên trong E-E-A-T). Khách đọc thấy mẹo sai thực tế thì mất uy tín, khác hẳn trường hợp bài chưa có trải nghiệm.

**Cách đang làm và đã có kết quả:** dùng phiếu hỏi anh Nguyên. Đợt 2 đã viết xong 8/8 bài, thanh tra Đạt, và 6 bài trong số đó vừa hết lỗi ở mục 0. Đợt 3 (8 bài) đang chờ câu trả lời. Em đề xuất **đợt 4 cho 10 bài nhiều nhấp nhất còn thiếu**:

| Bài | Nhấp 90 ngày | Hiển thị |
|---|---|---|
| /ban-do-du-lich-phu-quoc/ | 132 | 6.699 |
| /quan-oc-phu-quoc/ | 88 | 6.235 |
| /sieu-thi-o-phu-quoc/ | 77 | 5.078 |
| /tho-chau-phu-quoc/ | 66 | 4.854 |
| /review-can-ho-hillside-dia-trung-hai/ | 47 | 2.897 |
| /dia-diem-du-lich-dep-o-hon-son/ | 34 | 2.381 (cũng lạc chủ đề, xem mục 3) |
| /sunset-sanato-phu-quoc/ | 29 | 871 |
| /truyen-thuyet-dinh-cau/ | 28 | 1.421 |
| /pha-dem-phu-quoc/ | 19 | 4.539 |
| /dia-diem-check-in-phu-quoc/ | 31 | 1.206 (đã có trong phiếu đợt 3) |

Mỗi bài 3 câu hỏi về giờ đi, mẹo, giá thực tế có ghi tháng. Anh Nguyên trả lời xong thì em viết vào bài theo luật «tên + 10 năm giới thiệu một lần». Chỗ nào chưa có câu trả lời thì để trống, không điền `[Điền giá…]` lên trang thật.

## 2. Đổi năm giả · /review-khach-san-la-festa-phu-quoc-co-gi-dac-biet/

- **Tiêu đề đã sạch.** Tiêu đề SEO hiện tại là «Review La Festa Phú Quốc: Khách Sạn 5 Sao Có Gì Đặc Biệt?», không còn «2026» (bài sửa lần cuối 18/11/2026). Phần «tiêu đề có 2026» trong lần quét 09/11 không còn đúng.
- **Thân bài còn 3 chỗ năm cũ, cùng một ý (La Capri Beach Club):**
  1. H3 «La Capri Beach Club: Khu vực bãi biển sôi động (khai trương tháng 4/2024)» → bỏ phần trong ngoặc.
  2. Mục lục (TOC) tự lấy từ H3 trên, sửa H3 là mục lục tự hết.
  3. «Dự kiến khai trương vào tháng 4/2024, đây sẽ là điểm nhấn mới…» → câu viết như chưa mở cửa, đã lỗi thời. Đổi thành «La Capri Beach Club mở cửa từ tháng 4/2024…» sau khi kiểm câu lạc bộ còn hoạt động (nguồn: trang khách sạn hoặc Google Maps, ghi tháng kiểm).
- **Cũng cần sửa:**
  - «Giá phòng tham khảo: từ $133/đêm (~3.200.000 VNĐ)…» không ghi nguồn và tháng. Lấy giá từ đội đặt phòng Rooty (ghi tháng 11/2026), không có thì ghi «[CẦN KIỂM CHỨNG]».
  - H2 «Giới thiệu về La Festa Phú Quốc» là H2 rỗng nghĩa, nên đổi thành «La Festa Phú Quốc ở đâu, có gì đặc biệt?».
  - H3 «Các lớp học nấu ăn, workshop văn hóa (nếu có)»: chưa chắc có thì bỏ H3 này.
- **Không cần đổi tiêu đề.** Sửa 3 chỗ trên là đủ để đóng dòng «Đổi năm giả».

## 3. 19 bài «Lạc chủ đề» (18 sau khi bỏ /ru/bun-quay/)

Có 4 hướng xử lý: (1) Viết lại gắn với Phú Quốc · (2) noindex · (3) Gộp + 301 · (4) Xoá 410.

| Bài | Nhấp / hiển thị / vị trí | Hướng | Lý do & việc cụ thể |
|---|---|---|---|
| /loi-cau-hon-ngot-ngao/ | 247 / 3.246 / 5,4 | **(1)**, KHÔNG noindex | Bài mang về 247 nhấp/90 ngày, nhiều thứ 2 toàn blog. Noindex là bỏ số nhấp đó. Bài đã dẫn sang Cầu Hôn Phú Quốc và tour Symphony: thêm phần «Cầu hôn ở Phú Quốc: Cầu Hôn Sunset Town, giờ hoàng hôn, show», đổi H1 có «Phú Quốc». Đo lại sau 4 tuần |
| /dia-diem-du-lich-dep-o-hon-son/ | 34 / 2.381 / 8,7 | (1) | Hòn Sơn gần Phú Quốc. Thêm «Đi Hòn Sơn từ Phú Quốc / Rạch Giá thế nào». Đang có cả lỗi thiếu trải nghiệm |
| /top-10-bai-bien-dep-nhat-viet-nam/ | 11 / 1.156 / 6,8 | (1) **làm bài trụ cột của cụm «biển Việt Nam»** | Bài nhiều nhấp nhất trong 3 bài cùng chủ đề. Mở rộng mục bãi biển Phú Quốc (Bãi Sao, Bãi Khem, Bãi Dài) và dẫn sang các bài Phú Quốc |
| /cac-dia-diem-du-lich-bien-o-viet-nam/ | 5 / 1.007 / 7,5 | (3) → /top-10-bai-bien-dep-nhat-viet-nam/ | Trùng ý «biển đẹp Việt Nam» |
| /top-cac-dia-diem-duoc-menh-danh-la-maldives-viet-nam/ | 1 / 82 / 28,7 | (3) → /top-10-bai-bien-dep-nhat-viet-nam/ | Cùng cụm, gần như không có nhấp |
| /en/kien-giang-tourism/ | 10 / 344 / 7,7 | (1) | Bài tổng quan cả vùng. Phải cập nhật **Kiên Giang đã nhập vào An Giang (7/2025)** và dẫn sang các bài Phú Quốc |
| /danh-lam-thang-canh-o-kien-giang/ | 4 / 299 / 8,3 | (1) **làm bài trụ cột tiếng Việt về Kiên Giang** | Có nhấp. Cập nhật An Giang và dẫn sang Phú Quốc |
| /du-lich-kien-giang/ | 0 / 109 / 35,5 | (3) → /danh-lam-thang-canh-o-kien-giang/ | Trùng ý, vị trí 35, 0 nhấp |
| /lich-trinh-du-lich-nam-du/ | 5 / 419 / 10,8 | (1) | Nam Du có tàu đi từ Phú Quốc. Thêm mục «từ Phú Quốc đi Nam Du» |
| /thiet-ke-tour-du-lich-mice/ | 2 / 55 / 12,6 | (3) → /tour-doan-cong-ty-phu-quoc-team-building-gala-dinner/ | Rooty có bán tour đoàn và MICE ở Phú Quốc. Gộp vào trang bán |
| /en/mice-tourism/ | 0 / 2.032 / 28,9 | (1) | Có nhu cầu tìm kiếm (2.032 hiển thị). Viết lại theo góc «MICE in Phu Quoc», dẫn sang trang team building |
| /en/common-problems-when-scuba-diving/ | 0 / 137 / 16,9 | (1) | Rooty bán tour lặn ngắm san hô. Thêm bối cảnh lặn ở Phú Quốc (An Thới, Hòn Móng Tay) và dẫn sang tour |
| /san-ho-la-dong-vat-hay-thuc-vat/ | 0 / 137 / 13,2 | (1) | Thêm mục «Xem san hô ở đâu tại Phú Quốc» và dẫn sang tour lặn |
| /du-lich-mien-tay/ | 0 / 137 / 25,8 | (2) noindex, **chị quyết** | 6.802 từ, 0 nhấp, ngoài Phú Quốc. Nếu chi nhánh Cần Thơ có bán tour miền Tây thì giữ và gắn vào trang chi nhánh |
| /en/western-travel/ | 0 / 25 / 17,2 | (2) noindex, chị quyết như bài trên | Giống bài trên |
| /30-thang-4-la-ngay-gi/ | 0 / 56 / 60,9 | (3) → /30-thang-4-nen-di-du-lich-o-dau-phu-quoc/ | Bài lịch sử, ngoài ngành. 301 sang bài du lịch 30/4 |
| /lich-thi-dau-le-hoi-phao-hoa-quoc-te-da-nang-2025/ | 0 / 4 / 24,2 | (3) → /lich-ban-phao-hoa-dia-trung-hai-phu-quoc/ | Sự kiện 2025 đã qua, ngoài Phú Quốc. Đưa về bài pháo hoa Phú Quốc |
| /thong-bao-huy-tour-cano-dao-ngay-12-07/ | 0 / 9 / 5,1 | (2) noindex | Thông báo hết hạn, 209 từ. Làm giống các thông báo cũ khác |

Không bài nào nên xoá 410: bài nào cũng có lượt hiển thị hoặc có chỗ 301 phù hợp.

## 4. 12 cụm «Trùng từ khóa»

| Cụm | Trùng thật? (GSC) | Bài trụ cột | Việc cần làm |
|---|---|---|---|
| Địa Trung Hải: /dia-trung-hai-phu-quoc/ · /cac-show-dien-tai-dia-trung-hai-phu-quoc/ | **Không.** A thắng 39/42 truy vấn chung. B chỉ đứng 56–75 cho từ chính («địa trung hải phú quốc» A 11,9/862 · B 61,7/82) | /dia-trung-hai-phu-quoc/ | Giữ cả hai. Bài show chỉ nhắm từ «show / Kiss of the Sea / Symphony», có link qua lại |
| Nam đảo / 4 đảo / 3 đảo | **Không.** 11 truy vấn chung, bài phụ chỉ có 1 hiển thị mỗi truy vấn | /kinh-nghiem-di-nam-dao-phu-quoc/ | Giữ. Bài 3 đảo (0 nhấp, 133 hiển thị) đổi góc «so sánh tour 3 đảo và 4 đảo» và dẫn sang tour đang bán |
| Bún quậy: /bun-quay-phu-quoc/ · /review-bun-quay-kien-xay/ | **Có, nhưng chia vai đúng.** 69 truy vấn chung. Bài Kiến Xây thắng tên quán («bún quậy kiến xây» B 6,2/10.020), bài chung thắng «bún quậy phú quốc» (A 7,3/1.518). Từ «bún quậy» thì cả hai đứng khoảng 9 | /bun-quay-phu-quoc/ | Không gộp. Bài chung dẫn «bún quậy Kiến Xây» sang bài review. Bài review dẫn «các quán bún quậy Phú Quốc» về bài chung |
| Symphony: /symphony-of-the-sea-phu-quoc/ · /symphony-of-the-sea-mua-3-phu-quoc/ | **Có.** Cùng một show. Bài mùa 3 chỉ có 49 hiển thị | /symphony-of-the-sea-phu-quoc/ | **Gộp + 301:** chuyển thông tin mùa 3 vào bài chính, rồi 301 bài mùa 3 |
| Khách sạn (9 bài) | **Phần lớn không.** Mỗi bài có một bổ ngữ riêng. Chồng nhau thật ở cặp «gần biển ↔ resort 5 sao» (20 truy vấn chung) và «gần biển ↔ gần chợ đêm». Từ «khách sạn phú quốc» không bài nào đủ mạnh (67,7 và 11,9) | **Thiếu trụ cột.** Bài «khách sạn Phú Quốc» (slug `khach-san-phu-quoc`) đang làm trong dây chuyền | Viết xong bài trụ cột, dẫn xuống 9 bài con. Bài con giữ đúng bổ ngữ (gần biển / gần chợ đêm / Bãi Trường / Bãi Sao / 5 sao / homestay) |
| Danh lam thắng cảnh: Phú Quốc · Kiên Giang · địa điểm du lịch | **Không.** 3 truy vấn chung, khác vùng | — | Bài Kiên Giang xử lý theo mục 3 |
| Safari / Vinpearl / VinWonders | **Có.** VinWonders ↔ Vinpearl 18 truy vấn chung. Bài Safari chỉ đứng 43,9 cho «vinpearl safari phú quốc» (104 hiển thị) | Safari: /vinpearl-safari-phu-quoc/ · VinWonders: /kinh-nghiem-du-lich-vinwonders-phu-quoc/ | Bài VinWonders rút phần Safari còn 1 đoạn + link. Bài «kinh nghiệm đi Vinpearl» làm bài tổng (resort + VinWonders + Safari) dẫn sang 2 bài trên |
| Gành Dầu: /ganh-dau-phu-quoc/ · /an-gi-o-ganh-dau-phu-quoc/ | **Có.** Bài chung còn đứng trên bài ăn uống cho «nhà hàng gành dầu» (13,1 so với 28,9) | /ganh-dau-phu-quoc/ | **Gộp + 301** bài ăn uống (154 hiển thị) vào mục «Ăn gì ở Gành Dầu» |
| Hàm Ninh: /lang-chai-ham-ninh-co-gi-an/ · /lang-chai-ham-ninh-phu-quoc/ | **Có.** Bài «có gì ăn» đứng trên bài chính cho từ chính («làng chài hàm ninh» 21,9 so với 60,3). Cả hai đều yếu | /lang-chai-ham-ninh-phu-quoc/ | **Gộp + 301** «có gì ăn» vào bài chính (slug rộng hơn) |
| Nên đi mấy ngày / tháng mấy / 30-4 | **Không.** Bài «mấy ngày» đã 301. Bài tháng mấy và bài 30/4 chỉ có 2 truy vấn chung | /nen-di-du-lich-phu-quoc-thang-may/ | Bài 30/4 dẫn sang bài tháng mấy. Bài «đi mấy ngày» chuyển nháp, giữ redirect (dòng đa ngôn ngữ cũ) |
| Bãi Trường: tổng quan · resort · quán ăn | **Không.** Chia vai đúng: bài resort thắng «khách sạn bãi trường», bài tổng quan thắng «bãi trường» | /bai-truong-phu-quoc-co-gi/ | Bài tổng quan dẫn sang 2 bài con |
| Hòn Thơm: kinh nghiệm · Santorini Hòn Thơm | **Không.** 1 truy vấn chung | /kinh-nghiem-du-lich-hon-thom-phu-quoc/ | Giữ, link qua lại |

**Tóm lại:** chỉ 3 cụm cần gộp + 301 (Symphony, Gành Dầu, Hàm Ninh). Thêm 2 cụm cần chia lại vai (Safari/VinWonders) và viết bài trụ cột (khách sạn). 7 cụm còn lại không trùng thật, chỉ cần link qua lại.

## Việc tiếp theo (chờ chị duyệt)

1. Duyệt phiếu hỏi đợt 4 (10 bài) để gửi anh Nguyên.
2. Duyệt các hướng xử lý ở mục 3 và 4, nhất là: giữ index bài «lời cầu hôn», số phận 2 bài miền Tây, gộp 3 cụm.
3. Sửa 3 chỗ năm cũ ở bài La Festa (cần đăng nhập WordPress).
