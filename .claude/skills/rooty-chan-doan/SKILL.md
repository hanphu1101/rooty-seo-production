---
name: rooty-chan-doan
description: Chẩn đoán vì sao rootytrip.com (hoặc một website WordPress khác) rớt top — một câu là chạy đủ 4 bước: GSC tìm ngày rớt, đối chiếu đợt cập nhật thuật toán chính thức của Google, quét toàn bộ bài blog tìm 8 loại lỗi nội dung (đổi năm giả, thiếu trải nghiệm, lạc chủ đề, trùng từ khoá, chèn thương mại, đa ngôn ngữ/mỏng, link tự thân, tác giả) kèm GEO + chính sách spam, rồi xếp thứ tự sửa. Mọi kết luận gắn nhãn ĐÃ KIỂM / NGHI VẤN. Dùng khi người dùng nói "rớt top", "tụt hạng", "mất traffic", "tìm lý do rớt", "chẩn đoán", "source context", "vì sao blog không lên".
---

# Chẩn đoán rớt top

Nguyên tắc: **không kết luận nguyên nhân khi chưa có số liệu**. Lỗi đang có ≠ lý do rớt. Mọi câu trong báo cáo gắn nhãn
**[ĐÃ KIỂM]** (đo được, có số) hoặc **[NGHI VẤN]** (suy luận — phải đọc lại trang trước khi khẳng định). Không bịa số.

## 1. Chạy chẩn đoán tự động (app)
App ở `app/server.py` (cổng 8010). Kiểm app có chạy không: `curl -s http://localhost:8010/api/config`.
- Chưa chạy → chạy nền: `python -X utf8 app/server.py` (đợi ~5 giây).
- Bắt đầu: `curl -s -X POST http://localhost:8010/api/chandoan/run -H "Content-Type: application/json" -d "{\"site\":\"\"}"`
  (để trống = SITE_URL trong `.env`; website khác thì ghi tên miền — chỉ ra báo cáo, không nạp bảng sửa lỗi).
- Theo dõi: `curl -s http://localhost:8010/api/job/chandoan` mỗi ~20 giây tới khi `running` = false (2–3 phút).
- Đọc báo cáo: `curl -s http://localhost:8010/api/chandoan/last` → trường `md`; file đầy đủ ở `reports/chan-doan-rot-top-<host>-<ngày>.md`.

Không mở được app → chạy thẳng bộ quét (bước ③ không có GSC):
```bash
cd app && python -X utf8 -c "import blogscan as B, json; i,o,s=B.scan('https://rootytrip.com'); print(json.dumps(s, ensure_ascii=False)); json.dump(i, open('../reports/du-lieu/blogscan.json','w',encoding='utf-8'), ensure_ascii=False)"
```

## 2. Đọc lại phần NGHI VẤN (việc của bạn, máy không làm được)
Với 3 loại NGHI VẤN đứng đầu bảng ③: mở 3–5 bài mỗi loại (danh sách trong `/api/t/sualoi`, lọc «Loại lỗi», hoặc tab B5 · Sửa lỗi từng trang) và đọc:
- **Thiếu trải nghiệm**: có đoạn nào chỉ Rooty viết được (HDV kể, giá khách thực trả, mẹo, ảnh tự chụp)? Có → «Không phải lỗi».
- **Lạc chủ đề**: bài có thật sự ngoài Phú Quốc không, hay chỉ tiêu đề không ghi?
- **Trùng từ khoá**: các bài trong cụm có cùng trả lời một câu hỏi không? Có số liệu GSC Truy vấn × Trang (B10 · Xung đột từ khoá) thì dùng — đó mới là bằng chứng.
- **Thương mại**: đọc thấy bán hàng gượng không?
Ghi kết luận từng loại: «xác nhận x/y bài».

## 3. Trả lời người dùng (tiếng Việt, ngắn, có cấu trúc)
1. **Có rớt thật không, từ ngày nào** — [ĐÃ KIỂM] nếu có GSC; nếu chưa có thì nói thẳng và hướng dẫn xuất GSC file Ngày 6 tháng → nhập ở tab B10.
2. **Trùng đợt cập nhật nào** của Google (tên, ngày) → nghĩa là nên ưu tiên nhóm lỗi nào (spam update → thao túng; core update → chất lượng; không trùng → kỹ thuật / đối thủ / mùa vụ).
3. **Bảng lỗi** theo thứ tự ưu tiên: loại lỗi · số bài · nhãn · vì sao ảnh hưởng · kết quả bạn đọc lại ở bước 2.
4. **Việc sửa** top 3–6, chỉ chỗ «Cần sửa gì» ở tab B5; nhắc quy trình đo trước/sau (đổi «Đã sửa» → sau 4 tuần nhập GSC → «Đo hiệu quả»).
5. **Giới hạn**: cái gì chưa kiểm được và cần số liệu gì.

Không tự sửa website, không gửi gì ra ngoài. Ghi một dòng vào `log.md` nếu đang chạy trong dây chuyền.
