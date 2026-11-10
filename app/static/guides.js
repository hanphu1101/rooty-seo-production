// Hướng dẫn chi tiết từng tab — theo 10 bước SEO, viết cho Rooty Trip.
window.GUIDES = {
  tongquan: {
    step: 'Tổng quan', title: 'Quy trình SEO 10 bước · 5 giai đoạn',
    goal: 'Một màn hình xem toàn bộ dự án SEO của rootytrip.com: mỗi bước đang ở đâu, việc gì cần làm tiếp. Bấm vào thẻ để mở tab của bước đó.',
    steps: [
      '<b>Discovery</b> (B1–B4): hiểu khách → tìm từ khoá → gom cụm chủ đề → soi đối thủ. Làm trong tháng 1, chốt bản đồ chủ đề đầu tháng 2.',
      '<b>Improving</b> (B5): audit và sửa nền móng (kỹ thuật, silo, UX/UI, onsite, entity) trước khi đổ nội dung.',
      '<b>Create & Optimize</b> (B6–B8): viết nội dung đúng ý định tìm kiếm → onpage (10–15 ngày sau khi đăng) → entity.',
      '<b>Promotion</b> (B9): link nội bộ (15–30 ngày sau onpage) → backlink chỉ khi qua cửa quyết định (khoảng tháng 6).',
      '<b>Evaluate</b> (B10): nhập số mỗi tháng, review mỗi quý, quay lại bước cần điều chỉnh.'
    ],
    done: ['Nguyên tắc: nội dung cần ~100 ngày để chín · làm đúng thứ tự, đúng thời điểm · chưa lên trang 1 thì AI cũng chưa nhắc tên.'],
    cmd: '/rooty-ke-hoach-seo tháng này làm gì'
  },
  khach: {
    step: 'Bước 1 · Discovery', title: 'Thu thập dữ liệu thị trường — Chân dung khách hàng & Hành trình mua hàng',
    goal: 'Hiểu ai mua tour/combo/vé Phú Quốc của Rooty, họ cần gì, sợ gì, tìm thông tin ở đâu và đi qua những giai đoạn nào trước khi đặt — dựa trên <b>dữ liệu thật thay vì phỏng đoán</b>. Đây là nền cho từ khoá (B2), cụm chủ đề (B3) và nội dung (B6).',
    steps: [
      '<b>① Thu thập dữ liệu</b> (bảng "Nguồn dữ liệu khách"): bấm "Nạp dữ liệu mẫu" để có 9 nguồn cần thu — phỏng vấn sale/CSKH, phỏng vấn HDV, 100 tin nhắn Zalo/Fanpage, 50 đánh giá Google/Tripadvisor, dữ liệu đặt tour 12 tháng, khảo sát khách sau tour, GA4 nhân khẩu học, câu hỏi trong Search Console, nhóm Facebook/TikTok. Mẫu khảo sát và kịch bản phỏng vấn có sẵn (link phía dưới). Thu xong mỗi nguồn → ghi "Phát hiện chính", đổi "Đã phân tích".',
      '<b>② Chân dung khách hàng</b> — mỗi nhóm điền đủ 5 phần: <b>Nhân khẩu học</b> (tuổi, giới tính, nghề nghiệp, thu nhập, nơi sống, học vấn) · <b>Tâm lý & lối sống</b> (tính cách, giá trị, sở thích) · <b>Nhu cầu & động cơ</b> (vì sao đi, muốn đạt gì) · <b>Điểm đau</b> (lo lắng, rào cản, bất mãn + câu hay hỏi) · <b>Hành vi tiêu dùng</b> (tìm thông tin ở đâu, online/offline, yếu tố quyết định, ngân sách, thời điểm, đặt trước bao lâu). 4 chân dung mẫu: gia đình có trẻ nhỏ · cặp đôi/trăng mật · nhóm bạn trẻ · khách đoàn công ty.',
      '<b>Tỷ trọng</b>: lấy từ dữ liệu đặt tour (booking có trẻ em, 2 người, ≥ 5 người, có VAT…) — nhóm lớn nhất được ưu tiên nội dung trước.',
      '<b>③ Hành trình mua hàng</b> — 5 giai đoạn: <b>Nhận thức</b> (biết nhu cầu, biết Phú Quốc/Rooty) → <b>Cân nhắc</b> (tìm hiểu, so sánh) → <b>Quyết định</b> (chọn và đặt) → <b>Sử dụng & giữ chân</b> (trải nghiệm tour) → <b>Trung thành & giới thiệu</b> (đánh giá, quay lại, giới thiệu). Mỗi ghi nhận có: câu hỏi, hành động, <b>điểm chạm</b> (TikTok, Google, AI, website, Zalo, HDV, phó nháy…), cảm xúc, rào cản, cơ hội cho Rooty, nội dung đáp ứng, chỉ số đo.',
      '<b>Đọc bản đồ</b>: lọc theo từng nhóm khách. Ô "Rào cản" và cảm xúc 😟 là chỗ Rooty đang mất khách → ưu tiên sửa (nội dung, trang tour, tốc độ phản hồi Zalo).',
      '<b>Xác nhận</b>: chân dung chỉ đổi "Đã xác nhận" khi có ≥ 2 nguồn dữ liệu khác loại ủng hộ và sale + 1 HDV đồng ý.',
      '<b>Chuyển tiếp</b>: mỗi câu hỏi trong hành trình là hạt giống từ khoá (B2); cột "Loại nội dung" cho biết cần trang gì (B3, B6).'
    ],
    done: ['≥ 5 nguồn dữ liệu "Đã phân tích", có dữ liệu đặt tour', '3–4 chân dung đủ 5 phần, có tỷ trọng, "Đã xác nhận"', 'Mỗi giai đoạn hành trình có ≥ 2 ghi nhận, đủ điểm chạm và rào cản', 'Mọi câu hỏi ở giai đoạn Cân nhắc & Quyết định đã gắn nội dung/trang đáp ứng'],
    cmd: '/rooty-tu-khoa tổng hợp chân dung khách và hành trình từ dữ liệu trong bảng Nguồn dữ liệu khách'
  },
  tukhoa: {
    step: 'Bước 2 · Discovery', title: 'Nghiên cứu từ khoá — danh sách từ khoá khách thật sự gõ',
    goal: 'Lập danh sách các từ/cụm từ mà khách mục tiêu (chân dung ở B1) thực tế gõ vào Google để tìm tour, combo, vé Phú Quốc và thông tin liên quan — đủ số liệu và ý định tìm kiếm để chọn đúng từ khoá làm trước.',
    steps: [
      '<b>① Brainstorm từ khoá gốc (seed)</b> từ góc độ người bán: <b>tên sản phẩm</b> (tour 4 đảo, combo Phú Quốc, vé VinWonders…) · <b>thương hiệu</b> (rooty trip) · <b>tính năng</b> (có HDV bản địa, có chụp ảnh) · <b>nhu cầu cốt lõi</b> (du lịch Phú Quốc, lịch trình, chi phí) · <b>địa điểm</b>. Bấm "Nạp dữ liệu mẫu" để có 20 seed gợi ý, thêm seed từ câu hỏi ở bảng Hành trình (B1).',
      '<b>Mở rộng tự động</b>: bấm "Mở rộng các từ khoá gốc" — trang lấy gợi ý tìm kiếm của Google cho từng seed (kèm đuôi giá, có gì, ở đâu, kinh nghiệm, nên, review…) → thêm từ khoá dài vào danh sách, tự đoán ý định và giai đoạn hành trình. Mỗi seed ~30 giây.',
      '<b>② Dùng công cụ chuyên dụng</b> để có <b>lượng tìm kiếm</b>: <b>Google Keyword Planner</b> (miễn phí — nhập seed, tải CSV ý tưởng từ khoá) · <b>Search Console</b> (từ khoá thật đang đưa khách tới web) · <b>Ahrefs/Semrush</b> (mở rộng theo cấp, KD, ý định, Parent topic) · <b>Keywordtool.io</b>. Xuất CSV → "Nhập CSV": trang tự nhận cột (kể cả file UTF-16 của Keyword Planner), bỏ trùng.',
      '<b>Phân tích hành vi & đối thủ</b>: lấy từ khoá đối thủ đang top ở B4 (phần Gap) chuyển sang đây; xem "Mọi người cũng hỏi" và tìm kiếm liên quan cuối trang Google.',
      '<b>③ Phân loại theo ý định tìm kiếm</b>: <b>Informational</b> = Thông tin (phú quốc có gì) · <b>Navigational</b> = Điều hướng (rooty trip) · <b>Commercial</b> = Cân nhắc (nên đi 3 đảo hay 4 đảo) · <b>Transactional</b> = Mua (giá tour 4 đảo, đặt combo). Tự đoán chỉ là gợi ý — kiểm lại bằng cách Google từ khoá xem kết quả là bài viết hay trang bán.',
      '<b>Làm sạch & ưu tiên</b>: đổi "Bỏ" cho từ khoá không liên quan (tên đối thủ, nơi khác). Ưu tiên Cao = Mua/Cân nhắc + có lượng tìm + Rooty có sản phẩm. Lọc "Cơ hội nhanh" = đang ở vị trí 8–30.'
    ],
    done: ['Có ≥ 15 seed phủ đủ sản phẩm chính, đã mở rộng', '≥ 300 từ khoá sạch, ≥ 70% có lượng tìm hoặc số hiển thị', '100% có ý định; từ khoá Mua/Cân nhắc có ưu tiên'],
    cmd: '/rooty-tu-khoa làm sạch, gắn ý định và ưu tiên cho bảng từ khoá'
  },
  cum: {
    step: 'Bước 3 · Discovery', title: 'Nhóm & phân loại từ khoá theo cụm chủ đề (Topic Cluster)',
    goal: 'Gom từ khoá thành <b>nhóm URL</b> (cùng ý định → một bài) và <b>cụm chủ đề</b> (một Pillar + nhiều Cluster), để mỗi từ khoá chính thuộc đúng một URL và cả website có cấu trúc silo rõ ràng.',
    steps: [
      '<b>Gom theo ý định (SERP)</b>: hai từ khoá cho kết quả Google gần giống nhau (trùng ≥ 3–4 URL trong top 10) → cùng một nhóm URL, viết chung một bài. Bấm "Gợi ý gom nhóm tự động": trang gom theo từ khoá cha (nếu CSV Ahrefs có Parent keyword) hoặc theo các từ chính trùng nhau, và đoán cụm — <b>chỉ điền ô trống</b>; kiểm lại bằng cách Google 2 từ khoá nghi ngờ.',
      '<b>Phân định Pillar & Cluster</b>: trong mỗi cụm, nhóm có từ khoá rộng, lượng tìm cao nhất (head term) → <b>Pillar page</b> (3.000–5.000 từ, thường là trang danh mục, VD /tour-phu-quoc-tron-goi/). Các nhóm từ khoá dài, ngách, câu hỏi → <b>Cluster content</b> (1.000–2.000 từ), mỗi bài link về Pillar và Pillar link ra các bài.',
      '<b>Đặt tên cụm</b> cho Rooty: Tour đảo · Tour trong ngày · Tour trọn gói · Combo & khách sạn · Vé tham quan · Điểm đến · Lên kế hoạch · Ẩm thực · Thương hiệu.',
      '<b>Gắn URL</b>: bảng cụm bên dưới hiện từng nhóm, tổng lượng tìm và trang đích. Nhóm "Cần viết" → bấm "Tạo bài cho nhóm chưa có trang" để đưa vào dây chuyền Content (B6). Bấm vào một nhóm để mở và sửa từ khoá ở B2.',
      '<b>Đánh dấu vai trò trang</b> ở bảng Trang đích: Pillar (trụ cột) / Cluster (vệ tinh) / Trang sản phẩm. Mỗi cụm đúng 1 Pillar.',
      '<b>Làm trên Excel/Sheets nếu thích</b>: "Xuất CSV" → lọc theo Keyword, Search Volume, Parent/Intent, tô màu theo nhóm → sửa xong nhập lại.'
    ],
    done: ['Không còn từ khoá ưu tiên Cao “chưa gom nhóm”', 'Mỗi cụm có đúng 1 trang Pillar', 'Mọi nhóm URL đã có trang hoặc đã tạo bài ở B6', 'Không có 2 trang cùng nhắm một từ khoá chính'],
    cmd: '/rooty-tu-khoa kiểm lại gom nhóm: so SERP các từ khoá trong từng nhóm URL và đề xuất tách/gộp'
  },
  doithu: {
    step: 'Bước 4 · Discovery', title: 'Phân tích đối thủ cạnh tranh — điểm mạnh, điểm yếu & từ khoá đang xếp hạng',
    goal: 'Biết ai đang thắng ở từng cụm, họ mạnh/yếu ở đâu, đang có những từ khoá nào mà Rooty chưa có — để chọn chỗ Rooty thắng được nhanh nhất.',
    steps: [
      '<b>Tìm đối thủ</b>: với mỗi cụm (B3), Google 2–3 từ khoá đại diện (ẩn danh) → ghi domain top 5 tự nhiên và các bên đang <b>chạy Google Ads</b>. Gồm công ty tour địa phương, OTA (Klook, Traveloka — có sẵn trong mẫu), blog du lịch, báo.',
      '<b>Đánh giá điểm mạnh</b>: <b>nội dung</b> (độ sâu, chuẩn SEO, tương tác mạng xã hội) · <b>backlink & uy tín</b> (báo lớn, blog ngành; DR/DA, số domain trỏ về) · <b>UX/UI & tốc độ</b>, di động · <b>thương hiệu, giá, chính sách</b>.',
      '<b>Đánh giá điểm yếu</b>: <b>khoảng trống nội dung</b> (chủ đề họ chưa viết) · <b>bài cũ</b>, heading/title chưa tối ưu · <b>chuyển đổi thấp</b>, chăm sóc/phản hồi chậm (thử nhắn hỏi tour).',
      '<b>Soi website tự động</b>: bấm "Soi website tất cả đối thủ" — đo tốc độ phản hồi, nén, title/meta, H1, viewport, schema, hreflang, số URL trong sitemap và số bài blog → ghi vào "Chỉ số kỹ thuật".',
      '<b>Từ khoá đối thủ</b>: Ahrefs/Semrush → nhập domain đối thủ → <b>Organic keywords</b> (tổng từ khoá, top traffic keywords) → xuất CSV → "Nhập CSV từ khoá đối thủ". Bấm "Phân loại Common/Gap": <b>Gap</b> = đối thủ có, Rooty chưa có · <b>Common</b> = cả hai cùng có (ai cao hơn) — giống mục Common Keywords của Semrush.',
      '<b>Chọn chiến trường</b>: Gap có cơ hội Cao (lượng tìm ≥ 500, ý định Mua/Cân nhắc) → "Chuyển Gap sang Từ khoá" để gom nhóm (B3) và viết (B6). Từ khoá đầu ngành cạnh tranh cao → đánh bằng nhiều bài long-tail dễ lên trước.',
      '<b>Khoảng trống Rooty thắng được</b>: ghi rõ cho mỗi đối thủ — HDV bản địa, phó nháy, giá thực tế khách đã trả, phản hồi Zalo nhanh, bài cập nhật mới.'
    ],
    done: ['≥ 5 đối thủ "Đã phân tích", mỗi cụm chính có ≥ 2 đối thủ', 'Mỗi đối thủ có đủ điểm mạnh, điểm yếu, khoảng trống', 'Đã nhập từ khoá của ≥ 2 đối thủ và phân loại Common/Gap', 'Gap cơ hội Cao đã chuyển sang bảng Từ khoá'],
    cmd: '/rooty-offsite phân tích điểm mạnh, điểm yếu đối thủ từ bảng Đối thủ và đề xuất chiến trường cho Rooty'
  },
  kythuat: {
    step: 'Bước 5 · Improving', title: 'Audit tổng thể website & điều chỉnh — Technical · Silo · UX/UI · Onsite · Entity',
    goal: 'Kiểm toàn diện rootytrip.com theo 5 hạng mục, chấm điểm từng hạng mục và sửa nền móng trước khi đổ nội dung. Checklist 74 mục — <b>58 mục trang tự chấm</b> (đọc website, báo cáo crawl, PageSpeed và dữ liệu ở các tab B2, B3, B8, B9), 16 mục kiểm tay có hướng dẫn.',
    steps: [
      '<b>Chạy</b>: bấm "Chạy crawl" (5–8 phút, quét toàn site) rồi "Kiểm tự động" (~1 phút). 5 thẻ điểm phía trên cho biết % đạt từng hạng mục — bấm thẻ để lọc.',
      '<b>⚙️ Technical SEO</b> — <b>Crawl & index</b>: robots.txt, sitemap.xml (và 25 URL mẫu trong sitemap), meta robots noindex/nofollow, canonical, cho cả Googlebot lẫn bot AI. <b>Tốc độ & Core Web Vitals</b>: LCP, INP, CLS trên cả <b>mobile và desktop</b> (PageSpeed Insights + báo cáo GSC). <b>Mã nguồn & bảo mật</b>: lỗi 404/5xx, redirect 301/302 dây chuyền hoặc vòng lặp, SSL/HTTPS, HSTS, mixed content, mobile-friendly, schema hợp lệ, hreflang.',
      '<b>🏗️ Silo</b> — <b>Phân cấp</b>: Trang chủ → Danh mục (tầng 1) → Trang con/bài viết (≤ 3 click), breadcrumb, URL. <b>Topical map & phễu</b>: trang đã gán cụm, mỗi cụm 1 Pillar, đủ nội dung cho <b>TOFU</b> (Thông tin) – <b>MOFU</b> (Cân nhắc) – <b>BOFU</b> (Mua). <b>Liên kết nội bộ</b>: không có trang mồ côi, trang tour nhận ≥ 5 link, không có trang chỉ 1 link.',
      '<b>🖱️ UX/UI</b> — <b>Điều hướng</b>: menu logic, thanh tìm kiếm, breadcrumb hiển thị. <b>CTA</b>: trang tour có nút Zalo/gọi/Messenger. <b>Hành vi (GA4)</b>: đã cài GA4/GTM; xem tỷ lệ tương tác (ngược với tỷ lệ thoát), thời gian tương tác, điểm rớt trên phễu xem tour → bấm Zalo → đặt (GA4 → Khám phá → Phễu). <b>Di động</b>: cỡ chữ ≥ 16px, nút bấm đủ lớn, ảnh không tràn, không popup che nội dung — đặt thử tour trên điện thoại thật.',
      '<b>📝 Onsite</b> — <b>Thẻ meta & heading</b>: title không trùng & đủ độ dài, meta description, đúng 1 H1, H2/H3 là câu hỏi thật theo từ khoá. <b>Chất lượng nội dung</b>: đoạn mở trả lời thẳng, trang mỏng, nội dung trùng lặp (H1 trùng), đáp ứng đúng search intent. <b>Hình ảnh</b>: alt, WebP/AVIF, dung lượng ≤ 200KB (kiểm 20 ảnh mẫu).',
      '<b>🏷️ Entity</b> — <b>NAP</b>: tên, hotline, địa chỉ giống nhau trên website (trang chủ + liên hệ), Google Business Profile, mạng xã hội, OTA (cập nhật ở tab B8). <b>Schema thực thể & Knowledge Graph</b>: Organization/TravelAgency/LocalBusiness đủ name, url, logo, telephone, address; sameAs; Person cho tác giả. <b>Social & citation</b>: ≥ 5 hồ sơ mạng xã hội, ≥ 5 báo chí/citation (tab B9), kiểm Knowledge Panel khi Google "Rooty Trip".',
      '<b>Điều chỉnh</b>: lọc "Chưa đạt" → làm 🔴 trước; cột "Cách kiểm / cách sửa" ghi cách làm cụ thể. Mục cần giao việc chi tiết từng URL → xem tab <b>B5 · Danh sách lỗi & sửa</b> (gom từ crawl, tự đóng khi đã sửa).',
      '<b>Nhịp</b>: kiểm tự động mỗi tháng và sau mỗi lần đổi theme/plugin/hosting; kiểm tay mỗi quý. <b>PageSpeed</b> hay bị giới hạn lượt gọi khi không có khoá — thêm <code>PAGESPEED_API_KEY</code> vào <code>.env</code>.'
    ],
    done: ['Không còn mục 🔴 "Chưa đạt" ở cả 5 hạng mục', 'Mỗi hạng mục ≥ 80% đạt', 'Core Web Vitals đạt cả mobile và desktop', 'Mọi mục kiểm tay có kết quả trong 90 ngày gần nhất'],
    cmd: '/rooty-ky-thuat đọc Checklist audit 5 hạng mục và viết kế hoạch sửa theo thứ tự ưu tiên cho dev và content'
  },
  audit: {
    step: 'Bước 5 · Improving', title: 'Audit tổng thể website & điều chỉnh',
    goal: 'Sửa nền móng trước khi đổ nội dung: kỹ thuật, cấu trúc silo, UX/UI, onsite và entity. Nền hỏng thì nội dung tốt cũng không lên.',
    steps: [
      '<b>Nạp lỗi tự động</b>: bấm “Chạy crawl” (hoặc “Nạp lỗi từ báo cáo” nếu đã có báo cáo) — gom lỗi từ crawl + GEO audit thành từng vấn đề kèm số trang, URL ví dụ, cách sửa. Mỗi lần crawl lại: lỗi đã hết tự chuyển “Đã sửa”, lỗi đã đánh dấu sửa mà vẫn còn sẽ tự mở lại.',
      '<b>Kỹ thuật (kiểm tay)</b>: Search Console → Trang (lỗi lập chỉ mục) và Sơ đồ trang web · PageSpeed Insights cho trang chủ + 1 trang tour + 1 bài (LCP < 2,5s, CLS < 0,1) · Rich Results Test · Cloudflare có chặn bot không.',
      '<b>Silo</b>: menu, breadcrumb, URL phản ánh cụm chủ đề (B3); trang quan trọng ≤ 3 click từ trang chủ.',
      '<b>UX/UI</b>: tự đặt thử 1 tour trên điện thoại — nút Zalo/đặt tour có hiện ngay không, popup có che nội dung không, ảnh có load nhanh không.',
      '<b>Onsite & Entity</b>: title/meta/H1 trùng hoặc thiếu (chi tiết ở B7), schema lỗi, thông tin thương hiệu lệch (B8).',
      '<b>Giao việc</b>: mỗi vấn đề ghi người sửa + hạn. Sửa xong đổi "Đã sửa", rồi chạy lại crawl để xác nhận không còn.',
      '<b>Sửa lỗi từng trang</b> (mục cuối trang): nhập báo cáo lỗi từ công cụ (Google Sheets → Tải xuống .xlsx, mỗi tab một loại lỗi có cột URL) → mỗi lỗi × trang thành một dòng. Làm theo trạng thái Mới → Đã xác nhận → Đang sửa → Đã sửa (lỗi “nghi vấn” đọc lại rồi chọn “Không phải lỗi” nếu sai). “Kiểm lại trang” để máy mở trang xác nhận lỗi đã hết (link tự thân, đổi năm giả).',
      '<b>Đo sửa có tác dụng không</b>: lúc đánh dấu “Đã sửa”, trang chụp lượt nhấp + vị trí GSC làm mốc trước. Sau ≥ 4 tuần nhập GSC Trang mới ở B10 → “Đo hiệu quả”. So nhóm đã sửa với nhóm chưa sửa (đối chứng) cùng loại lỗi — chênh rõ thì lỗi đó đáng sửa tiếp cho các trang còn lại. Quét lại bằng công cụ → nhập file mới: lỗi đã hết tự đóng, lỗi quay lại thành “Tái phát”.'
    ],
    done: ['Không còn vấn đề 🔴 Cao', 'Mọi vấn đề 🟡 có người sửa và hạn', 'Chạy lại crawl: lỗi cũ không xuất hiện lại', 'Mỗi loại lỗi đã sửa có kết quả đo trước/sau so với nhóm đối chứng'],
    cmd: '/rooty-ky-thuat lập danh sách lỗi cần dev sửa từ báo cáo crawl mới nhất'
  },
  content: {
    step: 'Bước 6 · Create & Optimize', title: 'Tạo dựng & tối ưu Content theo đúng ý định tìm kiếm (Search Intent)',
    goal: 'Mỗi bài/trang trả lời đúng điều người tìm kiếm thật sự muốn — đúng loại trang, đúng định dạng, trả lời ngay, cấu trúc rõ, có giá trị chỉ Rooty mới có — rồi mới qua 4 cổng QC và đăng.',
    steps: [
      '<b>① Xác định Search Intent</b> (mở bài → mục ①, hoặc bấm "Suy ý định" để lấy theo nhóm từ khoá ở B3): <b>Thông tin</b> (Informational — muốn học, tìm câu trả lời: "phú quốc có gì", "tháng mấy đi phú quốc đẹp") → bài blog, hướng dẫn, checklist · <b>Điều hướng</b> (Navigational — tìm đúng Rooty: "rooty trip") → trang chủ, giới thiệu, liên hệ · <b>Cân nhắc</b> (Commercial — so sánh trước khi mua: "nên đi 3 đảo hay 4 đảo", "review tour câu mực") → so sánh, review, top list · <b>Mua</b> (Transactional — sẵn sàng đặt: "giá tour 4 đảo", "đặt combo phú quốc") → trang tour/sản phẩm, danh mục, landing page.',
      '<b>② Phân tích SERP</b> (mục ②): bấm "Mở Google" — dùng cửa sổ ẩn danh — xem <b>top 10 đang là loại trang gì</b> (bài blog, trang OTA, danh mục, video) và ghi lại; tick các tính năng đặc biệt: <b>Featured Snippet</b> (→ viết đoạn trả lời 40–50 từ ngay dưới H2), <b>People Also Ask</b> (→ đưa câu hỏi thành H2/FAQ), <b>Local Pack</b> (→ cần Google Business Profile, B8), Video (→ nhúng video tour), AI Overview. Google trả loại trang nào thì làm loại đó — đừng viết bài blog cho từ khoá mà top 10 toàn trang bán.',
      '<b>Câu hỏi thật</b>: bấm "Lấy câu hỏi từ gợi ý Google" để có danh sách câu khách hay hỏi quanh từ khoá → chọn làm H2 và FAQ.',
      '<b>③ Viết & hoàn thiện</b> — dây chuyền 6 trạm (copy lệnh cho Claude): <b>giải quyết nhu cầu ngay đầu bài</b> (100–150 từ đầu trả lời thẳng, không lan man) · <b>heading logic</b> H2 = câu hỏi, câu đầu sau H2 là câu trả lời, H3 chia nhỏ — giúp cả người đọc, Google lẫn AI Search · <b>định dạng trực quan</b>: bảng (giá, lịch trình, so sánh), bullet, ảnh thật, video tour · <b>nguyên bản & giá trị thực</b>: kinh nghiệm HDV bản địa, giá khách đã trả, mẹo né đông, ảnh phó nháy — không sao chép top 10.',
      '<b>4 cổng QC</b>: dàn ý (19 tiêu chí) → bản nháp (21) → kiểm chứng dữ kiện → người duyệt. Chưa PASS thì không chuyển trạm được.',
      '<b>④ Chấm bài sau khi đăng</b>: dán "Link bài" → bấm "Chấm bài" (mục ③). Trang đọc bài thật và chấm theo ý định: trả lời ngay đầu bài, 1 H1, H2/H3, danh sách, ảnh; thêm H2 dạng câu hỏi + độ sâu cho bài Thông tin · bảng so sánh + heading so sánh cho bài Cân nhắc · <b>giá cụ thể</b> + nút Zalo/đặt + schema Offer cho trang Mua · hotline + schema Organization cho trang Điều hướng. Dưới 80 điểm → sửa rồi chấm lại.',
      '<b>Sau khi đăng</b>: onpage (B7) sau 10–15 ngày, link nội bộ (B9) sau 15–30 ngày. Bài cũ thì cập nhật, giữ nguyên URL.'
    ],
    done: ['Mọi bài có Ý định + Định dạng khớp với loại trang top 10', 'Đã ghi SERP và dùng câu hỏi thật làm H2/FAQ', '4 cổng QC PASS trước khi đăng', 'Bài đã đăng chấm ≥ 80 điểm theo intent'],
    cmd: 'chạy dây chuyền'
  },
  onpage: {
    step: 'Bước 7 · Create & Optimize', title: 'Tối ưu SEO Onpage — Title, Meta Description, Heading, URL, hình ảnh trên từng trang',
    goal: 'Mỗi URL của rootytrip.com đạt chuẩn ở 5 hạng mục, đúng với từ khoá chính của trang (lấy từ cột “Từ khoá chính” hoặc bảng Từ khoá ở B2/B3).',
    steps: [
      '<b>🏷️ Title</b>: dài <b>50–60 ký tự</b> (không bị cắt trên Google) · <b>từ khoá chính đặt gần đầu</b> · ngắn gọn, hấp dẫn, đúng nội dung · <b>thương hiệu ở cuối</b>. VD: <i>Tour 4 Đảo Phú Quốc: Giá, Lịch Trình 2026 | Rooty Trip</i>.',
      '<b>📄 Meta Description</b>: <b>120–160 ký tự</b> · tóm tắt nội dung, <b>chứa từ khoá chính</b> · có <b>lời kêu gọi hành động</b> tự nhiên (đặt qua Zalo, xem lịch trình, nhận ưu đãi…) để tăng tỷ lệ nhấp.',
      '<b>🔠 Heading</b>: <b>đúng 1 H1</b>, chứa từ khoá chính, gần giống Title (WordPress: tiêu đề bài = H1) · <b>H2, H3</b> chia ý chính/ý phụ, chứa từ khoá phụ hoặc liên quan (các từ khoá cùng nhóm URL ở B3).',
      '<b>🔗 URL</b>: ngắn gọn, <b>không dấu, viết thường, gạch ngang (-)</b> · <b>chứa từ khoá chính</b> · bỏ từ dư thừa (va, la, cua, thi…) và ngày tháng. VD: <code>/tour-4-dao-phu-quoc/</code>. Không đổi URL đang có traffic — nếu buộc đổi thì 301.',
      '<b>🖼️ Hình ảnh</b>: <b>tên file</b> không dấu, có gạch ngang, có nghĩa (<code>cap-treo-hon-thom.jpg</code>, không phải <code>IMG_1234.jpg</code>) · <b>alt</b> mô tả ngắn nội dung ảnh, có từ khoá ở vài ảnh, không nhồi nhét · <b>nén nhẹ, ưu tiên WebP</b>, ≤ 200KB.',
      '<b>Cách chấm</b>: "Chấm nhanh tất cả từ crawl" chấm Title, Meta, Heading (H1), URL cho mọi trang trong vài giây. "Chấm chi tiết trang quan trọng" tải từng trang (trang chủ, danh mục, Pillar, tour — tối đa 40) để chấm thêm H2/H3 và hình ảnh, kèm <b>gợi ý Title/Meta</b>. Hoặc bấm một dòng → "Chấm onpage trang này". Bấm thẻ hạng mục phía trên để lọc trang chưa đạt.',
      '<b>Sửa</b>: dán gợi ý Title/Meta vào plugin SEO (Rank Math/Yoast) — gợi ý là bản nháp, chỉnh lại cho tự nhiên; hoặc "Copy lệnh Claude viết lại" để Claude viết bản hoàn chỉnh. Sửa xong bấm chấm lại.',
      '<b>Thời điểm</b>: bài mới làm onpage 10–15 ngày sau khi đăng; trang cũ quan trọng làm ngay. Làm trang tour/danh mục/Pillar trước.'
    ],
    done: ['Trang quan trọng (trang chủ, danh mục, Pillar, tour) ≥ 85 điểm', 'Title 50–60 ký tự, có “| Rooty Trip”, không trùng', 'Meta 120–160 ký tự có lời kêu gọi trên mọi trang quan trọng', '≥ 80% ảnh WebP, tên file & alt chuẩn'],
    cmd: '/rooty-onpage https://rootytrip.com/tour-phu-quoc-tron-goi/'
  },
  entity: {
    step: 'Bước 8 · Create & Optimize', title: 'Tối ưu Entity — xác minh thực thể thương hiệu (social profiles, schema markup)',
    goal: 'Google hiểu rõ Rooty Trip là ai — một công ty lữ hành thật ở Phú Quốc, có hồ sơ chính thức nhất quán ở mọi nơi — để tăng độ uy tín (E-E-A-T, Knowledge Graph) và để AI trả lời đúng về Rooty.',
    steps: [
      '<b>① NAP gốc</b>: bấm "Lấy từ website" để điền Tên, Hotline, Địa chỉ, Website, Giờ mở cửa từ schema trang chủ → kiểm lại, bổ sung Logo URL, Email, Năm thành lập, Giấy phép lữ hành. Chọn <b>một hotline chính</b> dùng thống nhất mọi nơi.',
      '<b>② Tạo/chuẩn hoá social profiles</b>: Facebook Page, YouTube, Instagram, TikTok, LinkedIn, X (Twitter), Pinterest, Zalo OA. Tên, ảnh đại diện (logo), mô tả, hotline, địa chỉ, website giống hệt NAP gốc. Điền URL và Tên/Hotline/Địa chỉ đang hiển thị trên từng hồ sơ vào bảng.',
      '<b>Đồng bộ NAP</b>: bấm "Kiểm NAP các hồ sơ" — trang so Tên/Hotline/Địa chỉ của từng hồ sơ với NAP gốc → Khớp / Lệch (ghi rõ lệch ở đâu).',
      '<b>Liên kết chéo</b>: bấm "Quét liên kết chéo" — trang đọc trang chủ: có icon/link tới hồ sơ nào (<i>Web trỏ tới hồ sơ</i>), hồ sơ nào được khai báo trong schema <code>sameAs</code>, link có đúng là trang hồ sơ không (bắt lỗi kiểu icon TikTok trỏ về trang chủ TikTok), link trên web và trong sameAs có khớp nhau không. Ở mỗi hồ sơ, đặt link website trong bio/giới thiệu (<i>Hồ sơ trỏ về web</i> — mạng xã hội hay chặn kiểm tự động nên có thể phải kiểm tay).',
      '<b>③ Schema Markup JSON-LD</b>: trang sinh sẵn mã <b>TravelAgency</b> (loại LocalBusiness dành cho công ty lữ hành) + Organization với tên, logo, hotline, địa chỉ, giờ mở cửa, <b>sameAs</b> (mọi hồ sơ chính thức + Wikidata nếu có), kèm <b>WebSite</b> (có SearchAction nếu web có ô tìm kiếm) và <b>WebPage</b>. Danh sách "thiếu" cho biết schema hiện tại trên trang chủ còn thiếu gì. Copy mã → Rank Math → Schema (trang chủ) → kiểm bằng Rich Results Test.',
      '<b>④ Nguồn xác thực bên thứ ba</b>: <b>Google Business Profile</b> (xác minh địa chỉ văn phòng thật — quan trọng nhất), Bing Places, Apple Business Connect; danh bạ & citation: Trang Vàng, danh sách doanh nghiệp lữ hành của Cục Du lịch Quốc gia, Foursquare; nền tảng đánh giá: Tripadvisor, Klook, Traveloka. Đánh dấu "Đã xác minh" khi xong. Có báo chí nói về Rooty → ghi ở tab B9.',
      '<b>Thực thể & dữ kiện</b>: ghi các thực thể khác (điểm đến, tour chủ lực, HDV/tác giả) với thuộc tính có nguồn — dùng cho bài viết và schema Person/TouristTrip.'
    ],
    done: ['NAP gốc đủ, 1 hotline chính', 'Mọi hồ sơ chính “Đã có”, “Khớp” NAP, link 2 chiều với website', 'Không còn cảnh báo ⚠ ở bảng hồ sơ', 'Schema trang chủ hết mục “thiếu”, Rich Results Test không lỗi', 'Google Business Profile đã xác minh'],
    cmd: '/rooty-local-seo chuẩn hoá NAP và viết mô tả hồ sơ cho các nền tảng trong bảng Hồ sơ thương hiệu'
  },
  link: {
    step: 'Bước 9 · Promotion', title: 'Link Building — liên kết nội bộ & backlink',
    goal: 'Dẫn người đọc và Googlebot đi đúng tầng (trang chủ → danh mục → trang chi tiết), dồn “sức mạnh” SEO về trang tour/danh mục cần đẩy top, rồi xây “lá phiếu tín nhiệm” từ website uy tín cùng ngành du lịch.',
    steps: [
      '<b>⓪ Kế hoạch cho một trang cần lên top</b> (VD tour 3 đảo): chọn trang + từ khoá → “Lập kế hoạch link”. Trang dựng <b>silo kim tự tháp</b>: đỉnh = trang tour (chốt đơn) · giữa = danh mục + <b>bài trụ</b> (bài thông tin chính, VD “Tour 3 đảo có đáng đi?”) · đáy = <b>bài vệ tinh</b> (Hòn Móng Tay, Hòn Mây Rút, lặn san hô…). Vệ tinh → trụ + đích, trụ → đích, đích → trụ, vệ tinh nối ngang 1–2 bài cùng địa danh (“bánh xe nhỏ trong cụm” — được phép vì cùng chủ đề, có ích cho người đọc). Anchor theo tỉ lệ an toàn: chính xác ~15%, biến thể ~55%, thương hiệu ~10%, mô tả ~20% — không lặp một cụm cho mọi link. Link chỉ bằng “Đặt ngay!”/ảnh không truyền ý nghĩa → thêm 1 link chữ mô tả.',
      '<b>Bánh xe / kim tự tháp link kiểu cũ</b> (dựng site vệ tinh Web 2.0, blog phụ, PBN, tier 2–3 trỏ link về site chính): Google xếp vào <b>link spam</b> (xem tab B10 · Thuật toán Google) — không làm. Sức mạnh bên ngoài nên đến từ báo/blog du lịch thật, đối tác, Google Business Profile, review platform.',
      '<b>① Internal link — đọc bản đồ</b>: mỗi lần "Chạy crawl" (B5) trang ghi lại mọi link nội bộ kèm anchor và vị trí (nội dung / menu / footer / sidebar). Phần thống kê cho biết: link trong nội dung vs menu, <b>anchor chung chung</b> (“tại đây”, “xem thêm” — nên đổi thành anchor mô tả), link ảnh không alt, và <b>trang tour/danh mục/Pillar ít link trỏ vào nhất</b>.',
      '<b>Gợi ý link nội bộ</b>: bấm nút — trang đọc các bài blog, tìm <b>câu đã nhắc tới</b> tên tour/danh mục (theo từ khoá chính hoặc H1) mà chưa gắn link, ưu tiên 25 trang đích ít link nhất → mỗi gợi ý có bài nguồn, anchor và đúng câu cần gắn. Mở bài trên WordPress, gắn link vào câu đó, đổi trạng thái “Đã gắn”. Crawl lại để xác nhận.',
      '<b>Nguyên tắc</b>: anchor tự nhiên, chứa từ khoá của trang đích, đa dạng (không lặp y hệt); link theo tầng và theo cụm (bài con ↔ Pillar, bài con → 2–3 bài cùng cụm + 1 trang tour); 3–8 link/bài là vừa, không trỏ lan man; không link tới URL redirect/404.',
      '<b>② Backlink — chọn nguồn chất lượng</b>: ghi mỗi cơ hội với <b>Uy tín (DR/DA)</b> (từ Ahrefs/Moz), <b>Liên quan chủ đề</b> (du lịch, Phú Quốc, khách sạn = Cao), <b>Vị trí đặt</b> (trong nội dung giá trị hơn footer/sidebar). Trang tự tính <b>điểm chất lượng</b> 0–100.',
      '<b>Chiến lược</b>: <b>Guest post</b> trên blog du lịch có traffic · <b>Digital PR / báo chí</b> (câu chuyện HDV bản địa, số liệu khách của Rooty, sự kiện Phú Quốc) · <b>Broken link</b> (phần ③: tìm link gãy trên bài tổng hợp của site khác, đề xuất thay bằng bài Rooty) · <b>Linkable asset</b> (bảng chi phí Phú Quốc cập nhật, bản đồ điểm check-in, lịch show, công cụ tính chi phí — thứ người khác tự dẫn nguồn) · đối tác khách sạn/nhà hàng.',
      '<b>Kiểm định kỳ</b>: "Kiểm backlink còn sống" mở từng trang nguồn: còn link không, dofollow hay nofollow/sponsored, nằm trong nội dung hay footer, anchor thực tế → cập nhật “Đang live” / “Mất link”.',
      '<b>Anchor an toàn</b>: đa số anchor backlink là tên thương hiệu hoặc URL; anchor chứa từ khoá nên ≤ 30%. Không PBN, không mua link hàng loạt. Backlink đẩy mạnh khoảng tháng 6–8, sau khi nội dung lõi xong (cửa quyết định offsite).'
    ],
    done: ['Không trang tour/danh mục/Pillar nào < 3 link trong nội dung', 'Không còn anchor chung chung trong nội dung', 'Mọi gợi ý link nội bộ đã xử lý (Đã gắn / Bỏ)', 'Backlink kiểm mỗi tháng, ≥ 70% đang live, anchor từ khoá ≤ 30%'],
    cmd: '/rooty-lien-ket-noi-bo lập kế hoạch link cho cụm Tour đảo'
  },
  geo: {
    step: 'GEO · AI Search', title: 'Được ChatGPT, Gemini, AI Overview, Perplexity nhắc tên Rooty — Checklist GEO của GTV',
    goal: 'Website được AI chọn làm nguồn và nhắc tên Rooty Trip khi khách hỏi về du lịch Phú Quốc. GEO là phần cộng thêm của cùng một nền SEO: chưa lên trang 1 Google thì AI cũng chưa chọn mình.',
    steps: [
      '<b>G0 · Chấm mức & số nền (tháng 1)</b>: nạp bộ câu hỏi AI (30 câu, GTV khuyên 28–40: 50% sát lúc mua · 35% cân nhắc · 15% mới tìm hiểu) → đo lần đầu trên từng máy AI = <b>số nền</b>, ghi ngày + phiên bản mô hình. Nói trước với sếp 5 điều không hứa (không bán llms.txt, không coi schema là cách được trích, không hứa AI trả lời y hệt…).',
      '<b>G1 · Cho máy đọc được</b>: bot tìm nguồn của AI được vào (B5 · T25, T26, M04), máy chủ phản hồi nhanh (T17), canonical/index sạch (T11, T16), HTML ≤ 2MB, ~400 ký tự đầu sau H1 là đoạn mở đầu liền mạch — khối Tác giả/Ngày/Lượt xem không chen giữa.',
      '<b>G2 · Website là nguồn sự thật</b> 🔒: tự gõ <code>site:rootytrip.com</code> + 5–10 câu khách hay hỏi (giá, lịch trình, đón ở đâu, huỷ tour) — phải có trang trả lời bằng chữ trên site. Có đủ trang Giới thiệu, Bảng giá, FAQ, Chính sách. NAP & schema nhất quán (B8). Bài trọng điểm có tác giả thật và kinh nghiệm nằm trong nội dung.',
      '<b>G3 · Cấu trúc đoạn trong bài</b> (cài từ lúc viết, không vá sau): bấm “Chấm GEO 30 bài” hoặc mở một bài ở B6 → “Chấm GEO”. 4 cửa chặn 🔒: <b>#14</b> 100–150 từ đầu trả lời thẳng · <b>#15</b> H2 là câu hỏi thật, 1 trang 1 câu hỏi · <b>#16</b> câu đầu sau H2 là câu trả lời 40–50 từ đúng mẫu · <b>#17</b> mỗi mục cắt rời vẫn hiểu, không “điều này / như đã nói”, không H2 “Tổng quan / Kết luận”. Thêm: dữ kiện dạng câu trích được, nguồn + tháng/năm, thông tin chỉ Rooty có, cập nhật thật ~30 ngày cho trang giá.',
      '<b>G4 · Được nhắc ở nơi khác</b> (tháng 4–7): video YouTube đúng chủ đề, bài báo/blog du lịch đang lên top, review platform; có mặt trong 1/3 đầu các bài “top công ty tour Phú Quốc” mà AI đang trích — ghi ở B9. Được nhắc tên quan trọng hơn được đặt link.',
      '<b>G5 · Đo → báo cáo</b> (tháng 1, 6, 10 và mỗi quý): mỗi câu chạy ≥ 3 lần mỗi máy, dán câu trả lời vào ô đo → trang tự ghi nhắc tên / trích link / thứ tự / đối thủ. Báo theo chủ đề và theo máy AI, cảnh báo nếu > 70% lượt nhắc dồn vào một máy. Số đo AI chỉ tham khảo xu hướng — đối chiếu referral AI trong GA4 (B10) trước khi tuyên bố thắng.',
      '<b>Tự kiểm</b>: bấm “Tự kiểm từ dữ liệu” — 17 việc tự lấy kết quả từ B5, điểm chấm bài, GSC và các lần đo AI; việc thủ công (site: test, trang sự thật, offsite, quy tắc báo cáo) chị tự đổi “Trạng thái”.'
    ],
    done: ['Qua hết việc 🔒 cửa chặn (G0 #1–3, G2 #9, G3 #14–17)', 'Mọi bài trọng điểm điểm GEO ≥ 80 và qua 4 cửa chặn G3', 'Có số nền tháng 1 và đo lại tháng 6, 10 với cùng bộ câu hỏi, mỗi câu ≥ 3 lần/máy', 'Tỷ lệ nhắc tên Rooty theo chủ đề tăng so với số nền'],
    cmd: '/rooty-do-hien-dien-ai đo bộ câu hỏi tháng này'
  },
  gia: {
    step: 'Bước 6 · Create & Optimize', title: 'Giá & dữ kiện — một nguồn sự thật, đổi giá là biết bài nào phải sửa',
    goal: 'Mọi giá, giờ, lịch, khoảng cách dùng trong bài đều lấy từ một bảng có nguồn + ngày kiểm. Khi giá đổi, biết ngay bài nào đang ghi giá cũ để sửa — đây cũng là cách cập nhật “độ mới thật” thay vì chỉ đổi năm trên tiêu đề.',
    steps: [
      '<b>Lấy giá gốc</b>: bấm “Lấy giá từ trang sản phẩm Rooty” — đọc giá trong schema của mọi trang tour/combo (tab B3 cần có trang từ crawl). Bấm lại mỗi tuần/tháng: giá nào khác lần trước sẽ tự ghi “Giá cũ” + lịch sử và chuyển trạng thái “Đã đổi — dò lại bài”.',
      '<b>Thêm tay</b> dữ kiện không có trên trang sản phẩm (giá vé cáp treo, VinWonders, giờ show, lịch tàu…): “+ Thêm”, ghi nguồn chính thức + ngày kiểm, điền “Từ khoá tìm trong bài” (mỗi dòng một cách gọi, VD “cáp treo Hòn Thơm”, “vé cáp treo”).',
      '<b>Đổi giá</b>: bấm dòng → sửa “Giá trị” → Lưu. Trang tự lưu giá cũ + lịch sử (ngày: cũ → mới).',
      '<b>Dò bài</b>: “Dò bài đang ghi giá” đọc toàn bộ blog, tìm câu nhắc dữ kiện kèm giá. ✅ = ghi đúng giá hiện tại · ❌ = ghi khác → tạo việc “Giá cũ” ở B5 · Sửa lỗi từng trang với “Cần sửa gì” (đổi số nào thành số nào, ở câu nào). Lưu ý giá trẻ em / gói khác cũng bị báo — người xem lại, đúng thì chọn “Không phải lỗi”.',
      '<b>Sửa xong</b>: ở B5 chuyển “Đã sửa” → “Kiểm lại trang” (máy mở bài xem còn giá cũ không) → sau 4 tuần “Đo hiệu quả”. Bài viết mới: lấy giá từ bảng này, ghi “giá cập nhật tháng MM/YYYY”.'
    ],
    done: ['Mọi giá dùng trong bài có trong bảng, có nguồn + ngày kiểm', 'Không dữ kiện nào quá hạn kiểm lại', 'Không còn bài “Giá cũ” chưa xử lý'],
    cmd: '/rooty-fact-check kiểm lại giá trong bài theo bảng Giá & dữ kiện'
  },
  chandoan: {
    step: 'Chẩn đoán', title: 'Chẩn đoán rớt top — một nút, 4 bước, có kiểm chứng',
    goal: 'Khi web rớt top: biết rớt từ ngày nào, có trùng đợt cập nhật của Google không, lỗi nào trên blog đang có thật (ĐÃ KIỂM) và lỗi nào chỉ là nghi vấn, rồi sửa theo thứ tự có lợi nhất.',
    steps: [
      '<b>Trước khi chạy</b>: nhập GSC file <i>Ngày</i> (6 tháng) ở tab B10 — không có số liệu này thì báo cáo chỉ liệt kê lỗi đang có, chưa nói được lỗi nào là nguyên nhân rớt.',
      '<b>Bấm “Chẩn đoán rớt top”</b> (2–3 phút, chạy nền). ① tìm ngày bắt đầu rớt (TB 7 ngày giảm > 20% so với đỉnh) · ② đối chiếu với core/spam update chính thức · ③ quét toàn bộ bài blog mọi ngôn ngữ qua WordPress REST API + HTML: 8 loại lỗi, kèm GEO và chính sách spam · ④ xếp thứ tự sửa.',
      '<b>Đọc nhãn</b>: [ĐÃ KIỂM] = đo chính xác (đổi năm giả, link tự thân, bài mỏng/đã gộp, tác giả) · [NGHI VẤN] = máy đoán (thiếu trải nghiệm, lạc chủ đề, trùng từ khoá, thương mại) — người đọc lại bài trước khi sửa, sai thì chọn “Không phải lỗi”.',
      '<b>Sửa</b>: lỗi của rootytrip.com tự nạp vào B5 · Sửa lỗi từng trang (mỗi dòng có “Cần sửa gì”). Chạy lại chẩn đoán sau khi sửa: lỗi đã kiểm mà không còn thấy sẽ tự chuyển “Hết lỗi”.',
      '<b>Website khác</b> (WordPress): nhập tên miền vào ô trên — ra báo cáo nhưng không nạp vào bảng sửa lỗi của Rooty.',
      '<b>Gõ một câu với Claude Code</b>: “rootytrip đang rớt top, tìm lý do” → skill /rooty-chan-doan chạy đúng quy trình này rồi đọc lại các bài nghi vấn hàng đầu để xác nhận.'
    ],
    done: ['Biết ngày bắt đầu rớt và có trùng đợt cập nhật nào không', 'Mọi lỗi NGHI VẤN ưu tiên cao đã được người đọc xác nhận', 'Lỗi top 3 đã giao người sửa + hạn, có mốc đo trước/sau'],
    cmd: 'rootytrip đang rớt top, tìm lý do'
  },
  kiemweb: {
    step: 'Bước 5 · Improving', title: 'Kiểm nhiều website / nhiều trang cùng lúc',
    goal: 'Dán một lúc nhiều website (site công ty, site vệ tinh, đối thủ, khách) hoặc nhiều link bài — trang tự kiểm song song và ra danh sách lỗi cần sửa cho từng địa chỉ.',
    steps: [
      '<b>Dán danh sách</b>: mỗi dòng một địa chỉ, tối đa 50/lần. Chỉ tên miền → kiểm toàn site (34 mục tự động giống tab B5: robots, sitemap, HTTPS/HSTS, tốc độ phản hồi, Core Web Vitals nếu có khoá PageSpeed, bot AI, canonical, hreflang, schema, NAP, ô tìm kiếm, GA4, ảnh…). Link có đường dẫn → kiểm một trang (chấm GEO 11 tiêu chí + onpage).',
      '<b>Ghi nhóm</b> (VD “Đối thủ”, “Site vệ tinh”) để lọc và so sánh. Bấm “Kiểm tất cả cùng lúc” — chạy nền, 4 địa chỉ song song, có thể chuyển tab khác.',
      '<b>Đọc kết quả</b>: sắp từ điểm thấp nhất. Bấm một dòng → “Lỗi cần sửa” xếp 🔴 trước, “Chi tiết” có từng mục ✅/❌. Site đối thủ: dùng để biết họ làm tốt gì mà mình chưa có.',
      '<b>Theo dõi</b>: sửa xong bấm “Kiểm lại” trên dòng đó; Xuất CSV để gửi dev hoặc khách.',
      'Lưu ý: kiểm toàn site chỉ đọc trang chủ + robots + sitemap (không crawl hết). Muốn crawl sâu một site (trang mồ côi, link hỏng, độ sâu) → đặt SITE_URL trong .env và dùng tab B5 · Audit.'
    ],
    done: ['Mọi site của công ty ≥ 80%', 'Không còn lỗi 🔴 ở site nào', 'Có bảng so sánh với đối thủ chính'],
    cmd: '/rooty-ky-thuat đọc kết quả tab Kiểm nhiều website và lập danh sách việc cho dev theo từng site'
  },
  algo: {
    step: 'Bước 10 · Evaluate', title: 'Theo dõi thuật toán Google — lên top bền mà không vi phạm',
    goal: 'Biết ngay khi Google tung đợt cập nhật, đo xem Rooty bị ảnh hưởng không, và giữ mọi cách làm SEO nằm trong chính sách của Google để không bị hạ hạng hay phạt.',
    steps: [
      '<b>Nguồn tin</b>: chỉ tin nguồn chính thức — Google Search Status Dashboard (ngày bắt đầu/kết thúc core update, spam update, sự cố) và blog Google Search Central. Trang tự lấy lại mỗi 24 giờ khi mở app; bấm “Lấy tin mới từ Google” để lấy ngay. Tin từ hội nhóm/tool “nhiệt kế SERP” chỉ để tham khảo.',
      '<b>Khi có đợt đang triển khai</b> (banner đỏ): không sửa site vội — thứ hạng dao động 1–3 tuần là bình thường. Ghi lại mọi thay đổi lớn trong Change log (B10) để không lẫn nguyên nhân.',
      '<b>Khi đợt xong 1–2 tuần</b>: nhập GSC file Ngày + Trang ở B10 → bấm “Lấy tin mới” để đo lại ảnh hưởng (14 ngày trước vs 14 ngày sau). Giảm ≥ 10%: xem trang nào giảm (B10 · Content audit), đọc “Việc cần làm” của đợt đó, ghi “Kết luận”, chọn “Đã review”. Du lịch có mùa vụ — so thêm cùng kỳ năm trước.',
      '<b>Chính sách spam</b>: bấm “Tự kiểm từ dữ liệu” mỗi tháng. Ưu tiên sửa mục “Vi phạm — cần sửa” và “Có rủi ro” trước khi làm nội dung mới. Kiểm GSC → Bảo mật & Thao tác thủ công mỗi tuần.',
      '<b>Lên top nhanh mà sạch</b>: đẩy trang vị trí 8–20, sửa Title/Meta cho CTR, link nội bộ về trang cần lên, sửa lỗi 🔴, viết đúng ý định có trải nghiệm thật, được nhắc tên ở nơi khác. Mỗi việc ghi Change log + đo trước/sau.',
      '<b>Hằng tuần</b>: đọc tin “Quan trọng chưa đọc” (chính sách, AI Overview/AI Mode, core update), ghi việc cần làm cho Rooty.'
    ],
    done: ['Mọi đợt core/spam đã review và có kết luận', 'Không còn chính sách nào “Vi phạm — cần sửa”', 'Không có thao tác thủ công trong Search Console', 'Không còn tin quan trọng chưa đọc'],
    cmd: '/rooty-bao-cao đợt cập nhật thuật toán gần nhất ảnh hưởng Rooty thế nào'
  },
  danhgia: {
    step: 'Bước 10 · Evaluate', title: 'Review — audit & lên phương án cải thiện (GSC, GA4, định kỳ hàng quý)',
    goal: 'Đo xem SEO có đạt mục tiêu về thứ hạng, traffic và chuyển đổi không; phát hiện sớm lỗi kỹ thuật, biến động thuật toán, trang sụt giảm; rồi quyết định giữ / cập nhật / gộp / xoá từng URL và lên việc cho quý sau.',
    steps: [
      '<b>① Nhập số liệu</b> (một nút, tự nhận loại file): GSC → Hiệu suất → chọn khoảng thời gian → Xuất → CSV: file <b>Ngày</b> (số liệu tháng + cảnh báo tuần), <b>Trang</b> (từng URL), <b>Truy vấn</b> (thứ hạng từ khoá, tự cập nhật bảng B2). GA4 → Báo cáo → Tương tác → <b>Trang đích</b>, thêm bộ lọc Nhóm kênh = Organic Search → Tải CSV (phiên, tỷ lệ tương tác, sự kiện chính). Ghi "Kỳ số liệu" (VD 3 tháng gần nhất) trước khi nhập.',
      '<b>② Chỉ số GSC</b>: thứ hạng (vị trí TB), <b>CTR</b> (sức hút Title/Meta), hiển thị & lượt nhấp, lỗi lập chỉ mục (GSC → Trang: ghi số trang lỗi vào dòng tháng). <b>Chỉ số GA4</b>: phiên & người dùng organic, <b>tỷ lệ tương tác</b> (ngược với tỷ lệ thoát), thời gian tương tác TB, <b>tỷ lệ chuyển đổi</b> (bấm Zalo, gọi, gửi form). Thẻ KPI so với tháng trước; du lịch có mùa vụ nên so thêm cùng kỳ năm trước.',
      '<b>Hàng tuần</b>: xuất GSC Ngày → nhập → banner so 7 ngày gần nhất với 7 ngày trước (giảm ≥ 20% sẽ cảnh báo) · kiểm lỗi index mới · kiểm backlink mất (B9).',
      '<b>③ Xung đột từ khoá</b>: cần file Truy vấn × Trang (cài add-on "Search Analytics for Sheets" cho Google Sheets, hoặc Looker Studio nối GSC, xuất cột query, page, clicks, impressions, position) → trang liệt kê từ khoá có ≥ 2 trang Rooty cạnh tranh, gợi ý trang nên giữ.',
      '<b>④ Content audit hàng quý</b>: nhập GSC Trang (3 tháng) + GA4 Trang đích → "Phân loại content audit". Luật: <b>Giữ</b> = ≥ 30 nhấp, top 10, tương tác tốt · <b>Cập nhật/viết lại</b> = nhiều hiển thị nhưng vị trí 8–30, CTR thấp so với vị trí, tương tác thấp, hoặc trang bán ít traffic · <b>Gộp</b> = bài mỏng, ít nhấp, trùng chủ đề · <b>Xoá/301 hoặc Noindex</b> = 0 nhấp, < 50 hiển thị trong kỳ, nội dung ngắn (không áp dụng cho trang tour/danh mục). Duyệt cột "Quyết định" → "Tạo việc cập nhật" đưa 15 trang nhiều hiển thị nhất sang tab Content.',
      '<b>Audit kỹ thuật hàng quý</b>: tab B5 (tốc độ, Core Web Vitals, mobile, URL, uptime hosting) — chạy crawl + kiểm tự động + 16 mục kiểm tay.',
      '<b>⑤ Change log</b>: mỗi lần sửa một trang thêm 1 dòng (ngày, URL, sửa gì). "Đo lại hiệu quả" ghi lượt nhấp/vị trí trước (trong 7 ngày đầu) và sau (từ tuần thứ 4) → Tốt lên / Không đổi / Giảm. Cần nhập GSC Trang mới trước khi đo.',
      '<b>⑥ Lịch review</b>: nạp 13 việc mẫu tuần/tháng/quý; bấm "Đã làm hôm nay" sau mỗi lần — việc quá hạn hiện viền đỏ. Cuối quý: lập danh sách việc cho quý sau (tab Kế hoạch 10 tháng) và review KPI.'
    ],
    done: ['Số liệu tháng đủ GSC + GA4, có nhận xét & việc tháng sau', 'Không có việc review quá hạn', 'Mỗi quý: content audit có quyết định cho mọi trang có số liệu, xung đột từ khoá đã xử lý', 'Mọi thay đổi lớn có trong change log và đã đo lại'],
    cmd: '/rooty-bao-cao báo cáo tháng này từ số liệu đã nhập ở tab B10'
  },
  kehoach: {
    step: 'Quản lý', title: 'Kế hoạch 10 tháng — 37 công đoạn',
    goal: 'Lộ trình đầy đủ theo tháng: việc nào làm lúc nào, ai làm, đã xong chưa. Viền xanh = đang trong hạn tháng này, viền đỏ = trễ.',
    steps: [
      'Lần đầu bấm "Nạp công đoạn". Đặt tháng bắt đầu dự án trong file <code>.env</code>: <code>PROJECT_START=2026-11</code>.',
      'Bấm một dòng để giao người, đặt hạn, ghi kết quả, mở SOP hoặc copy lệnh cho Claude.',
      'Các dòng "◇ CỬA" là điểm phải quyết định trước khi đi tiếp.'
    ],
    done: ['Mỗi tháng: không còn việc trễ chưa có lý do'],
    cmd: '/rooty-ke-hoach-seo tháng này làm gì'
  }
};
