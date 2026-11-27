# SOP 12 · Tự lập & vận hành kế hoạch SEO (không cần Claude)

Mọi bước làm được bằng **app SEO Automation + Lark + Google Sheet**. Claude chỉ giúp nhanh phần đọc, tổng hợp và viết; thiếu Claude thì làm tay theo đúng thứ tự dưới đây.

Mở file này từ app: tab **Kế hoạch** → nút «Tự lập kế hoạch (không cần Claude)».

## Bước 0 · Khai web (một lần)
1. Lark → Base chính → bảng **«Danh sách website»** → thêm dòng: Tên · Website · Mã Base (link Base riêng của web) · GSC (`sc-domain:ten-mien` hoặc `https://ten-mien/`) · GA4 (mã thuộc tính) · Bật = Có.
2. Ba ô thêm:
   - **Bắt đầu dự án**: tháng T1, dạng `2026-12` (tab Kế hoạch tính «đang ở tháng mấy», việc trễ theo ô này).
   - **Loại web**: `Tour` hoặc `Khách sạn` (chọn luật phân tích từ khoá).
   - **Tên thương hiệu**: các tên của mình, cách nhau dấu phẩy (VD Routine: `Routine, PITO, Calista, Wyndham, Times Corner, Praha, Daystar, Lyn Hotel, Casepia, Duo`). Khách sạn mới mở → thêm tên vào đây, nếu không app coi là khách sạn khác.
3. Base mới tạo bằng app Lark trên máy: thêm app Hub `cli_aa1a8ae21a78ded2` quyền full_access vào Base, nếu không app báo 91403.
4. Mở app → chọn web ở ô chọn trên cùng → bấm «Khởi tạo bảng Lark» nếu Base còn trống.

**Xong khi:** chọn web trong app không báo lỗi; tab Tổng quan hiện số GSC.

## Bước 1 · Số nền (tháng 1 — làm trước mọi thứ)
1. Search Console + GA4: thêm email `doc-search-console@rootytrip-seo.iam.gserviceaccount.com` (GSC: quyền Đầy đủ/Hạn chế; GA4: Người xem).
2. GA4 → Key events: bấm Zalo, gọi, gửi form/đặt phòng/đặt tour thành công.
3. Tab **B10 · Đánh giá** → «Nhập CSV (GSC / GA4)» 3 tháng gần nhất (cách xuất ghi ngay trên tab).

**Xong khi:** B10 có số tháng gần nhất (lượt nhấp, hiển thị, phiên organic, chuyển đổi), mỗi số có khoảng ngày. Không có số nền thì chưa đặt KPI.

## Bước 2 · Từ khoá
1. Google Keyword Planner → nhập từ khoá gốc: loại dịch vụ, khu vực, tên thương hiệu → «Tải xuống ý tưởng từ khoá». Hoặc dán kết quả vào Google Sheet.
2. Tab **B2 · Từ khoá** → «Nhập từ link Google Sheet» (dán link đúng tab) hoặc «Nhập CSV».
   - Sheet phải chia sẻ quyền Xem cho email service account ở Bước 1, hoặc «Bất kỳ ai có đường liên kết».
3. Bấm **«Phân tích & gom nhóm»** → xem bảng **Tổng hợp theo cụm chủ đề** → bấm từng cụm, soát bảng bên dưới:
   - Sai cụm → sửa ô «Cụm chủ đề».
   - Không nhắm (tên đối thủ, lạc đề) → «Trạng thái» = Bỏ. Web khách sạn: tên khách sạn khác tự chuyển Bỏ.
4. Lưu ý: luật khu vực viết cho Phú Quốc. Web ở nơi khác → gán cụm khu vực bằng tay.

**Xong khi:** không còn dòng «(chưa phân tích)»; mọi từ khoá không Bỏ đều có Cụm chủ đề + Nhóm URL.

## Bước 3 · Chủ đề → trang đích
1. Tab **B3 · Cụm chủ đề & silo**: mỗi **Nhóm URL** = một trang. Điền «Trang đích» (URL có sẵn hoặc URL dự kiến). Nhóm chưa có trang → «Tạo bài cho nhóm chưa có trang».
2. Kiểm tay bằng Google: gõ 2 từ khoá, top 10 trùng ≥ 3–4 kết quả → chung một trang; khác → tách trang.
3. **Một từ khoá chính = một URL.** Hai URL cùng nhắm một từ khoá → gộp hoặc đổi từ khoá.
4. Ưu tiên = lượng tìm × khả năng thắng × gần lúc khách đặt (trang dịch vụ/khu vực/sản phẩm trước, cẩm nang sau).

**Xong khi:** mọi nhóm URL có trang đích + mức ưu tiên; không có 2 URL cùng từ khoá chính.

## Bước 4 · Đối thủ & kỹ thuật
1. Tab **B4 · Đối thủ**: 5 bên đang top cho từ khoá chính. Ghi họ có gì mình thiếu (giá, ảnh thật, bảng so sánh, FAQ, đánh giá).
2. Tab **B5 · Audit 5 hạng mục** → «Kiểm tự động» + «Chạy crawl». Lỗi vào **B5 · Danh sách lỗi & sửa** → giao người sửa (dev) + hạn.
3. Sửa xong → tab **B10 · Đánh giá** → mục **Nhật ký thay đổi**: ghi 1 dòng kèm **Phép kiểm** (`CÓ: chuỗi phải thấy` / `KHÔNG: chuỗi không được còn`) → bấm «Thanh tra».

**Xong khi:** B5 không còn lỗi mức Cao; Thanh tra Đạt mọi dòng đã sửa.

## Bước 5 · Lên lịch (tab Kế hoạch)
1. Web mới, bảng trống → bấm **«Nạp công đoạn»**: có sẵn 37 công đoạn của quy trình 10 tháng (`00-tong-quan.md`). Ô «Xong khi» mẫu viết cho Rooty → sửa cột **«Xong khi»** trên Lark (bảng «Việc SEO» của Base web đó) cho đúng web mình.
2. Muốn việc chi tiết theo tuần: thêm dòng thẳng vào bảng **«Việc SEO»** trên Lark (tab Kế hoạch chưa có nút thêm). Cột: Mã · Công đoạn · Mảng · Pha · Từ tháng · Đến tháng · Cửa chặn · Người phụ trách · Hạn · Đầu ra · Xong khi · Trạng thái = Chưa làm. «Mảng» và «Pha» chọn đúng tên có sẵn trong ô chọn.
3. Thứ tự không đảo:
   1. Đo lường + sửa lỗi kỹ thuật (T1)
   2. Từ khoá → bản đồ chủ đề (chốt đầu T2)
   3. Trang đích + trang nhận diện (T2 → hết T3)
   4. Onpage (sau nội dung 10–15 ngày)
   5. Liên kết nội bộ (sau onpage 15–30 ngày)
   6. Offsite (T4–T6, chỉ khi nội dung lõi xong)
4. Nội dung cần ~100 ngày để chín → đếm ngược từ mùa cao điểm của web (xem cột tháng trong file Keyword Planner).
5. «Xong khi» phải kiểm được: một file, một con số, một chuỗi phải thấy trên trang. Không ghi «đã tối ưu», «đã làm».

Mẫu tham khảo: kế hoạch Routine `reports/routinehospitality/ke-hoach-seo-2026-11-27.md` và 41 việc trong `reports/routinehospitality/viec-seo-2026-11-27.csv`.

**Xong khi:** tab Kế hoạch có việc cho đủ 10 tháng; mỗi việc có người phụ trách, hạn, «Xong khi».

## Bước 6 · Vận hành
| Nhịp | Việc | Ở đâu |
|---|---|---|
| Thứ Hai | Bật «Chỉ việc tháng này + trễ», nhắc người làm việc trễ | Tab Kế hoạch |
| Khi xong việc | Người làm đổi trạng thái «Xong» (app hỏi lại tiêu chí), dán link kết quả | Tab Kế hoạch |
| Khi sửa web | Ghi Nhật ký thay đổi + Phép kiểm → Thanh tra | B10 · Đánh giá (mục Nhật ký thay đổi) |
| Hằng tuần | Bài đăng GBP, trả lời đánh giá trong 48 giờ | B8 · Google Maps |
| Cuối tháng | Nhập CSV GSC/GA4, so với số nền và tháng trước | B10 · Đánh giá |
| Cuối quý | Đối chiếu KPI, quyết định ở các cửa ◇ | Tab Kế hoạch |

## Làm ở Google Sheet → nhập vào app (mọi bảng, kể cả kế hoạch)
Bảng nào trong app cũng có nút **«Nhập từ Google Sheet»** (cạnh ô Tìm). Tab **Kế hoạch** có **«Nhập kế hoạch từ Google Sheet»** và **«Tải kế hoạch (CSV)»**.
1. Lấy mẫu cột: tab Kế hoạch → «Tải kế hoạch (CSV)» → mở bằng Google Sheet (Tệp → Nhập). Bảng khác: «Xuất CSV» nếu có, hoặc gõ dòng tiêu đề đúng tên cột app hiện trong hộp dán link.
2. Làm việc trên Sheet: đổi Trạng thái, Người phụ trách, Hạn, thêm dòng mới… Ngày ghi `07/12/2026` hoặc `2026-12-07`; tháng dự án ghi `3` hoặc `T3`.
3. Chia sẻ sheet (quyền Xem cho email service account, hoặc «Bất kỳ ai có đường liên kết») → bấm nút nhập → dán link đúng tab.
4. App so theo **cột khoá**: Kế hoạch = «Mã»; Liên kết = «Từ URL» + «Đến URL» + «Anchor»; bảng khác = cột đầu tiên (VD Từ khoá, URL). Dòng đã có → cập nhật ô sheet có giá trị; dòng chưa có → thêm. **Ô trống không xoá dữ liệu** trong app.
5. Kế hoạch: «Pha» ghi `Pha 2` hoặc `2` là được; «Trạng thái» phải là Chưa làm / Đang làm / Xong / Bị chặn / Không áp dụng. Chuyển «Xong» trên sheet thì app bắt đầu đếm mốc kiểm lại từ lúc nhập.

### Theo dõi kế hoạch làm ở Google Sheet (tự đồng bộ)
1. Tab **Kế hoạch** → **«Gắn link sheet kế hoạch»** → dán link đúng tab (cột như trên, bắt buộc có «Mã»). Link lưu ở ô «Sheet kế hoạch» trong bảng Danh sách website.
2. Từ đó **mỗi lần mở tab Kế hoạch app tự đọc sheet** (cách nhau tối thiểu 1 phút); bấm «Đồng bộ ngay» khi cần. Dòng trên cùng ghi giờ đồng bộ và số dòng thêm/cập nhật, hoặc lỗi đọc sheet.
3. Mỗi việc đổi trạng thái trên sheet được ghi 1 dòng vào **Nhật ký** (VD «Việc SEO RH07: Chưa làm → Xong (sheet)»).
4. Khung **«Tuần này»**: việc vừa xong 7 ngày · việc đang trễ (qua tháng kết thúc hoặc qua ngày «Hạn») · việc đến hạn 7 ngày tới.
5. App chỉ đọc sheet, không ghi ngược. Sửa trên app thì sửa luôn trên sheet, nếu không lần đồng bộ sau sheet sẽ ghi đè ô đó.

### App kiểm lại việc làm ở nơi khác
- **Liên kết nội bộ / backlink**: nhập bảng link (Loại = Nội bộ, Trạng thái = Kế hoạch hoặc Đã gắn) → tab **B9 · Link building** → «Kiểm link còn sống». App mở trang nguồn: thấy link tới **đúng trang đích** → «Đang live» (báo cả khi anchor khác kế hoạch); dòng «Đã gắn» mà không thấy → «Mất link»; dòng «Kế hoạch» chưa thấy → giữ nguyên.
- **Sửa trên web (onpage, kỹ thuật, nội dung)**: nhập bảng **Nhật ký thay đổi** với cột «Phép kiểm» (`CÓ: …` / `KHÔNG: …`) → bấm «Thanh tra».
- **Bài viết**: chấm bản nháp Google Docs (mục dưới).
- **Việc kế hoạch khác**: app không tự xác nhận được — người duyệt đối chiếu «Xong khi» với link ở cột «Kết quả / link».

## Viết bài ngoài app → app chấm (Google Docs)
1. Viết trên **Google Docs**. Tiêu đề bài dùng kiểu **Title** hoặc **Heading 1**; mỗi mục dùng kiểu **Heading 2** (Định dạng → Kiểu đoạn văn). Chữ in đậm không tính là H2.
2. Chia sẻ file: quyền Xem cho `doc-search-console@rootytrip-seo.iam.gserviceaccount.com`, hoặc «Bất kỳ ai có đường liên kết».
3. Kiểm nhanh: tab **B6 · Content** → «Kiểm nhanh bài Google Docs» → dán link + từ khoá chính → đọc kết quả → sửa trên Docs → «Kiểm lại».
4. Lưu điểm vào bài: mở thẻ bài → mục ④ → dán «Link bản nháp Google Docs» → «Chấm bản nháp Google Docs». Điểm và chi tiết lưu ở cột «Điểm GEO», «Chấm GEO».
5. App chấm được: mở đầu trả lời thẳng, H2 dạng câu hỏi, câu đầu mỗi H2, H2 rỗng nghĩa, đoạn mở bằng «điều này», độ dài, mật độ dữ kiện có số, trích nguồn, dấu hiệu kinh nghiệm thật, còn «[CẦN KIỂM CHỨNG]». **Không** kiểm được dữ kiện đúng hay sai — người duyệt vẫn đối chiếu nguồn (cổng 3) trước khi đăng.

**Xong khi:** 4 tiêu chí 🔒 đều ✅, không còn [CẦN KIỂM CHỨNG], người duyệt đã đối chiếu số liệu với nguồn.

## Phần không có Claude phải tự làm hoặc chậm hơn
- **Viết bài**: viết tay hoặc thuê người viết trên Google Docs, app chấm theo mục trên; dây chuyền 6 trạm đầy đủ (`ORCHESTRATOR.md`, `gates/`) vẫn cần người làm từng cổng.
- **Nhận xét báo cáo**: app có số; phần nhận xét tự viết theo cấu trúc `11-do-luong-bao-cao.md`.
- **Đo hiện diện AI**: hỏi tay bộ câu hỏi cố định trên ChatGPT/Gemini/Perplexity, mỗi câu 3 lần, ghi vào tab GEO · AI Search.

Tài liệu từng mảng: SOP 01–11 trong thư mục `quy-trinh/` (trong app: nút «Mở SOP» ở từng việc của tab Kế hoạch).
