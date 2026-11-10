"""
GEO · AI Search — chấm bài theo Checklist GEO của GTV (điểm chạm G3 "cấu trúc đoạn", tiêu chí 14–25,
kèm vài tiêu chí G1/G2 đo được trên từng bài), và phân tích câu trả lời của AI khi đo hiện diện (G5).

Mỗi tiêu chí trả về số thứ tự trong checklist GTV để người đọc tra lại bản gốc.
Các con số đo bằng máy là ƯỚC LƯỢNG — tiêu chí nào cần mắt người thì ghi rõ "kiểm tay".
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

_HERE = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(_HERE.parent / "scripts"))
from geo_audit import decode, fetch, jsonld_types  # noqa: E402

CHECKLIST = json.loads((_HERE / "geo_checklist.json").read_text(encoding="utf-8"))

# ------------------------------------------------------------------ đọc bài theo khối

SKIP_TAGS = {"script", "style", "noscript", "svg", "nav", "footer", "header", "aside", "form", "button", "select", "iframe"}
SKIP_CLASS = re.compile(r"(^|[\s_-])(toc|ez-toc|post-meta|share|social|breadcrumb|related|comment|sidebar|newsletter|author-box|rating)", re.I)
HIDE_CLASS = re.compile(r"accordion|tab-pane|tabpanel|collapse(?!d)|toggle-content|elementor-tab-content", re.I)
END_HEADINGS = re.compile(r"^(tin tức liên quan|bài viết liên quan|có thể bạn (sẽ )?thích|xem thêm|tour liên quan|bình luận|để lại bình luận)", re.I)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class BlockParser(HTMLParser):
    """Thứ tự khối nội dung sau H1: ('h2', text) · ('h3', text) · ('p', text) · ('li', text) · ('table', số dòng)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks: list[tuple[str, str]] = []
        self.raw_after_h1: list[str] = []      # mọi chữ sau H1 (kể cả khối meta) — để soi ~400 ký tự đầu
        self.h1 = ""
        self.hidden_blocks = 0
        self.ext_links: list[str] = []
        self._stack: list[tuple[str, bool, bool]] = []   # (tag, bỏ qua, ẩn)
        self._cur: str | None = None
        self._buf: list[str] = []
        self._in_h1 = False
        self._seen_h1 = False
        self._ended = False
        self._table_rows = 0
        self._in_table = 0

    def _skipping(self):
        return any(s for _, s, _ in self._stack)

    def _hidden(self):
        return any(h for _, _, h in self._stack)

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag in VOID:
            if tag == "br" and self._cur:
                self._buf.append(" ")
            return
        cls = a.get("class", "") + " " + a.get("id", "")
        skip = tag in SKIP_TAGS or bool(SKIP_CLASS.search(cls))
        hide = bool(HIDE_CLASS.search(cls)) or tag == "details"
        self._stack.append((tag, skip, hide))
        if tag == "h1" and not self._seen_h1:
            self._in_h1 = True
            self._buf = []
            return
        if not self._seen_h1 or self._ended or self._skipping():
            return
        if tag == "a" and a.get("href", "").startswith("http"):
            self.ext_links.append(a["href"])
        if tag == "table":
            self._in_table += 1
            self._table_rows = 0
        elif tag == "tr" and self._in_table:
            self._table_rows += 1
        elif tag in ("h2", "h3", "h4", "p", "li", "blockquote") and not self._cur:
            self._cur = tag
            self._buf = []

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        # đóng tới đúng thẻ (HTML thật hay thiếu thẻ đóng)
        idx = next((i for i in range(len(self._stack) - 1, -1, -1) if self._stack[i][0] == tag), None)
        hidden_before = self._hidden()
        if self._in_h1 and tag == "h1":
            self.h1 = " ".join("".join(self._buf).split())
            self._in_h1, self._seen_h1 = False, True
        elif self._cur == tag:
            text = " ".join("".join(self._buf).split())
            if text:
                kind = "h2" if tag == "h2" else ("h3" if tag in ("h3", "h4") else ("q" if tag == "blockquote" else tag))
                if kind == "h2" and END_HEADINGS.search(text):
                    self._ended = True
                else:
                    self.blocks.append((kind, text))
                    if hidden_before and kind in ("p", "li"):
                        self.hidden_blocks += 1
            self._cur = None
        elif tag == "table" and self._in_table:
            self._in_table -= 1
            if not self._ended and self._seen_h1:
                self.blocks.append(("table", str(self._table_rows)))
        if idx is not None:
            del self._stack[idx:]

    def handle_data(self, data):
        if self._in_h1:
            self._buf.append(data)
            return
        if not self._seen_h1 or self._ended:
            return
        if not any(t in ("script", "style") for t, _, _ in self._stack) and data.strip():
            self.raw_after_h1.append(data.strip())
        if self._cur and not self._skipping():
            self._buf.append(data)


# ------------------------------------------------------------------ tiện ích chữ

def nfc(s):
    return unicodedata.normalize("NFC", s or "")


def strip_accents(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "").replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def words(s):
    return re.findall(r"\w+", s or "")


def sentences(s):
    parts = re.split(r"(?<=[.!?…])\s+(?=[A-ZÀ-Ỹ0-9\"“(])", s or "")
    return [p.strip() for p in parts if p.strip()]


STOP = set("phú quốc pq ở tại và của cho với có không là gì nào bao nhiêu như thế nào nên đi những các một mấy giá vé tour".split())


def core_tokens(kw):
    toks = [t for t in words(nfc(kw).lower()) if len(t) > 1]
    core = [t for t in toks if t not in STOP]
    return core or toks


QUESTION_RE = re.compile(r"\?|\b(là gì|ở đâu|bao nhiêu|bao lâu|bao xa|khi nào|lúc nào|thế nào|như thế nào|ra sao|có nên|nên|có \w+( \w+)? không|"
                         r"cách|làm sao|tại sao|vì sao|mấy giờ|mấy|nào|gì|ai|hướng dẫn|kinh nghiệm|lưu ý|mẹo)\b", re.I)
EMPTY_HEAD = re.compile(r"^(tổng quan|giới thiệu|kết luận|lời kết|tóm lại|tổng kết|thông tin chung|phần \d+|mở đầu|lời mở đầu)\W*$", re.I)
STORY_OPEN = re.compile(r"^(phú quốc (là|được mệnh danh)|bạn (đang|có|đã)|nếu bạn|có lẽ|chắc hẳn|hẳn (là|ai)|ai (cũng|đã)|du lịch phú quốc (là|đang)|"
                        r"không phải ngẫu nhiên|trong những năm gần đây|nhắc đến|nói đến|khi nhắc|mỗi khi|hòn đảo ngọc)", re.I)
ANAPHORA = re.compile(r"^(điều này|việc này|như đã nói|như đã đề cập|như trên|như vậy|những điều trên|những thông tin trên|"
                      r"nó |chúng nó|đây là lý do|vì thế|do đó|bên cạnh đó)", re.I)
NUM_FACT = re.compile(r"\d[\d.,]*\s*(?:%|km|m\b|mét|cm|ha|hecta|phút|giờ|h\b|tiếng|ngày|đêm|năm|tháng|đ\b|₫|vnđ|vnd|đồng|nghìn|ngàn|triệu|tỷ|k\b|"
                      r"người|khách|chỗ|điểm|tầng|chuyến|lượt|độ|°c|sao)|\b\d{1,2}[:h]\d{2}\b|\b(?:19|20)\d{2}\b", re.I)
SOURCE_RE = re.compile(r"\btheo\s+(?:số liệu|thống kê|báo|thông tin|công bố|website|trang|sở|bộ|tổng cục|ubnd|sun group|vinpearl|cục)|\bnguồn\s*:|"
                       r"\(nguồn|\bcông bố\b|\bthống kê\b", re.I)
QUOTE_RE = re.compile(r"[“\"][^”\"]{20,300}[”\"]\s*[,.]?\s*(?:[-—–]\s*)?(?:anh|chị|ông|bà|hdv|hướng dẫn viên|khách|theo|chia sẻ|cho biết|nói|kể)|"
                      r"(?:chia sẻ|cho biết|kể|nói)\s*:\s*[“\"]", re.I)
EXPERIENCE = re.compile(r"\b(chúng tôi|chúng mình|team rooty|rooty trip|rooty|hdv của|hướng dẫn viên (của )?rooty|khi dẫn đoàn|dẫn khách|"
                        r"kinh nghiệm thực tế|thực tế (cho thấy|khách)|mẹo|tự chụp|ảnh: rooty|khách của rooty|khách hay hỏi|đã đi|lần gần nhất|"
                        r"giờ đẹp|né đông|tránh đông)\b", re.I)
COMMERCIAL = re.compile(r"\b(giá|bảng giá|vé|combo|tour|so sánh|review|khuyến mãi|ưu đãi|đặt)\b", re.I)


def _date(s):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s or "")
    if m:
        try:
            return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    m = re.search(r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", s or "")
    if m:
        try:
            return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            return None
    return None


def _jsonld_nodes(blocks):
    out = []

    def walk(n):
        if isinstance(n, dict):
            out.append(n)
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    for b in blocks:
        try:
            walk(json.loads(b))
        except Exception:
            continue
    return out


def _types(n):
    t = n.get("@type")
    return set(t if isinstance(t, list) else [t]) if t else set()


class _Meta(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.jsonld, self.title = {}, [], ""
        self._j = self._t = False
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta":
            k = (a.get("name") or a.get("property") or "").lower()
            if k:
                self.meta[k] = a.get("content", "")
        elif tag == "script" and "ld+json" in a.get("type", "").lower():
            self._j, self._buf = True, []
        elif tag == "title":
            self._t = True

    def handle_endtag(self, tag):
        if tag == "script" and self._j:
            self.jsonld.append("".join(self._buf))
            self._j = False
        elif tag == "title":
            self._t = False

    def handle_data(self, d):
        if self._j:
            self._buf.append(d)
        elif self._t:
            self.title += d


# ------------------------------------------------------------------ cấu trúc bài

def sections(blocks):
    """→ intro (đoạn trước H2 đầu) + [{h2, paras:[...], sub:[h3], tables}]"""
    intro, secs, cur = [], [], None
    for kind, text in blocks:
        if kind == "h2":
            cur = {"h2": text, "paras": [], "sub": [], "tables": 0, "first_passage": []}
            secs.append(cur)
            continue
        target = cur["paras"] if cur else intro
        if kind in ("p", "li", "q"):
            target.append(text)
            if cur is not None and not cur["sub"]:
                cur["first_passage"].append(text)
        elif kind == "h3" and cur is not None:
            cur["sub"].append(text)
        elif kind == "table" and cur is not None:
            cur["tables"] += 1
    return intro, secs


def h2_type(h):
    s = h.lower()
    if re.search(r"là gì|nghĩa là|là ai", s):
        return "định nghĩa"
    if re.search(r"bao nhiêu|giá|chi phí|mấy giờ|bao lâu|bao xa|khi nào|ở đâu", s):
        return "dữ kiện"
    if re.search(r"so sánh| vs |hay |nên chọn|khác (nhau|gì)|tốt hơn", s):
        return "so sánh"
    if re.search(r"có nên|có \w+( \w+)? không|nên không|được không", s):
        return "có/không"
    if re.search(r"cách|làm sao|như thế nào|thế nào|hướng dẫn|đi .* (bằng|từ)|các bước", s):
        return "cách làm"
    return "khác"


def answer_ok(htype, first):
    """Câu đầu sau H2 có đúng mẫu trả lời không (GTV #16)."""
    f = first.lower()
    if htype == "định nghĩa":
        return " là " in f[:160]
    if htype == "dữ kiện":
        return bool(NUM_FACT.search(first)) or bool(re.search(r"\b(nằm|cách|ở|tại)\b", f[:120]))
    if htype == "so sánh":
        return bool(re.search(r"\b(nên|hơn|phù hợp|chọn|thích hợp|rẻ hơn|đắt hơn)\b", f[:200]))
    if htype == "có/không":
        return bool(re.match(r"^(có|không|nên|chưa|được|được phép|tuỳ|tùy)\b", f))
    if htype == "cách làm":
        return bool(re.match(r"^(để|muốn|bạn (có thể|cần|nên)|có \d+|có (hai|ba|bốn|năm) cách)", f)) or bool(re.search(r"\b\d+\s*bước|\bbước\b", f[:200]))
    return len(words(first)) >= 12


# ------------------------------------------------------------------ chấm bài

def _c(no, name, ok, detail, gate=False, auto=True):
    return {"no": no, "name": name, "ok": ok, "detail": detail, "gate": gate, "auto": auto}


def check(url: str, kw: str = "", intent: str = "", today: dt.date | None = None) -> dict:
    today = today or dt.date.today()
    st, body, hd, _ = fetch(url)
    if st != 200:
        return {"error": f"Trang trả mã {st} — không chấm được", "checks": [], "score": 0}
    html = decode(body, hd)
    bp = BlockParser()
    mp = _Meta()
    try:
        bp.feed(html)
        mp.feed(html)
    except Exception:
        pass
    blocks = [(k, nfc(t)) for k, t in bp.blocks]
    intro, secs = sections(blocks)
    body_txt = " ".join(t for k, t in blocks if k in ("p", "li", "q"))
    n_words = len(words(body_txt))
    if n_words < 150:
        return {"error": f"Trang chỉ có {n_words} chữ trong phần nội dung — không phải bài viết, bỏ qua chấm GEO", "checks": [], "score": 0}
    kw = nfc(kw or bp.h1)
    core = core_tokens(kw)
    is_info = intent in ("Thông tin", "") and not re.search(r"\b(tour|combo|vé)\b", kw.lower())
    commercial = intent in ("Mua", "Cân nhắc") or bool(COMMERCIAL.search(kw))
    C = []

    # G1 #8 — đọc được bằng máy
    raw = nfc(" ".join(bp.raw_after_h1))
    first400 = raw[:400]
    junk = [k for k in ("Tác giả", "Ngày đăng", "Cập nhật:", "Lượt xem", "Chia sẻ", "Share", "Đăng ký nhận") if k in first400[:200]]
    size_mb = len(body) / 1048576
    C.append(_c(8, "HTML ≤ 2MB", size_mb <= 2, f"{size_mb:.2f} MB"))
    C.append(_c(8, "~400 ký tự đầu sau H1 là một mạch liền (không chen khối tác giả/ngày/chia sẻ)", not junk,
                ("chen giữa: " + ", ".join(junk) + " — đưa khối meta xuống dưới đoạn mở đầu") if junk else "sạch"))
    C.append(_c(8, "Nội dung chính không giấu trong tab/accordion", bp.hidden_blocks <= 2,
                f"{bp.hidden_blocks} đoạn nằm trong tab/accordion" + (" — đưa nội dung quan trọng ra ngoài" if bp.hidden_blocks > 2 else "")))

    # G3 #14 — mở đầu = câu trả lời
    intro_txt = " ".join(intro)
    opening = " ".join(words(intro_txt)[:150]) if intro else " ".join(words(body_txt)[:150])
    ol = opening.lower()
    cov = sum(1 for t in core if t in ol) / max(len(core), 1)
    story = STORY_OPEN.search((intro[0] if intro else "").lower().strip())
    facts_open = len(NUM_FACT.findall(opening))
    ok14 = cov >= 0.6 and not story and facts_open >= 1 and len(words(intro_txt)) >= 40
    C.append(_c(14, "Mở đầu = câu trả lời (100–150 từ đầu trả lời thẳng, có dữ kiện, không kể chuyện dẫn dắt)", ok14,
                f"{len(words(intro_txt))} từ trước H2 đầu · phủ {round(cov*100)}% từ chính của «{kw}» · {facts_open} dữ kiện có số"
                + (f" · mở bằng kiểu dẫn dắt «{story.group(0)}…»" if story else ""), gate=True))
    if is_info:
        n_tab = sum(1 for k, _ in blocks if k == "table")
        first_tab_pos = next((i for i, (k, _) in enumerate(blocks) if k == "table"), None)
        early = first_tab_pos is not None and first_tab_pos <= max(len(blocks) * 0.4, 8)
        C.append(_c(14, "Bài thông tin có bảng tóm tắt dữ kiện (Key-Facts) ở nửa đầu bài", early,
                    f"{n_tab} bảng" + ("" if n_tab == 0 else (" · bảng đầu ở " + ("nửa đầu" if early else "cuối bài")))))

    # G3 #15 — H2 = câu hỏi thật, phạm vi 1 trang 1 câu hỏi
    h2s = [s["h2"] for s in secs]
    q = [h for h in h2s if QUESTION_RE.search(h.lower())]
    empty = [h for h in h2s if EMPTY_HEAD.search(h.strip())]
    n_sub = len(h2s) + sum(len(s["sub"]) for s in secs)
    qr = len(q) / max(len(h2s), 1)
    C.append(_c(15, "H2 là câu hỏi thật khách hỏi (≥ 60% H2)", qr >= 0.6 and len(h2s) >= 3,
                f"{len(q)}/{len(h2s)} H2 dạng câu hỏi" + (" · chưa đủ 3 H2" if len(h2s) < 3 else ""), gate=True))
    C.append(_c(17, "Không có tiêu đề mục rỗng nghĩa («Tổng quan», «Kết luận», «Giới thiệu»…)", not empty,
                ("rỗng nghĩa: " + " · ".join(empty[:4])) if empty else "không có"))
    C.append(_c(15, "Độ dài 500–2.000 từ, 7–20 tiêu đề phụ (rộng quá → tách trang)", 500 <= n_words <= 2000 and 7 <= n_sub <= 20,
                f"{n_words} từ · {n_sub} tiêu đề H2/H3" + (" · quá dài, cân nhắc tách thành nhiều trang" if n_words > 2000 else "")))

    # G3 #16 — câu đầu sau H2 = câu trả lời 40–50 từ
    good16, bad16, lens = 0, [], []
    for s in secs:
        if not s["paras"]:
            bad16.append(f"«{s['h2'][:50]}» không có đoạn trả lời")
            continue
        first_par = s["paras"][0]
        sent = sentences(first_par)[0] if sentences(first_par) else first_par
        ans = first_par if len(words(first_par)) <= 70 else sent
        lw = len(words(ans))
        lens.append(lw)
        t = h2_type(s["h2"])
        if answer_ok(t, sent) and 15 <= lw <= 80:
            good16 += 1
        else:
            bad16.append(f"«{s['h2'][:50]}» ({t}, {lw} từ)")
    r16 = good16 / max(len(secs), 1)
    C.append(_c(16, "Câu/đoạn đầu sau mỗi H2 trả lời thẳng (đúng mẫu: định nghĩa «X là…», cách làm «Để X…», so sánh kết luận trước, có/không trả lời ngay) · mục tiêu 40–50 từ",
                r16 >= 0.7 and bool(secs),
                f"{good16}/{len(secs)} mục đạt · độ dài câu trả lời trung vị {sorted(lens)[len(lens)//2] if lens else 0} từ"
                + ("\n   chưa đạt: " + " · ".join(bad16[:5]) if bad16 else ""), gate=True))

    # G3 #17 — đoạn tự đứng
    paras = [t for k, t in blocks if k == "p"]
    ana = [p for p in paras if ANAPHORA.search(p.strip().lower())]
    plen = [len(words(" ".join(s["first_passage"]))) for s in secs if s["first_passage"]]
    in_band = sum(1 for x in plen if 80 <= x <= 200)
    ent_secs = sum(1 for s in secs if any(t in (" ".join(s["paras"][:2])).lower() for t in core) or re.search(r"(?<![.!?]\s)\b[A-ZĐ][a-zà-ỹ]+ [A-ZĐ][a-zà-ỹ]+", " ".join(s["paras"][:2])))
    ok17 = not ana and (in_band / max(len(plen), 1)) >= 0.5 and ent_secs / max(len(secs), 1) >= 0.7
    C.append(_c(17, "Mỗi mục H2 cắt rời vẫn hiểu: có tên thực thể, không mở đoạn bằng «điều này / như đã nói», khối ý chính 100–170 từ", ok17,
                f"{len(ana)} đoạn mở bằng từ hồi chỉ" + (f" (VD «{ana[0][:60]}…»)" if ana else "")
                + f" · {in_band}/{len(plen)} mục có khối ý chính 80–200 từ · {ent_secs}/{len(secs)} mục nêu lại tên thực thể", gate=True))

    # G3 #18 — mật độ E-A-V (ước lượng bằng dữ kiện có số)
    facts = NUM_FACT.findall(body_txt)
    dens = len(facts) / max(n_words, 1) * 100
    num_sents = [s for s in sentences(body_txt) if NUM_FACT.search(s)]
    quotable = sum(1 for s in num_sents if len(words(s)) >= 8)
    C.append(_c(18, "Dữ kiện dày & trích được: ≥ 1 dữ kiện có số / 100 từ, ≥ 80% câu chứa số là câu hoàn chỉnh (GTV: ≥ 3 thuộc tính E-A-V/100 từ — máy chỉ đếm được thuộc tính có số nên đặt ngưỡng thấp hơn)",
                dens >= 1.0 and (quotable / max(len(num_sents), 1)) >= 0.8,
                f"{len(facts)} dữ kiện có số · {dens:.1f}/100 từ · {quotable}/{len(num_sents)} câu chứa số đủ chủ–vị (≥ 8 từ)"))

    # G3 #19 — quote + số liệu + nguồn
    host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
    ext = [l for l in bp.ext_links if host not in l and not re.search(r"facebook|zalo|tiktok|youtube|instagram|google\.com/maps|twitter|x\.com|pinterest", l)]
    src = len(SOURCE_RE.findall(body_txt)) + len(ext)
    quotes = len(QUOTE_RE.findall(body_txt)) + sum(1 for k, _ in blocks if k == "q")
    C.append(_c(19, "Có trích nguồn sau dữ kiện (theo…/nguồn/link ngoài uy tín) + số liệu hoặc lời trích", src >= 1 and (len(facts) >= 3 or quotes >= 1),
                f"{src} chỗ trích nguồn ({len(ext)} link ngoài) · {quotes} lời trích · {len(facts)} số liệu"))

    # G3 #20 — thông tin chỉ Rooty có
    exp = EXPERIENCE.findall(body_txt.lower())
    exp_kinds = sorted({e if isinstance(e, str) else e[0] for e in exp})
    C.append(_c(20, "Có thông tin chỉ Rooty mới có (kinh nghiệm HDV, mẹo, giờ đẹp, ảnh tự chụp, giá khách thực đi) — máy đếm dấu hiệu, người xác nhận",
                len(exp) >= 3, f"{len(exp)} dấu hiệu: " + (", ".join(exp_kinds[:8]) or "không thấy")))

    # G2 #13 — tác giả thật + kinh nghiệm trong nội dung
    nodes = _jsonld_nodes(mp.jsonld)
    author = ""
    for n in nodes:
        a = n.get("author")
        for x in (a if isinstance(a, list) else [a]):
            if isinstance(x, dict) and x.get("name") and "Organization" not in _types(x):
                author = x["name"]
        if author:
            break
    author = author or mp.meta.get("author", "")
    first_person = len(re.findall(r"\b(chúng tôi|mình|tôi|team|khi dẫn đoàn|dẫn khách)\b", body_txt.lower()))
    C.append(_c(13, "Có tác giả thật (Person) và kinh nghiệm nằm trong nội dung, không chỉ ở box tác giả", bool(author) and first_person >= 2,
                (f"tác giả: {author}" if author else "không thấy tác giả là người trong schema/meta") + f" · {first_person} câu kể ngôi thứ nhất/kinh nghiệm"))

    # G3 #22 — độ mới thật
    mod = None
    for n in nodes:
        if n.get("dateModified"):
            mod = _date(str(n["dateModified"]))
            if mod:
                break
    mod = mod or _date(mp.meta.get("article:modified_time", "")) or _date(mp.meta.get("og:updated_time", ""))
    age = (today - mod).days if mod else None
    limit = 30 if commercial else 365
    title_year = re.findall(r"\b(20\d{2})\b", mp.title + " " + bp.h1)
    spoof = bool(title_year) and age is not None and age > 60 and str(today.year) in title_year
    C.append(_c(22, f"Độ mới thật: cập nhật ≤ {limit} ngày ({'trang giá/bán/so sánh' if commercial else 'bài thông tin'}), không chỉ đổi năm trên tiêu đề",
                age is not None and age <= limit and not spoof,
                (f"dateModified {mod:%d/%m/%Y} ({age} ngày trước)" if mod else "không thấy dateModified")
                + (f" · tiêu đề ghi năm {title_year[0]} nhưng nội dung không cập nhật — dễ bị coi là đổi ngày giả" if spoof else "")))

    # G3 #24 — phản tác dụng guard
    types = set()
    for n in nodes:
        types |= {str(t) for t in _types(n)}
    listicle = bool(re.search(r"\b(top \d+|\d+ (công ty|đơn vị|địa chỉ|nơi)|tốt nhất|uy tín nhất)\b", bp.h1.lower()))
    agg = "AggregateRating" in types and not (types & {"Product", "TouristTrip", "LocalBusiness", "TravelAgency"})
    C.append(_c(24, "Không gắn AggregateRating lên bài tự viết; bài «top / uy tín nhất» không tự xếp Rooty #1 khi không có cách chấm công khai",
                not agg, ("có AggregateRating trên bài viết — gỡ" if agg else "không có AggregateRating trên bài")
                + (" · bài dạng danh sách xếp hạng: người kiểm Rooty có tự xếp #1 không, có ghi cách chấm" if listicle else "")))

    # Kiểm tay
    C.append(_c(21, "Mỗi dữ kiện quan trọng nằm trong một đoạn mà chính đoạn đó chứng minh được (AI xác minh từng đoạn trước khi gắn link)", None,
                "kiểm tay: đọc từng con số/khẳng định — câu chứa nó có đủ chủ thể + số + nguồn trong cùng đoạn không", auto=False))
    C.append(_c(23, "Visual semantic + Blur Test: ảnh đầu trang trả đúng ý định, thứ bậc hình khớp H2, không popup cắt ngang", None,
                "kiểm tay: chụp màn hình, làm mờ 50% — vẫn nhận ra bài nói về gì và làm được gì", auto=False))
    C.append(_c(25, "So với AI Overview đang hiện: phủ sâu ý AI bỏ sót, theo định dạng AI ưa (định nghĩa đầu, danh sách, dữ kiện)", None,
                f"kiểm tay: Google «{kw}» → đọc AI Overview → ghi ý nó thiếu → bổ sung", auto=False))

    auto = [c for c in C if c["auto"]]
    passed = sum(1 for c in auto if c["ok"])
    score = round(passed / max(len(auto), 1) * 100)
    gate_fail = [c for c in C if c["gate"] and c["ok"] is False]
    g3_nos = sorted({c["no"] for c in C if 14 <= c["no"] <= 25})
    g3_pass = sum(1 for n in g3_nos if all(c["ok"] for c in C if c["no"] == n and c["auto"]) and any(c["auto"] for c in C if c["no"] == n))
    return {"score": score, "passed": passed, "total": len(auto), "words": n_words, "h1": bp.h1, "author": author,
            "modified": mod.isoformat() if mod else "", "gate_ok": not gate_fail, "g3": f"{g3_pass}/12", "checks": C}


def render(res: dict, kw: str = "") -> str:
    if res.get("error"):
        return res["error"]
    head = (f"Điểm GEO {res['score']}/100 · {res['passed']}/{res['total']} tiêu chí đo được · G3 đạt {res['g3']} · "
            + ("✅ qua 4 cửa chặn G3" if res["gate_ok"] else "⛔ CHƯA qua cửa chặn (GTV: chưa qua thì các việc sau gần như không tác dụng)")
            + f" · {res['words']} từ")
    lines = [head]
    for c in res["checks"]:
        mark = "✅" if c["ok"] else ("✏️" if c["ok"] is None else "❌")
        lines.append(f"{mark} #{c['no']}{' 🔒' if c['gate'] else ''} {c['name']} — {c['detail']}")
    return "\n".join(lines)


# ------------------------------------------------------------------ G5 · phân tích câu trả lời của AI

BRAND_RE = re.compile(r"rooty\s*trip|rootytrip|\brooty\b", re.I)
DEFAULT_COMPETITORS = ["Klook", "Traveloka", "VinWonders", "Vinpearl", "Sun World", "Hòn Thơm", "Saigontourist", "Vietravel", "BestPrice",
                       "Mytour", "iVIVU", "Tripadvisor", "Booking.com", "Agoda", "Trip.com", "Phú Quốc Express", "John Tour", "Du lịch Việt",
                       "Tugo", "Fiditour", "Lữ hành Việt Nam", "Phu Quoc Tours", "Vietnam Travel", "Kkday", "GetYourGuide"]


def analyze_answer(text: str, competitors: list[str] | None = None, brand_facts: dict | None = None) -> dict:
    t = nfc(text or "")
    tl = t.lower()
    mention = bool(BRAND_RE.search(t))
    urls = re.findall(r"https?://[^\s)\]>\"']+", t)
    rooty_urls = [u for u in urls if "rootytrip" in u.lower()]
    # vị trí lần đầu nhắc tên trong danh sách các thương hiệu được nêu
    comps = []
    for c in (competitors or DEFAULT_COMPETITORS):
        m = re.search(r"(?<![\w.])" + re.escape(c.lower()) + r"(?!\w)", tl) if c else None
        if m and not BRAND_RE.search(c):
            comps.append((m.start(), c))
    order = sorted(comps + ([(BRAND_RE.search(t).start(), "Rooty Trip")] if mention else []))
    rank = next((i + 1 for i, (_, n) in enumerate(order) if n == "Rooty Trip"), None)
    issues = []
    if mention and brand_facts:
        # kiểm hotline / website AI nêu có khớp thông tin thương hiệu không
        phones = re.findall(r"(?<!\d)(?:\+?84|0)[\s.]?\d{2,3}(?:[\s.]?\d){6,7}(?!\d)", t)
        good = re.sub(r"\D", "", brand_facts.get("Hotline chính", ""))[-9:]
        for p in phones:
            d = re.sub(r"\D", "", p)[-9:]
            if good and d != good and BRAND_RE.search(t[max(0, t.find(p) - 200): t.find(p) + 50]):
                issues.append(f"số điện thoại {p} gần tên Rooty không khớp hotline {brand_facts.get('Hotline chính')}")
    return {"mention": mention, "link": bool(rooty_urls), "rooty_urls": rooty_urls, "urls": urls,
            "competitors": [n for _, n in sorted(comps)], "rank": rank, "issues": issues}


def presence_summary(rows: list[dict], question_count: int = 0) -> dict:
    """rows: bản ghi bảng Đo hiện diện AI. Báo theo chủ đề và theo máy AI (GTV #30–31), không theo từng câu."""
    by_engine = defaultdict(lambda: {"runs": 0, "mention": 0, "link": 0})
    by_topic = defaultdict(lambda: {"runs": 0, "mention": 0, "link": 0})
    runs_per = Counter()
    comp = Counter()
    wrong = 0
    dates = []
    for f in rows:
        e = f.get("Máy AI") or "?"
        tp = f.get("Chủ đề") or "?"
        m = f.get("Nhắc tên Rooty") == "Có"
        lk = f.get("Trích link Rooty") == "Có"
        for d in (by_engine[e], by_topic[tp]):
            d["runs"] += 1
            d["mention"] += m
            d["link"] += lk
        runs_per[(f.get("Mã câu") or f.get("Câu hỏi"), e)] += 1
        for c in re.split(r"[,;\n]", f.get("Đối thủ xuất hiện") or ""):
            if c.strip():
                comp[c.strip()] += 1
        if f.get("Thông tin đúng") in ("Sai", "Một phần"):
            wrong += 1
        if f.get("Ngày chạy"):
            dates.append(f["Ngày chạy"])
    pct = lambda d: {**d, "mentionPct": round(d["mention"] / d["runs"] * 100, 1) if d["runs"] else 0,
                     "linkPct": round(d["link"] / d["runs"] * 100, 1) if d["runs"] else 0}
    total_mention = sum(d["mention"] for d in by_engine.values())
    conc = {e: round(d["mention"] / total_mention * 100, 1) for e, d in by_engine.items()} if total_mention else {}
    few = sum(1 for v in runs_per.values() if v < 3)
    return {"runs": len(rows), "engines": {e: pct(d) for e, d in by_engine.items()}, "topics": {t: pct(d) for t, d in sorted(by_topic.items())},
            "competitors": comp.most_common(10), "wrong": wrong, "pairs": len(runs_per), "pairsUnder3": few,
            "concentration": conc, "concentrationAlert": [e for e, v in conc.items() if v > 70],
            "questions": question_count}
