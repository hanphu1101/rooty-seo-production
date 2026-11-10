# SOP 03 · Kỹ thuật

**Công đoạn:** 05 · R1 · 11 · 27 · 29  **Skill:** `rooty-ky-thuat`  **Script:** `scripts/crawl_site.py`, `scripts/geo_audit.py`

> **Làm trên trang:** tab **B5 · Technical SEO** (checklist 36 mục, nút "Kiểm tự động" chấm 26 mục, nút "Chạy crawl") và **B5 · Audit & sửa lỗi** (giao việc sửa, tự đóng/mở lại sau mỗi lần crawl).

## 05 · Rà soát toàn diện (T1)
Chạy:
```bash
python -X utf8 scripts/crawl_site.py https://rootytrip.com --max-pages 800
python -X utf8 scripts/geo_audit.py https://rootytrip.com --max-pages 30
```
`crawl_site.py` đi theo link nội bộ như Googlebot và xuất `reports/crawl-<ngày>.csv` (mọi URL: mã trạng thái, title, H1, số từ, canonical, noindex, độ sâu click, số link trỏ vào) + báo cáo trang mồ côi, trang sâu, trang lỗi.

Kiểm thêm bằng tay:
| Hạng mục | Cách kiểm | Đạt |
|---|---|---|
| Lập chỉ mục | Search Console → Trang (Pages) | Không có lỗi tăng bất thường; trang quan trọng "Đã lập chỉ mục" |
| Sitemap | GSC → Sơ đồ trang web | Đã gửi, không lỗi, chỉ chứa URL 200 + indexable |
| robots.txt | mở /robots.txt | Không chặn /wp-content/uploads, CSS, JS; mở bot AI tìm nguồn |
| HTTPS & bản chuẩn | thử http://, www | Tất cả 301 về 1 bản duy nhất |
| Core Web Vitals | GSC → Trải nghiệm; PageSpeed Insights trang chủ + 1 trang tour + 1 bài | LCP < 2,5s, INP < 200ms, CLS < 0,1 trên di động |
| Di động | xem trên điện thoại thật | Nút đặt tour dễ bấm, không popup che nội dung |
| Schema | Rich Results Test | Không lỗi; có Organization, BreadcrumbList, BlogPosting/Article; trang tour có Product/TouristTrip + Offer nếu có giá |
| Trang lỗi | crawl + GSC | 404 có link trỏ vào → sửa link hoặc 301 |
| Chuỗi redirect | crawl | Không quá 1 bước |
| Trùng lặp | crawl: title/H1 trùng | Mỗi URL một title riêng |
| Phân trang, tag, tác giả | crawl | Trang tag/lưu trữ mỏng → noindex |

## R1 · Sửa lỗi kỹ thuật từ rà soát (T1–T2)
Lỗi đã thấy ở audit 08/11/2026, ưu tiên theo tác động:
1. **Khối "chuyên mục · Tác giả · Ngày đăng · Lượt xem" nằm giữa H1 và đoạn mở đầu** (14/15 trang) → sửa template bài viết (theme WordPress): đưa khối xuống dưới đoạn đầu hoặc thu gọn còn 1 dòng nhỏ sau đoạn mở. Một lần sửa, lợi mọi bài.
2. **JSON-LD lỗi cú pháp** (bài Dinh Cậu và 1 bài khác) → sửa plugin/đoạn chèn tay; kiểm bằng Rich Results Test.
3. **Ảnh thiếu alt** (trang chủ 152/405) → bổ sung alt cho ảnh nội dung; ảnh trang trí để alt rỗng.
4. Các lỗi mới từ `crawl_site.py`.

Mỗi lỗi ghi: trang · lỗi · cách sửa · người sửa · ngày xong. Sửa xong chạy lại script để xác nhận.

## 11 · Cấu trúc website & mẫu trang tour (15 ngày đầu T2)
- **Menu** phản ánh topical map: Tour đảo · Tour trong ngày · Combo · Vé · Cẩm nang · Về Rooty.
- **URL** ngắn, không dấu, không ngày tháng: `/tour-4-dao-phu-quoc/`, `/ve-vinwonders-phu-quoc/`.
- **Mẫu trang tour** (wireframe) — thứ tự từ trên xuống:
  1. H1 + đoạn trả lời 2–3 câu (tour gì, bao lâu, giá từ, điểm khác biệt)
  2. Bảng thông tin nhanh: thời gian · giá từ · điểm đón · bao gồm · không bao gồm
  3. Nút đặt / Zalo (cố định trên di động)
  4. Lịch trình theo giờ
  5. Ảnh thật của Rooty (có alt)
  6. Bảng giá theo mùa/đối tượng
  7. Chính sách huỷ/đổi, lưu ý
  8. Đánh giá khách (thật, có tên/ngày)
  9. FAQ 4–6 câu
  10. Tour liên quan
- Breadcrumb trên mọi trang. Độ sâu click: mọi trang tour/bài lõi ≤ 3 click từ trang chủ.

## 27 · Đọc log máy chủ (T7)
Lấy access log 30 ngày (hosting/cPanel hoặc Cloudflare). Đếm lượt Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, PerplexityBot, ClaudeBot… theo thư mục.
Câu hỏi: bot có vào trang tour/bài lõi không? Có tốn lượt vào trang rác (tag, tham số, trang tìm kiếm) không? Bot AI còn vào được không (Cloudflare có chặn)?

## 29 · Kỹ thuật nâng cao (T7–T8)
- Độ sâu click và trang mồ côi (chạy lại `crawl_site.py`, so với T1).
- Phân bổ link nội bộ: trang tiền (tour/combo) có nhận đủ link chưa.
- Onpage tầng 2–3: trang danh mục, trang tag, trang tác giả.
- Tốc độ lại lần 2, ảnh WebP, lazy-load đúng (ảnh đầu trang không lazy).
