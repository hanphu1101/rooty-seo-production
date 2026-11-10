---
name: rooty-chay-day-chuyen
description: Quản đốc dây chuyền Rooty SEO Production — đọc index.md và log.md, chọn bài cần làm, gọi đúng skill của trạm, chấm cổng QC, ghi sổ. Dùng khi người dùng nói "chạy dây chuyền", "chạy hết", "bài mới: <từ khoá>", hoặc hỏi bài nào đang ở đâu.
---

# Chạy dây chuyền

1. Đọc `CLAUDE.md` rồi `ORCHESTRATOR.md` — làm đúng 5 bước trong ORCHESTRATOR.
2. Đọc `index.md` và 20 dòng cuối `log.md`.
3. Chọn việc theo ưu tiên: bài bị trả về → bài dở ở trạm thấp nhất → từ khoá mới trong `01-prompts/hang-doi-tu-khoa.md`.
4. Gọi skill của trạm:
   - Trạm 1 → `rooty-research`
   - Trạm 2 → `rooty-outline` → chấm `gates/cong-1-dan-y.md`
   - Trạm 3 → `rooty-viet-bai` → chấm `gates/cong-2-ban-nhap.md`
   - Trạm 4 → `rooty-fact-check` → chấm `gates/cong-3-kiem-chung.md`
   - Trạm 5 → `rooty-media-brief`
   - Trạm 6 → `rooty-humanize` → chuẩn bị `gates/cong-4-nguoi-duyet.md`
5. Khi chấm cổng, dùng một subagent **chưa đọc bài trước đó** làm giám khảo (đưa nó file tiêu chí + bài, không đưa kết luận của mình) để tránh tự chấm dễ dãi.
6. FAIL → sửa tối đa 2 vòng; vòng 3 vẫn FAIL → ghi `CẦN NGƯỜI`.
7. Cập nhật `index.md`, thêm dòng vào `log.md`.
8. Dừng ở trạm 6. Không đăng, không gửi gì ra ngoài. Báo người dùng ngắn gọn: bài nào qua cổng nào, bài nào chờ duyệt.

Mặc định mỗi lần chạy chỉ đẩy 1 bài qua 1 cổng. Chỉ chạy nhiều khi người dùng nói "chạy hết".
