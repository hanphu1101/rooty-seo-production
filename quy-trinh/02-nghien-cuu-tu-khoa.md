# SOP 02 · Nghiên cứu & từ khoá

**Công đoạn:** 02 · 03 · 04 · 09 · ◇10  **Skill:** `rooty-tu-khoa`  **Đầu ra lưu ở:** `nghien-cuu/`

## 02 · Phân tích đối thủ theo loại trang (T1)
Không so "cả website", mà so **từng loại trang**:

| Loại trang | Câu hỏi cần trả lời |
|---|---|
| Trang tour (4 đảo, Nam đảo, Bắc đảo, câu mực…) | Ai đang top 3? Họ có giá, lịch trình theo giờ, ảnh thật, đánh giá, FAQ, chính sách không? |
| Trang combo / khách sạn | Họ trình bày combo thế nào, có so sánh hạng phòng không? |
| Trang vé (VinWonders, cáp treo Hòn Thơm, Grand World…) | Họ có giá cập nhật, hướng dẫn đổi vé, giờ mở cửa? |
| Cẩm nang điểm đến | Độ dài, cấu trúc, có thông tin riêng không? |
| Lịch trình / chi phí | Có bảng chi phí thật không? |

Đối thủ gồm: công ty tour địa phương, OTA (Klook, Traveloka), blog du lịch lớn, báo. Ghi **khoảng trống**: thứ họ thiếu mà Rooty có (HDV bản địa, phó nháy, giá thực tế).

## 03 · Nền tảng marketing (T1)
- **Chân dung khách** (3–4 nhóm): gia đình có trẻ nhỏ · cặp đôi/trăng mật · nhóm bạn trẻ · khách đoàn công ty. Mỗi nhóm: lo lắng gì, hỏi gì, đặt qua kênh nào.
- **Hành trình đặt tour:** mơ ước (cẩm nang, điểm đẹp) → lên kế hoạch (lịch trình, chi phí, thời điểm) → so sánh (tour nào, bên nào) → đặt (giá, chính sách, đón tiễn) → sau chuyến (đánh giá, chia sẻ).
- Cập nhật `00-context/brand.md`, `giong-van.md`.

## 04 · Từ khoá → chủ đề → trang đích (T1)
**Nguyên tắc:** từ chủ đề mới xác định trang, **không làm ngược lại**.

1. **Thu thập:** Search Console (truy vấn 16 tháng), gợi ý Google, "Mọi người cũng hỏi", câu sale nhận được, công cụ từ khoá (Ahrefs/Semrush/Google Keyword Planner nếu có).
2. **Làm sạch:** bỏ trùng, bỏ không liên quan, gắn **ý định**: thông tin · điều hướng · cân nhắc · mua.
3. **Gom theo SERP:** hai từ khoá cho ra **cùng top 10** (trùng ≥ 3–4 URL) → cùng một trang. Khác SERP → khác trang.
4. **Gán trang đích:** mỗi cụm → một URL (có sẵn hoặc cần tạo). Một URL chỉ nhận một cụm chính, tránh ăn thịt từ khoá.

Bảng đầu ra `nghien-cuu/tu-khoa-chu-de.csv`:
`cum, tu_khoa_chinh, tu_khoa_phu, luong_tim, y_dinh, loai_trang, url_dich, co_san(0/1), uu_tien`

## 09 · Nhóm mở rộng — traffic sớm (T1–T2)
Từ khoá ít cạnh tranh, ý định thông tin, để site có traffic và dữ liệu sớm: "ăn gì ở Phú Quốc", "chợ đêm Phú Quốc mấy giờ mở", "đi Phú Quốc mang gì"… Dùng Search Console: truy vấn có **impressions cao, vị trí 8–30** là cơ hội nhanh nhất.

## ◇10 · Bản đồ chủ đề (chốt đầu T2) — cửa chặn
Bản thiết kế toàn bộ nội dung. Chưa chốt thì chưa viết hàng loạt.

```
Du lịch Phú Quốc (trang trụ)
├ Tour đảo ─ tour 4 đảo · 3 đảo · Hòn Thơm · Hòn Móng Tay · lặn san hô · so sánh 3 vs 4 đảo
├ Tour trong ngày ─ Bắc đảo · Nam đảo · câu mực đêm · Grand World
├ Combo & khách sạn ─ combo 3N2Đ · 4N3Đ · theo hạng sao · cho gia đình
├ Vé tham quan ─ VinWonders · cáp treo Hòn Thơm · show Kiss of the Sea · Safari
├ Điểm đến ─ Thị trấn Hoàng Hôn · Bãi Sao · Bãi Khem · Dinh Cậu · chợ đêm…
├ Lên kế hoạch ─ lịch trình 3N2Đ/4N3Đ · chi phí · thời điểm đẹp · đi lại · mang gì
├ Ẩm thực ─ đặc sản · quán ngon · hải sản
└ Thương hiệu ─ giới thiệu · đội HDV · chính sách · FAQ · đánh giá khách
```
Mỗi node: URL, loại trang, từ khoá chính, trạng thái (có sẵn tốt / cần sửa / cần viết), link lên trụ và sang node anh em.

Đầu ra: `nghien-cuu/topical-map.md`. Từ đây đẩy từng bài vào hàng đợi dây chuyền.
