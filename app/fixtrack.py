"""
Theo dõi sửa lỗi từng trang: nhập báo cáo lỗi (file Excel/Google Sheets xuất .xlsx, mỗi tab một loại lỗi, có cột URL),
lưu mỗi lỗi × trang thành một dòng có trạng thái, kiểm lại trang sau khi sửa, và đo thứ hạng trước/sau.

Chỉ dùng thư viện chuẩn (đọc .xlsx bằng zipfile + XML).
"""
from __future__ import annotations

import io
import re
import urllib.parse
import zipfile
from xml.etree import ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
REL_NS = "{http://schemas.openxmlformats.org/package/2006/relationships}"

STATUS = ["Mới", "Đã xác nhận", "Đang sửa", "Đã sửa", "Sửa chưa đạt", "Tái phát", "Hết lỗi (quét lại)", "Không phải lỗi", "Bỏ qua"]
OPEN = {"Mới", "Đã xác nhận", "Đang sửa", "Sửa chưa đạt", "Tái phát"}
FIXED = {"Đã sửa", "Hết lỗi (quét lại)"}
EFFECT = ["Chờ đo", "Tốt lên", "Không đổi", "Giảm", "Chưa có số liệu"]


# ------------------------------------------------------------------ đọc xlsx

def _col(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def read_xlsx(data: bytes) -> dict[str, list[list]]:
    """→ {tên tab: [[ô, …], …]} — giá trị đã tính (chuỗi hoặc số)."""
    z = zipfile.ZipFile(io.BytesIO(data))
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t")))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).iter(f"{REL_NS}Relationship")}
    out = {}
    for sh in wb.find("m:sheets", NS):
        target = rels[sh.get(f"{{{NS['r']}}}id")].lstrip("/")
        path = target if target.startswith("xl/") else "xl/" + target
        rows = []
        for row in ET.fromstring(z.read(path)).iter(f"{{{NS['m']}}}row"):
            cells = {}
            for c in row.findall("m:c", NS):
                t, v = c.get("t"), c.find("m:v", NS)
                if t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter(f"{{{NS['m']}}}t"))
                elif v is None:
                    continue
                elif t == "s":
                    val = shared[int(v.text)]
                elif t in ("str", "e", "b"):
                    val = v.text
                else:
                    try:
                        f = float(v.text)
                        val = int(f) if f.is_integer() else f
                    except (TypeError, ValueError):
                        val = v.text
                cells[_col(c.get("r"))] = val
            if cells:
                rows.append([cells.get(i) for i in range(max(cells) + 1)])
        out[sh.get("name")] = rows
    return out


# ------------------------------------------------------------------ báo cáo → dòng lỗi

def norm_path(u: str) -> str:
    u = (u or "").strip()
    p = urllib.parse.urlsplit(u).path if u.startswith("http") else u
    p = "/" + p.strip("/") + "/" if p.strip("/") else "/"
    return p.lower()


def _clean_type(sheet: str) -> str:
    return re.sub(r"^\s*\d+\s*[.)·-]\s*", "", sheet).strip()


def _header_row(rows):
    for i, r in enumerate(rows[:6]):
        cells = [str(x or "").strip().lower() for x in r]
        if "url" in cells or "các url" in cells:
            return i
    return None


def parse_report(sheets: dict[str, list[list]]) -> tuple[list[dict], dict]:
    """→ (danh sách lỗi theo trang, {loại lỗi: thông tin từ tab Tổng quan})"""
    overview = {}
    for name, rows in sheets.items():
        hi = next((i for i, r in enumerate(rows[:6]) if r and any(str(x or "").strip() == "Lỗi trong báo cáo" for x in r)), None)
        if hi is None:
            continue
        h = [str(x or "").strip() for x in rows[hi]]
        idx = {k: h.index(k) for k in h if k}
        for r in rows[hi + 1:]:
            get = lambda k: r[idx[k]] if k in idx and idx[k] < len(r) else None
            tab = get("Tab chi tiết")
            if tab:
                overview[_clean_type(str(tab))] = {"ten": get("Lỗi trong báo cáo"), "ket_luan": get("Kết luận sau khi quét"),
                                                   "so_bai": get("Số bài dính"), "cach_do": get("Cách đo")}
    items = []
    for name, rows in sheets.items():
        hi = _header_row(rows)
        if hi is None:
            continue
        kind = _clean_type(name)
        note = " ".join(str(x) for x in (rows[0] if hi > 0 else []) if x)   # dòng mô tả đầu tab
        h = [str(x or "").strip() for x in rows[hi]]
        low = [x.lower() for x in h]
        multi = "các url" in low and "url" not in low
        ucol = low.index("các url" if multi else "url")
        prev = []
        for r in rows[hi + 1:]:
            r = list(r) + [None] * (len(h) - len(r))
            for i, v in enumerate(r):   # «Như trên» → lấy giá trị dòng trên
                if isinstance(v, str) and v.strip().lower().startswith("như trên") and i < len(prev) and prev[i]:
                    r[i] = str(prev[i]) + v.strip()[8:]
            prev = r
            if ucol >= len(r) or not r[ucol]:
                continue
            detail = " · ".join(f"{h[i]}: {v}" for i, v in enumerate(r)
                                if i != ucol and h[i] and h[i] not in ("#",) and v not in (None, ""))
            lang = next((str(r[i]) for i, x in enumerate(low) if x in ("nn", "ngôn ngữ") and i < len(r) and r[i]), "")
            urls = [norm_path(x) for x in re.split(r"\s*[·,\n]\s*", str(r[ucol])) if x.strip().startswith("/") or x.strip().startswith("http")]
            if not urls:
                continue
            if multi:   # một cụm nhiều URL (trùng từ khoá) → một dòng, URL đầu là trang đại diện
                items.append({"type": kind, "url": urls[0], "lang": lang, "detail": detail + " · Các URL: " + " · ".join(urls), "note": note})
            else:
                items.append({"type": kind, "url": urls[0], "lang": lang, "detail": detail, "note": note})
    return items, overview


def key(kind: str, url: str) -> str:
    return f"{kind} · {norm_path(url)}"


# ------------------------------------------------------------------ kiểm lại trang sau khi sửa

class _Links:
    def __init__(self):
        from html.parser import HTMLParser

        outer = self

        class P(HTMLParser):
            def __init__(self):
                super().__init__(convert_charrefs=True)
                self.depth_skip = 0
                self.seen_h1 = False
                self.in_title = False

            def handle_starttag(self, tag, attrs):
                a = dict(attrs)
                if tag in ("nav", "header", "footer", "aside"):
                    self.depth_skip += 1
                if tag == "h1":
                    self.seen_h1 = True
                if tag == "title":
                    self.in_title = True
                if tag == "a" and self.seen_h1 and not self.depth_skip:
                    outer.links.append(((a.get("href") or "").strip(), a.get("class") or ""))

            def handle_endtag(self, tag):
                if tag in ("nav", "header", "footer", "aside") and self.depth_skip:
                    self.depth_skip -= 1
                if tag == "title":
                    self.in_title = False

            def handle_data(self, d):
                if self.in_title:
                    outer.title += d
                elif self.seen_h1 and not self.depth_skip:
                    outer.text.append(d)
        self.links, self.text, self.title = [], [], ""
        self.p = P()


def recheck(kind: str, url: str, fetch, decode, detail: str = "") -> tuple[bool | None, str]:
    """Kiểm lại một lỗi trên trang đang chạy. → (còn lỗi?, chi tiết). None = loại lỗi này phải kiểm tay."""
    k = kind.lower()
    if "giá cũ" in k:
        from factbook import money_values
        olds = {v for x in (detail or "").split(" ‖ ") for _, v in money_values(parse_detail(x).get("Bài đang ghi", ""))}
        st, body, hd, final = fetch(url)
        if st != 200:
            return (False, f"trang trả mã {st}") if st in (301, 302, 404, 410) else (None, f"không tải được (mã {st})")
        from linkbuild import END_MARK
        L = _Links()
        try:
            L.p.feed(decode(body, hd))
        except Exception:
            pass
        text = " ".join(" ".join(L.text).split())
        m = END_MARK.search(text)
        text = text[:m.start()] if m else text
        still = sorted({r for r, v in money_values(text) if v in olds})
        return (True, "bài vẫn còn ghi " + ", ".join(still)) if still else (False, "không còn thấy giá cũ trong bài")
    if not ("tự thân" in k or "năm" in k):
        return None, "loại lỗi này cần người kiểm"
    st, body, hd, final = fetch(url)
    if st in (301, 302, 307, 308):
        return False, f"trang đã chuyển hướng (mã {st}) — coi như đã gộp/xoá"
    if st == 404 or st == 410:
        return False, f"trang trả mã {st} — đã xoá"
    if st != 200:
        return None, f"không tải được (mã {st})"
    L = _Links()
    try:
        L.p.feed(decode(body, hd))
    except Exception:
        pass
    me = norm_path(url)
    if "link tự thân" in k or "tự thân" in k:
        own = [h for h, cls in L.links if h and not h.startswith("#") and norm_path(urllib.parse.urljoin(url, h).split("#")[0]) == me
               and not re.search(r"share|facebook|zalo|twitter|pinterest", h)]
        return (True, f"còn {len(own)} link trỏ về chính bài") if own else (False, "không còn link trỏ về chính bài")
    if "năm" in k:   # đổi năm giả
        from linkbuild import END_MARK
        text = " ".join(" ".join(L.text).split())
        m = END_MARK.search(text)
        if m:
            text = text[:m.start()]
        m = re.search(r"Lượt xem:\s*[\d.,]+", text[:600])
        if m:
            text = text[m.end():]
        years_title = re.findall(r"\b20\d\d\b", L.title)
        if not years_title:
            return False, "tiêu đề không còn ghi năm"
        y = max(years_title)
        n = len(re.findall(r"\b" + y + r"\b", text))
        old = len(re.findall(r"\b(?:2019|202[0-4])\b", text))
        bad = n <= 1
        return bad, f"tiêu đề ghi {y}; thân bài nhắc {y} {n} lần, còn {old} lần nhắc năm ≤ 2024" + (" — vẫn chỉ đổi năm trên tiêu đề" if bad else "")
    return None, "loại lỗi này cần người kiểm"


# ------------------------------------------------------------------ cần sửa gì (gợi ý cụ thể cho từng dòng lỗi)

def parse_detail(detail: str) -> dict:
    out = {}
    for part in re.split(r"\s+·\s+(?=[^·:]{1,40}:\s)", detail or ""):
        if ":" in part:
            k, v = part.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def _num(v):
    try:
        return float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return 0


def fix_hint(kind: str, detail: str) -> str:
    """Cần sửa gì cho một lỗi trên một trang — viết thành việc làm được ngay."""
    d = parse_detail(detail)
    k = (kind or "").lower()
    note = d.get("Ghi chú", "")
    if "năm" in k:
        title = d.get("Tiêu đề", "")
        y = (re.findall(r"20\d\d", title) or ["năm mới"])[-1]
        old = int(_num(d.get("Nhắc năm ≤2024")))
        steps = [f"Cập nhật thông tin thật của năm {y} trong thân bài: giá vé/tour, giờ mở cửa, lịch hoạt động, sự kiện, khuyến mãi — mỗi số ghi nguồn + tháng/năm."]
        if old:
            steps.append(f"Sửa {old} chỗ còn ghi năm 2019–2024 (thông tin cũ).")
        steps += [f"Không có gì mới để cập nhật → bỏ «{y}» khỏi tiêu đề (giữ nguyên slug nếu bài đã có traffic).",
                  "Không chỉ đổi ngày cập nhật. Sửa xong bấm «Kiểm lại trang»."]
        return " ".join(f"{'①②③④⑤'[i]} {x}" for i, x in enumerate(steps))
    if "trải nghiệm" in k:
        return ("Đọc lại bài để xác nhận (danh sách nghi vấn). Nếu đúng thiếu: thêm 2–3 đoạn chỉ Rooty có — HDV kể lúc dẫn đoàn (tháng nào, đoàn mấy người), "
                "mẹo né đông / giờ đẹp, giá thực tế khách đã trả, ảnh tự chụp có chú thích; ghi rõ người kể. "
                "Nếu bài đã có trải nghiệm thật → chọn «Không phải lỗi».")
    if "lạc chủ đề" in k:
        why = d.get("Lý do", "")
        return ((f"Bài nói về {why[:1].lower() + why[1:]}, ngoài phạm vi Phú Quốc. " if why else "Bài nằm ngoài phạm vi Phú Quốc. ")
                + "Xem GSC (B10) rồi chọn 1: ① có traffic & liên quan khách đi Phú Quốc → viết lại theo góc Phú Quốc (VD «kết hợp X với Phú Quốc») · "
                "② có traffic nhưng không liên quan → noindex · ③ ít traffic, có bài Phú Quốc gần chủ đề → gộp nội dung + 301 · ④ không traffic → xoá (410). Ghi lựa chọn vào «Đã sửa gì».")
    if "trùng" in k:
        n = int(_num(d.get("Số bài")))
        return (f"Cụm {d.get('Cụm chủ đề', '')} có {n} bài cùng tranh một nhóm từ khoá. ① Xem GSC Truy vấn × Trang (B10 · Xung đột từ khoá) chọn 1 bài chính (nhiều nhấp nhất). "
                "② Bài còn lại: gộp nội dung vào bài chính + 301, hoặc đổi sang góc/từ khoá riêng (VD review 1 khách sạn cụ thể). "
                "③ Bài phụ đặt link nội bộ về bài chính bằng anchor từ khoá chính. Danh sách URL ở «Chi tiết lỗi»." + (f" Ghi chú báo cáo: {note}" if note else ""))
    if "thương mại" in k:
        return (f"Không phải lỗi chắc chắn — đọc lại. Bài có {d.get('Link tới tour/vé', '?')} link tour/vé và {d.get('Câu kêu gọi đặt', '?')} câu kêu gọi đặt / {d.get('Số từ', '?')} từ. "
                "Giữ 1–2 link tour/vé đặt đúng chỗ khách cần (cạnh giá/lịch trình) và 1 lời mời đặt ở cuối bài; bỏ CTA lặp giữa các đoạn thông tin. Đọc thấy tự nhiên → «Không phải lỗi».")
    if "ngôn ngữ" in k:
        loai, tt = d.get("Loại", ""), d.get("Trạng thái", "")
        if "gộp" in loai:
            extra = re.search(r"link nội bộ hỏng.*", note)
            return (f"Bài đã 301 + canonical {tt} nhưng vẫn để Published → chuyển sang Draft trong WordPress cho gọn (giữ nguyên redirect). Không ảnh hưởng thứ hạng."
                    + (f" Sửa thêm: {extra.group(0)}." if extra else ""))
        if "noindex" in loai:
            return f"Đang noindex — hợp lý ({note}). Kiểm không còn link nội bộ trỏ tới rồi chọn «Không phải lỗi»."
        if "404" in loai:
            return f"URL 404. {note}"
        if "ngắn" in loai:
            return (f"Bài {tt}. " + (f"{note}. " if note else "")
                    + "Bài thông báo/chúc Tết đã hết hạn → noindex; bài cẩm nang → bổ sung nội dung đủ ý cho khách nước ngoài (giá, cách đi, lưu ý) hoặc gộp vào bài cùng chủ đề + 301.")
        if "trung" in loai.lower():
            return f"Kiểm chứng cho thấy KHÔNG mỏng ({tt}) → chọn «Không phải lỗi». {note}"
        return note or "Xem chi tiết lỗi."
    if "tự thân" in k:
        anchor = d.get("Anchor text", "")
        n = int(_num(d.get("Số link tự thân")) or 1)
        return ((f"Bỏ link ở anchor «{anchor}»" if anchor else "Bỏ link trỏ về chính bài") + (f" ({n} link)" if n > 1 else "")
                + " — hoặc đổi sang trỏ trang tour/vé/bài liên quan đúng ý anchor đó. Sửa xong bấm «Kiểm lại trang». "
                "Gốc lỗi: quy trình viết bài đang chèn link từ khoá chính về chính bài → nhắc người viết bỏ bước này.")
    if "tác giả" in k:
        lang = d.get("NN", "")
        return ("① (làm 1 lần cho cả site) Trang tác giả /huong-dan-vien-lam-thanh-nguyen/: thêm schema Person (name, jobTitle «Hướng dẫn viên du lịch», image, sameAs Facebook/LinkedIn cá nhân, worksFor Rooty Trip). "
                "② Trong bài: 1–2 câu kinh nghiệm của chính tác giả (lúc dẫn đoàn), không chỉ ở box tác giả."
                + (f" ③ Bài tiếng {lang}: ghi đúng người viết/biên dịch (VD «Biên dịch: …, nội dung gốc: Lâm Thành Nguyên») thay vì một người đứng tên mọi ngôn ngữ." if lang and lang != "VI" else ""))
    if "giá cũ" in k:
        parts = [parse_detail(x) for x in (detail or "").split(" ‖ ")]
        lines = [f"Đổi «{x.get('Bài đang ghi', '?')}» thành «{x.get('Giá hiện tại', '?')}» ({x.get('Dữ kiện', '')}) ở câu: «{x.get('Câu', '')[:160]}»"
                 for x in parts]
        return (" ‖ ".join(lines) + ". Xem trước: số trong bài có thể là giá trẻ em / gói khác / mùa khác — đúng thì chọn «Không phải lỗi». "
                "Ghi rõ «giá cập nhật tháng MM/YYYY» trong bài. Sửa xong bấm «Kiểm lại trang».")
    return "Xem «Chi tiết lỗi» và «Mô tả loại lỗi», ghi cách sửa cụ thể vào đây."
