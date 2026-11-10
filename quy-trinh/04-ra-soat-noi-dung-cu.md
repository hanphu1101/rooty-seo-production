# SOP 04 · Rà soát nội dung cũ (content audit)

**Công đoạn:** ◇06 · 07  **Skill:** `rooty-content-audit`  **Hạn:** xong trong 3 tháng đầu

Rooty đã có nhiều bài (từ 2020) → bắt buộc làm. Bài cũ yếu, trùng chủ đề kéo cả site xuống và làm Google/AI phân vân không biết trang nào là trang chính.

## Bước 1 · Kiểm kê
`scripts/crawl_site.py` → `reports/crawl-<ngày>.csv`. Ghép thêm dữ liệu Search Console 12 tháng (Hiệu suất → Trang → Xuất): clicks, impressions, vị trí trung bình.

## Bước 2 · Gán hành động cho từng URL

| Hành động | Khi nào | Làm gì |
|---|---|---|
| **Giữ** | Có traffic tốt, nội dung còn đúng | Không đụng, chỉ thêm link nội bộ |
| **Cập nhật** | Có impressions nhưng vị trí 8–30; hoặc thông tin cũ (giá, lịch, năm) | Đưa vào dây chuyền ở trạm 1 với cờ "cập nhật" |
| **Gộp** | 2+ bài cùng chủ đề/cùng SERP (ăn thịt từ khoá) | Chọn 1 bài mạnh nhất làm chính, chuyển nội dung tốt sang, 301 bài kia về |
| **Xoá + 301** | Không traffic, không link, có trang thay thế liên quan | 301 về trang gần nghĩa nhất |
| **Xoá (410)** | Không traffic, không liên quan (tin cũ hết hạn, nội dung ngoài ngành) | 410 hoặc noindex |
| **Noindex** | Cần giữ cho người dùng nhưng mỏng (tag, lưu trữ) | noindex, follow |

Quy tắc nhanh:
- 12 tháng **0 click và < 100 impressions** + nội dung mỏng → ứng viên xoá/gộp.
- **Ngoài chủ đề** du lịch Phú Quốc/Kiên Giang/miền Tây (VD tin vé máy bay đi Ấn Độ) → cân nhắc xoá hoặc noindex; giữ nếu có traffic và liên quan khách của Rooty.
- **Ăn thịt từ khoá:** Search Console → một truy vấn có 2+ trang Rooty thay nhau hiện → gộp.

Đầu ra: `nghien-cuu/content-audit.csv` thêm cột `hanh_dong, url_dich_301, ly_do, uu_tien, trang_thai`.

## Bước 3 · Thực hiện (theo đợt, mỗi đợt ≤ 30 URL)
1. Redirect 301 làm bằng plugin (Rank Math/Redirection) hoặc server — **ghi lại mọi redirect**.
2. Sửa link nội bộ đang trỏ vào URL bị xoá/gộp (để không qua redirect).
3. Cập nhật sitemap.
4. Theo dõi Search Console 2–4 tuần sau mỗi đợt.

## Cửa ◇06
Website đã có nội dung? Rooty: **có** → làm công đoạn 07. Ghi quyết định vào tab Việc SEO.
