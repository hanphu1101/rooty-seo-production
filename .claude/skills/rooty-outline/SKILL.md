---
name: rooty-outline
description: Trạm 2 — dựng dàn ý bài SEO/GEO từ 03-research/<slug>/, với H2 là câu hỏi thật và câu trả lời dự kiến cho mỗi mục, rồi tự chấm theo Cổng 1 (19 tiêu chí). Đầu ra ở 04-outlines/<slug>/.
---

# Trạm 2 · Dàn ý

**Đầu vào:** `03-research/<slug>/research.md`, `nguon.md`.
**Đầu ra:** `04-outlines/<slug>/outline.md` + `_gate.md`.

## Các bước

1. Viết **câu hỏi chính** bằng đúng lời khách. Một bài một câu hỏi — phủ quá rộng thì đề xuất tách.
2. Viết **H1** chứa thực thể chính.
3. Viết **đoạn mở đầu nháp 100–150 từ** trả lời thẳng câu hỏi chính (đây là đoạn AI hay trích nhất).
4. Biến từng cụm câu hỏi con thành **H2 dạng câu hỏi thật**. Thứ tự: ở đâu → có gì → giá → đi thế nào → kinh nghiệm → tour liên quan.
5. Dưới mỗi H2 ghi:
   - `Dạng:` định nghĩa / cách làm / so sánh / có-không
   - `Câu trả lời đầu (40–50 từ):` …
   - `Dữ kiện dùng:` trỏ dòng trong `nguon.md`
   - `Góc Rooty:` (nếu có)
6. Thêm **bảng dữ kiện nhanh** nếu là bài thông tin.
7. Ghi 3–8 **link nội bộ** và vị trí CTA (sau phần trả lời, không chen giữa).
8. Chấm `gates/cong-1-dan-y.md` → ghi `_gate.md`.

Cấm H2: "Tổng quan", "Giới thiệu", "Kết luận", "Lời kết".
