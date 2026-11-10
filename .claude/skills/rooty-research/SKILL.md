---
name: rooty-research
description: Trạm 1 — nghiên cứu một từ khoá du lịch Phú Quốc trước khi viết: ý định tìm kiếm, câu hỏi con khách hỏi Google/ChatGPT, đối thủ top 3, AI Overview đang trả lời gì, dữ kiện có nguồn. Đầu ra ở 03-research/<slug>/.
---

# Trạm 1 · Nghiên cứu

**Đầu vào:** một từ khoá (VD "cáp treo hòn thơm") hoặc slug.
**Đầu ra:** `03-research/<slug>/` gồm `research.md` và `nguon.md`. Nếu tải trang gốc về thì lưu bản text vào `02-raw/<slug>/` (chỉ thêm, không sửa).

## Các bước

1. **Slug**: viết thường, không dấu, gạch ngang (VD `cap-treo-hon-thom`). Kiểm `index.md` xem đã có bài trùng/gần trùng chưa — nếu có, ghi đề xuất cập nhật bài cũ thay vì viết mới.
2. **Bài Rooty đã có**: tìm `site:rootytrip.com <từ khoá>`. Ghi các URL liên quan (dùng làm link nội bộ hoặc phát hiện trùng).
3. **Ý định & loại trang**: khách muốn biết gì — địa điểm, giá, cách đi, lịch trình, so sánh, hay đặt tour?
4. **Câu hỏi con** (quan trọng nhất cho GEO): gom 15–30 câu khách thật sự hỏi, từ "Mọi người cũng hỏi", gợi ý tìm kiếm, và tự hỏi: "nếu khách hỏi ChatGPT câu chính, nó sẽ tách ra những câu nhỏ nào?". Gom thành ≤ 4 cụm.
5. **Đối thủ top 3** + **AI Overview**: họ trả lời câu chính thế nào, thiếu gì, sai gì, lỗi thời gì. Chỗ thiếu = cơ hội.
6. **Dữ kiện**: giá vé, giờ mở cửa, khoảng cách, thời điểm đẹp, cách đi. Ưu tiên trang chính thức. Mỗi dữ kiện một dòng trong `nguon.md`: `dữ kiện | URL | ngày xem | mức chắc chắn (cao/vừa/thấp)`.
7. **Góc Rooty**: liệt kê thứ chỉ Rooty có cho chủ đề này (xem `00-context/brand.md`): tour liên quan, kinh nghiệm HDV, ảnh có sẵn. Thiếu thì ghi câu hỏi để hỏi team: "Cần hỏi HDV: giờ nào ít khách nhất ở …?".

## Mẫu research.md

```
# <từ khoá>
- Câu hỏi chính:
- Ý định / loại trang:
- Từ khoá phụ:
- Bài Rooty liên quan:
## Cụm câu hỏi con
### Cụm 1: …
## Đối thủ & AI Overview
## Chỗ trống có thể thắng
## Góc chỉ Rooty có
## Câu cần hỏi team
```

Không bịa. Không mở được nguồn → không ghi dữ kiện đó.
