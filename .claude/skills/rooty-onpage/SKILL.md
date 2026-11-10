---
name: rooty-onpage
description: Tối ưu onpage cho một hoặc nhiều URL rootytrip.com — chấm theo checklist onpage (title, meta, H1, đoạn mở, H2, ảnh, schema, nút đặt tour), đề xuất bản sửa cụ thể, và điều chỉnh bài đang ở top 10–30 dựa trên Search Console. Dùng khi người dùng nói "onpage", "tối ưu trang", "sửa title meta", "bài rớt hạng", "bài top 10-30".
---

# Onpage

Làm theo `quy-trinh/06-onpage.md`.

## Chấm một URL
1. Tải trang (WebFetch hoặc `scripts/geo_audit.py --urls <url>`).
2. Chấm từng mục checklist trong SOP: ✅ / ❌ + lý do.
3. Với mỗi ❌, viết **bản sửa sẵn để dán**: title mới, meta mới, đoạn mở 100–150 từ mới, H2 mới, alt ảnh, JSON-LD (chỉ dùng dữ kiện có trên trang).
4. Ghi `reports/onpage/<slug>-<ngày>.md`.

## Trang tour/combo/vé
Thêm kiểm: bảng thông tin nhanh, giá từ, bao gồm/không bao gồm, chính sách huỷ, đánh giá thật, FAQ, nút đặt trên di động, schema Product/TouristTrip + Offer khớp giá hiển thị. So với mẫu trang tour ở SOP 03 · công đoạn 11.

## Điều chỉnh bài top 10–30 (23)
Cần file Search Console (Truy vấn × Trang). Lọc vị trí 8–30, impressions cao. Với từng URL: so top 3 hiện tại → quyết định sửa nhẹ / bổ sung / viết lại theo SOP. CTR thấp ở vị trí tốt → title/meta trước. Bổ sung/viết lại → đưa vào dây chuyền nội dung.

Không tự sửa trên WordPress. Người dùng dán bản sửa.
