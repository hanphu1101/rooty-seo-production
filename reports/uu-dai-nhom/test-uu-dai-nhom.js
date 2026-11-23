// Chạy: node reports/uu-dai-nhom/test-uu-dai-nhom.js
// Số mong đợi tính tay từ bảng giá gốc wiki (G4: NL 800.000, TE 400.000) trừ ưu đãi CSBH.
const assert = require('assert');
const U = require('./uu-dai-nhom.js');

const G4 = { productId: 514, donGia: 700000, donGiaTreEm: 350000, tourGhep: true };
const ca = [
  // [người lớn, trẻ em, tổng theo CSBH]
  [1, 0, 700000],              // 800 − 100
  [4, 0, 2800000],             // 3.200 − 400
  [3, 2, 2800000],             // 4 vé quy đổi: 2.400 + 800 − (300 + 100) → không giảm thêm
  [5, 0, 3450000],             // 4.000 − (400 + 150)
  [6, 0, 4100000],             // 4.800 − (400 + 300)
  [4, 1, 3125000],             // 4,5 vé: 3.600 − (400 + 75)
  [4, 2, 3450000],             // 5 vé: 4.000 − (400 + 150)
  [10, 0, 6700000],            // 8.000 − (400 + 900)
  [0, 8, 2800000],             // 4 vé: 3.200 − 400
  [0, 10, 3450000]             // 5 vé: 4.000 − 550
];
for (const [nl, te, mong] of ca) {
  const r = U.tongTien({ ...G4, nguoiLon: nl, treEm: te });
  assert.strictEqual(r.tong, mong, `G4 ${nl} NL + ${te} TE: ra ${r.tong}, CSBH ${mong}`);
}

// Tour riêng và tour không thuộc danh sách: không giảm thêm
assert.strictEqual(U.tongTien({ ...G4, tourGhep: false, nguoiLon: 6, treEm: 0 }).giamNhom, 0);
assert.strictEqual(U.tongTien({ productId: 12496, donGia: 950000, donGiaTreEm: 525000, tourGhep: true, nguoiLon: 6, treEm: 0 }).giamNhom, 0);

// G2 (đảo + cáp): giá gốc 650 + 900 vé = 1.550 → web 1.450; 6 NL → CSBH 9.300 − 700 = 8.600
assert.strictEqual(U.tongTien({ productId: 30393, donGia: 1450000, donGiaTreEm: 945000, tourGhep: true, nguoiLon: 6, treEm: 0 }).tong, 8600000);
// G2CHONTHOM: 8 NL → 8 × 1.420 − (400 + 600) = 10.360
assert.strictEqual(U.tongTien({ productId: 31814, donGia: 1320000, donGiaTreEm: 935000, tourGhep: true, nguoiLon: 8, treEm: 0 }).tong, 10360000);

console.log('ĐẠT: ' + (ca.length + 4) + ' trường hợp');
