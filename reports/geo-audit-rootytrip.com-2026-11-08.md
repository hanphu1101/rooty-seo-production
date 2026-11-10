# GEO audit — https://rootytrip.com

Ngày chạy: 2026-11-08 · 15 trang · script `scripts/geo_audit.py`

## 1. Quyền vào website của bot AI (Checklist việc #2 — cửa chặn)

| Nhóm | Bot | Trạng thái |
|---|---|---|
| Bot đi tìm nguồn (cần MỞ để được trích dẫn) | OAI-SearchBot | ✅ Mở |
| Bot đi tìm nguồn (cần MỞ để được trích dẫn) | Claude-SearchBot | ✅ Mở |
| Bot đi tìm nguồn (cần MỞ để được trích dẫn) | PerplexityBot | ✅ Mở |
| Bot đi tìm nguồn (cần MỞ để được trích dẫn) | Googlebot | ✅ Mở |
| Bot đi tìm nguồn (cần MỞ để được trích dẫn) | Bingbot | ✅ Mở |
| Bot chạy khi người dùng hỏi (cần MỞ) | ChatGPT-User | ✅ Mở |
| Bot chạy khi người dùng hỏi (cần MỞ) | Claude-User | ✅ Mở |
| Bot chạy khi người dùng hỏi (cần MỞ) | Perplexity-User | ✅ Mở |
| Bot lấy dữ liệu huấn luyện (tuỳ chọn, không ảnh hưởng Google Search) | GPTBot | ✅ Mở |
| Bot lấy dữ liệu huấn luyện (tuỳ chọn, không ảnh hưởng Google Search) | ClaudeBot | ✅ Mở |
| Bot lấy dữ liệu huấn luyện (tuỳ chọn, không ảnh hưởng Google Search) | Google-Extended | ✅ Mở |
| Bot lấy dữ liệu huấn luyện (tuỳ chọn, không ảnh hưởng Google Search) | CCBot | ✅ Mở |

**Kết luận:** ✅ Các bot đi tìm nguồn và bot chạy khi người dùng hỏi đều được vào (theo robots.txt). Vẫn cần kiểm tường lửa/CDN.

## 2. Tổng hợp lỗi theo tần suất

| Lỗi | Số trang |
|---|---|
| Khối meta chen giữa H1 và câu trả lời | 14/15 |
| Ít H2 dạng câu hỏi khách thật sự hỏi AI | 11/15 |
| JSON-LD lỗi cú pháp | 2/15 |
| N/N ảnh thiếu alt | 1/15 |

## 3. Chi tiết từng trang

### Rooty Trip Phú Quốc - Tour, Combo & Vé Tham Quan

- URL: https://rootytrip.com
- Trạng thái: 200 · phản hồi 114ms · HTML 570KB · 4116 từ
- H1: Du lịch Phú Quốc cùng Rooty Trip
- H2 (10, tỷ lệ dạng câu hỏi 0%): Khám Phá Phú Quốc Cuối Năm · Vi Vu Phú Quốc Cuối Năm · Cảm nhận của khách hàng về Rooty Trip · Báo chí viết về Rooty Trip · Tour trong ngày · Tour trọn gói · Combo nghỉ dưỡng · Đi du lịch Phú Quốc cùng HDV bản địa · Kinh nghiệm du lịch Phú Quốc · Đối tác Rooty Trip
- 400 ký tự đầu sau H1: _Những địa điểm tham quan & trải nghiệm trong tour của Rooty Trip Đội ngũ hướng dẫn viên địa phương nhiệt tình và vui tính sẽ cho quý khách những trải nghiệm đáng nhớ về Phú Quốc và con người nơi đây Đội ngũ phó nháy "yêu cái đẹp" giúp lưu giữ những kỷ niệm, khoảnh khắc của bạn cùng gia đình, bạn bè tại Phú Quốc Bộ phận tư vấn viên, sales của Rooty am hiểu về địa phương hỗ trợ tư vấn lịch trình, ki_
- Tác giả: có · Cập nhật: 2026-11-02T13:27:34+07:00 · sameAs: có
- ✅ Phản hồi máy chủ 114ms (<200ms tốt)
- ✅ Canonical tự trỏ
- ✅ Schema: Answer, BreadcrumbList, ContactPoint, Country, EducationalOrganization, FAQPage, GeoCoordinates, ImageObject
- ❌ Ít H2 dạng câu hỏi khách thật sự hỏi AI (<30%)
- ❌ 152/405 ảnh thiếu alt

### Địa điểm check-in Địa Trung Hải Phú Quốc: 22 chỗ đẹp 2026

- URL: https://rootytrip.com/dia-trung-hai-phu-quoc/
- Trạng thái: 200 · phản hồi 204ms · HTML 390KB · 5047 từ
- H1: 22 địa điểm check-in Địa Trung Hải Phú Quốc đẹp nhất
- H2 (6, tỷ lệ dạng câu hỏi 33%): Địa Trung Hải Phú Quốc nằm ở đâu? · Địa Trung Hải Phú Quốc có gì? 22 điểm check-in · Cách đi đến Địa Trung Hải từ Dương Đông, sân bay và An Thới · Ăn gì ở Địa Trung Hải Phú Quốc? · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Vui chơi Phú Quốc Tác giả: Lâm Thành Nguyên Ngày đăng: 24-10-2023 Cập nhật: 07-11-2026 Lượt xem: 26697 Thị trấn Địa Trung Hải Phú Quốc — còn gọi là Thị trấn Hoàng Hôn (Sunset Town) — nằm ở mũi Ông Bốn, phường An Thới, cực nam đảo Phú Quốc. Từ Dương Đông tới đây 29,7 km, chạy xe khoảng 42 phút; từ sân bay là 19,6 km, khoảng 27 phút. Khu thuộc dự án Sun Premier Village Primavera của Sun Group, rộng _
- Tác giả: có · Cập nhật: 2026-11-07T14:22:20+07:00 · sameAs: không
- ✅ Phản hồi máy chủ 204ms (đạt mức tối thiểu <350ms)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content

### 36 Địa Điểm Du Lịch Phú Quốc Đẹp Nhất 2026 Kèm Giá Vé

- URL: https://rootytrip.com/dia-diem-du-lich-phu-quoc/
- Trạng thái: 200 · phản hồi 146ms · HTML 460KB · 10027 từ
- H1: 36 địa điểm du lịch Phú Quốc đẹp nhất 2026 kèm giá vé
- H2 (9, tỷ lệ dạng câu hỏi 0%): Địa điểm du lịch Bắc đảo Phú Quốc (Gành Dầu – Cửa Cạn – Ông Lang) · Địa điểm du lịch trung tâm Dương Đông và phía Đông · Địa điểm du lịch Nam đảo (An Thới – Thị trấn Hoàng Hôn) · Các đảo nhỏ quanh Phú Quốc (quần đảo An Thới) · Một số địa điểm du lịch khác tại Phú Quốc bạn có thể quan tâm: · Kinh nghiệm du lịch Phú Quốc · Gợi ý lịch trình du lịch Phú Quốc · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Vui chơi Phú Quốc địa điểm Tác giả: Lâm Thành Nguyên Ngày đăng: 25-10-2023 Cập nhật: 07-11-2026 Lượt xem: 46948 Đảo Phú Quốc , nằm ngoài khơi bờ biển Việt Nam, đã trở thành một điểm du lịch hàng đầu nổi tiếng với những bãi biển tuyệt đẹp , những khu chợ sôi động và lịch sử phong phú . Rooty Trip giới thiệu tới bạn về 36 địa điểm du lịch Phú Quốc , giúp bạn khám phá những gì hòn đảo này mang lại, v_
- Tác giả: có · Cập nhật: 2026-11-07T09:08:36+07:00 · sameAs: không
- ✅ Phản hồi máy chủ 146ms (<200ms tốt)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content
- ❌ Ít H2 dạng câu hỏi khách thật sự hỏi AI (<30%)

### Du lịch Kiên Giang có gì? TOP 24 địa điểm đẹp, nổi tiếng

- URL: https://rootytrip.com/du-lich-kien-giang/
- Trạng thái: 200 · phản hồi 82ms · HTML 352KB · 5445 từ
- H1: Giới thiệu 24 điểm du lịch Kiên Giang đẹp và nổi tiếng nhất
- H2 (8, tỷ lệ dạng câu hỏi 0%): Đảo ngọc Phú Quốc · Kiên Hải, Kiên Giang · Thành Phố Rạch Giá · Hòn Đất – Kiên Lương – Hà Tiên · Vườn quốc gia U Minh Thượng · Trải nghiệm văn hóa và ẩm thực tại Kiên Giang · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Tin mới Tác giả: Lâm Thành Nguyên Ngày đăng: 20-02-2024 Cập nhật: 28-10-2026 Lượt xem: 18388 Kiên Giang là tỉnh có diện tích lớn nhất vùng Tây Nam Bộ của Việt Nam. Nơi đây nổi tiếng với rất nhiều danh lam thắng cảnh về thiên nhiên cũng như các di tích văn hóa lịch sử. Chính vì vậy, Kiên Giang còn được mệnh danh là “thiên đường” đối với những bạn thích du lịch và trải nghiệm du lịch miền Tây. Bài v_
- Tác giả: có · Cập nhật: 2026-10-28T10:06:00+07:00 · sameAs: không
- ✅ Phản hồi máy chủ 82ms (<200ms tốt)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content
- ❌ Ít H2 dạng câu hỏi khách thật sự hỏi AI (<30%)

### Dinh Cậu Phú Quốc - Địa điểm du lịch tâm linh 87 năm tuổi

- URL: https://rootytrip.com/dinh-cau-bieu-tuong-tam-linh-cua-phu-quoc/
- Trạng thái: 200 · phản hồi 123ms · HTML 341KB · 3273 từ
- H1: Dinh Cậu Phú Quốc – Nơi gắn kết giữa văn hóa và tâm linh trên đảo ngọc
- H2 (8, tỷ lệ dạng câu hỏi 12%): Giới thiệu Dinh Cậu Phú Quốc · Lịch sử Dinh Cậu Phú Quốc · Kiến trúc độc đáo của Dinh Cậu Phú Quốc · Dinh Cậu Phú Quốc có gì? · Truyền thuyết về Dinh Cậu Phú Quốc · Kinh nghiệm du lịch Dinh Cậu Phú Quốc · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Vui chơi Phú Quốc địa điểm du lịch phú quốc Tác giả: Lâm Thành Nguyên Ngày đăng: 06-10-2020 Cập nhật: 28-10-2026 Lượt xem: 5240 Dinh Cậu Phú Quốc là một di tích lịch sử văn hóa tâm linh có kiến trúc độc đáo, mang đậm dấu ấn của văn hóa dân tộc. Nơi đây thu hút du khách bởi vẻ đẹp cổ kính, uy nghi và là điểm đến tâm linh quan trọng của người dân địa phương. Hãy cùng Rooty Trip khám phá địa điểm tâm_
- Tác giả: có · Cập nhật: 2026-10-28T08:48:28+07:00 · sameAs: không
- ✅ Phản hồi máy chủ 123ms (<200ms tốt)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content
- ❌ Ít H2 dạng câu hỏi khách thật sự hỏi AI (<30%)
- ❌ JSON-LD lỗi cú pháp: Expecting ',' delimiter: line 21 column 5 (char 650)

### Cẩm Nang Tham Quan Danh Lam Thắng Cảnh Ở Kiên Giang

- URL: https://rootytrip.com/danh-lam-thang-canh-o-kien-giang/
- Trạng thái: 200 · phản hồi 113ms · HTML 343KB · 3367 từ
- H1: Lộ Diện Những Danh Lam Thắng Cảnh Ở Kiên Giang Ít Ai Biết
- H2 (6, tỷ lệ dạng câu hỏi 0%): Giới thiệu về Kiên Giang – Vùng đất của những kỳ quan · Những danh lam thắng cảnh không thể bỏ qua ở Kiên Giang · Di tích lịch sử và văn hóa đặc sắc · Kinh nghiệm du lịch Kiên Giang tự túc từ A đến Z · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Vui chơi Phú Quốc Tác giả: Rooty Trip Ngày đăng: 14-04-2025 Cập nhật: 28-10-2026 Lượt xem: 2033 Nếu bạn đang tìm kiếm một vùng đất hội tụ đầy đủ biển xanh, cát trắng, núi non hùng vĩ, di tích lịch sử và nền văn hóa phong phú, thì Kiên Giang chính là điểm đến lý tưởng cho chuyến hành trình sắp tới. Với hơn 140 hòn đảo lớn nhỏ, rừng nguyên sinh, thắng cảnh thơ mộng và những câu chuyện lịch sử hào hù_
- Tác giả: có · Cập nhật: 2026-10-28T08:31:51+07:00 · sameAs: có
- ✅ Phản hồi máy chủ 113ms (<200ms tốt)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content
- ❌ Ít H2 dạng câu hỏi khách thật sự hỏi AI (<30%)

### Bãi Dài Phú Quốc - Khám bãi bãi biển dài nhất nhì Phú Quốc

- URL: https://rootytrip.com/bai-dai-phu-quoc/
- Trạng thái: 200 · phản hồi 133ms · HTML 352KB · 3446 từ
- H1: Bãi Dài Phú Quốc – Khám phá một trong những bãi biển dài nhất Phú Quốc
- H2 (8, tỷ lệ dạng câu hỏi 12%): Giới thiệu về Bãi Dài Phú Quốc · Thời điểm lý tưởng du lịch Bãi Dài Phú Quốc · Hướng dẫn cách đi Bãi Dài Phú Quốc · Bãi Dài Phú Quốc có gì chơi? · Món ngon nhất định phải thử khi du lịch Bãi Dài Phú Quốc · Câu hỏi thường gặp · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Vui chơi Phú Quốc bãi dài phú quốc Tác giả: Lâm Thành Nguyên Ngày đăng: 29-05-2020 Cập nhật: 27-10-2026 Lượt xem: 7055 Nhắc đến du lịch Phú Quốc, chắc chắn bạn không nên bỏ qua Bãi Dài – một trong những bãi biển đẹp nhất hành tinh với bờ cát trắng mịn trải dài ôm lấy làn nước biển xanh ngọc bích. Nơi đây được mệnh danh là “viên ngọc ẩn mình” của đảo ngọc, sở hữu vẻ đẹp hoang sơ, bình yên cùng hệ s_
- Tác giả: có · Cập nhật: 2026-10-27T17:53:51+07:00 · sameAs: không
- ✅ Phản hồi máy chủ 133ms (<200ms tốt)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content
- ❌ Ít H2 dạng câu hỏi khách thật sự hỏi AI (<30%)

### Phú Quốc có mấy sân Golf? Review sân golf Vinpearl Phú Quốc

- URL: https://rootytrip.com/san-golf-phu-quoc/
- Trạng thái: 200 · phản hồi 127ms · HTML 333KB · 3010 từ
- H1: Review sân golf Vinpearl Phú Quốc – Tuyệt tác giữa rừng nguyên sinh
- H2 (9, tỷ lệ dạng câu hỏi 11%): Khám phá sân golf Vinpearl Phú Quốc · Thiết kế đỉnh cao của sân golf 27 hố chuẩn quốc tế · Trọn bộ tiện ích 5 sao khi chơi golf tại Vinpearl Phú Quốc · Giá sân golf Phú Quốc & cách đặt lịch chơi nhanh chóng · Trải nghiệm thực tế từ golfer · Lưu ý & lời khuyên dành cho người mới · Nghỉ ở đâu gần sân golf Phú Quốc? · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Vui chơi Phú Quốc Tác giả: Rooty Trip Ngày đăng: 12-04-2024 Cập nhật: 27-10-2026 Lượt xem: 3700 Nằm trong khu nghỉ dưỡng Vinpearl Phú Quốc , sân golf Phú Quốc là điểm đến lý tưởng dành cho những ai yêu thích sự kết hợp giữa thể thao đẳng cấp và không gian nghỉ dưỡng giữa thiên nhiên tuyệt mỹ. Hiện nay, Rooty Trip đang cung cấp các combo nghỉ dưỡng – chơi golf tại Vinpearl Phú Quốc, giúp du khách d_
- Tác giả: có · Cập nhật: 2026-10-27T17:48:47+07:00 · sameAs: có
- ✅ Phản hồi máy chủ 127ms (<200ms tốt)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content
- ❌ Ít H2 dạng câu hỏi khách thật sự hỏi AI (<30%)

### Du Lịch Gành Dầu Phú Quốc: Ở Đâu, Ăn Gì, Chơi Gì?

- URL: https://rootytrip.com/ganh-dau-phu-quoc/
- Trạng thái: 200 · phản hồi 73ms · HTML 373KB · 4194 từ
- H1: Du lịch Gành Dầu Phú Quốc: Trọn bộ combo nghỉ dưỡng, khám phá và ẩm thực
- H2 (8, tỷ lệ dạng câu hỏi 25%): Giới thiệu về Gành Dầu – Điểm đến không thể bỏ lỡ khi du lịch Phú Quốc · Chơi gì khi đến Gành Dầu Phú Quốc? · Ăn gì ở Gành Dầu Phú Quốc? Gợi ý 5 địa điểm đáng thử · Các quán cà phê chill tại Gành Dầu – trải nghiệm phong cách địa phương · Ở đâu khi du lịch Gành Dầu Phú Quốc? · Câu hỏi thường gặp về du lịch Gành Dầu Phú Quốc · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Vui chơi Phú Quốc ăn gì ở gành dầu phú quốc Tác giả: Ngô Trung Liêm Ngày đăng: 03-06-2025 Cập nhật: 27-10-2026 Lượt xem: 3546 Nằm ẩn mình nơi Tây Bắc hoang sơ của đảo ngọc, Gành Dầu Phú Quốc hiện lên như một viên ngọc thô với vẻ đẹp thiên nhiên hùng vĩ, thu hút du khách bởi sự bình yên và hoang sơ vốn có. Đây là một trong những địa điểm du lịch Phú Quốc lý tưởng nhất nếu bạn đang tìm kiếm một nơi _
- Tác giả: có · Cập nhật: 2026-10-27T17:47:47+07:00 · sameAs: không
- ✅ Phản hồi máy chủ 73ms (<200ms tốt)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content

### Kinh nghiệm du lịch miền Tây mùa nước nổi check in cực đỉnh

- URL: https://rootytrip.com/du-lich-mien-tay/
- Trạng thái: 200 · phản hồi 78ms · HTML 378KB · 7518 từ
- H1: Kinh nghiệm du lịch miền Tây mùa nước nổi từ A-Z
- H2 (7, tỷ lệ dạng câu hỏi 14%): Du lịch miền Tây có gì hấp dẫn? · Top địa điểm du lịch miền Tây không nên bỏ qua · Những trải nghiệm không thể bỏ qua khi du lịch miền Tây · Những điều cần biết khi khám phá miền Tây Việt Nam · Gợi ý lịch trình tour du lịch miền Tây hấp dẫn · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Tin mới Tác giả: Lâm Thành Nguyên Ngày đăng: 20-02-2024 Cập nhật: 27-10-2026 Lượt xem: 5892 Miền Tây không phải là nơi khiến bạn “wow” ngay từ cái nhìn đầu tiên như biển đảo hay resort sang trọng. Nhưng nếu bạn từng đi một lần, bạn sẽ hiểu vì sao nhiều người lại quay lại nơi này thêm nhiều lần nữa. Đó là cảm giác ngồi trên chiếc xuồng nhỏ len lỏi qua rừng tràm, là buổi sáng sớm giữa chợ nổi tấp nậ_
- Tác giả: có · Cập nhật: 2026-10-27T17:42:47+07:00 · sameAs: không
- ✅ Phản hồi máy chủ 78ms (<200ms tốt)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content
- ❌ Ít H2 dạng câu hỏi khách thật sự hỏi AI (<30%)

### Top 7 khu vui chơi Phú Quốc đã đi là phải thử trong năm 2026

- URL: https://rootytrip.com/khu-vui-choi-phu-quoc/
- Trạng thái: 200 · phản hồi 315ms · HTML 342KB · 4041 từ
- H1: Review TOP 7 khu vui chơi giải trí và tham quan ở Phú Quốc năm 2026
- H2 (10, tỷ lệ dạng câu hỏi 0%): Corona Casino Phú Quốc · VinWonders Phú Quốc · Vinpearl Safari Phú Quốc · Grand World Phú Quốc · Thị trấn hoàng hôn (Địa Trung Hải Phú Quốc) · Quần đảo An Thới Phú Quốc · Hòn Thơm · Chợ đêm Phú Quốc · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Vui chơi Phú Quốc Tác giả: Lâm Thành Nguyên Ngày đăng: 18-08-2023 Cập nhật: 27-10-2026 Lượt xem: 9858 Phú Quốc là thiên đường nghỉ dưỡng được biết đến với tên gọi đảo ngọc. Không chỉ cuốn hút bởi những bãi biển đẹp, hòn đảo thơ mộng mà còn dẫn dắt khách du lịch thập phương bởi nhiều khu vui chơi hiện đại , được đầu tư hoành tráng, đa dạng các loại hình dịch vụ. Cùng Rooty Trip điểm qua top 7 khu v_
- Tác giả: có · Cập nhật: 2026-10-27T16:35:32+07:00 · sameAs: không
- ✅ Phản hồi máy chủ 315ms (đạt mức tối thiểu <350ms)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content
- ❌ Ít H2 dạng câu hỏi khách thật sự hỏi AI (<30%)

### Chợ Dương Đông Phú Quốc: Hải Sản, Đặc Sản, Tips Mua 2026

- URL: https://rootytrip.com/cho-duong-dong-phu-quoc/
- Trạng thái: 200 · phản hồi 289ms · HTML 337KB · 2975 từ
- H1: Khám Phá Chợ Dương Đông – Trung Tâm Sầm Uất Nhất Phú Quốc
- H2 (7, tỷ lệ dạng câu hỏi 29%): Chợ Dương Đông ở đâu? · Cách di chuyển tới Chợ Dương Đông · Nên mua gì ở chợ Dương Đông? · Một vài kinh nghiệm mua sắm ở chợ Dương Đông Phú Quốc · Một vài địa điểm du lịch gần chợ Dương Đông Phú Quốc · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Vui chơi Phú Quốc Khám phá Phú Quốc Tác giả: Lâm Thành Nguyên Ngày đăng: 09-07-2021 Cập nhật: 27-10-2026 Lượt xem: 8058 Bạn đang tìm kiếm một địa điểm để thưởng thức và mua hải sản tươi ngon tại Phú Quốc? Chợ Dương Đông chính là điểm đến lý tưởng dành cho bạn! Nơi đây được mệnh danh là “thiên đường hải sản” với vô số quầy hàng bày bán đa dạng các loại hải sản tươi sống được đánh bắt trong ngày. Đừ_
- Tác giả: có · Cập nhật: 2026-10-27T16:29:12+07:00 · sameAs: không
- ✅ Phản hồi máy chủ 289ms (đạt mức tối thiểu <350ms)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content

### Bãi Khem Phú Quốc có gì? Cẩm nang du lịch 2026

- URL: https://rootytrip.com/tim-hieu-bai-khem-phu-quoc/
- Trạng thái: 200 · phản hồi 84ms · HTML 366KB · 4111 từ
- H1: Bãi Khem Phú Quốc 2026: Bãi biển TOP 50 thế giới có gì?
- H2 (9, tỷ lệ dạng câu hỏi 44%): Giới thiệu về Bãi Khem Phú Quốc · Nên đi bãi Khem vào thời gian nào? · Làm thế nào để đến được Bãi Khem Phú Quốc? · Bãi Khem Phú Quốc có gì chơi? · Ăn gì ở Bãi Khem Phú Quốc? · Nghỉ dưỡng tại các resort và khách sạn gần Bãi Khem · Kinh nghiệm cần biết trước khi tới Bãi Khem Phú Quốc · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Vui chơi Phú Quốc bãi khem mùa nào đẹp Tác giả: Lâm Thành Nguyên Ngày đăng: 29-05-2020 Cập nhật: 27-10-2026 Lượt xem: 11172 Bãi Khem Phú Quốc đã từng được xếp vào danh sách top 50 bãi biển đẹp nhất trên thế giới , do công ty du lịch Flight Network (Canada) công bố. Nơi đây được biết đến với cảnh hoàng hôn tuyệt đẹp, các khu resort cao cấp và những hoạt động chèo thuyền thú vị. Vậy, khi bạn đặt châ_
- Tác giả: có · Cập nhật: 2026-10-27T16:22:53+07:00 · sameAs: không
- ✅ Phản hồi máy chủ 84ms (<200ms tốt)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content
- ❌ JSON-LD lỗi cú pháp: Expecting ',' delimiter: line 21 column 5 (char 680)

### Symphony of the Sea Phú Quốc tạm ngừng 4–9/11/2026

- URL: https://rootytrip.com/symphony-of-the-sea-phu-quoc-tam-ngung-2026/
- Trạng thái: 200 · phản hồi 83ms · HTML 312KB · 1903 từ
- H1: Symphony of the Sea Phú Quốc tạm ngừng từ 4–9/11/2026
- H2 (6, tỷ lệ dạng câu hỏi 17%): Symphony of the Sea Phú Quốc tạm ngừng hoạt động 6 ngày · Chính sách hoàn vé Symphony of the Sea trong thời gian tạm ngừng · Symphony of the Sea mùa 3 dự kiến trở lại ngày 10/11/2026 · Du khách cần lưu ý gì khi đến Sunset Town đầu tháng 11? · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Tin mới Tác giả: Lâm Thành Nguyên Ngày đăng: 27-10-2026 Cập nhật: 27-10-2026 Lượt xem: 39 Sun World Phú Quốc vừa thông báo show Symphony of the Sea và nhà hàng Sun Bavaria GastroPub tại Sunset Town sẽ tạm ngừng hoạt động từ ngày 04/11 đến hết ngày 09/11/2026 để chuẩn bị cho sự trở lại của Symphony of the Sea mùa 3. Dự kiến, cả hai sẽ hoạt động trở lại từ ngày 10/11/2026. Nội dung bài viết Toggle T_
- Tác giả: có · Cập nhật: 2026-10-27T09:30:16+07:00 · sameAs: không
- ✅ Phản hồi máy chủ 83ms (<200ms tốt)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content
- ❌ Ít H2 dạng câu hỏi khách thật sự hỏi AI (<30%)

### Sun PhuQuoc Airways giảm 20% vé đến Ahmedabad

- URL: https://rootytrip.com/sun-phuquoc-airways-giam-20-ve-ahmedabad/
- Trạng thái: 200 · phản hồi 74ms · HTML 317KB · 1913 từ
- H1: Sun PhuQuoc Airways ưu đãi 20% vé máy bay đến Ahmedabad, Ấn Độ
- H2 (6, tỷ lệ dạng câu hỏi 0%): Sun PhuQuoc Airways triển khai ưu đãi 20% vé máy bay đến Ahmedabad · Ahmedabad – Điểm đến giàu bản sắc văn hóa của Ấn Độ · Đặt vé sớm để tận dụng ưu đãi · Khám phá thêm những hành trình mới cùng Rooty Trip · Tin tức liên quan · Có thể bạn sẽ thích
- 400 ký tự đầu sau H1: _Tin mới Tác giả: Rooty Trip Ngày đăng: 20-10-2026 Cập nhật: 20-10-2026 Lượt xem: 33 Sun PhuQuoc Airways triển khai chương trình ưu đãi giảm 20% giá vé cơ bản dành cho hành khách đặt vé đến Ahmedabad (Ấn Độ) từ ngày 16/10 đến hết ngày 13/11/2026. Chương trình áp dụng cho các chuyến bay đến hết ngày 03/06/2027, mang đến thêm cơ hội tiết kiệm chi phí cho du khách có kế hoạch khám phá Ấn Độ. Nội dung _
- Tác giả: có · Cập nhật: 2026-10-20T13:29:59+07:00 · sameAs: có
- ✅ Phản hồi máy chủ 74ms (<200ms tốt)
- ✅ Canonical tự trỏ
- ✅ Schema: BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, Place, PostalAddress
- ❌ Khối meta chen giữa H1 và câu trả lời (Tác giả:, Ngày đăng:, Lượt xem:, Cập nhật:) — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content
- ❌ Ít H2 dạng câu hỏi khách thật sự hỏi AI (<30%)

## 4. Những thứ script KHÔNG kiểm được (làm tay hoặc dùng skill)

- Trang có lên trang 1 Google cho ít nhất 1 câu hỏi con không (việc #1) → Search Console.
- Thử `site:domain + câu hỏi khách hay hỏi` (việc #9) → skill `rooty-geo-audit`.
- AI có nhắc tên Rooty Trip không, nói có đúng không (việc #3, #30) → skill `rooty-do-hien-dien-ai`.
- Tường lửa/CDN có chặn bot AI không dù robots.txt mở.
- Thông tin thương hiệu nhất quán trên GBP, Facebook, OTA (việc #11).
