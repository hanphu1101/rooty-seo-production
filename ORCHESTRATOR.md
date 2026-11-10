# ORCHESTRATOR — quản đốc dây chuyền

Khi được gọi "chạy dây chuyền" (skill `rooty-chay-day-chuyen`), làm đúng thứ tự sau.

## 1. Đọc trạng thái

- Đọc `index.md` — bảng mọi bài và trạm hiện tại.
- Đọc 20 dòng cuối `log.md` — việc gần nhất, bài nào bị trả về.

## 2. Chọn việc

Ưu tiên theo thứ tự:
1. Bài bị **trả về** (FAIL cổng) → sửa ở đúng trạm bị trả.
2. Bài đang **dở** ở trạm thấp nhất → đẩy tiếp một trạm.
3. Từ khoá mới trong `01-prompts/hang-doi-tu-khoa.md` → mở bài mới ở trạm 1.

Mỗi lần chạy chỉ đẩy **một bài qua tối đa một cổng**, trừ khi người dùng nói rõ "chạy hết".

## 3. Làm việc ở trạm

- Gọi skill của trạm (xem bảng trong `CLAUDE.md`).
- Đầu ra ghi vào `<thư mục trạm>/<slug>/`.
- Nếu trạm có cổng: chấm theo file `gates/…`, ghi `_gate.md` vào thư mục bài.
  - **PASS** (đủ mọi tiêu chí "Bắt buộc" + ≥ 80% tiêu chí còn lại) → sang trạm sau.
  - **FAIL** → sửa tối đa 2 vòng. Vòng 3 vẫn FAIL → dừng, ghi `CẦN NGƯỜI` vào `index.md`.

## 4. Ghi sổ

- Cập nhật dòng của bài trong `index.md` (trạm, trạng thái, ngày).
- Thêm 1 dòng vào `log.md`: `YYYY-MM-DD HH:MM · slug · trạm · PASS/FAIL/CẦN NGƯỜI · ghi chú ngắn`.

## 5. Dừng

- Dừng ở `08-humanized/`. **Không đăng WordPress, không gửi email/tin nhắn.**
- Báo người dùng: bài nào đã qua cổng nào, bài nào chờ duyệt, bài nào cần người.

## Chế độ chạy

| Lệnh | Ý nghĩa |
|---|---|
| `chạy dây chuyền` | Đẩy 1 bài qua 1 cổng (mặc định, an toàn) |
| `chạy dây chuyền cho <slug>` | Chỉ làm bài đó |
| `chạy hết` | Đẩy mọi bài tới khi gặp cổng người hoặc CẦN NGƯỜI |
| `bài mới: <từ khoá>` | Thêm vào hàng đợi và mở trạm 1 |
