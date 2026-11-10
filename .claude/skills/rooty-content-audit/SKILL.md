---
name: rooty-content-audit
description: Rà soát nội dung cũ trên rootytrip.com — kiểm kê mọi URL, ghép dữ liệu Search Console, gán hành động giữ / cập nhật / gộp / xoá-301 / xoá-410 / noindex cho từng bài, phát hiện ăn thịt từ khoá, lập kế hoạch redirect theo đợt. Dùng khi người dùng nói "content audit", "rà soát bài cũ", "bài trùng", "xoá bài", "gộp bài".
---

# Rà soát nội dung cũ

Làm theo `quy-trinh/04-ra-soat-noi-dung-cu.md`.

1. **Kiểm kê:** dùng `reports/crawl-*.csv` mới nhất (chưa có → chạy `scripts/crawl_site.py` với `--max-pages` đủ lớn).
2. **Ghép Search Console:** cần file xuất "Trang" 12 tháng (clicks, impressions, vị trí) trong `reports/du-lieu/`. Chưa có → hỏi người dùng. Ghép theo URL (chuẩn hoá dấu `/` cuối).
3. **Gán hành động** theo bảng và quy tắc trong SOP. Mỗi dòng phải có `ly_do` một câu. Gộp → ghi `url_dich_301` là bài mạnh nhất.
4. **Ăn thịt từ khoá:** nếu có file xuất truy vấn × trang, tìm truy vấn có ≥ 2 URL Rooty → đề xuất gộp.
5. **Chủ đề lệch:** bài ngoài du lịch Phú Quốc/Kiên Giang/miền Tây → đánh dấu xem xét.
6. Ghi `nghien-cuu/content-audit.csv` (UTF-8 có BOM để mở Excel không lỗi font) + tóm tắt `reports/content-audit-<ngày>.md`: số URL mỗi hành động, đợt 1 (≤ 30 URL ưu tiên cao nhất), danh sách redirect cần tạo.
7. Bài "Cập nhật" → thêm vào hàng đợi dây chuyền với ghi chú "cập nhật, giữ URL".

**Không tự xoá, không tự tạo redirect.** Người dùng duyệt từng đợt.
