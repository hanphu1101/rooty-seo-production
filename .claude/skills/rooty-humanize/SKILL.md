---
name: rooty-humanize
description: Trạm 6 — chuốt giọng bài đã kiểm chứng cho tự nhiên, đúng giọng Rooty Trip, bỏ "mùi AI" mà không làm hỏng cấu trúc GEO; xuất bản cuối và checklist cho người duyệt (Cổng 4). Đầu ra ở 08-humanized/<slug>/.
---

# Trạm 6 · Chuốt giọng

**Đầu vào:** `06-verified/<slug>/verified.md`, `07-media-brief/<slug>/brief.md`, `00-context/giong-van.md`.
**Đầu ra:** `08-humanized/<slug>/final.md` + `_checklist-duyet.md`.

## Được sửa
- Câu cứng, câu sáo, từ lặp, nhịp đều đều kiểu AI.
- Thêm chi tiết đời thường đã có trong research (mùi chợ đêm, gió chiều Bãi Sao…) nếu đúng sự thật.
- Xưng hô, giọng theo `giong-van.md`.

## Không được sửa
- 150 từ mở đầu vẫn phải trả lời thẳng câu hỏi chính.
- Câu đầu mỗi H2 vẫn là câu trả lời.
- Không thêm dữ kiện mới (thêm thì phải quay lại trạm 4).
- Không đổi H2.

## Cuối trạm
1. Ghép vị trí ảnh từ brief vào `final.md` dạng `![alt](ten-file.jpg)`.
2. Tạo `_checklist-duyet.md` từ mẫu trong `gates/cong-4-nguoi-duyet.md`, liệt kê sẵn các `[CẦN HỎI HDV]` còn lại.
3. Cập nhật `index.md`: trạng thái `CHỜ DUYỆT`.

Dừng ở đây. Không đăng WordPress.
