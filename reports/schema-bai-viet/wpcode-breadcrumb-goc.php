<?php
/**
 * Rooty · Đưa BreadcrumbList ra gốc schema bài viết (WPCode, PHP snippet, chạy mọi nơi).
 *
 * Rank Math gắn breadcrumb vào WebPage (WebPage.breadcrumb → #breadcrumb). BlogPosting trỏ tới
 * WebPage hai lần (isPartOf + mainEntityOfPage) nên trên validator breadcrumb hiện 2 lần bên trong
 * BlogPosting và không đứng riêng ở gốc. Bỏ tham chiếu đó thì BreadcrumbList (vẫn nằm trong @graph)
 * thành mục gốc ngang hàng BlogPosting.
 *
 * Đã bật cho mọi bài viết 25/11/2026 (thử bằng ?rooty_schema_test=1, chị Hân duyệt).
 *
 * Trên web: WPCode #87135, PHP, Run Everywhere, Active.
 */
function rooty_bc_bat() {
	return true;
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
