# Rooty SEO Production — luật chơi

Đây là dây chuyền sản xuất nội dung SEO + GEO cho **Rooty Trip** (rootytrip.com — tour, combo nghỉ dưỡng, vé tham quan Phú Quốc). Mục tiêu kép: bài lên top Google **và** được ChatGPT, Gemini, Google AI Overview, Perplexity nhắc tên Rooty Trip khi khách hỏi về du lịch Phú Quốc.

Đọc file này trước mọi việc. Sau đó đọc `ORCHESTRATOR.md` để biết bài đang ở trạm nào.

Ngoài nội dung, toàn bộ quy trình SEO 10 tháng (kỹ thuật, từ khoá, onpage, liên kết nội bộ, local SEO, offsite, đo lường…) nằm ở `quy-trinh/` — mỗi mảng một SOP và một skill `rooty-*`. Việc gì không nằm trong dây chuyền bài viết → tìm SOP của mảng đó trước khi làm.

## Nguyên tắc không được phá

1. **Một bài = một thư mục slug**, đi qua các trạm theo thứ tự. Không nhảy trạm, không sửa file ở trạm trước — muốn sửa thì trả bài về trạm đó và ghi lý do vào `log.md`.
2. **`02-raw/` là bất biến.** Chỉ thêm, không sửa, không xoá. Đây là nguồn gốc mọi dữ kiện.
3. **Chưa PASS cổng thì chưa đi tiếp.** Mỗi cổng có file tiêu chí trong `gates/`. Ghi kết quả chấm (PASS/FAIL từng tiêu chí + lý do) vào file `_gate.md` trong thư mục bài.
4. **Không bịa dữ kiện.** Giá vé, giờ mở cửa, khoảng cách, tên đơn vị phải có nguồn trong `02-raw/` hoặc `03-research/` kèm ngày lấy. Chưa có nguồn → ghi `[CẦN KIỂM CHỨNG]`, không đoán.
5. **Không tự đăng, không tự gửi gì ra ngoài.** Dây chuyền dừng ở `08-humanized/`. Người duyệt (cổng 4) mới được đăng lên WordPress.
6. **Mỗi lần người sửa bài của AI → thêm một dòng luật** vào mục "Luật học được" cuối file này, để lần sau không lặp lại lỗi đó.

## Bản đồ trạm

| Trạm | Thư mục | Skill | Cổng ra |
|---|---|---|---|
| 0 | `00-context/` | (người cập nhật) | — |
| 1 · Nghiên cứu | `03-research/<slug>/` | `rooty-research` | — |
| 2 · Dàn ý | `04-outlines/<slug>/` | `rooty-outline` | Cổng 1 · `gates/cong-1-dan-y.md` |
| 3 · Viết nháp | `05-drafts/<slug>/` | `rooty-viet-bai` | Cổng 2 · `gates/cong-2-ban-nhap.md` |
| 4 · Kiểm chứng | `06-verified/<slug>/` | `rooty-fact-check` | Cổng 3 · `gates/cong-3-kiem-chung.md` |
| 5 · Brief hình ảnh | `07-media-brief/<slug>/` | `rooty-media-brief` | — |
| 6 · Chuốt giọng | `08-humanized/<slug>/` | `rooty-humanize` | Cổng 4 · `gates/cong-4-nguoi-duyet.md` (NGƯỜI) |

Ngoài dây chuyền bài viết còn ba việc thường dùng:
- `rooty-geo-audit` — chạy `scripts/geo_audit.py` + kiểm tay, ra báo cáo trong `reports/`.
- `rooty-do-hien-dien-ai` — đo Rooty Trip có được AI nhắc tên không, ghi vào `01-prompts/theo-doi-hien-dien.csv`.
- `rooty-chan-doan` — khi web rớt top: GSC → đối chiếu cập nhật thuật toán → quét toàn blog 8 loại lỗi → thứ tự sửa; mọi kết luận gắn nhãn ĐÃ KIỂM / NGHI VẤN.

## Quy tắc viết GEO (áp cho mọi bài — tóm từ Checklist GEO của GTV)

- **Mở đầu = câu trả lời.** 100–150 từ đầu sau H1 trả lời thẳng câu hỏi chính. Không mở bằng "Phú Quốc là hòn đảo xinh đẹp…".
- **H2 = câu hỏi thật** khách gõ vào Google/ChatGPT ("Địa Trung Hải Phú Quốc nằm ở đâu?", "Vé cáp treo Hòn Thơm bao nhiêu tiền?"). Cấm H2 rỗng nghĩa: "Tổng quan", "Giới thiệu", "Kết luận".
- **Câu đầu sau mỗi H2 = câu trả lời 40–50 từ**, theo loại: định nghĩa → "X là…" · cách làm → "Để X, làm N bước…" · so sánh → kết luận trước · có/không → trả lời ngay rồi mới nêu điều kiện.
- **Mỗi đoạn tự đứng được.** Cắt rời một H2 vẫn hiểu: có tên địa điểm + bối cảnh + dữ kiện. Không dùng "điều này", "như đã nói ở trên".
- **Dữ kiện dạng câu hoàn chỉnh**, trích được: "Cáp treo Hòn Thơm dài 7.899,9 m, đi hết khoảng 15 phút." chứ không phải "7.899,9m".
- **Có thứ chỉ Rooty mới có**: kinh nghiệm hướng dẫn viên bản địa, ảnh tự chụp, giờ đẹp để check-in, mẹo né đông, giá thực tế khách đã đi. Bài mà tóm tắt top 10 Google là ra được → làm lại.
- **Số liệu kèm nguồn + tháng/năm.** Bài giá/so sánh cập nhật thật mỗi ~30 ngày. Cấm chỉ đổi năm trên tiêu đề.
- **Tác giả thật**, kinh nghiệm nằm trong nội dung ("Khi dẫn đoàn tháng 6…"), không chỉ ở box tác giả.
- **Không xếp Rooty #1** trong bài liệt kê nếu không có cách chấm công khai.

## 5 điều không hứa (nói rõ với sếp/khách)

Không bán llms.txt như đòn bẩy · không coi schema là cách được trích dẫn · không hứa AI trả lời y hệt mỗi lần · không trích dẫn tên/nguồn bịa · không nhồi "chính chủ".

## Luật học được

<!-- Mỗi lần người sửa bài, thêm 1 dòng: ngày · lỗi · luật mới. Ví dụ:
- 2026-11-10 · AI viết giá vé VinWonders cũ · Luôn lấy giá từ trang chính thức, ghi ngày lấy, không dùng giá trong bài cũ của Rooty. -->
- 2026-11-08 · Audit thấy khối "Tác giả · Ngày đăng · Lượt xem" chen giữa H1 và đoạn mở đầu ở 14/15 trang · Khi đề xuất sửa giao diện, đưa khối meta xuống dưới đoạn mở đầu hoặc ra ngoài thẻ main content.
