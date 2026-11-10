# Rooty SEO Production

Hệ thống SEO + GEO cho rootytrip.com, dựng theo khuôn "Vibe-code AI Agents Workflow" (Vincent Do, sự kiện AI Powered Marketing & SEO 22/08/2026), Checklist GEO và Quy trình SEO 10 tháng của GTV SEO.

Gồm hai phần:
1. **Quy trình SEO toàn diện 10 tháng** — 37 công đoạn, 11 mảng (mục tiêu, từ khoá, kỹ thuật, rà soát bài cũ, nội dung, onpage, liên kết nội bộ, local SEO & đánh giá, offsite & PR, GEO, đo lường). Đọc `quy-trinh/00-tong-quan.md`.
2. **Dây chuyền nội dung** — một bài đi qua **6 trạm, 4 cổng QC**. AI làm phần nặng, người giữ cổng cuối và là người duy nhất được đăng bài.

Theo dõi cả hai trên trang web `app/` (tab **Bài viết** và **Việc SEO**), dữ liệu lưu trên Lark Base.

```
rooty-seo-production/
├ 00-context/          # brand · giọng văn · bài mẫu đạt  ← TEAM ĐIỀN TRƯỚC
├ 01-prompts/          # bộ câu hỏi đo AI · bảng theo dõi · hàng đợi từ khoá
├ 02-raw/              # nguồn gốc — chỉ thêm, không sửa
├ 03-research/         ← Trạm 1 · rooty-research
├ 04-outlines/         ← Trạm 2 · rooty-outline     · Cổng 1 (19 tiêu chí)
├ 05-drafts/           ← Trạm 3 · rooty-viet-bai    · Cổng 2 (21 tiêu chí)
├ 06-verified/         ← Trạm 4 · rooty-fact-check  · Cổng 3 (kiểm chứng)
├ 07-media-brief/      ← Trạm 5 · rooty-media-brief
├ 08-humanized/        ← Trạm 6 · rooty-humanize    · Cổng 4 (NGƯỜI duyệt)
├ gates/               # tiêu chí từng cổng
├ quy-trinh/           # SOP 11 mảng SEO + cong-doan.json (37 công đoạn)
├ nghien-cuu/          # từ khoá, topical map, content audit, offsite… (AI tạo dần)
├ reports/             # báo cáo crawl, GEO audit, báo cáo tháng
├ scripts/             # geo_audit.py · crawl_site.py — chỉ cần Python
├ app/                 # trang theo dõi (kanban bài + việc SEO), lưu Lark Base
├ mau/                 # trang bài mẫu chuẩn GEO
├ .claude/skills/      # 18 skill gọi bằng /tên
├ CLAUDE.md            # luật chơi — AI đọc đầu tiên
├ ORCHESTRATOR.md      # quản đốc
└ index.md · log.md    # sổ theo dõi
```

## Bắt đầu (lần đầu)

1. Mở thư mục này trong Claude Code (desktop app → chọn folder, hoặc `claude` trong terminal tại đây).
2. Điền các chỗ ✏️ trong `00-context/brand.md` và chỉnh `00-context/giong-van.md`.
3. Bỏ 2–3 bài hay nhất vào `00-context/bai-mau/`.
4. Gõ một trong các lệnh dưới.

## Trang làm SEO trên web (lưu Lark Base)

```bash
python -X utf8 app/server.py
```
Mở http://localhost:8010: 12 tab theo 10 bước SEO (Khách hàng → Từ khoá → Cụm & silo → Đối thủ → Audit → Content → Onpage → Entity → Link building → Đánh giá) + Tổng quan + Kế hoạch 10 tháng. Mỗi tab có hướng dẫn chi tiết và bảng dữ liệu riêng. Cách nối Lark Base: xem `app/README.md`.

## Lệnh hằng ngày

| Gõ trong Claude Code | Việc |
|---|---|
| `bài mới: tour 4 đảo phú quốc` | Thêm từ khoá và mở trạm 1 |
| `chạy dây chuyền` | Đẩy 1 bài qua 1 cổng |
| `chạy hết` | Đẩy mọi bài tới cổng người |
| `/rooty-ke-hoach-seo tháng này làm gì` | Xem việc SEO đến hạn, trễ, cửa sắp tới |
| `/rooty-tu-khoa` | Nghiên cứu từ khoá, đối thủ, topical map |
| `/rooty-ky-thuat` | Crawl + lỗi kỹ thuật cần dev sửa |
| `/rooty-content-audit` | Rà soát bài cũ: giữ/cập nhật/gộp/xoá |
| `/rooty-onpage <url>` | Chấm onpage + bản sửa sẵn để dán |
| `/rooty-lien-ket-noi-bo` | Kế hoạch link nội bộ theo cụm |
| `/rooty-local-seo` | Google Business Profile, đánh giá, NAP |
| `/rooty-offsite` | Offsite, PR, có nên mua link không |
| `/rooty-bao-cao` | Báo cáo SEO tháng |
| `/rooty-geo-audit` | Audit GEO website hằng tháng |
| `/rooty-do-hien-dien-ai` | Đo ChatGPT/Gemini có nhắc Rooty không |
| `/rooty-chan-doan` | Chẩn đoán rớt top: GSC + thuật toán + quét toàn blog 8 loại lỗi, nhãn ĐÃ KIỂM / NGHI VẤN |

Chạy riêng script audit:
```bash
python -X utf8 scripts/geo_audit.py https://rootytrip.com --max-pages 30
```

## Audit đầu tiên — 08/11/2026 (15 trang)

- ✅ robots.txt mở cho mọi bot AI (cả bot tìm nguồn lẫn bot huấn luyện).
- ✅ Tốc độ máy chủ tốt (phần lớn < 200ms), canonical tự trỏ, có schema BlogPosting/Person/Organization, có tác giả và ngày cập nhật.
- ❌ **14/15 trang**: khối "chuyên mục · Tác giả · Ngày đăng · Lượt xem" nằm giữa H1 và đoạn mở đầu → AI đọc 400 ký tự đầu sẽ gặp rác trước câu trả lời. Sửa giao diện: chuyển khối này xuống dưới đoạn đầu hoặc ra ngoài main content. **Một lần sửa theme, lợi cho mọi bài.**
- ❌ **11/15 trang**: ít H2 dạng câu hỏi (< 30%). Khi cập nhật bài cũ, đổi H2 thành câu khách hỏi.
- ❌ 2/15 trang JSON-LD lỗi cú pháp (VD bài Dinh Cậu) — schema hỏng thì Google bỏ qua.
- ❌ Trang chủ 152/405 ảnh thiếu alt.

Chi tiết: `reports/geo-audit-rootytrip.com-2026-11-08.md`.

## An toàn
- AI không tự đăng WordPress, không gửi email/tin nhắn.
- Không lưu API key, mật khẩu trong thư mục này.
- Số liệu đo AI chỉ để xem xu hướng; đối chiếu GA4 trước khi báo cáo thắng.
