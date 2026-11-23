/*
 * Ưu đãi nhóm tour ghép (CSBH khách lẻ B2C, wiki 02.1 / 02.2 / 02.8):
 *   100.000/vé cho vé 1–4, 150.000/vé từ vé thứ 5; trẻ em (1m–1m4) = ½ vé, hưởng ½ mức.
 *   Đếm vé quy đổi: 1 người lớn = 1 vé, 1 trẻ em = ½ vé (chị Hân chốt 23/11/2026:
 *   «2 trẻ em là 1 người lớn» → 3 NL + 2 TE = 4 vé, chưa tới vé thứ 5).
 * Đơn giá trên web đã trừ sẵn 100.000/NL và 50.000/TE, nên chỉ cần giảm thêm
 *   50.000 × (số vé quy đổi − 4) khi trên 4 vé.
 * Chỉ áp cho TOUR GHÉP của các sản phẩm trong TOUR_CO_UU_DAI_NHOM.
 */
(function (root) {
  // id sản phẩm WooCommerce → mã tour (wiki 02)
  var TOUR_CO_UU_DAI_NHOM = {
    514: 'G4 · Tour 3 đảo',
    30393: 'G2 · Tour 4 đảo + cáp treo Hòn Thơm',
    17774: 'G2 · Tour Cano Đảo Cáp Treo và Buffet (trang trùng)',
    31814: 'G2CHONTHOM · Tour cáp treo Hòn Thơm 1 ngày'
  };
  var GIAM_THEM_MOI_VE = 50000; // 150.000 − 100.000 đã trừ sẵn trong đơn giá
  var SO_VE_MUC_1 = 4;

  function soVeQuyDoi(nguoiLon, treEm) {
    return (nguoiLon || 0) + (treEm || 0) / 2;
  }

  function giamThemNhom(nguoiLon, treEm) {
    var ve = soVeQuyDoi(nguoiLon, treEm);
    return ve > SO_VE_MUC_1 ? Math.round((ve - SO_VE_MUC_1) * GIAM_THEM_MOI_VE) : 0;
  }

  // Tổng tiền một đơn tour ghép. donGia/donGiaTreEm là giá web (đã trừ ưu đãi 1 vé).
  function tongTien(o) {
    var goc = o.donGia * o.nguoiLon + o.donGiaTreEm * o.treEm + (o.phuThu || 0);
    var giam = (o.tourGhep && TOUR_CO_UU_DAI_NHOM[o.productId]) ? giamThemNhom(o.nguoiLon, o.treEm) : 0;
    return { tamTinh: goc, giamNhom: giam, tong: goc - giam };
  }

  var api = { TOUR_CO_UU_DAI_NHOM: TOUR_CO_UU_DAI_NHOM, soVeQuyDoi: soVeQuyDoi, giamThemNhom: giamThemNhom, tongTien: tongTien };
  if (typeof module === 'object' && module.exports) module.exports = api; else root.RootyUuDaiNhom = api;
})(this);
