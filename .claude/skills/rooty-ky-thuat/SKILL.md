---
name: rooty-ky-thuat
description: SEO kỹ thuật cho rootytrip.com — crawl toàn site (scripts/crawl_site.py), audit GEO kỹ thuật, kiểm index/sitemap/robots/redirect/tốc độ/schema, lập danh sách lỗi cần dev sửa, đọc log máy chủ, rà soát nâng cao độ sâu click. Dùng khi người dùng nói "kỹ thuật", "crawl", "lỗi website", "index", "tốc độ", "log máy chủ".
---

# SEO kỹ thuật

Làm theo `quy-trinh/03-ky-thuat.md`.

## Rà soát (05, 29)
```bash
python -X utf8 scripts/crawl_site.py https://rootytrip.com --max-pages 800
python -X utf8 scripts/geo_audit.py https://rootytrip.com --max-pages 30
```
Đặt `--max-pages` lớn hơn số URL trong sitemap để crawl hết (mới kết luận được trang mồ côi).

Đọc 2 báo cáo, rồi viết `reports/loi-ky-thuat-<ngày>.md` gồm bảng:
`# · lỗi · số trang · ví dụ URL · mức (🔴 chặn index / 🟡 ảnh hưởng xếp hạng / 🟢 nên sửa) · cách sửa cụ thể trên WordPress · ai sửa`
Xếp 🔴 trước. Lỗi theme (VD khối meta trước đoạn mở) ghi rõ file/template cần sửa nếu đoán được, kèm cách kiểm lại.

## Kiểm tay — nhắc người dùng làm (Claude không đăng nhập được)
Search Console (Trang, Sơ đồ trang web, Trải nghiệm), PageSpeed Insights cho 3 URL mẫu, Rich Results Test, Cloudflare/tường lửa có chặn bot AI không. Người dùng dán kết quả → Claude tổng hợp.

## Sau khi dev sửa (R1)
Chạy lại script, so với báo cáo trước: lỗi nào hết, lỗi nào còn, lỗi nào mới.

## Log máy chủ (27)
Người dùng xuất access log vào `reports/du-lieu/log/`. Viết script nhỏ (Python, thư viện chuẩn) đếm lượt theo user-agent (Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, PerplexityBot, ClaudeBot, Claude-User…) × thư mục × mã trạng thái. Báo cáo: bot có vào trang tiền không, có phí lượt vào trang rác không, bot AI có bị 403 không.

Không tự sửa website. Chỉ đề xuất.
