# SOP 11 · Đo lường & báo cáo

**Công đoạn:** ◇22 (T5–T6) · ◇30 (T9) · 32 (T10) + báo cáo hằng tháng  **Skill:** `rooty-bao-cao`

## Thiết lập đo (T1 — làm trước mọi thứ)
- [ ] Search Console: đã xác minh domain property (gồm cả http/https, www).
- [ ] GA4: sự kiện chuyển đổi cho **bấm gọi, Zalo, Messenger, gửi form, đặt tour**; đánh dấu là key event.
- [ ] GA4: nhóm kênh "AI" (nguồn chatgpt.com, perplexity.ai, gemini.google.com, copilot…) để đo referral từ AI thật.
- [ ] Theo dõi thứ hạng 30–50 từ khoá chủ lực (công cụ có sẵn hoặc Search Console lọc truy vấn).
- [ ] Ghi số nền T1 vào báo cáo đầu tiên.

## Báo cáo tháng — `reports/bao-cao-<YYYY-MM>.md`
Người cập nhật số: xuất Search Console + GA4 ra CSV, bỏ vào `reports/du-lieu/<YYYY-MM>/`. Phần còn lại AI làm (`rooty-bao-cao`).

Cấu trúc:
1. **Tóm tắt 3 dòng**: tăng/giảm gì, vì sao, tháng sau làm gì.
2. **KPI** so với mục tiêu quý và tháng trước: clicks, impressions, CTR, vị trí TB, phiên organic, chuyển đổi organic, referral AI.
3. **Trang thắng / trang thua** (top 10 mỗi loại theo thay đổi clicks).
4. **Từ khoá chủ lực**: vị trí hiện tại, thay đổi.
5. **Tiến độ**: bài đã đăng, việc SEO đã xong (lấy từ bảng theo dõi), việc trễ.
6. **Nhận xét do AI viết** — chỉ ra chỉ số lệch, xu hướng 3 tháng cùng chiều ("ba tháng cùng chiều thì không còn là dao động").
7. **Việc tháng sau** (≤ 5 việc, có người làm).

Người duyệt trước khi gửi quản lý: tự kiểm 5 con số ngẫu nhiên khớp nguồn.

## Cửa ◇22 · Thứ hạng ban đầu như kỳ vọng? (T5–T6)
So vị trí trang đích với dự kiến. Đạt → tiếp tục. Không đạt → tìm nguyên nhân (nội dung chưa chín? sai ý định? kỹ thuật?) → điều chỉnh (SOP 06 · 23).

## Cửa ◇30 · Đạt chỉ tiêu Q3? (T9)
Đối chiếu KPI. Chưa đạt → review quản lý (SOP 01 · 31).

## 32 · Báo cáo kép + case study (T10)
SEO truyền thống (traffic, chuyển đổi, từ khoá) **và** kết quả AI (tỷ lệ được nhắc tên theo chủ đề × máy AI) — so với số nền tháng 1. Số đo AI dán nhãn "tham khảo xu hướng", đối chiếu referral AI trong GA4.

## Nguyên tắc báo cáo
- Mọi con số có nguồn + khoảng thời gian.
- Không tuyên bố thắng chỉ dựa vào "AI có nhắc".
- So cùng kỳ khi có mùa vụ (du lịch Phú Quốc mùa cao điểm khác hẳn mùa mưa).
