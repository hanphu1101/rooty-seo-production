<?php
/**
 * Rooty · Đưa BreadcrumbList ra gốc schema bài viết (WPCode, PHP snippet, chạy mọi nơi).
 *
 * Rank Math gắn breadcrumb vào WebPage (WebPage.breadcrumb → #breadcrumb). BlogPosting trỏ tới
 * WebPage hai lần (isPartOf + mainEntityOfPage) nên trên validator breadcrumb hiện 2 lần bên trong
 * BlogPosting và không đứng riêng ở gốc. Bỏ tham chiếu đó thì BreadcrumbList (vẫn nằm trong @graph)
 * thành mục gốc ngang hàng BlogPosting.
 *
 * Chạy thử: chỉ áp khi URL có ?rooty_schema_test=1. Kiểm xong đổi rooty_bc_bat() thành return true.
 */
function rooty_bc_bat() {
	return isset( $_GET['rooty_schema_test'] );
}

add_filter( 'rank_math/json_ld', function ( $data, $jsonld ) {
	if ( ! rooty_bc_bat() || ! is_singular( 'post' ) ) {
		return $data;
	}
	foreach ( $data as $k => $node ) {
		if ( is_array( $node ) && isset( $node['breadcrumb'] ) ) {
			unset( $data[ $k ]['breadcrumb'] );
		}
	}
	return $data;
}, 99, 2 );
