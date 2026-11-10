---
name: rooty-tu-khoa
description: Nghiên cứu từ khoá và dựng bản đồ chủ đề cho Rooty Trip — phân tích đối thủ theo loại trang, gom từ khoá theo SERP thành cụm, gán trang đích, tìm từ khoá traffic sớm, dựng topical map. Dùng khi người dùng nói "nghiên cứu từ khoá", "topical map", "bản đồ chủ đề", "đối thủ", "từ khoá nào nên làm".
---

# Từ khoá & bản đồ chủ đề

Làm theo `quy-trinh/02-nghien-cuu-tu-khoa.md`. Đầu ra lưu ở `nghien-cuu/`.

## Nguồn dữ liệu (hỏi người dùng nếu chưa có)
- Search Console: Hiệu suất → Truy vấn + Trang, 16 tháng → CSV vào `reports/du-lieu/`.
- File xuất từ công cụ từ khoá (Ahrefs/Semrush/Keyword Planner) nếu có.
- Câu hỏi sale/CSKH hay nhận.
Không có lượng tìm kiếm thật → ghi "chưa có số", không bịa.

## Các việc
1. **Đối thủ (02):** với mỗi loại trang (tour, combo, vé, cẩm nang, lịch trình), tìm top 3 Google cho 2–3 từ khoá đại diện; bảng so sánh: có giá? lịch trình theo giờ? ảnh thật? đánh giá? FAQ? → cột "khoảng trống Rooty có thể thắng". Ghi `nghien-cuu/doi-thu.md`.
2. **Gom cụm (04):** gắn ý định; hai từ khoá trùng ≥ 3–4 URL trong top 10 → cùng cụm. Gán URL đích (ưu tiên URL Rooty đã có — kiểm bằng `site:rootytrip.com` và `reports/crawl-*.csv`). Ghi `nghien-cuu/tu-khoa-chu-de.csv` đúng cột trong SOP.
3. **Ăn thịt từ khoá:** truy vấn có ≥ 2 URL Rooty nhận impressions → đánh dấu để xử lý ở content audit.
4. **Traffic sớm (09):** từ dữ liệu Search Console, lọc vị trí 8–30 + impressions cao → danh sách cơ hội nhanh.
5. **Topical map (10):** dựng cây theo mẫu trong SOP, mỗi node ghi URL · loại trang · từ khoá chính · trạng thái (tốt / cần sửa / cần viết). Ghi `nghien-cuu/topical-map.md`.
6. Đẩy node "cần viết/cần sửa" vào `01-prompts/hang-doi-tu-khoa.md` (hoặc tạo bài trên trang theo dõi qua `POST http://localhost:8010/api/bai` nếu server đang chạy).
