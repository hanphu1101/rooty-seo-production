# Chấm bài mẫu nen-o-khu-nao-phu-quoc · 16/11/2026

Bài mẫu (không đi dây chuyền). Chấm hai lớp:

## Cổng 2 · bản nháp — FAIL
Giám khảo độc lập (subagent chưa đọc bài, chỉ nhận `gates/cong-2-ban-nhap.md` + bài + bối cảnh).
- Tiêu chí bắt buộc: **2/5 đạt** (số 2 không áp dụng vì chưa có Cổng 1)
- Tiêu chí thường: **7/15 = 47 %** (cần ≥ 80 %)

| # | Tiêu chí | B | Kết quả | Ghi chú |
|---|---|---|---|---|
| 1 | Mở đầu 100–150 từ trả lời thẳng | B | PASS | 127 từ |
| 2 | Đúng cấu trúc Cổng 1 | B | — | chưa có Cổng 1 |
| 3 | Câu đầu sau H2 = trả lời 40–50 từ | B | FAIL | 1/10 H2 đạt; Bắc đảo 14 từ; 2 H2 trống |
| 4 | H2 cắt rời vẫn hiểu | B | PASS | sát ngưỡng ("điều này", "bên dưới" giữa đoạn) |
| 5 | Đoạn 40–170 từ | | FAIL | 5 đoạn < 40 từ |
| 6 | Bảng dữ kiện nửa trên | | PASS | |
| 7 | Không dữ kiện bịa / có trong nguon.md | B | FAIL | xem ghi chú đối chiếu bên dưới |
| 8 | Câu chứa số hoàn chỉnh | | PASS | |
| 9 | ≥ 3 dữ kiện/100 từ ở phần trả lời | | FAIL | đoạn "khách sạn hay resort", "gia đình" thưa |
| 10 | Nguồn + tháng/năm ngay sau câu | | FAIL | nguồn dồn về bảng cuối |
| 11 | ≥ 1 trích dẫn | | FAIL | |
| 12 | ≥ 2 đoạn chỉ Rooty viết được | B | FAIL | 7–8 ô [CẦN HDV] trống |
| 13 | Test ngược top 5 + AI | | FAIL | |
| 14 | Kinh nghiệm trong nội dung | | FAIL | |
| 15 | Đúng giọng | | PASS | "Rooty" → "Rooty Trip"/"chúng mình" |
| 16 | Không mùi AI | | PASS | |
| 17 | Không nhồi từ khoá | | PASS | |
| 18 | CTA sau phần trả lời | | PASS | |
| 19 | 3–8 link nội bộ | | FAIL | 13 link |
| 20 | Không tự xếp #1 | | PASS | |
| 21 | Title/meta + gợi ý FAQ | | FAIL | title 59, meta 157 đạt; thiếu FAQ |

**Đối chiếu tiêu chí 7 (người viết kiểm lại 16/11/2026):** các số giám khảo nêu là "không nguồn" đều có trong bài Rooty đã đăng — "16h30–17h30 dạo Cầu Hôn" (rootytrip.com/cho-dem-vuifest-phu-quoc/), "hợp đồng thời hạn 10 năm" (rootytrip.com/cho-dem-phu-quoc-chinh-thuc-dung-hoat-dong/), tác giả "đồng hành từ năm 2018" (schema Person trang hồ sơ tác giả, đã ghi trong brand.md), resort 5 sao / Sol by Meliá 4 sao (bài resort Bãi Trường, review Sol by Meliá) — nhưng **chưa chép vào nguon.md** và **toàn nguồn nội bộ**. Tiêu chí 7 vẫn FAIL đúng luật cho tới khi bổ sung nguon.md + nguồn ngoài.

## Chấm GEO bằng bộ chấm của app (`app/geocheck.py`) — 87/100
- Đạt: mở đầu = câu trả lời (128 từ), 10/10 H2 dạng câu hỏi, không H2 rỗng nghĩa, 1.098 từ / 10 tiêu đề, dữ kiện 4,2/100 từ, 19/19 câu có số đủ chủ–vị, độ mới, không AggregateRating.
- Chưa đạt: #17 khối ý chính 100–170 từ (4/10 mục) · #13 kinh nghiệm trong nội dung (0 câu ngôi thứ nhất).
- Lưu ý điểm cao hơn thực tế: chấm trên bản dựng tạm ở 127.0.0.1 nên link rootytrip.com bị đếm là "link ngoài" (#19); #20 "thông tin chỉ Rooty có" máy chỉ đếm chữ "Rooty", chưa phải kinh nghiệm thật.
