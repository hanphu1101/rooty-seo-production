<?php
/*
 * BẢN NHÁP — CHƯA CÀI LÊN WEB. WPCode · loại PHP Snippet · chạy mọi nơi.
 * Ưu đãi nhóm tour ghép: giảm thêm 50.000 × (số vé quy đổi − 4), trẻ em = ½ vé.
 * Công thức giống reports/uu-dai-nhom/uu-dai-nhom.js (đã có bộ thử).
 *
 * Theme Mona thêm tour vào giỏ ở Product::product_type_tour() và ghi tổng tiền vào
 * dữ liệu dòng giỏ hàng (m_total); đơn hàng lấy m_total đó ở
 * custom_checkout_create_order_line_item(). Đoạn này chạy SAU theme (ưu tiên 99)
 * và trừ ưu đãi nhóm vào m_total.
 *
 * CẦN KIỂM TRÊN BẢN THỬ trước khi cài: tên khoá trong dữ liệu giỏ hàng
 * (m_total, qty_peole, qty_child, type tour ghép/riêng) — em đọc được tên biến
 * trong code theme nhưng chưa thấy dữ liệu giỏ hàng thật.
 */

const ROOTY_UDN_TOURS = array( 514, 30393, 17774, 31814 ); // G4, G2, G2 (trang trùng), G2CHONTHOM
const ROOTY_UDN_GIAM  = 50000;

function rooty_udn_giam_them( $nguoi_lon, $tre_em ) {
	$ve = (float) $nguoi_lon + (float) $tre_em / 2;
	return $ve > 4 ? (int) round( ( $ve - 4 ) * ROOTY_UDN_GIAM ) : 0;
}

add_filter( 'woocommerce_add_cart_item_data', function ( $data, $product_id ) {
	if ( ! in_array( (int) $product_id, ROOTY_UDN_TOURS, true ) || ! isset( $data['m_total'] ) ) {
		return $data;
	}
	// Chỉ tour ghép. CẦN KIỂM: khoá lưu loại gói (ghép/riêng) trong $data.
	if ( isset( $data['type_tour'] ) && false === stripos( (string) $data['type_tour'], 'ghép' ) ) {
		return $data;
	}
	$giam = rooty_udn_giam_them( $data['qty_peole'] ?? 0, $data['qty_child'] ?? 0 );
	if ( $giam > 0 && empty( $data['rooty_udn_giam'] ) ) {
		$data['m_total']        = (int) $data['m_total'] - $giam;
		$data['rooty_udn_giam'] = $giam; // để hiện trên giỏ hàng và tránh trừ 2 lần
	}
	return $data;
}, 99, 2 );

// Hiện dòng ưu đãi trong giỏ hàng / trang thanh toán / đơn hàng
add_filter( 'woocommerce_get_item_data', function ( $rows, $item ) {
	if ( ! empty( $item['rooty_udn_giam'] ) ) {
		$rows[] = array(
			'name'  => 'Ưu đãi nhóm (từ vé thứ 5)',
			'value' => '−' . number_format( $item['rooty_udn_giam'], 0, ',', '.' ) . 'đ',
		);
	}
	return $rows;
}, 10, 2 );

add_action( 'woocommerce_checkout_create_order_line_item', function ( $line, $key, $values ) {
	if ( ! empty( $values['rooty_udn_giam'] ) ) {
		$line->add_meta_data( 'Ưu đãi nhóm (từ vé thứ 5)', '−' . number_format( $values['rooty_udn_giam'], 0, ',', '.' ) . 'đ' );
	}
}, 99, 3 );

/*
 * BƯỚC 2 (đề xuất, làm riêng): máy chủ tự lấy đơn giá trong sản phẩm thay vì tin số
 * trình duyệt gửi lên (hiện khách rành kỹ thuật sửa được giá trước khi thanh toán).
 * Cần tên trường lặp lưu giá trong sản phẩm (single-product.php đọc $item['price_…'],
 * $item['price_child_…']) — kiểm trên bản thử rồi mới viết.
 */
