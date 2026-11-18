<?php
/**
 * Plugin Name: Rooty — Mật khẩu ứng dụng qua header X-Rooty-Auth
 * Description: Một số hosting (LiteSpeed/Nginx/proxy) cắt header Authorization nên WordPress không nhận Mật khẩu ứng dụng.
 *              File này đọc header phụ X-Rooty-Auth (cùng nội dung "Basic …") để App SEO sửa bài qua REST API.
 *              Chỉ áp cho yêu cầu REST (/wp-json/), không đổi gì khác. Xoá file là tắt.
 * Cài: tải lên wp-content/mu-plugins/ (tạo thư mục nếu chưa có) — plugin «bắt buộc», tự chạy, không cần bật.
 */
if ( empty( $_SERVER['PHP_AUTH_USER'] ) && ! empty( $_SERVER['HTTP_X_ROOTY_AUTH'] )
	&& false !== strpos( $_SERVER['REQUEST_URI'] ?? '', '/wp-json/' ) ) {
	$rooty_auth = $_SERVER['HTTP_X_ROOTY_AUTH'];
	if ( 0 === stripos( $rooty_auth, 'Basic ' ) ) {
		$rooty_pair = base64_decode( substr( $rooty_auth, 6 ), true );
		if ( $rooty_pair && false !== strpos( $rooty_pair, ':' ) ) {
			list( $_SERVER['PHP_AUTH_USER'], $_SERVER['PHP_AUTH_PW'] ) = explode( ':', $rooty_pair, 2 );
		}
	}
}
