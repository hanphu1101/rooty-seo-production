# Rà schema bài viết rootytrip.com · 25/11/2026

Phạm vi: 376 URL trong `post-sitemap.xml` (208 VI · 121 EN · 18 KO · 19 RU · 10 ZH). Em đọc JSON-LD trên HTML thật của từng bài, rồi mở bài mẫu /taxi-phu-quoc/ trên validator.schema.org. Danh sách từng bài: [danh-sach-376-bai.csv](danh-sach-376-bai.csv).

## 1. Breadcrumb bị lồng 2 lần trong BlogPosting · 375/376 bài · ĐÃ KIỂM

Trên validator, mỗi bài chỉ hiện **1 mục gốc là BlogPosting**. BreadcrumbList nằm bên trong BlogPosting 2 lần:
- BlogPosting → `isPartOf` → WebPage → `breadcrumb`
- BlogPosting → `mainEntityOfPage` → WebPage → `breadcrumb`

Trong mã, BreadcrumbList vốn đã nằm ở gốc `@graph`. Nó bị kéo vào trong vì WebPage có thuộc tính `breadcrumb` trỏ tới nó, mà BlogPosting trỏ tới WebPage 2 lần. Phần này do Rank Math tự sinh, giống hệt nhau ở mọi bài, nên **sửa một chỗ là xong cả 375 bài**, không phải sửa từng bài.

**Cách sửa:** bỏ thuộc tính `breadcrumb` khỏi WebPage. Khi đó BreadcrumbList thành mục gốc riêng, ngang hàng BlogPosting. Rank Math không có nút tắt cho việc này, phải thêm một đoạn PHP qua WPCode: [wpcode-breadcrumb-goc.php](wpcode-breadcrumb-goc.php). Đoạn mã chỉ áp cho bài viết (post), không đụng trang chủ, trang thường hay sản phẩm.

Thứ tự làm: bật ở chế độ thử (chỉ chạy khi URL có `?rooty_schema_test=1`) → dán URL thử vào validator, thấy 2 mục gốc BlogPosting + BreadcrumbList → bật cho tất cả → xoá cache WP Rocket.

Bài còn lại là /ko/phu-quoc-food-guide/: URL này đang bị chuyên mục cùng slug che (xem mục 4), nên không có BlogPosting.

## 2. 8 bài có thêm schema chèn tay (ô «Insert Script to <head>») · cần sửa từng bài

Ngoài schema Rank Math, 8 bài này còn một khối JSON-LD thứ hai chèn tay. Khối này lặp lại BlogPosting / WebPage / BreadcrumbList với @id khác (`#article` thay vì `#richSnippet`), nên Google thấy 2 bài viết trên cùng một trang.

| Bài | Khối chèn tay có gì | Lỗi | Đề xuất |
|---|---|---|---|
| /chua-ho-quoc-phu-quoc/ | TravelAgency, WebSite, Person, WebPage, **BreadcrumbList thứ 2**, ImageObject, BlogPosting, **FAQPage** | Trùng BlogPosting + breadcrumb; FAQPage (Google không còn hiển thị); kiểu `Webpage` viết sai | Xoá cả khối |
| /bi-mat-nuoc-mam-truyen-thong-phu-quoc/ | như trên + ItemList, **BreadcrumbList thứ 2** | Trùng BlogPosting + breadcrumb | Xoá cả khối |
| /khach-san-phu-quoc-gan-bien/ | như trên + ItemList, **BreadcrumbList thứ 2** | Trùng BlogPosting + breadcrumb; `Webpage` viết sai | Xoá cả khối |
| /en/seaside-hotels-in-phu-quoc/ | **chép y khối của bài tiếng Việt** /khach-san-phu-quoc-gan-bien/ | Trang EN khai URL, @id, nội dung tiếng Việt của trang VI | Xoá cả khối |
| /phu-quoc-thuoc-tinh-nao/ | TravelAgency, WebSite, Person, WebPage, ImageObject, BlogPosting | Trùng BlogPosting | Xoá cả khối |
| /en/phu-quoc-island/ | **chép y khối của bài tiếng Việt** /phu-quoc-thuoc-tinh-nao/ | Trang EN khai URL của trang VI | Xoá cả khối |
| /dia-diem-du-lich-dep-o-hon-son/ | Article (tác giả Rooty Trip, ngày 13/02/2026) | Trùng với BlogPosting của Rank Math, khác tác giả và ngày | Xoá cả khối |
| /en/aquatopia-water-park/ | TouristAttraction | `addressRegion: Kien Giang` đã cũ (nay là An Giang); không trùng | Giữ, sửa thành An Giang, hoặc xoá nếu muốn gọn |

Lỗi chung của 6 khối lớn (TravelAgency…BlogPosting):
- @id TravelAgency là `kg:/g/11fl5fcr0h`, khác thực thể chính `https://rootytrip.com/#travelagency` → Google thấy 2 công ty.
- Mô tả HDV ghi «hơn 5 năm kinh nghiệm», lệch với «10 năm dẫn tour» trong bài.
- Nhồi rất nhiều thuộc tính không có tác dụng (accessMode, citation, copyrightYear, articleBody cả bài…). Đây là schema soạn từ 2023–2024, chưa cập nhật lại.

Xoá 7 khối thì Rank Math vẫn giữ đủ BlogPosting, tác giả, breadcrumb cho các bài này, không mất gì.

## 3. Lỗi ký tự trong tên (nhẹ, không bắt buộc)

- 23 bài: tên mục cuối của breadcrumb có `&#038;` thay vì `&`. Ví dụ /taxi-phu-quoc/: «Bảng Giá, Hotline &#038; Kinh Nghiệm».
- 47 bài: headline BlogPosting có `&amp;`.

Validator vẫn hiển thị đúng dấu `&`, nhưng một số công cụ đọc nguyên văn. Có thể xử lý trong cùng đoạn mã ở mục 1 nếu chị muốn. Danh sách bài nằm trong cột cuối file CSV.

## 4. Không phải lỗi schema nhưng thấy khi rà

/ko/phu-quoc-food-guide/ đang hiện trang chuyên mục (CollectionPage) thay vì bài viết, vì có chuyên mục trùng slug. Việc này đã báo trước đây, vẫn chờ chị quyết.

## Không thấy

Không có JSON hỏng, không có aggregateRating/review tự chấm, không có FAQPage ngoài bài chùa Hộ Quốc.
