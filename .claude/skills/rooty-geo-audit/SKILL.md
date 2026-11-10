---
name: rooty-geo-audit
description: Audit GEO cho rootytrip.com (hoặc một danh sách URL) — chạy scripts/geo_audit.py để kiểm bot AI, canonical, noindex, tốc độ, H1/H2, đoạn mở đầu, schema; rồi kiểm tay các việc script không làm được (site: test, nhất quán thương hiệu) và ra danh sách việc ưu tiên. Dùng định kỳ hằng tháng hoặc khi người dùng nói "audit", "kiểm website".
---

# GEO audit

## 1. Chạy script
```bash
python scripts/geo_audit.py https://rootytrip.com --max-pages 30
# hoặc chỉ một số trang:
python scripts/geo_audit.py https://rootytrip.com --urls <url1> <url2>
```
Báo cáo ra `reports/geo-audit-<domain>-<ngày>.md`. Trên Windows nếu lỗi font tiếng Việt thì thêm `-X utf8` sau `python`.

## 2. Kiểm tay (script không làm được)
1. **site: test** (Checklist việc #9 — cửa chặn): tìm `site:rootytrip.com` + 5–10 câu khách hay hỏi nhất (giá tour 4 đảo, combo 3N2Đ, đón sân bay, chính sách huỷ, tour cho gia đình có trẻ nhỏ…). Câu nào không có trang trả lời bằng chữ → ghi thành bài mới vào `01-prompts/hang-doi-tu-khoa.md`.
2. **Trang sự thật của thương hiệu** (việc #10): giới thiệu · bảng giá · FAQ · chính sách huỷ/hoàn · liên hệ — có đủ và cập nhật không?
3. **Thông tin nhất quán** (việc #11): tên, địa chỉ, hotline, năm thành lập giống nhau trên web, Google Business Profile, Facebook, TikTok, Traveloka/Klook (nếu có).
4. **Tường lửa/CDN**: robots.txt mở nhưng Cloudflare có chặn bot AI không? (Cloudflare → Security → Bots.)

## 3. Ra việc ưu tiên
Viết cuối báo cáo một bảng **Top 10 việc**, xếp theo: cửa chặn trước → ảnh hưởng nhiều trang → dễ làm. Mỗi việc: làm gì · trang nào · ai làm (dev / content / SEO) · ước lượng công.

So với báo cáo tháng trước (nếu có trong `reports/`): cái gì đã sửa, cái gì mới hỏng.
