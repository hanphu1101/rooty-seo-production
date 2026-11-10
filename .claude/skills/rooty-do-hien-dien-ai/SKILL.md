---
name: rooty-do-hien-dien-ai
description: Đo mức hiện diện của Rooty Trip trên AI (ChatGPT, Gemini, Google AI Overview, Perplexity) bằng bộ câu hỏi cố định trong 01-prompts/bo-cau-hoi-ai.csv — mỗi câu chạy nhiều lần, ghi có được nhắc tên/trích link không, AI nói đúng hay sai về Rooty, đối thủ nào xuất hiện. Dùng khi người dùng nói "đo AI", "đo hiện diện", "ChatGPT có nhắc Rooty không".
---

# Đo hiện diện trên AI

## Nguyên tắc (từ Checklist GEO việc #3, #30–#32)
- **Bộ câu hỏi cố định** trong `01-prompts/bo-cau-hoi-ai.csv` — không đổi giữa các lần đo, nếu thêm câu thì ghi ngày thêm.
- **Mỗi câu chạy ≥ 3 lần** mỗi máy AI (chuẩn 5), báo **tỷ lệ**, không báo kết quả 1 lần. AI trả lời khác nhau mỗi lần.
- **Ghi ngày chạy, tên máy AI, phiên bản model** cho mọi dòng.
- **Báo cáo theo chủ đề**, không theo từng câu.
- Số đo AI chỉ để **tham khảo xu hướng**; đối chiếu lượt truy cập thật từ chatgpt.com, perplexity.ai, gemini… trong GA4 trước khi kết luận thắng.

## Cách chạy
Claude không tự đăng nhập ChatGPT/Gemini của người dùng. Hai cách:
1. **Người dùng tự hỏi** (khuyên dùng lúc đầu): Claude in ra danh sách câu hỏi; người dùng hỏi trong chế độ ẩn danh, dán câu trả lời vào `02-raw/ai-answers/<ngày>/<máy-AI>-<id>-<lần>.md`. Claude đọc và chấm.
2. **Qua API** (khi đã có key, người dùng tự cấu hình): viết script trong `scripts/` gọi API có bật tìm kiếm web, lưu câu trả lời thô vào `02-raw/ai-answers/`. Không ghi key vào file trong thư mục này.

## Chấm mỗi câu trả lời → 1 dòng trong `01-prompts/theo-doi-hien-dien.csv`
`ngay, may_ai, model, id_cau, lan, nhac_ten_rooty (0/1), trich_link_rooty (0/1), url_duoc_trich, thong_tin_dung (dung/sai/khong_noi), loi_sai, doi_thu_xuat_hien`

## Báo cáo `reports/hien-dien-ai-<ngày>.md`
- Tỷ lệ được nhắc tên theo **chủ đề × máy AI** (bảng).
- So với lần trước.
- **AI nói sai gì về Rooty** → việc sửa (trang sự thật, thông tin nhất quán).
- **Đối thủ hay xuất hiện** và trang nào của họ được trích → gợi ý bài cần viết/cập nhật (đưa vào `hang-doi-tu-khoa.md`).
- **URL AI bịa** trên rootytrip.com → ứng viên tạo trang hoặc redirect.
