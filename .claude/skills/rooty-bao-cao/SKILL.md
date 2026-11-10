---
name: rooty-bao-cao
description: Báo cáo SEO hằng tháng và báo cáo kép cuối dự án cho Rooty Trip — đọc số Search Console + GA4 người dùng xuất ra, so với tháng trước, mục tiêu quý và số nền, viết nhận xét xu hướng, liệt kê trang thắng/thua và việc tháng sau; kiểm các cửa quyết định. Dùng khi người dùng nói "báo cáo tháng", "báo cáo SEO", "đạt KPI chưa", "báo cáo cuối".
---

# Báo cáo SEO

Làm theo `quy-trinh/11-do-luong-bao-cao.md`.

## Đầu vào (người dùng xuất, đặt vào `reports/du-lieu/<YYYY-MM>/`)
- Search Console: Hiệu suất → Trang và Truy vấn (tháng này + tháng trước, hoặc so sánh).
- GA4: phiên organic, key event theo kênh; referral từ AI (chatgpt.com, perplexity.ai, gemini…).
- (Tuỳ) dữ liệu thứ hạng, số đánh giá GBP.
Thiếu file nào → nói rõ phần nào không làm được, không đoán số.

## Các bước
1. Đọc CSV (Python thư viện chuẩn). Tính: tổng clicks, impressions, CTR, vị trí TB; % thay đổi so với tháng trước; so với mục tiêu quý trong `nghien-cuu/kpi.md`.
2. Trang thắng/thua: top 10 tăng/giảm clicks tuyệt đối.
3. Tiến độ: `GET http://localhost:8010/api/bai` và `/api/viec` nếu server chạy (bài đã đăng, việc xong/trễ).
4. Nhận xét: chỉ ra chỉ số lệch, xu hướng ≥ 3 tháng cùng chiều (đọc các báo cáo cũ trong `reports/`), lưu ý mùa vụ du lịch.
5. Việc tháng sau ≤ 5, có người làm.
6. **Tự kiểm 5 số ngẫu nhiên** khớp file nguồn — ghi kết quả kiểm ở cuối báo cáo.
7. Ghi `reports/bao-cao-<YYYY-MM>.md` — chế độ NHÁP. Không gửi đi đâu.

## Cửa quyết định
Tháng 5–6 (◇22) và tháng 9 (◇30): thêm mục "Kết luận cửa" — đạt / chưa đạt + đề xuất điều chỉnh.
