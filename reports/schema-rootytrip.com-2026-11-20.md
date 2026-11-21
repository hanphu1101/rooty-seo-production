# Kiểm schema rootytrip.com · 20/11/2026

Em quét HTML thật của 931 URL trong bảng Trang (mọi ngôn ngữ). Danh sách đầy đủ từng trang (loại schema, schema chèn tay, vấn đề) nằm trong file `schema-rootytrip.com-2026-11-20.csv`, mở bằng Excel được. Các trang có vấn đề xếp đầu file.

> Nhắc lại: schema giúp Google hiểu đúng thực thể, nhưng **không phải cách để được AI trích dẫn** (CLAUDE.md, mục «5 điều không hứa»).

## 1. Trang chủ — hiện trạng và chỗ sai

Trang chủ đang có **2 khối JSON-LD**:

| Khối | Nguồn | Gồm |
|---|---|---|
| 1 | Rank Math tự sinh | Place · Organization `#organization` · WebSite · ImageObject · **WebPage** |
| 2 | Đoạn chèn tay (khả năng cao ở ô Header Script của trang chủ, giống trang tác giả) | **TravelAgency `#organization`** · FAQPage · **BreadcrumbList** |

Đối chiếu góp ý:

1. **TravelAgency trùng @id `#organization` với Organization của Rank Math.** Google sẽ gộp 2 node khác loại thành một thực thể, không rõ là gì. Cách sửa: Organization giữ `#organization` (các trang khác như trang tác giả đang trỏ `worksFor` về id này), còn TravelAgency có @id riêng.
2. **BreadcrumbList ở trang chủ** có 9 mục, liệt kê menu chứ không phải đường dẫn. Trang chủ không cần breadcrumb, nên bỏ. Thêm vào đó, 7/9 URL trong khối này bị chuyển hướng (301) hoặc 404 (`/combo-phu-quoc/`).
3. **WebPage mặc định của Rank Math:** bỏ, thay bằng **CollectionPage**. Trang chủ là trang gom các nhóm tour, combo và vé.
4. **Organization thiếu thuộc tính, cần LocalBusiness.** Giờ mở cửa, giá, toạ độ, cách thanh toán là thuộc tính của LocalBusiness, không phải Organization. Nên tách ra **2 TravelAgency** (TravelAgency là một loại LocalBusiness), mỗi cái gắn với một địa điểm: trụ sở Phú Quốc và chi nhánh TP.HCM, cùng trỏ `parentOrganization` về Organization.

Các lỗi khác trong khối chèn tay:

- **Giờ mở cửa** ghi 06:00–23:30, nhưng chân trang web ghi «Giờ hỗ trợ: 7:30 – 21:00 hằng ngày». Bản mới dùng 7:30–21:00 theo chân trang.
- **Logo** là file `.svg`. Google cần ảnh PNG/JPG/WebP (tối thiểu 112×112 px). Cần tải lên một logo PNG.
- **alternateName** có 7 tên, gồm cả «công ty Rooty Trip», «cty rooty trip». Đây là nhồi từ khoá vào tên. Bản mới chỉ giữ «Rooty Trip Phú Quốc».
- **description** là câu quảng cáo («Bạn muốn du lịch Phú Quốc?…»). Bản mới mô tả sự thật: công ty lữ hành tại Phú Quốc, thành lập năm 2018, làm những gì.
- **founder** để lộ ngày sinh và email cá nhân của anh Hậu. Không cần thiết, và là dữ liệu cá nhân. Bản mới chỉ trỏ về `https://rootytrip.com/ceo/#person`, đã có sẵn trên trang /ceo/.
- **sameAs**:
  - Link `linkedin.com/in/rootytrip/` là dạng hồ sơ cá nhân và không mở được.
  - `gab.com/rootytrip` trả lỗi 403.
  - `twitter.com` đã chuyển sang `x.com`.
  - Link YouTube cũ `@RootyTrip` là kênh **«Rooty Trip Backup»**. Kênh chính là `@RootyTripPhúQuốc` (chị Hân xác nhận 20/11/2026), bản mới đã đổi.
  - Bản mới bỏ 2 link lỗi. Nên thêm link Google Maps, TikTok, Instagram nếu có.
- **hasOfferCatalog** trỏ `/ticket/`, trang này **404**. Trang đúng là `/ve-tham-quan/`.
- **FAQPage:** 2 câu hỏi trong schema **không hiện trên trang**. Google yêu cầu nội dung FAQ phải hiển thị cho người xem, và từ 2023 chỉ hiện FAQ dạng rich result cho trang chính phủ và y tế. Bỏ, hoặc thêm khối FAQ thật lên trang.
- **Tên thương hiệu:** Rank Math ghi «Rooty Trip», khối tay ghi «Rooty Trip Phú Quốc». Bản mới chốt **Rooty Trip** làm tên chính, như `00-context/brand.md` đã đề nghị. Chị đổi nếu muốn chọn tên khác.

## 2. Schema trang chủ đề xuất

> **Cập nhật 21/11/2026 — thay cho các ghi chú bên dưới.** Theo góp ý: trang chủ **không** dùng CollectionPage/ItemList/BreadcrumbList/FAQPage/WebPage; chi nhánh khai bằng `subOrganization` trong TravelAgency `#travelagency`, **không** dùng `parentOrganization` hay `department`. File `schema-trang-chu-moi.json` đã sửa theo đúng cấu trúc này. Trên web đang chạy bản của chị Hân (`schema-han.txt`), WebPage Rank Math đã tắt (WPCode #86933). Quét lại 931 trang ngày 21/11: **0 trang có vấn đề**.

*Sửa lại ngày 20/11/2026 theo góp ý thứ hai: giữ Organization, WebSite, Place của Rank Math; chỉ tắt WebPage.*

File `schema-trang-chu-moi.json` là **khối chèn tay mới**, đã kiểm JSON hợp lệ. Bản cập nhật 20/11/2026: chị Hân chọn @type Organization, gửi logo và link Maps của 2 cửa hàng. Gồm:

- **Organization** `#travelagency`: thực thể công ty. Có logo PNG 512×512, mô tả, liên hệ, mạng xã hội (YouTube kênh chính), người sáng lập, danh mục sản phẩm; trỏ `department` sang 2 cửa hàng.
- **TravelAgency** `#travelagency-phu-quoc`: trụ sở 191 Trần Hưng Đạo. Toạ độ lấy theo Google Maps (10.18665, 103.96939); toạ độ cũ lệch khoảng 2,5 km. Có link Maps, giờ mở cửa, giá, thanh toán.
- **TravelAgency** `#travelagency-hcm`: chi nhánh Tầng 5 Lite The Gateway, có link Maps.
- **CollectionPage** `#collectionpage`: kèm ItemList 4 nhóm sản phẩm.

Hai cửa hàng trỏ `parentOrganization` về `#travelagency`. Không còn BreadcrumbList và FAQPage.

Sau khi gắn, trang chủ sẽ có: Organization, WebSite, Place, ImageObject (của Rank Math) và Organization `#travelagency`, TravelAgency ×2, CollectionPage (khối tay).

File đã điền đủ logo và link Maps, không còn chỗ trống nào. Nên kiểm thêm: số điện thoại chi nhánh TP.HCM (0933 555 222, theo chân trang) và chi nhánh TP.HCM có mở cửa 7:30–21:00 không.

**Cách gắn:**
1. Thay toàn bộ khối chèn tay cũ (TravelAgency + FAQ + Breadcrumb) bằng nội dung file mới, bọc trong `<script type="application/ld+json">…</script>`.
2. Tắt **riêng WebPage** của Rank Math ở trang chủ, các phần khác của Rank Math giữ nguyên. Thêm đoạn PHP sau trong WPCode (loại PHP Snippet, chạy mọi nơi):
   ```php
   add_filter( 'rank_math/json_ld', function ( $data ) {
       if ( is_front_page() ) {
           unset( $data['WebPage'] );
       }
       return $data;
   }, 99 );
   ```
3. Xoá cache WP Rocket, rồi kiểm bằng https://validator.schema.org và https://search.google.com/test/rich-results.
   Nếu trang chủ vẫn còn WebPage, nghĩa là bản Rank Math này đặt tên khoá khác. Báo em để chỉnh.
4. Nên bổ sung cho Organization của Rank Math (Rank Math → Titles & Meta → Local SEO): logo PNG, tên thống nhất «Rooty Trip», và các trang mạng xã hội (Social Meta).

## 3. Các trang khác cần sửa

| Vấn đề | Số trang | Mức | Cách sửa |
|---|---|---|---|
| **Khối FAQ lỗi cú pháp**: thừa dấu `}` ở cuối nên Google bỏ cả khối | 29 (22 VI, 6 EN, 1 KO) | Cao | Xoá dấu `}` thừa cuối khối, hoặc xoá khối nếu FAQ không hiện trên trang |
| **TravelAgency dùng @id `#website`** trùng với WebSite: trang danh mục tour/combo (3n2d, 4n3d, trong ngày, EN/KO packages) | 11 | Cao | Đổi @id thành `#travelagency-phu-quoc` (hoặc chỉ tham chiếu `{"@id": "https://rootytrip.com/#organization"}`), bỏ bản sao WebSite trong khối tay |
| **Product không có offers** (giá): tour/khách sạn «Liên hệ» | 71 (31 VI, 32 EN, 8 ngôn ngữ khác) | Vừa | Nhập giá cho sản phẩm trong WooCommerce; khách sạn không bán giá cố định thì đổi loại schema sang `Hotel`/`Service` thay vì `Product` |
| **FAQPage có câu hỏi không hiện trên trang** | 8 | Vừa | Thêm FAQ thật lên trang hoặc bỏ schema FAQ |
| **CreativeWorkSeries kèm điểm sao tự chấm** (4.8/5, 31 lượt) trên bài blog: cafe Phú Quốc, thuê xe máy, tour 3 đảo có đáng đi không + 2 bài EN | 5 | Cao | **Bỏ.** Điểm sao không gắn với đánh giá thật hiện trên trang là vi phạm hướng dẫn đánh giá của Google, có thể bị phạt thủ công |
| Node không có `@type` trên trang từ khoá sản phẩm EN (`/en/tu-khoa-san-pham/…`) | 84 | Thấp | Do Rank Math; đặt các trang taxonomy này noindex hoặc tắt schema cho taxonomy |

Schema chèn tay đang có ở các trang (ngoài Rank Math):

- TravelAgency: trang chủ, `/en/`, 6 trang liên hệ (VI/EN/KO/JA/RU/ZH), 13 trang danh mục tour/combo, 2 bài khách sạn gần biển
- FAQPage: trang chủ, `/chua-ho-quoc-phu-quoc/`, `/dia-diem-check-in-phu-quoc/`, `/kinh-nghiem-du-lich-vinwonders-phu-quoc/`, `/resort-5-sao-phu-quoc/`, `/san-ho-la-dong-vat-hay-thuc-vat/`, `/taxi-phu-quoc/`, `/en/marriage-proposal/`, `/en/things-to-do-in-phu-quoc/`. Cộng với 29 bài có khối FAQ hỏng nói ở trên.
- CreativeWorkSeries (sao tự chấm): 5 bài nói ở trên
- TouristAttraction: `/en/aquatopia-water-park/`

Danh sách URL từng nhóm: lọc cột «Vấn đề» trong file CSV.
