---
name: rooty-fact-check
description: Trạm 4 — kiểm chứng từng dữ kiện (giá, giờ, khoảng cách, lịch, số liệu) trong bản nháp đã PASS Cổng 2 bằng nguồn mở được, sửa chỗ sai/lỗi thời, chấm Cổng 3. Đầu ra ở 06-verified/<slug>/.
---

# Trạm 4 · Kiểm chứng

**Đầu vào:** `05-drafts/<slug>/draft.md` (đã PASS), `03-research/<slug>/nguon.md`.
**Đầu ra:** `06-verified/<slug>/verified.md` + `_gate.md` (bảng kiểm chứng).

## Các bước
1. Quét bài, liệt kê **mọi câu có dữ kiện**: số tiền, giờ, ngày, km, phút, năm, tên đơn vị vận hành, xếp hạng, "lớn nhất/dài nhất".
2. Với từng dữ kiện, **mở lại nguồn** (không dựa vào trí nhớ). Ưu tiên trang chính thức của điểm tham quan/đơn vị vận hành.
3. Ghi bảng theo mẫu trong `gates/cong-3-kiem-chung.md`.
4. Sửa trong `verified.md`: SAI/LỖI THỜI → thay bản đúng + nguồn; KHÔNG TÌM ĐƯỢC NGUỒN → xoá câu hoặc viết lại không có số.
5. Xử lý hết `[CẦN KIỂM CHỨNG]`. `[CẦN HỎI HDV]` thì giữ lại và liệt kê ở đầu `_gate.md` để người hỏi team.
6. Chấm cổng 3.

Đặc biệt cẩn thận: giá vé mùa cao điểm/thấp điểm, giờ show (Kiss of the Sea, Sun Set…), lịch tạm ngưng, giá vé máy bay — các thứ này đổi thường xuyên.
