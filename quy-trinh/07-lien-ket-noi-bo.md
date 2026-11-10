# SOP 07 · Liên kết nội bộ

**Công đoạn:** 18 · (29)  **Skill:** `rooty-lien-ket-noi-bo`  **Khi nào:** 15–30 ngày sau nội dung + onpage, theo từng cụm

## Nguyên tắc
1. **Theo cụm chủ đề** (topical map): bài con ↔ trang trụ, bài con ↔ bài anh em liên quan.
2. **Dòng chảy về trang tiền:** bài cẩm nang → trang tour/combo/vé liên quan. Trang tour là nơi nhận nhiều link nhất.
3. **Anchor mô tả rõ**, đa dạng tự nhiên: "tour 4 đảo Nam Phú Quốc", "bảng giá vé cáp treo Hòn Thơm" — không "tại đây", "xem thêm".
4. **Link trong nội dung** mạnh hơn link ở sidebar/footer. 3–8 link/bài là vừa.
5. Không link tới URL redirect hoặc 404.
6. Độ sâu click: trang quan trọng ≤ 3 click từ trang chủ.

## Quy trình mỗi cụm
1. Chạy `python -X utf8 scripts/crawl_site.py https://rootytrip.com` → xem cột `inlinks` và `depth` của các URL trong cụm.
2. Lập bảng `nghien-cuu/lien-ket-<cum>.csv`: `tu_url, den_url, anchor, vi_tri (đoạn/câu), trang_thai`.
   - Mọi bài con → trụ (1 link).
   - Trụ → mọi bài con.
   - Bài con → 2–3 bài anh em + 1 trang tour liên quan.
3. Gắn link trên WordPress, đánh dấu xong.
4. Chạy lại crawl xác nhận: không còn trang mồ côi trong cụm, trang tour có số inlinks tăng.

## Trang mồ côi
URL có trong sitemap nhưng 0 link nội bộ trỏ tới → hoặc gắn link (nếu giữ), hoặc xử lý theo SOP 04.

## Ví dụ cụm "Tour đảo"
```
/tour-dao-phu-quoc/ (trụ)
 ├→ /tour-4-dao-phu-quoc/      ←→ /tour-3-dao-phu-quoc/
 ├→ /hon-thom-phu-quoc/        → /ve-cap-treo-hon-thom/
 ├→ /lan-ngam-san-ho-phu-quoc/ → /tour-4-dao-phu-quoc/
 └→ /nen-di-3-dao-hay-4-dao/   → cả 2 trang tour
```
(URL minh hoạ — dùng URL thật từ topical map.)
