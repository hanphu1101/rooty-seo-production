---
name: rooty-ke-hoach-seo
description: Quản lý dự án SEO 10 tháng của Rooty Trip — xem đang ở tháng/pha nào, việc SEO nào đến hạn hoặc trễ, đặt KPI, lập kế hoạch traffic, chuẩn bị review quý và bộ bàn giao. Dùng khi người dùng hỏi "tháng này làm gì", "dự án SEO đang ở đâu", "đặt KPI", "kế hoạch traffic", "review quý", "bàn giao".
---

# Kế hoạch & quản lý dự án SEO

Đọc trước: `quy-trinh/00-tong-quan.md`, `quy-trinh/01-quan-ly-muc-tieu.md`, `quy-trinh/cong-doan.json`.

## "Tháng này làm gì?"
1. Lấy trạng thái việc SEO: nếu server trang theo dõi đang chạy, gọi `GET http://localhost:8010/api/viec`; nếu không, đọc `cong-doan.json`.
2. Xác định tháng hiện tại của dự án (T1…T10) từ `PROJECT_START` trong `.env` (mặc định tháng đầu tiên có việc "Đang làm").
3. Liệt kê: việc **trễ** (đã qua tháng `den`, chưa Xong) · việc **đến hạn tháng này** · **cửa ◇** sắp tới cần quyết định · việc tháng sau cần chuẩn bị.
4. Nhắc 3 nguyên tắc: nội dung cần ~100 ngày · dây chuyền nội dung → onpage (+10–15 ngày) → link nội bộ (+15–30 ngày) · chưa top thì AI chưa chọn.

## Đặt KPI (công đoạn 01)
Cần số nền. Hỏi người dùng xuất Search Console + GA4 3 tháng gần nhất vào `reports/du-lieu/`. Đề xuất KPI theo quý theo bảng trong SOP 01, ghi vào `nghien-cuu/kpi.md`. Kiểm GA4 đã có sự kiện chuyển đổi chưa.

## Kế hoạch traffic (công đoạn 17)
Từ `nghien-cuu/tu-khoa-chu-de.csv`: traffic dự kiến = lượng tìm × CTR theo vị trí mục tiêu (vị trí 1 ≈ 25–30%, 3 ≈ 10%, 5 ≈ 5–6%, 10 ≈ 2%; đây là ước lượng, ghi rõ). Tổng phải vượt mục tiêu ≥ 20%; thiếu → đề xuất chủ đề bổ sung.

## Review quý / bàn giao (31, 33)
Tổng hợp từ báo cáo tháng (`reports/bao-cao-*.md`) + bảng theo dõi. Bàn giao theo checklist SOP 01.

Không tự đổi trạng thái việc trên bảng theo dõi trừ khi người dùng bảo.
