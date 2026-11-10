#!/usr/bin/env python3
"""
GEO audit cho website — kiểm các "cửa chặn" kỹ thuật trong Checklist GEO (G0–G3).

Chỉ dùng thư viện chuẩn của Python, không cần cài gì thêm.

Cách chạy:
    python scripts/geo_audit.py https://rootytrip.com
    python scripts/geo_audit.py https://rootytrip.com --max-pages 30
    python scripts/geo_audit.py https://rootytrip.com --urls https://rootytrip.com/tour-a https://rootytrip.com/tour-b

Kết quả: in tóm tắt ra màn hình + ghi báo cáo Markdown vào reports/geo-audit-<domain>-<ngày>.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

USER_AGENT = "Mozilla/5.0 (compatible; RootyGEOAudit/1.0)"
TIMEOUT = 20

# Phân loại bot AI theo mục đích (Checklist GEO, việc #2)
AI_BOTS = {
    "Bot đi tìm nguồn (cần MỞ để được trích dẫn)": [
        "OAI-SearchBot", "Claude-SearchBot", "PerplexityBot", "Googlebot", "Bingbot",
    ],
    "Bot chạy khi người dùng hỏi (cần MỞ)": [
        "ChatGPT-User", "Claude-User", "Perplexity-User",
    ],
    "Bot lấy dữ liệu huấn luyện (tuỳ chọn, không ảnh hưởng Google Search)": [
        "GPTBot", "ClaudeBot", "Google-Extended", "CCBot",
    ],
}

# Tiêu đề mục "rỗng nghĩa" — làm đoạn nội dung mất ngữ cảnh khi AI cắt trang (việc #17)
EMPTY_HEADINGS = {
    "tổng quan", "giới thiệu", "kết luận", "lời kết", "tóm lại", "overview",
    "introduction", "conclusion", "summary", "thông tin", "chi tiết", "mô tả",
}


# ---------------------------------------------------------------- HTTP

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # để 301/302 trả về dạng HTTPError, giữ nguyên mã + Location


_NO_REDIRECT_OPENER = urllib.request.build_opener(_NoRedirect)


def fetch(url: str, follow: bool = True) -> tuple[int, bytes, dict, float]:
    """Trả về (status, body, headers, giây_chờ_byte_đầu). follow=False: không đi theo redirect."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"})
    t0 = time.perf_counter()
    opener = urllib.request.urlopen if follow else _NO_REDIRECT_OPENER.open
    try:
        with opener(req, timeout=TIMEOUT) as r:
            first = r.read(1)
            ttfb = time.perf_counter() - t0
            body = first + r.read()
            headers = {k.lower(): v for k, v in r.headers.items()}
            status = r.status
    except urllib.error.HTTPError as e:
        ttfb = time.perf_counter() - t0
        body = e.read() if hasattr(e, "read") else b""
        headers = {k.lower(): v for k, v in (e.headers or {}).items()}
        status = e.code
    if headers.get("content-encoding") == "gzip" or body[:2] == b"\x1f\x8b":
        try:
            body = gzip.decompress(body)
        except OSError:
            pass
    return status, body, headers, ttfb


def decode(body: bytes, headers: dict) -> str:
    m = re.search(r"charset=([\w-]+)", headers.get("content-type", ""))
    for enc in ([m.group(1)] if m else []) + ["utf-8", "cp1258", "latin-1"]:
        try:
            return body.decode(enc)
        except (LookupError, UnicodeDecodeError):
            continue
    return body.decode("utf-8", "replace")


# ---------------------------------------------------------------- HTML parsing

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = ""
        self.meta = {}
        self.canonical = None
        self.headings: list[tuple[str, str]] = []
        self.jsonld: list[str] = []
        self.images_total = 0
        self.images_no_alt = 0
        self.text_after_h1: list[str] = []
        self.body_text: list[str] = []
        self._stack: list[str] = []
        self._cur_heading = None
        self._heading_buf: list[str] = []
        self._in_title = False
        self._in_jsonld = False
        self._jsonld_buf: list[str] = []
        self._skip = 0
        self._seen_h1 = False

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical = a.get("href")
        elif tag in ("h1", "h2", "h3"):
            self._cur_heading = tag
            self._heading_buf = []
        elif tag == "img":
            self.images_total += 1
            if not a.get("alt", "").strip():
                self.images_no_alt += 1
        elif tag == "script":
            if "ld+json" in a.get("type", "").lower():
                self._in_jsonld = True
                self._jsonld_buf = []
            else:
                self._skip += 1
        elif tag in ("style", "noscript", "svg", "nav", "footer", "header"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == self._cur_heading:
            text = " ".join("".join(self._heading_buf).split())
            self.headings.append((tag, text))
            if tag == "h1":
                self._seen_h1 = True
            self._cur_heading = None
        elif tag == "script":
            if self._in_jsonld:
                self.jsonld.append("".join(self._jsonld_buf))
                self._in_jsonld = False
            elif self._skip:
                self._skip -= 1
        elif tag in ("style", "noscript", "svg", "nav", "footer", "header") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_jsonld:
            self._jsonld_buf.append(data)
            return
        if self._cur_heading:
            self._heading_buf.append(data)
        if self._skip:
            return
        s = data.strip()
        if not s:
            return
        self.body_text.append(s)
        if self._seen_h1 and not self._cur_heading:
            self.text_after_h1.append(s)


def jsonld_types(blocks: list[str]) -> tuple[list[str], bool, list[str]]:
    """Trả về (danh sách @type, có sameAs không, lỗi parse)."""
    types, errors, same_as = [], [], False

    def walk(node):
        nonlocal same_as
        if isinstance(node, dict):
            t = node.get("@type")
            if isinstance(t, list):
                types.extend(map(str, t))
            elif t:
                types.append(str(t))
            if node.get("sameAs"):
                same_as = True
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for b in blocks:
        try:
            walk(json.loads(b))
        except json.JSONDecodeError as e:
            errors.append(str(e)[:80])
    return sorted(set(types)), same_as, errors


# ---------------------------------------------------------------- sitemap

def sitemap_urls(base: str, robots_txt: str, limit: int) -> list[str]:
    candidates = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", robots_txt)
    candidates += [urllib.parse.urljoin(base, p) for p in ("/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml")]
    seen, out, queue = set(), [], list(dict.fromkeys(candidates))
    while queue and len(out) < limit:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            status, body, _, _ = fetch(sm)
            if status != 200:
                continue
            root = ET.fromstring(body)
        except Exception:
            continue
        # chỉ lấy <loc> con trực tiếp của <url>/<sitemap> — bỏ qua <image:loc>, <video:loc>
        locs = []
        for entry in root:
            for child in entry:
                if child.tag.split("}")[-1] == "loc" and child.text:
                    locs.append(child.text.strip())
        locs = [u for u in locs if not re.search(r"\.(jpe?g|png|gif|webp|svg|pdf|mp4)(\?|$)", u, re.I)]
        if root.tag.endswith("sitemapindex"):
            # ưu tiên sitemap bài viết/trang/tour trước
            locs.sort(key=lambda u: 0 if re.search(r"post|page|tour|product|hotel", u) else 1)
            queue.extend(locs)
        else:
            out.extend(u for u in locs if u not in out)
    return out[:limit]


# ---------------------------------------------------------------- audit

def audit_robots(base: str) -> tuple[str, list[dict]]:
    robots_url = urllib.parse.urljoin(base, "/robots.txt")
    status, body, headers, _ = fetch(robots_url)
    text = decode(body, headers) if status == 200 else ""
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(text.splitlines())
    rows = []
    for group, bots in AI_BOTS.items():
        for bot in bots:
            rows.append({"group": group, "bot": bot, "allowed": rp.can_fetch(bot, base.rstrip("/") + "/")})
    return text, rows


def audit_page(url: str) -> dict:
    r = {"url": url, "issues": [], "good": []}
    try:
        status, body, headers, ttfb = fetch(url)
    except Exception as e:
        r["status"] = "ERR"
        r["issues"].append(f"Không tải được trang: {e}")
        return r
    r["status"] = status
    r["ttfb_ms"] = round(ttfb * 1000)
    r["html_kb"] = round(len(body) / 1024)
    if status != 200:
        r["issues"].append(f"Mã trạng thái {status}")
        return r

    html = decode(body, headers)
    p = PageParser()
    try:
        p.feed(html)
    except Exception:
        pass

    # G1 · tốc độ máy chủ (việc #6)
    if r["ttfb_ms"] < 200:
        r["good"].append(f"Phản hồi máy chủ {r['ttfb_ms']}ms (<200ms tốt)")
    elif r["ttfb_ms"] < 350:
        r["good"].append(f"Phản hồi máy chủ {r['ttfb_ms']}ms (đạt mức tối thiểu <350ms)")
    else:
        r["issues"].append(f"Phản hồi máy chủ chậm: {r['ttfb_ms']}ms (khuyến nghị <350ms)")

    # G1 · HTML ≤ 2MB (việc #8)
    if len(body) > 2 * 1024 * 1024:
        r["issues"].append(f"HTML nặng {r['html_kb']}KB (> 2MB, máy AI có thể cắt bớt)")

    # G1 · lập chỉ mục & canonical (việc #7)
    robots_meta = (p.meta.get("robots", "") + " " + headers.get("x-robots-tag", "")).lower()
    if "noindex" in robots_meta:
        r["issues"].append("🔴 Trang đang noindex — không thể được AI lấy làm nguồn")
    if not p.canonical:
        r["issues"].append("Thiếu thẻ canonical")
    else:
        c = urllib.parse.urljoin(url, p.canonical).rstrip("/")
        if c != url.rstrip("/"):
            r["issues"].append(f"Canonical trỏ sang URL khác: {c}")
        else:
            r["good"].append("Canonical tự trỏ")

    r["title"] = " ".join(p.title.split())
    r["meta_description"] = p.meta.get("description", "")
    if not r["title"]:
        r["issues"].append("Thiếu thẻ title")
    if not r["meta_description"]:
        r["issues"].append("Thiếu meta description")
    if not p.lang:
        r["issues"].append("Thẻ <html> thiếu thuộc tính lang")

    # Cấu trúc tiêu đề (việc #15, #17)
    h1s = [t for tag, t in p.headings if tag == "h1"]
    h2s = [t for tag, t in p.headings if tag == "h2"]
    r["h1"] = h1s
    r["h2"] = h2s
    if len(h1s) == 0:
        r["issues"].append("Không có H1")
    elif len(h1s) > 1:
        r["issues"].append(f"Có {len(h1s)} thẻ H1 (nên chỉ 1)")
    empty = [h for h in h2s if h.strip().lower().rstrip(":") in EMPTY_HEADINGS]
    if empty:
        r["issues"].append(f"H2 rỗng nghĩa (AI cắt đoạn sẽ mất ngữ cảnh): {', '.join(empty)}")
    question_h2 = [h for h in h2s if h.strip().endswith("?")]
    if h2s:
        r["question_h2_ratio"] = round(len(question_h2) / len(h2s), 2)

    # Mở đầu = câu trả lời (việc #14): ~400 ký tự đầu sau H1
    opening = " ".join(" ".join(p.text_after_h1).split())[:400]
    r["opening_400"] = opening
    if h1s and len(opening) < 150:
        r["issues"].append("Đoạn mở đầu sau H1 quá ngắn hoặc bị chen bởi nút/khối khác")
    junk = [k for k in ("Tác giả:", "Ngày đăng:", "Lượt xem:", "Cập nhật:", "Chia sẻ", "Share") if k in opening[:250]]
    if junk:
        r["issues"].append("Khối meta chen giữa H1 và câu trả lời (" + ", ".join(junk) + ") — chuyển xuống dưới đoạn mở đầu hoặc đánh dấu ngoài main content")

    # Tỷ lệ H2 dạng câu hỏi thật (việc #15) — bỏ qua khối liên quan cuối bài
    content_h2 = [h for h in h2s if h.lower() not in ("tin tức liên quan", "có thể bạn sẽ thích", "bài viết liên quan")]
    if len(content_h2) >= 3 and sum(h.endswith("?") for h in content_h2) / len(content_h2) < 0.3:
        r["issues"].append("Ít H2 dạng câu hỏi khách thật sự hỏi AI (<30%)")

    words = len(" ".join(p.body_text).split())
    r["word_count"] = words
    if words < 300:
        r["issues"].append(f"Nội dung chữ mỏng ({words} từ) — có thể đang dựng bằng JS hoặc nằm trong ảnh")

    # Schema (việc #12) — làm vì hiểu thực thể, KHÔNG phải để được trích dẫn
    types, same_as, errs = jsonld_types(p.jsonld)
    r["schema_types"] = types
    if errs:
        r["issues"].append(f"JSON-LD lỗi cú pháp: {errs[0]}")
    if not types:
        r["issues"].append("Không có dữ liệu có cấu trúc (JSON-LD)")
    else:
        r["good"].append("Schema: " + ", ".join(types[:8]))
    r["has_sameAs"] = same_as

    # Tác giả & ngày cập nhật (việc #13, #22)
    has_author = bool(p.meta.get("author")) or "Person" in types or re.search(r'"author"\s*:', html) is not None
    r["has_author"] = has_author
    modified = p.meta.get("article:modified_time") or (re.search(r'"dateModified"\s*:\s*"([^"]+)"', html) or [None, None])[1]
    r["date_modified"] = modified

    # Ảnh thiếu alt
    if p.images_total:
        r["images"] = f"{p.images_no_alt}/{p.images_total} ảnh thiếu alt"
        if p.images_no_alt / p.images_total > 0.3:
            r["issues"].append(r["images"])
    return r


# ---------------------------------------------------------------- report

def write_report(base: str, robots_text: str, bots: list[dict], pages: list[dict], out: Path) -> None:
    today = dt.date.today().isoformat()
    L = [f"# GEO audit — {base}", "", f"Ngày chạy: {today} · {len(pages)} trang · script `scripts/geo_audit.py`", ""]

    L += ["## 1. Quyền vào website của bot AI (Checklist việc #2 — cửa chặn)", ""]
    if not robots_text:
        L += ["⚠ Không đọc được robots.txt (mọi bot mặc định được vào).", ""]
    L += ["| Nhóm | Bot | Trạng thái |", "|---|---|---|"]
    for b in bots:
        L.append(f"| {b['group']} | {b['bot']} | {'✅ Mở' if b['allowed'] else '⛔ Chặn'} |")
    blocked_needed = [b["bot"] for b in bots if not b["allowed"] and "huấn luyện" not in b["group"]]
    L += ["", "**Kết luận:** " + (
        f"🔴 Đang chặn bot cần thiết: {', '.join(blocked_needed)} — mở ra trong robots.txt (và kiểm cả tường lửa/CDN như Cloudflare)."
        if blocked_needed else "✅ Các bot đi tìm nguồn và bot chạy khi người dùng hỏi đều được vào (theo robots.txt). Vẫn cần kiểm tường lửa/CDN."), ""]

    L += ["## 2. Tổng hợp lỗi theo tần suất", ""]
    counter: dict[str, int] = {}
    for pg in pages:
        for i in pg["issues"]:
            key = re.sub(r"\b\d+", "N", re.split(r"[:(]", i)[0]).strip()
            counter[key] = counter.get(key, 0) + 1
    if counter:
        L += ["| Lỗi | Số trang |", "|---|---|"]
        for k, v in sorted(counter.items(), key=lambda x: -x[1]):
            L.append(f"| {k} | {v}/{len(pages)} |")
    else:
        L.append("Không phát hiện lỗi kỹ thuật nào trong các trang đã quét.")
    L.append("")

    L += ["## 3. Chi tiết từng trang", ""]
    for pg in pages:
        L += [f"### {pg.get('title') or pg['url']}", "", f"- URL: {pg['url']}",
              f"- Trạng thái: {pg.get('status')} · phản hồi {pg.get('ttfb_ms', '?')}ms · HTML {pg.get('html_kb', '?')}KB · {pg.get('word_count', '?')} từ"]
        if pg.get("h1"):
            L.append(f"- H1: {' | '.join(pg['h1'])}")
        if pg.get("h2"):
            L.append(f"- H2 ({len(pg['h2'])}, tỷ lệ dạng câu hỏi {pg.get('question_h2_ratio', 0):.0%}): " + " · ".join(pg["h2"][:12]))
        if pg.get("opening_400"):
            L.append(f"- 400 ký tự đầu sau H1: _{pg['opening_400']}_")
        L.append(f"- Tác giả: {'có' if pg.get('has_author') else 'không thấy'} · Cập nhật: {pg.get('date_modified') or 'không thấy'} · sameAs: {'có' if pg.get('has_sameAs') else 'không'}")
        for g in pg["good"]:
            L.append(f"- ✅ {g}")
        for i in pg["issues"]:
            L.append(f"- ❌ {i}")
        L.append("")

    L += ["## 4. Những thứ script KHÔNG kiểm được (làm tay hoặc dùng skill)", "",
          "- Trang có lên trang 1 Google cho ít nhất 1 câu hỏi con không (việc #1) → Search Console.",
          "- Thử `site:domain + câu hỏi khách hay hỏi` (việc #9) → skill `rooty-geo-audit`.",
          "- AI có nhắc tên Rooty Trip không, nói có đúng không (việc #3, #30) → skill `rooty-do-hien-dien-ai`.",
          "- Tường lửa/CDN có chặn bot AI không dù robots.txt mở.",
          "- Thông tin thương hiệu nhất quán trên GBP, Facebook, OTA (việc #11).", ""]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="GEO audit cho website")
    ap.add_argument("site", help="Trang chủ, ví dụ https://rootytrip.com")
    ap.add_argument("--max-pages", type=int, default=15, help="Số trang lấy từ sitemap (mặc định 15)")
    ap.add_argument("--urls", nargs="*", help="Chỉ audit các URL này thay vì đọc sitemap")
    ap.add_argument("--out", help="Đường dẫn file báo cáo .md")
    args = ap.parse_args()

    base = args.site if args.site.startswith("http") else "https://" + args.site
    domain = urllib.parse.urlparse(base).netloc

    print(f"→ Đọc robots.txt của {domain} ...")
    robots_text, bots = audit_robots(base)
    urls = args.urls or ([base] + [u for u in sitemap_urls(base, robots_text, args.max_pages) if u.rstrip("/") != base.rstrip("/")])[: args.max_pages]
    print(f"→ Audit {len(urls)} trang ...")
    pages = []
    for i, u in enumerate(urls, 1):
        pg = audit_page(u)
        pages.append(pg)
        print(f"  [{i}/{len(urls)}] {pg.get('status')} {len(pg['issues'])} lỗi  {u}")

    out = Path(args.out) if args.out else Path(os.path.abspath(__file__)).parent.parent / "reports" / f"geo-audit-{domain}-{dt.date.today().isoformat()}.md"
    write_report(base, robots_text, bots, pages, out)
    blocked = [b["bot"] for b in bots if not b["allowed"]]
    print(f"\nBot bị chặn: {', '.join(blocked) or 'không có'}")
    print(f"Báo cáo: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
