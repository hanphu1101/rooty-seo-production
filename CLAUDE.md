# Rooty SEO Production — luật chơi

Đây là dây chuyền sản xuất nội dung SEO + GEO cho **Rooty Trip** (rootytrip.com — tour, combo nghỉ dưỡng, vé tham quan Phú Quốc). Mục tiêu kép: bài lên top Google **và** được ChatGPT, Gemini, Google AI Overview, Perplexity nhắc tên Rooty Trip khi khách hỏi về du lịch Phú Quốc.

Đọc file này trước mọi việc. Sau đó đọc `ORCHESTRATOR.md` để biết bài đang ở trạm nào.

Ngoài nội dung, toàn bộ quy trình SEO 10 tháng (kỹ thuật, từ khoá, onpage, liên kết nội bộ, local SEO, offsite, đo lường…) nằm ở `quy-trinh/` — mỗi mảng một SOP và một skill `rooty-*`. Việc gì không nằm trong dây chuyền bài viết → tìm SOP của mảng đó trước khi làm.

## Nguyên tắc không được phá

1. **Một bài = một thư mục slug**, đi qua các trạm theo thứ tự. Không nhảy trạm, không sửa file ở trạm trước — muốn sửa thì trả bài về trạm đó và ghi lý do vào `log.md`.
2. **`02-raw/` là bất biến.** Chỉ thêm, không sửa, không xoá. Đây là nguồn gốc mọi dữ kiện.
3. **Chưa PASS cổng thì chưa đi tiếp.** Mỗi cổng có file tiêu chí trong `gates/`. Ghi kết quả chấm (PASS/FAIL từng tiêu chí + lý do) vào file `_gate.md` trong thư mục bài.
4. **Không bịa dữ kiện.** Giá vé, giờ mở cửa, khoảng cách, tên đơn vị phải có nguồn trong `02-raw/` hoặc `03-research/` kèm ngày lấy. Chưa có nguồn → ghi `[CẦN KIỂM CHỨNG]`, không đoán.
5. **Không tự đăng, không tự gửi gì ra ngoài.** Dây chuyền dừng ở `08-humanized/`. Người duyệt (cổng 4) mới được đăng lên WordPress.
6. **Mỗi lần người sửa bài của AI → thêm một dòng luật** vào mục "Luật học được" cuối file này, để lần sau không lặp lại lỗi đó.
7. **«Xong» phải kiểm được, không tự báo.** Mỗi thay đổi trên web ghi vào Nhật ký thay đổi (app SEO Automation · B11) phải kèm ô «Phép kiểm» — mỗi dòng `CÓ: chuỗi phải thấy` / `KHÔNG: chuỗi không được còn` trên trang thật — để nút «Thanh tra» chấm Đạt/Không đạt. Công đoạn SEO chỉ chuyển «Xong» khi đạt tiêu chí «Xong khi» trong `quy-trinh/cong-doan.json`, rồi kiểm lại theo mốc tuần ghi ở đó.

## Bản đồ trạm

| Trạm | Thư mục | Skill | Cổng ra |
|---|---|---|---|
| 0 | `00-context/` | (người cập nhật) | — |
| 1 · Nghiên cứu | `03-research/<slug>/` | `rooty-research` | — |
| 2 · Dàn ý | `04-outlines/<slug>/` | `rooty-outline` | Cổng 1 · `gates/cong-1-dan-y.md` |
| 3 · Viết nháp | `05-drafts/<slug>/` | `rooty-viet-bai` | Cổng 2 · `gates/cong-2-ban-nhap.md` |
| 4 · Kiểm chứng | `06-verified/<slug>/` | `rooty-fact-check` | Cổng 3 · `gates/cong-3-kiem-chung.md` |
| 5 · Brief hình ảnh | `07-media-brief/<slug>/` | `rooty-media-brief` | — |
| 6 · Chuốt giọng | `08-humanized/<slug>/` | `rooty-humanize` | Cổng 4 · `gates/cong-4-nguoi-duyet.md` (NGƯỜI) |

Ngoài dây chuyền bài viết còn ba việc thường dùng:
- `rooty-geo-audit` — chạy `scripts/geo_audit.py` + kiểm tay, ra báo cáo trong `reports/`.
- `rooty-do-hien-dien-ai` — đo Rooty Trip có được AI nhắc tên không, ghi vào `01-prompts/theo-doi-hien-dien.csv`.
- `rooty-chan-doan` — khi web rớt top: GSC → đối chiếu cập nhật thuật toán → quét toàn blog 8 loại lỗi → thứ tự sửa; mọi kết luận gắn nhãn ĐÃ KIỂM / NGHI VẤN.

## Quy tắc viết GEO (áp cho mọi bài — tóm từ Checklist GEO của GTV)

- **Mở đầu = câu trả lời.** 100–150 từ đầu sau H1 trả lời thẳng câu hỏi chính. Không mở bằng "Phú Quốc là hòn đảo xinh đẹp…".
- **H2 = câu hỏi thật** khách gõ vào Google/ChatGPT ("Địa Trung Hải Phú Quốc nằm ở đâu?", "Vé cáp treo Hòn Thơm bao nhiêu tiền?"). Cấm H2 rỗng nghĩa: "Tổng quan", "Giới thiệu", "Kết luận".
- **Câu đầu sau mỗi H2 = câu trả lời 40–50 từ**, theo loại: định nghĩa → "X là…" · cách làm → "Để X, làm N bước…" · so sánh → kết luận trước · có/không → trả lời ngay rồi mới nêu điều kiện.
- **Mỗi đoạn tự đứng được.** Cắt rời một H2 vẫn hiểu: có tên địa điểm + bối cảnh + dữ kiện. Không dùng "điều này", "như đã nói ở trên".
- **Dữ kiện dạng câu hoàn chỉnh**, trích được: "Cáp treo Hòn Thơm dài 7.899,9 m, đi hết khoảng 15 phút." chứ không phải "7.899,9m".
- **Có thứ chỉ Rooty mới có**: kinh nghiệm hướng dẫn viên bản địa, ảnh tự chụp, giờ đẹp để check-in, mẹo né đông, giá thực tế khách đã đi. Bài mà tóm tắt top 10 Google là ra được → làm lại.
- **Số liệu kèm nguồn + tháng/năm.** Bài giá/so sánh cập nhật thật mỗi ~30 ngày. Cấm chỉ đổi năm trên tiêu đề.
- **Tác giả thật**, kinh nghiệm nằm trong nội dung ("Khi dẫn đoàn tháng 6…"), không chỉ ở box tác giả.
- **Không xếp Rooty #1** trong bài liệt kê nếu không có cách chấm công khai.

## 5 điều không hứa (nói rõ với sếp/khách)

Không bán llms.txt như đòn bẩy · không coi schema là cách được trích dẫn · không hứa AI trả lời y hệt mỗi lần · không trích dẫn tên/nguồn bịa · không nhồi "chính chủ".

## Luật học được

<!-- Mỗi lần người sửa bài, thêm 1 dòng: ngày · lỗi · luật mới. Ví dụ:
- 2026-11-10 · AI viết giá vé VinWonders cũ · Luôn lấy giá từ trang chính thức, ghi ngày lấy, không dùng giá trong bài cũ của Rooty. -->
- 2026-11-08 · Audit thấy khối "Tác giả · Ngày đăng · Lượt xem" chen giữa H1 và đoạn mở đầu ở 14/15 trang · Khi đề xuất sửa giao diện, đưa khối meta xuống dưới đoạn mở đầu hoặc ra ngoài thẻ main content.
- 2026-11-18 · AI gọi HDV Lâm Thành Nguyên là «anh Lâm» · Gọi người Việt theo TÊN (chữ cuối), không theo họ: Lâm Thành Nguyên → «anh Nguyên».
- 2026-11-18 · Chèn kinh nghiệm HDV vào bài bằng nhãn lặp «Kinh nghiệm của hướng dẫn viên … (Rooty Trip):» + «10 năm dẫn tour» nhiều lần → đọc gượng · Mỗi bài giới thiệu đầy đủ tên + số năm kinh nghiệm MỘT lần; các đoạn sau viết liền mạch vào văn bài («Anh Nguyên thường…», «Mẹo nhỏ:…»), không lặp nhãn, không lặp ý đoạn trước đã nói, đổi cách mở đoạn giữa các bài.
- 2026-11-21 · Schema trang chủ: AI đề xuất CollectionPage + ItemList, giữ BreadcrumbList/FAQ, và khai chi nhánh bằng parentOrganization · Trang chủ KHÔNG có BreadcrumbList, CollectionPage, ItemList, FAQPage, WebPage mặc định (Rank Math WebPage tắt bằng WPCode #86933). Thực thể chính là TravelAgency `https://rootytrip.com/#travelagency`; chi nhánh khai bằng `subOrganization` ở thực thể chính, KHÔNG dùng `parentOrganization`. Không dùng FAQPage (Google không còn hiển thị) và không dùng điểm sao tự chấm (CreativeWorkSeries/aggregateRating không có đánh giá thật). Sản phẩm giá 0 → TouristTrip (WPCode #86956). Schema chèn tay nằm ở ô «Insert Script to <head>» (plugin Header and Footer Scripts) của từng trang. Bản chuẩn trang chủ (chị Hân duyệt 21/11/2026): `reports/schema-trang-chu-chuan.json` — sửa schema trang chủ thì sửa từ bản này.
- 2026-11-23 · AI thay hộp tour Grand World (ngưng bán) bằng hộp «Tour VinWonders Phú Quốc & Grand World 1 ngày» theo tên cũ, nhưng tour đó đã đổi lịch trình, chỉ còn đi VinWonders · Trước khi chèn/đổi hộp tour hay nhắc tên tour trong bài, mở trang sản phẩm xem lịch trình hiện tại; tên tour và lịch trình theo trang sản phẩm, giá theo wiki bảng giá. Giá web daily tour = giá ghép − ưu đãi B2C 1 vé + giá Net vé đi kèm (wiki «02 · Daily Tour»).
- 2026-11-25 · Schema bài viết: breadcrumb bị lồng 2 lần trong BlogPosting (Rank Math gắn `WebPage.breadcrumb`, BlogPosting trỏ WebPage qua isPartOf + mainEntityOfPage) mà AI rà trên HTML vẫn tưởng đúng · Kiểm schema bằng validator.schema.org, không chỉ đọc JSON: BreadcrumbList phải là mục gốc riêng ngang hàng BlogPosting, WebPage không có `breadcrumb` (WPCode #87135). Mỗi bài chỉ một bộ schema Rank Math — không chèn tay thêm BlogPosting/Article/WebPage/BreadcrumbList/FAQPage vào ô «Insert Script to <head>», không dùng @id `kg:`, bài dịch không chép schema bài gốc. Sửa ô đó phải gõ trong khung CodeMirror rồi Update (sửa textarea ẩn sẽ bị ghi đè). `&amp;`/`&#038;` trong JSON-LD do Rank Math mã hoá sau bộ lọc, validator vẫn đọc «&» → không phải lỗi, không sửa.
- 2026-11-28 · 7 bài tiếng Hàn (do AI viết trước đây) có lời khách kèm tên, «TripAdvisor 1,200+», «hoàn 100%», «rẻ hơn 5–10%», kênh KakaoTalk, «HDV tiếng Hàn đi kèm», gói trăng mật không có thật · Sự thật chị Hân xác nhận: HDV tiếng Hàn CÓ nhưng **thuê ngoài theo yêu cầu**, không phải HDV công ty, không ghi «포함/24/7»; Rooty **không có KakaoTalk** (chỉ hotline, WhatsApp +84 886 068 886, email); TripAdvisor 4.9/5 với 610 đánh giá (11/2026); hoàn huỷ theo /ko/payment-and-refund-cancellation-policy/ (tour ngày huỷ trước 3 ngày miễn phí, Rooty huỷ do thời tiết → hoàn đủ/đổi lịch). Không viết lời khách có tên, số năm/số khách, «giá thấp nhất», «đối tác chính thức» khi không có nguồn; tên gói/tour và giá phải là sản phẩm đang bán trên web.
- 2026-11-28 · Bài Kiss Bridge (KO) khuyên đứng trên Cầu Hôn ngắm hoàng hôn, vé «trước/sau 4 giờ chiều 50.000/100.000» · Vé Cầu Hôn 100.000đ một giá (dưới 1m miễn phí), vào được 07:00–17:30 hoặc sau 20:15; **vé thường bị mời ra lúc 17:30** (chị Hân xác nhận) → không khuyên đứng trên cầu xem mặt trời lặn bằng vé thường: giờ đẹp trên cầu 16:00–17:30, ngắm hoàng hôn từ bãi biển Sunset Town. Vé show Symphony có kèm vé Cầu Hôn. Giá vé tham quan lấy theo wiki 04.1/04.2, ghi mốc tháng.
