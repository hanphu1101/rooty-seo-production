# Chẩn đoán rớt top — https://rootytrip.vn
_Ngày 17/11/2026 · máy chạy tự động · nhãn **[ĐÃ KIỂM]** = đo chính xác, **[NGHI VẤN]** = máy đoán theo dấu hiệu, người đọc lại để xác nhận._

## ① Có rớt thật không?
[ĐÃ KIỂM] Số liệu 2025-07-22 → 2026-11-14 (481 ngày). 28 ngày gần nhất: 184 lượt nhấp (-15.6% so 28 ngày trước). Đỉnh TB 7 ngày 49.6/ngày quanh 2025-12-25, hiện 5.9/ngày. → RỚT THẬT: giảm 88% so với đỉnh, bắt đầu khoảng 2026-01-01.

## ② Trùng đợt cập nhật thuật toán nào?
[ĐÃ KIỂM] Ngày bắt đầu rớt 2026-01-01 trùng với: **December 2025 core update** (2025-12-11 → 2025-12-29).
→ Trùng **core update**: ưu tiên chất lượng — trải nghiệm thật, đúng ý định, chủ đề tập trung. Không xoá/viết lại hàng loạt; sửa dần và đo.

## ③ Kiểm từng giả thuyết trên toàn blog
Quét 97 bài (EN 97) qua WordPress REST API + HTML công khai.

| # | Lỗi | Số bài | Nhãn | Vì sao ảnh hưởng thứ hạng |
|---|---|---|---|---|
| 1 | Đổi năm giả | 10 | [ĐÃ KIỂM] | Năm mới chỉ nằm trên tiêu đề, thân bài không có thông tin năm đó → thao túng độ mới; dễ bị hạ ở các đợt spam/core. |
| 2 | Lạc chủ đề | 5 | [NGHI VẤN] | Bài ngoài phạm vi Phú Quốc làm loãng chủ đề chính của site → giảm độ tin cậy chủ đề (topical authority). |
| 3 | Trùng từ khóa | 1 | [NGHI VẤN] | Nhiều bài cùng tranh một nhóm từ khoá → Google không biết chọn bài nào, các bài kéo nhau xuống; nhiều trang na ná nhau còn gần với «trang cửa ngõ» trong chính sách spam. |
| 4 | Tác giả | 96 | [ĐÃ KIỂM] | Một người đứng tên phần lớn bài mọi ngôn ngữ, thiếu xác minh (schema Person, hồ sơ cá nhân) → tín hiệu E-E-A-T yếu. |
| 5 | Link tự thân | 86 | [ĐÃ KIỂM] | Link trỏ về chính bài — Google gần như bỏ qua; sửa cho sạch, không kỳ vọng tăng hạng. |
| 6 | Đa ngôn ngữ | 4 | [ĐÃ KIỂM] | Bài ngoại ngữ quá mỏng, bài đã gộp vẫn Published → rác chỉ mục, ảnh hưởng nhỏ. |
| 7 | Thương mại | 2 | [NGHI VẤN] | Nhiều link/CTA bán hàng trong bài thông tin → trải nghiệm đọc kém; thường không phải nguyên nhân chính. |

Tác giả: 2 đứng tên 99% số bài (EN 96).

Chính sách spam có rủi ro: Nội dung sản xuất hàng loạt (Có rủi ro); Trang cửa ngõ (doorway) (Có rủi ro); Đổi năm / ngày cập nhật giả (Có rủi ro).

## ④ Thứ tự sửa đề xuất
1. **Đổi năm giả** — 10 bài [ĐÃ KIỂM]. Xem «Cần sửa gì» từng dòng ở tab B5 · Sửa lỗi từng trang.
2. **Lạc chủ đề** — 5 bài [NGHI VẤN]. Xem «Cần sửa gì» từng dòng ở tab B5 · Sửa lỗi từng trang.
3. **Trùng từ khóa** — 1 bài [NGHI VẤN]. Xem «Cần sửa gì» từng dòng ở tab B5 · Sửa lỗi từng trang.
4. **Tác giả** — 96 bài [ĐÃ KIỂM]. Xem «Cần sửa gì» từng dòng ở tab B5 · Sửa lỗi từng trang.
5. **Link tự thân** — 86 bài [ĐÃ KIỂM]. Xem «Cần sửa gì» từng dòng ở tab B5 · Sửa lỗi từng trang.
6. **Đa ngôn ngữ** — 4 bài [ĐÃ KIỂM]. Xem «Cần sửa gì» từng dòng ở tab B5 · Sửa lỗi từng trang.

Mỗi lần sửa: đổi trạng thái → «Đã sửa» (app tự chụp số liệu GSC làm mốc trước) → sau ≥ 4 tuần nhập GSC mới → «Đo hiệu quả», so với nhóm chưa sửa.

## Giới hạn của báo cáo
- Có số liệu GSC nên ① ② là đo thật.
- Nhãn NGHI VẤN cần người đọc lại bài trước khi sửa; máy có thể đoán sai.
- Chưa so trang nào rớt nhiều nhất: cần xuất GSC Trang 2 kỳ (so sánh) — xem B10 · Content audit.