---
name: rooty-lien-ket-noi-bo
description: Lập kế hoạch liên kết nội bộ theo cụm chủ đề cho rootytrip.com — tìm trang mồ côi, trang ít link, trang sâu, đề xuất từng link cụ thể (từ URL, đến URL, anchor, câu đặt link) dồn sức mạnh về trang tour/combo. Dùng khi người dùng nói "liên kết nội bộ", "internal link", "trang mồ côi", "gắn link".
---

# Liên kết nội bộ

Làm theo `quy-trinh/07-lien-ket-noi-bo.md`.

1. Lấy `reports/crawl-*.csv` mới nhất (cột `inlinks`, `depth`) và `nghien-cuu/topical-map.md`. Chưa có → chạy crawl / làm topical map trước.
2. Chọn **một cụm** (người dùng chỉ định hoặc cụm có trang tiền ít inlinks nhất).
3. Với mỗi bài trong cụm, đọc nội dung (WebFetch) và tìm **câu sẵn có** phù hợp để gắn link — ưu tiên sửa câu có sẵn hơn thêm câu mới.
4. Xuất `nghien-cuu/lien-ket-<cum>.csv`: `tu_url, den_url, anchor, cau_goc, cau_sau_khi_gan, ly_do, trang_thai`.
   - Bài con ↔ trụ; bài con → 2–3 anh em + 1 trang tour.
   - Anchor mô tả, đa dạng; không "tại đây".
   - Không link tới URL redirect/404 (kiểm trong CSV crawl).
5. Tóm tắt: trước/sau số inlinks dự kiến của từng trang tiền.

Người dùng gắn link trên WordPress, rồi chạy lại crawl để xác nhận.
