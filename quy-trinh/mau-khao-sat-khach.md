# Bộ công cụ thu thập dữ liệu khách hàng — Rooty Trip

Dùng cho **Bước 1 · Chân dung khách hàng & hành trình mua hàng**. Mục tiêu: thay "giả định" bằng dữ liệu thật. Kết quả ghi vào tab B1 trên trang theo dõi (bảng Nguồn dữ liệu → Phát hiện chính, rồi cập nhật Chân dung và Hành trình).

Nguyên tắc: **ẩn tên, số điện thoại** trước khi lưu hay dán cho AI. Không hỏi thông tin nhạy cảm không cần thiết.

---

## A. Phỏng vấn sale / CSKH (30 phút/người, 2–3 người)

1. Khách nhắn hỏi nhiều nhất là nhóm nào? (gia đình, cặp đôi, nhóm bạn, đoàn công ty, khách lớn tuổi, khách nước ngoài…) Ước lượng mỗi nhóm bao nhiêu %?
2. Câu **đầu tiên** khách hay nhắn là gì? Kể 5 câu nguyên văn bạn nhớ.
3. Khách thường hỏi gì **trước khi chốt**? Câu nào hỏi đi hỏi lại?
4. Lý do phổ biến nhất khách **chốt** với Rooty? Lý do khách **không chốt** hoặc im lặng?
5. Khách hay so sánh Rooty với bên nào? So sánh về điểm gì (giá, lịch trình, đánh giá)?
6. Khách biết đến Rooty từ đâu? (Google, TikTok, Facebook, bạn bè, OTA…)
7. Khách đặt trước ngày đi bao lâu? Đặt cho bao nhiêu người? Ngân sách thường nói ra là bao nhiêu?
8. Khách chê/phàn nàn gì nhất — trước, trong và sau tour?
9. Sản phẩm nào bán chạy nhất với từng nhóm khách?
10. Nếu được sửa một điều trên website để khách dễ đặt hơn, bạn sửa gì?

## B. Khảo sát khách sau tour (Google Form, ≤ 3 phút, gửi qua Zalo 24h sau tour)

**Về bạn**
1. Bạn đi cùng ai? ☐ Gia đình có trẻ nhỏ ☐ Gia đình không có trẻ nhỏ ☐ Người yêu/vợ chồng ☐ Bạn bè ☐ Đồng nghiệp/công ty ☐ Một mình
2. Độ tuổi của bạn? ☐ < 25 ☐ 25–34 ☐ 35–44 ☐ 45–54 ☐ ≥ 55
3. Bạn đến từ tỉnh/thành nào?
4. Nghề nghiệp? (tuỳ chọn)

**Lên kế hoạch**
5. Điều gì khiến bạn chọn Phú Quốc cho chuyến đi này?
6. Bạn tìm thông tin về chuyến đi ở đâu? (chọn nhiều) ☐ Google ☐ TikTok ☐ Facebook/nhóm du lịch ☐ YouTube ☐ Instagram ☐ ChatGPT/AI ☐ Bạn bè giới thiệu ☐ Klook/Traveloka ☐ Khác
7. Bạn biết đến Rooty Trip từ đâu?
8. Trước khi đặt, bạn lo lắng điều gì nhất? (chọn nhiều) ☐ Giá ☐ Chất lượng tour ☐ An toàn ☐ Say sóng/thời tiết ☐ Phù hợp với trẻ em/người lớn tuổi ☐ Uy tín công ty ☐ Đón tiễn ☐ Khác
9. Bạn đã so sánh với bao nhiêu công ty khác? ☐ 0 ☐ 1–2 ☐ 3–5 ☐ > 5
10. Điều gì khiến bạn quyết định đặt với Rooty?
11. Bạn đặt trước ngày đi bao lâu? ☐ < 1 tuần ☐ 1–2 tuần ☐ 2–4 tuần ☐ 1–2 tháng ☐ > 2 tháng
12. Ngân sách cả chuyến (mỗi người, không tính vé máy bay)? ☐ < 3 triệu ☐ 3–5 ☐ 5–10 ☐ > 10 triệu

**Trải nghiệm**
13. Chấm điểm chuyến đi (1–10). Bạn có giới thiệu Rooty cho bạn bè không? (0–10)
14. Khoảnh khắc bạn thích nhất? Điều gì làm bạn chưa hài lòng?
15. Lần tới bạn muốn đi đâu / trải nghiệm gì?

## C. Đọc đánh giá & tin nhắn — phiếu ghi

Mỗi đánh giá/hội thoại ghi 1 dòng:

| Nguồn | Nhóm khách | Giai đoạn hành trình | Khen | Chê / lo lắng | Câu hỏi nguyên văn | Tour |
|---|---|---|---|---|---|---|

Đủ 50–100 dòng thì đếm: lo lắng nào lặp nhiều nhất, câu hỏi nào lặp nhiều nhất → đó là **điểm đau** và **câu hỏi hay hỏi** của chân dung, và là chủ đề nội dung cần viết.

Có thể dán bảng này (đã ẩn tên) cho Claude: `/rooty-tu-khoa tổng hợp chân dung khách và hành trình từ bảng dữ liệu này`.

## D. Dữ liệu đặt tour — cách tính nhanh

Xuất 12 tháng booking (bỏ tên, SĐT): ngày đặt · ngày đi · số người lớn · trẻ em · sản phẩm · giá trị · kênh đến.
- **Tỷ trọng nhóm khách** = số booking có trẻ em / 2 người / ≥ 5 người / có VAT…
- **Đặt trước bao lâu** = trung vị (ngày đi − ngày đặt) theo nhóm.
- **Mùa cao điểm** = số booking theo tháng đi.
- **Giá trị trung bình** theo nhóm.

## E. Khi nào chân dung được "Đã xác nhận"
- Có ≥ 2 nguồn dữ liệu khác loại cùng ủng hộ (VD: dữ liệu đặt tour + phỏng vấn sale).
- Tỷ trọng khách có số từ dữ liệu đặt tour, không phải ước đoán.
- Sale và ít nhất 1 HDV đọc và đồng ý.
