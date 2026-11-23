<?php
/*
 * WPCode · PHP Snippet · chạy mọi nơi (Run Everywhere).
 * Ưu đãi nhóm tour ghép (CSBH khách lẻ, wiki 02.1 / 02.2 / 02.8):
 *   số vé quy đổi = người lớn + trẻ em ÷ 2; đơn giá web đã trừ sẵn 100.000/NL, 50.000/TE,
 *   từ vé thứ 5 giảm thêm 50.000/vé → giảm thêm = 50.000 × (vé quy đổi − 4).
 * Công thức giống reports/uu-dai-nhom/uu-dai-nhom.js (bộ thử 14 ca).
 *
 * Luồng theme Mona (đọc code 23/11/2026):
 *   - Trang tour: modules/default.js update_price_tour() tính «Tổng» = NL × giá + TE × giá TE + phụ thu,
 *     ghi vào .price-main-combo (text + data-price_total). Popup xác nhận và form CF7 lấy số này.
 *   - Nút «Thanh toán ngay» gọi ajax created_order_fake: máy chủ tự tính lại tiền từ giá lưu trong
 *     sản phẩm (không tin số trình duyệt), tạo đơn WooCommerce chờ thanh toán, trả link thanh toán.
 * Đoạn này: (1) sửa ô «Tổng» trên trang tour; (2) sau khi theme tạo đơn, trừ ưu đãi nhóm vào đơn.
 *
 * CHẾ ĐỘ THỬ: rooty_udn_bat() chỉ trả true cho admin → khách thấy và trả như cũ.
 * Khi chị Hân duyệt: đổi thân hàm rooty_udn_bat() thành `return true;`.
 */

if ( ! function_exists( 'rooty_udn_bat' ) ) {
	function rooty_udn_bat() {
		return current_user_can( 'manage_options' ); // CHẾ ĐỘ THỬ — chỉ admin
	}
}

if ( ! function_exists( 'rooty_udn_tours' ) ) {
	// id sản phẩm tiếng Việt: G4 3 đảo, G2 4 đảo + cáp, G2 trang trùng, G2CHONTHOM cáp treo Hòn Thơm
	function rooty_udn_tours() {
		return array( 514, 30393, 17774, 31814 );
	}
}

if ( ! function_exists( 'rooty_udn_giam_them' ) ) {
	function rooty_udn_giam_them( $nguoi_lon, $tre_em ) {
		$ve = (float) $nguoi_lon + (float) $tre_em / 2;
		return $ve > 4 ? (int) round( ( $ve - 4 ) * 50000 ) : 0;
	}
}

if ( ! function_exists( 'rooty_udn_id_vi' ) ) {
	function rooty_udn_id_vi( $id ) {
		return (int) apply_filters( 'wpml_object_id', (int) $id, 'product', true, 'vi' );
	}
}

if ( ! function_exists( 'rooty_udn_la_tour_ghep' ) ) {
	function rooty_udn_la_tour_ghep( $nhan ) {
		return (bool) preg_match( '/gh[eé]p|join|shared/iu', wp_strip_all_tags( (string) $nhan ) );
	}
}

// (2) Đơn hàng: ghi nhận đơn do created_order_fake tạo ra …
add_action( 'woocommerce_new_order', function ( $order_id ) {
	if ( wp_doing_ajax() && isset( $_POST['action'] ) && 'created_order_fake' === $_POST['action'] ) {
		$GLOBALS['rooty_udn_order'] = (int) $order_id;
	}
} );

// … và trừ ưu đãi sau khi theme tính xong (theme kết thúc bằng wp_send_json → shutdown vẫn chạy).
add_action( 'shutdown', function () {
	if ( empty( $GLOBALS['rooty_udn_order'] ) || ! rooty_udn_bat() ) {
		return;
	}
	$d = array();
	parse_str( wp_unslash( isset( $_POST['formData'] ) ? (string) $_POST['formData'] : '' ), $d );
	if ( ! in_array( rooty_udn_id_vi( isset( $d['proId'] ) ? $d['proId'] : 0 ), rooty_udn_tours(), true ) ) {
		return;
	}
	if ( ! rooty_udn_la_tour_ghep( isset( $d['typeCombo'] ) ? $d['typeCombo'] : '' ) ) {
		return;
	}
	$giam = rooty_udn_giam_them( isset( $d['qtyAdult'] ) ? $d['qtyAdult'] : 0, isset( $d['qtyChild'] ) ? $d['qtyChild'] : 0 );
	$order = $giam > 0 ? wc_get_order( $GLOBALS['rooty_udn_order'] ) : false;
	if ( ! $order || $order->get_meta( '_rooty_udn_giam' ) ) {
		return;
	}
	$nhan = '−' . number_format( $giam, 0, ',', '.' ) . 'đ';
	foreach ( $order->get_items() as $item ) {
		$item->set_subtotal( max( 0, (float) $item->get_subtotal() - $giam ) );
		$item->set_total( max( 0, (float) $item->get_total() - $giam ) );
		$item->add_meta_data( 'Ưu đãi nhóm (từ vé thứ 5)', $nhan, true );
		$item->save();
		break; // đơn tour chỉ có 1 dòng sản phẩm
	}
	$order->set_total( max( 0, (float) $order->get_total() - $giam ) );
	$order->update_meta_data( '_rooty_udn_giam', $giam );
	$order->add_order_note( 'Ưu đãi nhóm tour ghép (từ vé thứ 5): ' . $nhan );
	$order->save();
} );

// (1) Trang tour: sửa ô «Tổng» và hiện dòng ưu đãi nhóm.
add_action( 'wp_footer', function () {
	if ( ! rooty_udn_bat() || ! function_exists( 'is_product' ) || ! is_product() ) {
		return;
	}
	if ( ! in_array( rooty_udn_id_vi( get_the_ID() ), rooty_udn_tours(), true ) ) {
		return;
	}
	echo <<<'JS'
<script>
window.addEventListener('load', function () {
	var $ = window.jQuery;
	if (!$ || !$('.m-tour-class').length) return;
	function giamThem(nl, te) { var ve = nl + te / 2; return ve > 4 ? Math.round((ve - 4) * 50000) : 0; }
	function capNhat() {
		var $t = $('.m-tour-class .active .m-tour');
		var gia = Number($t.data('price')) || 0, giaTE = Number($t.data('price-child')) || 0, phuThu = Number($t.data('price-surcharge')) || 0;
		var nl = Number($('.m-quantity-people').val()) || 0, te = Number($('.m-quantity-child').val()) || 0;
		var cur = $('.m-tour-class').data('currency') || 'đ';
		var giam = (/gh[eé]p|join|shared/i.test($t.text()) && gia > 0 && (te === 0 || giaTE > 0)) ? giamThem(nl, te) : 0;
		$('.rooty-udn-note').remove();
		if (!giam) return;
		var tong = (nl * gia + te * giaTE + phuThu - giam).toLocaleString();
		$('.price-main-combo').html(cur + ' ' + tong).attr('data-price_total', cur + ' ' + tong)
			.after('<p class="rooty-udn-note" style="margin:4px 0 0;font-size:13px;color:#389683;font-weight:600">Đã gồm ưu đãi nhóm từ vé thứ 5: −' + giam.toLocaleString() + ' ' + cur + '</p>');
	}
	// nút +/− của theme bắn change không lan lên document → gắn thẳng vào ô số lượng (chạy sau handler của theme)
	$('.m-tour-class .count-input').on('change input', capNhat);
	$(document).on('click', '.m-tour-child-price', capNhat);
	capNhat();
});
</script>
JS;
}, 99 );
