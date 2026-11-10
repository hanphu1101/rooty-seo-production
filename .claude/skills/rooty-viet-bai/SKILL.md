---
name: rooty-viet-bai
description: Trạm 3 — viết bản nháp bài SEO/GEO từ dàn ý đã PASS Cổng 1, đúng giọng Rooty Trip và quy tắc viết GEO, rồi chấm Cổng 2 (21 tiêu chí). Đầu ra ở 05-drafts/<slug>/.
---

# Trạm 3 · Viết nháp

**Đầu vào:** `04-outlines/<slug>/outline.md` (đã PASS), `03-research/<slug>/nguon.md`, `00-context/giong-van.md`, `00-context/bai-mau/`.
**Đầu ra:** `05-drafts/<slug>/draft.md` + `_gate.md`.

## Trước khi viết
Đọc `00-context/giong-van.md` và ít nhất 1 bài trong `00-context/bai-mau/` để bắt giọng.

## Khi viết — làm đúng 8 việc
1. **150 từ đầu trả lời câu hỏi chính.** Câu đầu tiên đã có đáp án.
2. **Câu đầu mỗi H2 là câu trả lời 40–50 từ** theo dạng ghi trong dàn ý.
3. **Nhắc lại tên thực thể** đầu mỗi mục — không "nơi đây", "điều này", "như trên".
4. **Câu có số là câu hoàn chỉnh**: "Vé cáp treo Hòn Thơm giá 600.000 đồng/người lớn (Sun World, 11/2026)."
5. **Chỉ dùng dữ kiện trong `nguon.md`.** Thiếu → `[CẦN KIỂM CHỨNG]`, không đoán.
6. **Viết ≥ 2 đoạn chỉ Rooty có** — kinh nghiệm dẫn đoàn, mẹo, giờ đẹp, giá khách thực tế. Không có dữ liệu → ghi `[CẦN HỎI HDV: …]`.
7. **CTA tour/combo sau phần trả lời**, tự nhiên, một lần giữa bài + một lần cuối.
8. Đoạn 40–170 từ, dùng bảng/danh sách khi so sánh hoặc liệt kê.

## Tránh "mùi AI"
Không: "Hãy cùng khám phá", "không thể bỏ qua", "thiên đường", "đắm chìm", "trải nghiệm khó quên", "Tóm lại", mở bài bằng "Phú Quốc – hòn đảo ngọc…".

## Cuối bài
Thêm khối:
```
---
meta_title: (≤ 60 ký tự)
meta_description: (140–160 ký tự, chứa câu trả lời ngắn)
faq: 3–5 câu hỏi + trả lời 1–2 câu (nếu hợp)
link_noi_bo: [...]
```

Sau đó chấm `gates/cong-2-ban-nhap.md` → ghi `_gate.md`.
