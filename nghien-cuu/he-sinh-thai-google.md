# Hệ sinh thái Google cho Rooty Trip — làm phần nào, bỏ phần nào

Soạn 11/11/2026 · liên quan: `nghien-cuu/google-maps-huong-dan.md` (GBP), tab B8 · Entity, B9 · Link building, B10 · Thuật toán Google (bảng «Chính sách spam Google»)
Danh sách ghim bản đồ: `nghien-cuu/my-maps-diem-den.csv`

> AI chỉ soạn. Tài khoản Google của công ty do người phụ trách đăng nhập và tự tạo, tự đăng.

## 1. Kết luận ngắn

Quy trình "Google Entity Stacking" đang được chia sẻ có **phần đúng**: thông tin đồng nhất (NAP), có mặt trên YouTube, Google Maps, bản đồ du lịch hữu ích. Nhưng có **ba việc nằm trong danh sách chính sách spam của Google**: viết lại hoặc "spin" một đoạn cho hàng loạt file, tạo nhiều file hay site vệ tinh chỉ để đặt link, và dùng công cụ ép index. Rooty làm phần đúng, bỏ phần rủi ro.

Mục đích chị cần là **nối các bài trên web với nhau**. Việc này quyết định bởi **link nội bộ ngay trên rootytrip.com**. Các trang Google bên ngoài chỉ là cửa phụ đưa người đọc vào web, không thay được link nội bộ.

## 2. Từng nền tảng: làm hay bỏ?

| Nền tảng | Quyết định | Vì sao |
|---|---|---|
| Google Business Profile | ✅ **Làm** (đang làm) | Kênh khách tìm tour thật. Xem `google-maps-huong-dan.md` |
| YouTube | ✅ **Làm** — ưu tiên số 1 sau GBP | Khách xem video trước khi đặt tour. Video hiện ngay trên trang kết quả Google, và AI hay trích dẫn YouTube. Giá trị nằm ở lượt xem, không nằm ở link: link trong mô tả YouTube đi qua trang chuyển hướng nên gần như không truyền sức mạnh SEO [CẦN KIỂM CHỨNG trên video đầu tiên: xem mã nguồn link] |
| Google My Maps | ✅ **Làm 1 bản đồ** | "Bản đồ du lịch Phú Quốc của Rooty Trip": 35 ghim, mỗi ghim dẫn về đúng bài cẩm nang. Nhúng vào bài trên web cho khách dùng thật. Danh sách ghim đã soạn sẵn |
| Google Sites | ⚪ **Không ưu tiên** | Một trang giới thiệu thương hiệu thì vô hại nhưng gần như không đem khách. Nhiều trang Sites chỉ để đặt link là site vệ tinh, Google không tính |
| Google Docs / Sheets / Slides / Drive | ⚪ **Chỉ khi có tài liệu khách thật dùng** | Ví dụ checklist đồ mang đi đảo (PDF) hay bảng lịch tàu ra đảo. Mỗi tài liệu một nội dung riêng, có ích, gắn 1 link về bài gốc. **Không** tạo hàng loạt file chép cùng một đoạn |
| Blogger (Blogspot) | ⚪ **Không ưu tiên** | Chỉ đăng bài viết mới, khác hẳn nội dung web, theo đúng SOP 09 mục 3 (nội dung thật, không spin). **Không** viết lại bài của rootytrip.com: hai bản giống nhau sẽ cạnh tranh với chính web, và một blog toàn bài chép lại thì giống mạng blog vệ tinh (PBN) |
| Google Calendar / Groups | ❌ **Bỏ** | Không có khách du lịch tìm tour ở đây |
| Công cụ ép index / bắn link | ❌ **Bỏ** | Chính sách Google cấm "link tạo bằng chương trình tự động". Muốn bài trên rootytrip.com được index nhanh thì dùng Search Console → Kiểm tra URL → Yêu cầu lập chỉ mục |

**Ba việc trong quy trình được chia sẻ vi phạm chính sách Google** (nguồn: developers.google.com/search/docs/essentials/spam-policies, đã có trong bảng «Chính sách spam Google» ở tab B10):

- **"Spin" nội dung cho hàng loạt file** → *Scaled content abuse* (nội dung sản xuất hàng loạt): tạo nhiều trang ít giá trị để kéo thứ hạng, kể cả bằng cách xào lại câu chữ.
- **Tạo nhiều tài sản chỉ để đặt link về web** → *Link spam*: link tạo ra để thao túng thứ hạng.
- **Công cụ hỗ trợ index, bắn link** → *Link spam*: link tạo bằng chương trình tự động.

Hậu quả thường gặp không phải bị phạt cả web, mà là **mất công không được gì**: Google bỏ qua các link đó. Nếu làm nhiều và lộ liễu thì có thể bị thao tác thủ công (manual action) trong Search Console.

## 3. Việc làm ngay

### 3.1 Sửa link nội bộ — thứ thật sự nối các bài với nhau

Em đã đối chiếu bản đồ link nội bộ (crawl 08/11/2026, chỉ tính link trong nội dung, bỏ menu và chân trang) với 34 bài điểm đến trong bản đồ:

- `/ban-do-du-lich-phu-quoc/` đã link tới **25/34** bài. Còn thiếu: Công viên nước Hòn Thơm, Hòn Đồi Mồi, Bãi Khem, Bãi Ông Lang, Bãi Vòng, Dinh Cậu, Dinh Bà, Suối Đá Bàn, Sân bay Phú Quốc.
- `/dia-diem-du-lich-phu-quoc/` đã link tới **24/34** bài. Còn thiếu: Review cáp treo Hòn Thơm, Công viên nước Hòn Thơm, Hòn Đồi Mồi, Bãi Thơm, Bãi Vòng, Sunset Sanato, Dinh Cậu, Chùa Sư Muôn, Suối Đá Bàn, Sân bay Phú Quốc.

Thêm link chữ ở đúng đoạn nhắc tới điểm đó trong hai bài này. Việc gắn link giữa các bài vệ tinh với nhau và về trang tour: dùng tab **B9 · Link building → Gợi ý link nội bộ** và lệnh `/rooty-lien-ket-noi-bo`.

### 3.2 Bản đồ My Maps "Bản đồ du lịch Phú Quốc của Rooty Trip"

1. Vào mymaps.google.com bằng tài khoản Google của công ty (cùng tài khoản quản lý GBP) → **Tạo bản đồ mới** → đặt tên "Bản đồ du lịch Phú Quốc – Rooty Trip".
2. **Nhập** → tải lên `nghien-cuu/my-maps-diem-den.csv` → cột định vị chọn **Địa điểm**, cột tiêu đề chọn **Tên**.
3. **Kiểm từng ghim**: Google tự dò vị trí theo cột "Địa điểm" nên có thể ghim sai chỗ. Ghim lệch thì kéo về đúng chỗ. Đây là bước bắt buộc, vì khách sẽ dùng bản đồ để đi thật.
4. Kiểu ghim: tạo kiểu theo cột **Lớp** (Biển & đảo · Vui chơi · Tâm linh & lịch sử · Ăn uống & chợ · Thiên nhiên · Di chuyển · Rooty Trip) để khách lọc.
5. Thêm ảnh thật do đội phó nháy chụp vào các ghim chính (không lấy ảnh trên mạng).
6. **Chia sẻ** → bật "Bất kỳ ai có đường liên kết đều xem được" → **Nhúng vào trang web của tôi** → copy mã.
7. Dán mã nhúng vào `/ban-do-du-lich-phu-quoc/` (ngay dưới đoạn mở đầu) và `/dia-diem-du-lich-phu-quoc/`. Thêm link bản đồ vào phần Liên kết của hồ sơ GBP và mô tả kênh YouTube.
8. Khi có bài điểm đến mới trên web → thêm một ghim. Ghi chỗ đã dùng bản đồ vào bảng **Hồ sơ thương hiệu** (tab B8) để theo dõi.

Mỗi ghim chỉ có **1 link** về bài cẩm nang, gắn UTM `utm_campaign=my-maps` để xem trong GA4 bản đồ đưa bao nhiêu người vào web.

### 3.3 YouTube — 2 video/tháng

- Nguyên liệu có sẵn: video phó nháy quay trong tour (xin phép khách nếu có mặt khách).
- Mỗi video gắn với 1 bài cẩm nang. Tên video là câu hỏi thật ("Đi cáp treo Hòn Thơm mất bao lâu?").
- Phần mô tả: 2–3 câu trả lời câu hỏi, link bài blog (UTM `utm_campaign=youtube`), link trang tour liên quan.
- Nhúng video vào chính bài blog đó. Video giữ khách ở lại trang, và Google có thể hiện video kèm bài.
- Kênh: tên "Rooty Trip", mô tả và link khớp NAP; thêm link kênh vào `sameAs` của schema (tab B8).

### 3.4 Thống nhất thông tin trước khi tạo thêm gì

Đúng như bước 1 của quy trình chị gửi. Hiện còn lệch: schema trang chủ có tên "Rooty Trip" và "Rooty Trip Phú Quốc" (xem `google-maps-huong-dan.md` mục 8); `00-context/brand.md` còn trống địa chỉ, hotline. Chốt một bộ NAP rồi mới dùng cho My Maps, YouTube, GBP.

## 4. Đo hiệu quả

- GA4 → Nguồn / phương tiện / chiến dịch: `my-maps`, `youtube`, `gbp-post`, `gbp` — người vào và lượt bấm Zalo/đặt tour từ mỗi kênh.
- YouTube Studio: lượt xem, thời gian xem, lượt bấm link.
- Sau 3 tháng (tháng 2/2027) giữ kênh có khách thật, dừng kênh không có.
