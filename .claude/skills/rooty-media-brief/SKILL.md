---
name: rooty-media-brief
description: Trạm 5 — lập brief hình ảnh cho bài đã kiểm chứng: ảnh đầu trang trả đúng ý định, ảnh từng mục, alt text, bảng/biểu đồ tự làm, và kiểm tra bố cục hiển thị (Blur Test). Đầu ra ở 07-media-brief/<slug>/.
---

# Trạm 5 · Brief hình ảnh

**Đầu vào:** `06-verified/<slug>/verified.md`.
**Đầu ra:** `07-media-brief/<slug>/brief.md`.

## Nội dung brief
1. **Ảnh đầu trang (trên màn hình đầu tiên)**: phải cho thấy ngay chủ đề + chức năng trang. VD bài giá vé → ảnh có bảng giá hoặc quầy vé, không phải ảnh biển chung chung.
2. **Ảnh từng H2**: mô tả cảnh cần chụp/chọn, ưu tiên **ảnh Rooty tự chụp** (khách, HDV, góc đẹp). Ghi rõ "cần chụp mới" nếu kho không có.
3. **Alt text** cho từng ảnh: mô tả cụ thể, có tên địa điểm, không nhồi từ khoá. VD `Cầu Hôn ở Thị trấn Hoàng Hôn Phú Quốc lúc 17h30`.
4. **Tên file** dạng không dấu: `cau-hon-thi-tran-hoang-hon-phu-quoc.jpg`, nén ≤ 200KB, WebP nếu được.
5. **Bảng/biểu đồ tự làm** (bảng giá, bản đồ lộ trình, so sánh) — đây là "thông tin chỉ Rooty có".
6. **Kiểm bố cục (5 điểm)**: ảnh đầu trang đúng ý định · thứ bậc hình ảnh khớp H2 · thứ tự hiển thị = thứ tự HTML · thông tin quan trọng không giấu trong tab/accordion · không popup/quảng cáo chen nội dung chính.
7. **Blur Test**: nếu chụp màn hình rồi làm mờ 50%, vẫn nhận ra trang nói về gì và để làm gì không?
