"""
Kiểm tự động các mục Technical SEO (mã T01–T26 trong tables.TECH_CHECKLIST).
Chỉ dùng thư viện chuẩn. Trả về {mã: (kết_quả, chi_tiết)} với kết_quả ∈ Đạt / Chưa đạt / Chưa kiểm / Không áp dụng.
"""
from __future__ import annotations

import json
import os
import random
import re
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0, str(ROOT / "scripts"))
from geo_audit import AI_BOTS, PageParser, decode, fetch, jsonld_types, sitemap_urls  # noqa: E402

OK, BAD, NA, SKIP = "Đạt", "Chưa đạt", "Không áp dụng", "Chưa kiểm"


def _safe(fn):
    try:
        return fn()
    except Exception as e:  # một mục lỗi không làm hỏng cả lượt kiểm
        return SKIP, f"Không kiểm được: {str(e)[:120]}"


def _home(base):
    status, body, headers, ttfb = fetch(base + "/")
    html = decode(body, headers)
    p = PageParser()
    try:
        p.feed(html)
    except Exception:
        pass
    return status, html, headers, ttfb, p


def check_site(site: str, psi_key: str | None = None) -> dict:
    base = site.rstrip("/")
    if not base.startswith("http"):
        base = "https://" + base
    host = urllib.parse.urlsplit(base).netloc
    R = {}

    # ---- robots.txt
    st, body, hd, _ = fetch(base + "/robots.txt")
    robots = decode(body, hd) if st == 200 else ""
    R["T01"] = (OK, "robots.txt trả 200") if st == 200 else (BAD, f"robots.txt trả mã {st}")
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(robots.splitlines())
    blocked = [p for p in ("/", "/wp-content/uploads/a.jpg", "/wp-content/themes/a.css", "/wp-includes/js/a.js")
               if not rp.can_fetch("Googlebot", base + p)]
    R["T02"] = (OK, "Googlebot vào được trang, CSS, JS, ảnh") if not blocked else (BAD, "Đang chặn Googlebot: " + ", ".join(blocked))
    sm_lines = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", robots)
    R["T03"] = (OK, "Khai báo: " + ", ".join(sm_lines[:3])) if sm_lines else (BAD, "robots.txt chưa có dòng Sitemap:")

    # ---- sitemap
    urls = sitemap_urls(base, robots, 5000)
    R["T04"] = (OK, f"Đọc được {len(urls)} URL trong sitemap") if urls else (BAD, "Không tìm thấy sitemap đọc được (/sitemap.xml, /sitemap_index.xml)")
    if urls:
        sample = urls[:: max(1, len(urls) // 25)][:25]
        with ThreadPoolExecutor(6) as ex:
            res = list(ex.map(lambda u: (u, _safe(lambda: fetch(u, follow=False)[0])), sample))
        bad = [(u, s) for u, s in res if s != 200]
        R["T05"] = (OK, f"{len(sample)}/{len(sample)} URL mẫu trả 200") if not bad else \
            (BAD, f"{len(bad)}/{len(sample)} URL mẫu không trả 200:\n" + "\n".join(f"{s} · {u}" for u, s in bad[:8]))
    else:
        R["T05"] = (SKIP, "Không có sitemap để kiểm")

    # ---- HTTPS & URL
    def t06():
        s, _, h, _ = fetch("http://" + host + "/", follow=False)
        loc = h.get("location", "")
        return (OK, f"http → {s} → {loc}") if s in (301, 308) and loc.startswith("https://") else (BAD, f"http trả {s} {loc}".strip())
    R["T06"] = _safe(t06)

    def t07():
        alt = host[4:] if host.startswith("www.") else "www." + host
        try:
            s, _, h, _ = fetch("https://" + alt + "/", follow=False)
        except Exception:
            return BAD, f"{alt} không truy cập được — nên trỏ DNS và 301 về {host}"
        loc = h.get("location", "")
        return (OK, f"{alt} → {s} → {loc}") if s in (301, 308) and host in loc else (BAD, f"{alt} trả {s} {loc} (nên 301 về {host})")
    R["T07"] = _safe(t07)

    st, html, hd, _, p = _home(base)
    R["T08"] = (OK, hd.get("strict-transport-security", "")) if "strict-transport-security" in hd else (BAD, "Chưa có header Strict-Transport-Security")
    mixed = re.findall(r'(?:src|href)=["\']http://[^"\']+\.(?:js|css|jpe?g|png|webp|gif|svg)', html, re.I)
    R["T09"] = (OK, "Không thấy tài nguyên http:// trên trang chủ") if not mixed else (BAD, f"{len(mixed)} tài nguyên http://, VD: {mixed[0][:120]}")

    def t10():
        u = f"{base}/kiem-tra-404-{random.randint(10**6, 10**7)}/"
        s = fetch(u, follow=False)[0]
        return (OK, f"URL không tồn tại trả {s}") if s in (404, 410) else (BAD, f"URL không tồn tại trả {s} (soft-404)")
    R["T10"] = _safe(t10)

    canon = urllib.parse.urljoin(base + "/", p.canonical) if p.canonical else ""
    R["T11"] = (OK, f"canonical: {canon}") if canon.rstrip("/") == base.rstrip("/") else \
        (BAD, f"canonical trang chủ: {canon or 'không có'}")

    # ---- tốc độ
    def t17():
        ts = []
        for _ in range(3):
            ts.append(fetch(base + "/")[3] * 1000)
            time.sleep(0.3)
        m = round(statistics.median(ts))
        return (OK if m < 350 else BAD), f"Trung vị {m}ms (3 lần: {', '.join(str(round(t)) for t in ts)}ms)"
    R["T17"] = _safe(t17)

    def t18():
        req = urllib.request.Request(base + "/", headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip, br"})
        with urllib.request.urlopen(req, timeout=20) as r:
            enc = r.headers.get("content-encoding", "")
        return (OK, f"content-encoding: {enc}") if enc in ("gzip", "br", "zstd", "deflate") else (BAD, "Không thấy nén gzip/brotli")
    R["T18"] = _safe(t18)

    R["T19"] = _safe(lambda: _psi(base + "/", psi_key))

    # ---- mobile, ngôn ngữ
    R["T20"] = (OK, p.meta.get("viewport", "")) if "width=device-width" in p.meta.get("viewport", "") else (BAD, "Thiếu meta viewport width=device-width")
    R["T21"] = (OK, f"lang='{p.lang}'") if p.lang else (BAD, "Thẻ <html> thiếu lang")
    alts = re.findall(r'<link[^>]+hreflang=["\']([^"\']+)["\']', html, re.I)
    has_lang_versions = any(re.search(r"https?://[^/]+/(en|ja|ko|zh)/", u) for u in urls[:5000]) or re.search(r'href=["\'][^"\']*/(en|ja)/', html)
    if alts:
        R["T22"] = (OK, "hreflang: " + ", ".join(sorted(set(alts)))) if "x-default" in alts else (BAD, "Có hreflang (" + ", ".join(sorted(set(alts))) + ") nhưng thiếu x-default")
    else:
        R["T22"] = (BAD, "Site có bản /en/, /ja/ nhưng trang chủ không khai báo hreflang") if has_lang_versions else (NA, "Không thấy bản ngôn ngữ khác")

    # ---- schema
    def t23():
        pages = [base + "/"] + (urls[1:: max(1, len(urls) // 3)][:3] if urls else [])
        errs = []
        for u in pages:
            s, b, h, _ = fetch(u)
            pp = PageParser()
            pp.feed(decode(b, h))
            _, _, e = jsonld_types(pp.jsonld)
            if e:
                errs.append(f"{u} · {e[0]}")
        return (OK, f"{len(pages)} trang mẫu không lỗi JSON-LD") if not errs else (BAD, "\n".join(errs))
    R["T23"] = _safe(t23)
    types, same_as, _ = jsonld_types(p.jsonld)
    R["T24"] = (OK, "Có sameAs · schema: " + ", ".join(types[:8])) if same_as else (BAD, "Schema trang chủ chưa có sameAs · " + ", ".join(types[:8]))

    # ---- bot AI
    def bots(group_kw):
        rows = [(b, rp.can_fetch(b, base + "/")) for g, bs in AI_BOTS.items() if group_kw in g for b in bs]
        no = [b for b, ok in rows if not ok]
        return (OK, "Mở: " + ", ".join(b for b, _ in rows)) if not no else (BAD, "Đang chặn: " + ", ".join(no))
    R["T25"] = bots("đi tìm nguồn")
    R["T26"] = bots("người dùng hỏi")
    return R


def _psi(url, key, strategy="mobile"):
    q = {"url": url, "strategy": strategy, "category": "performance"}
    if key:
        q["key"] = key
    api = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?" + urllib.parse.urlencode(q)
    try:
        with urllib.request.urlopen(urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0"}), timeout=90) as r:
            d = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return SKIP, "PageSpeed giới hạn lượt gọi — thử lại sau, hoặc thêm PAGESPEED_API_KEY vào .env"
        return SKIP, f"PageSpeed lỗi HTTP {e.code}"
    score = d.get("lighthouseResult", {}).get("categories", {}).get("performance", {}).get("score")
    m = (d.get("loadingExperience") or {}).get("metrics") or {}
    lcp = m.get("LARGEST_CONTENTFUL_PAINT_MS", {}).get("percentile")
    cls = m.get("CUMULATIVE_LAYOUT_SHIFT_SCORE", {}).get("percentile")
    inp = m.get("INTERACTION_TO_NEXT_PAINT", {}).get("percentile")
    lab = f"điểm hiệu năng (lab) {round(score * 100) if score is not None else '?'}/100"
    if lcp is not None and cls is not None:
        cls_v = cls / 100  # API trả CLS × 100
        ok = lcp <= 2500 and cls_v <= 0.1 and (inp is None or inp <= 200)
        detail = f"Người dùng thật ({'di động' if strategy == 'mobile' else 'máy tính'}): LCP {lcp/1000:.1f}s · CLS {cls_v:.2f}" + (f" · INP {inp}ms" if inp is not None else "") + f" · {lab}"
        return (OK if ok else BAD), detail
    if score is None:
        return SKIP, "PageSpeed không trả kết quả"
    return (OK if score >= 0.5 else BAD), f"Chưa có dữ liệu người dùng thật; {lab} (đạt khi ≥ 50)"


# ------------------------------------------------------------------ mẫu trang để kiểm UX/Onsite/Entity

def _sample_pages(rows):
    ok = [r for r in rows if r.get("status") == "200" and "?" not in r["url"] and not re.search(r"/page/\d+/?$", r["url"])
          and not re.search(r"https?://[^/]+/(en|ja|ko|zh|ru|zh-hans|zh-hant)/", r["url"])]
    prod = next((r["url"] for r in ok if "/san-pham/" in r["url"]), None)
    blogs = [r["url"] for r in ok if re.fullmatch(r"https?://[^/]+/[a-z0-9-]+/?", r["url"])
             and not re.search(r"/(tour-|combo-|ve-|khach-san|lien-he|gioi-thieu|chinh-sach)", r["url"])
             and int(r.get("words") or 0) > 800][:3]
    contact = next((r["url"] for r in ok if "lien-he" in r["url"]), None)
    return prod, blogs, contact


def _get(url):
    st, body, hd, _ = fetch(url)
    html = decode(body, hd)
    p = PageParser()
    try:
        p.feed(html)
    except Exception:
        pass
    return st, html, p


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
        except ValueError:
            pass
    return out


def _types(n):
    t = n.get("@type")
    return [t] if isinstance(t, str) else (t or [])


# Số Việt Nam: di động 03/05/07/08/09 + 8 số, cố định 02x + 8 số, tổng đài 1800/1900; không dính vào dãy số dài khác
PHONE_RE = re.compile(r"(?<![\d.])(?:\+84[\s.\-]?|0)(?:[35789]\d|2\d\d)(?:[\s.\-]?\d){6,8}(?![\d])|(?<!\d)1[89]00[\s.\-]?\d{3,4}(?:[\s.\-]?\d{2,3})?(?!\d)")


def _phones(text):
    out = set()
    for m in PHONE_RE.finditer(text):
        d = re.sub(r"\D", "", m.group(0))
        if d.startswith("84"):
            d = "0" + d[2:]
        if (d.startswith("0") and len(d) in (10, 11)) or d.startswith(("1800", "1900")):
            out.add(d)
    return out


def check_extra(site: str, rows, psi_key=None) -> dict:
    """Mục kiểm cần tải thêm trang mẫu: T27, T28, S02, U02–U05, O09–O11, E01, E03, E04."""
    base = site.rstrip("/")
    R = {}
    st, home, hp = _get(base + "/")
    rb = (hp.meta.get("robots", "") or "").lower()
    R["T28"] = (BAD, f"meta robots trang chủ: {rb}") if ("noindex" in rb or "nofollow" in rb) else (OK, f"meta robots: {rb or 'không đặt (mặc định index, follow)'}")
    R["T27"] = _safe(lambda: _psi(base + "/", psi_key, "desktop"))
    R["U02"] = (OK, "Trang chủ có ô tìm kiếm") if re.search(r'<input[^>]+(type=["\']search["\']|name=["\']s["\'])', home, re.I) else (BAD, "Không thấy ô tìm kiếm trên trang chủ")
    R["U05"] = (OK, "Có mã: " + ", ".join(sorted(set(re.findall(r"\b(G-[A-Z0-9]{6,}|GTM-[A-Z0-9]{4,})\b", home)))[:4])) \
        if re.search(r"\b(G-[A-Z0-9]{6,}|GTM-[A-Z0-9]{4,})\b", home) else (BAD, "Không thấy mã GA4 (G-…) hoặc GTM trên trang chủ")

    prod, blogs, contact = _sample_pages(rows or [])
    samples = [base + "/"] + ([prod] if prod else []) + blogs
    pages = {base + "/": (home, hp)}
    for u in samples[1:]:
        try:
            _, h, pp = _get(u)
            pages[u] = (h, pp)
        except Exception:
            pass

    # Silo / UX: breadcrumb
    bc_schema = [u for u in samples[1:] if u in pages and any("BreadcrumbList" in _types(n) for n in _jsonld_nodes(pages[u][1].jsonld))]
    bc_visual = [u for u in samples[1:] if u in pages and re.search(r'breadcrumb', pages[u][0], re.I)]
    n = max(len(samples) - 1, 1)
    R["S02"] = (OK if len(bc_schema) == n else BAD, f"BreadcrumbList trên {len(bc_schema)}/{n} trang mẫu") if len(samples) > 1 else (SKIP, "Chưa có báo cáo crawl để chọn trang mẫu")
    R["U03"] = (OK if len(bc_visual) == n else BAD, f"Breadcrumb hiển thị trên {len(bc_visual)}/{n} trang mẫu") if len(samples) > 1 else (SKIP, "Chưa có trang mẫu")

    # CTA trang tour
    if prod and prod in pages:
        h = pages[prod][0]
        found = [n for n, pat in (("Zalo", r"zalo\.me|zalo\.vn|oa\.zalo"), ("Gọi", r'href=["\']tel:'), ("Messenger", r"m\.me/|messenger\.com"), ("Form đặt", r"<form"))
                 if re.search(pat, h, re.I)]
        R["U04"] = (OK if any(x in found for x in ("Zalo", "Gọi", "Messenger")) else BAD, f"Trang tour mẫu {prod}: " + (", ".join(found) or "không thấy nút liên hệ"))
    else:
        R["U04"] = (SKIP, "Chưa tìm được trang tour mẫu (cần báo cáo crawl)")

    # Ảnh
    imgs = []
    for u, (h, _) in pages.items():
        for tag in re.findall(r"<img\b[^>]*>", h, re.I):
            src = (re.search(r'\b(?:data-lazy-src|data-src|src)=["\']([^"\']+)["\']', tag) or [None, ""])[1]
            if not src or src.startswith("data:") or src.endswith(".svg"):
                continue
            alt = re.search(r'\balt=["\']([^"\']*)["\']', tag)
            imgs.append((urllib.parse.urljoin(u, src), bool(alt and alt.group(1).strip())))
    if imgs:
        with_alt = sum(a for _, a in imgs)
        R["O09"] = (OK if with_alt / len(imgs) >= 0.9 else BAD, f"{with_alt}/{len(imgs)} ảnh có alt ({round(with_alt / len(imgs) * 100)}%) trên {len(pages)} trang mẫu")
        webp = sum(1 for s, _ in imgs if re.search(r"\.(webp|avif)(\?|$)|format=webp", s, re.I))
        R["O10"] = (OK if webp / len(imgs) >= 0.8 else BAD, f"{webp}/{len(imgs)} ảnh là WebP/AVIF ({round(webp / len(imgs) * 100)}%)")
        uniq = list(dict.fromkeys(s for s, _ in imgs))[:20]

        def size(u):
            try:
                req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=15) as r:
                    return int(r.headers.get("content-length") or 0)
            except Exception:
                return 0
        with ThreadPoolExecutor(6) as ex:
            sizes = list(ex.map(size, uniq))
        big = [(u, s) for u, s in zip(uniq, sizes) if s > 200 * 1024]
        R["O11"] = (OK, f"{len(uniq)} ảnh mẫu đều ≤ 200KB") if not big else (BAD, f"{len(big)}/{len(uniq)} ảnh > 200KB:\n" + "\n".join(f"{round(s/1024)}KB · {u}" for u, s in big[:6]))
    else:
        for c in ("O09", "O10", "O11"):
            R[c] = (SKIP, "Không đọc được ảnh trên trang mẫu")

    # Entity: NAP trên web
    ph_home = _phones(re.sub(r"<[^>]+>", " ", home))
    ph_contact = set()
    if contact:
        try:
            _, ch, _ = _get(contact)
            ph_contact = _phones(re.sub(r"<[^>]+>", " ", ch))
        except Exception:
            pass
    if ph_home:
        same = (not contact) or bool(ph_home & ph_contact)
        R["E01"] = (OK if same else BAD, f"Số trên trang chủ: {', '.join(sorted(ph_home)[:4])}" + (f" · trang liên hệ: {', '.join(sorted(ph_contact)[:4]) or 'không thấy'}" if contact else " · không tìm thấy trang liên hệ"))
    else:
        R["E01"] = (BAD, "Không thấy số điện thoại dạng chữ trên trang chủ (có thể nằm trong ảnh/nút)")

    org = [n for n in _jsonld_nodes(hp.jsonld) if set(_types(n)) & {"Organization", "TravelAgency", "LocalBusiness", "Corporation"}]
    if org:
        o = max(org, key=len)
        need = ["name", "url", "logo", "telephone", "address"]
        miss = [k for k in need if not o.get(k)]
        R["E03"] = (OK if not miss else BAD, f"{'/'.join(_types(o))}: " + ("đủ " + ", ".join(need) if not miss else "thiếu " + ", ".join(miss)))
    else:
        R["E03"] = (BAD, "Trang chủ không có schema Organization/TravelAgency/LocalBusiness")

    if blogs and blogs[0] in pages:
        nodes = _jsonld_nodes(pages[blogs[0]][1].jsonld)
        person = any("Person" in _types(n) for n in nodes)
        R["E04"] = (OK if person else BAD, f"{blogs[0]}: " + ("có author Person" if person else "không thấy schema Person cho tác giả"))
    else:
        R["E04"] = (SKIP, "Chưa có bài viết mẫu")
    return R


def check_tables(T: dict) -> dict:
    """Mục kiểm dựa trên dữ liệu các tab khác: S04–S06, E02, E05–E07. T = {key: [fields…]}."""
    R = {}
    tr = [f for f in T.get("trang", []) if f.get("Loại trang") not in ("Trang tag", "Ngôn ngữ khác")]
    if tr:
        has = sum(1 for f in tr if f.get("Cụm chủ đề"))
        R["S04"] = (OK if has / len(tr) >= 0.8 else BAD, f"{has}/{len(tr)} trang đã gán cụm ({round(has / len(tr) * 100)}%)")
        cl = {}
        for f in T.get("trang", []):
            if f.get("Cụm chủ đề"):
                cl.setdefault(f["Cụm chủ đề"], 0)
                cl[f["Cụm chủ đề"]] += f.get("Vai trò silo") == "Pillar (trụ cột)"
        if cl:
            bad = [f"{c} ({n})" for c, n in cl.items() if n != 1]
            R["S05"] = (OK, f"{len(cl)} cụm đều có đúng 1 Pillar") if not bad else (BAD, f"{len(bad)}/{len(cl)} cụm không có đúng 1 Pillar: " + ", ".join(bad[:8]))
        else:
            R["S05"] = (BAD, "Chưa cụm nào được gán trang (tab B3)")
    else:
        R["S04"] = R["S05"] = (SKIP, "Bảng Trang đích trống — Chạy crawl / Nạp trang từ crawl")
    kw = [f for f in T.get("tukhoa", []) if f.get("Trạng thái") != "Bỏ"]
    if kw:
        tiers = {"TOFU (Thông tin)": "Thông tin", "MOFU (Cân nhắc)": "Cân nhắc", "BOFU (Mua)": "Mua"}
        parts, ok = [], True
        for label, it in tiers.items():
            xs = [f for f in kw if f.get("Ý định") == it]
            m = sum(1 for f in xs if f.get("Trang đích"))
            parts.append(f"{label}: {m}/{len(xs)} từ khoá có trang")
            ok = ok and xs and m / len(xs) >= 0.3
        R["S06"] = (OK if ok else BAD, " · ".join(parts) + " (đạt khi mỗi tầng ≥ 30%)")
    else:
        R["S06"] = (SKIP, "Bảng Từ khoá trống (tab B2)")
    hs = T.get("hoso", [])
    if hs:
        have = [f for f in hs if f.get("Trạng thái") == "Đã có"]
        unchecked = [f for f in have if f.get("Khớp NAP") in (None, "", "Chưa kiểm")]
        lech = [f.get("Nền tảng") for f in have if f.get("Khớp NAP") == "Lệch"]
        if not have:
            R["E02"] = (SKIP, "Chưa đánh dấu hồ sơ nào 'Đã có' ở tab B8")
        elif lech:
            R["E02"] = (BAD, "Lệch NAP: " + ", ".join(lech))
        elif unchecked:
            R["E02"] = (SKIP, f"{len(unchecked)}/{len(have)} hồ sơ chưa kiểm NAP")
        else:
            R["E02"] = (OK, f"{len(have)} hồ sơ đều khớp NAP")
        gbp = next((f for f in hs if "Google Business" in str(f.get("Nền tảng", ""))), None)
        R["E05"] = (OK, "GBP đã có, khớp NAP") if gbp and gbp.get("Trạng thái") == "Đã có" and gbp.get("Khớp NAP") == "Khớp" \
            else (BAD, f"GBP: {gbp.get('Trạng thái') if gbp else 'chưa có dòng'} · NAP {gbp.get('Khớp NAP') if gbp else '—'} (cập nhật ở tab B8)")
        R["E06"] = (OK if len(have) >= 5 else BAD, f"{len(have)} hồ sơ 'Đã có': " + ", ".join(f.get("Nền tảng", "") for f in have[:8]))
    else:
        R["E02"] = R["E05"] = R["E06"] = (SKIP, "Bảng Hồ sơ thương hiệu trống — tab B8 · Nạp dữ liệu mẫu rồi cập nhật")
    lk = [f for f in T.get("lienket", []) if f.get("Loại") in ("Báo chí", "Hồ sơ/citation") and f.get("Trạng thái") in ("Đã gắn", "Đang live")]
    R["E07"] = (OK if len(lk) >= 5 else BAD, f"{len(lk)} báo chí/citation đang live (tab B9)")
    return R


def check_crawl(rows, reports_dir=None) -> dict:
    """Các mục lấy từ báo cáo crawl: T12–T16, S01, S07–S09, O01–O07, O05, O12."""
    codes = ("T12", "T13", "T14", "T15", "T16", "S01", "S07", "S08", "S09", "O01", "O02", "O03", "O04", "O06", "O07")
    if not rows:
        msg = (SKIP, "Chưa có báo cáo crawl — bấm «Chạy crawl»")
        return {c: msg for c in codes}
    R = _crawl_tech(rows)
    page = lambda u: re.search(r"/page/\d+/?$", u) or "?" in u
    lang = lambda u: re.search(r"https?://[^/]+/(en|ja|ko|zh|ru|zh-hans|zh-hant)/", u)
    ok = [r for r in rows if r.get("status") == "200" and r.get("title") is not None and not page(r["url"])]
    vi = [r for r in ok if not lang(r["url"])]
    cat = [r for r in vi if re.fullmatch(r"https?://[^/]+/(tour-|combo-|ve-)[a-z0-9-]*/?", r["url"])]
    deep_cat = [r for r in cat if int(r.get("depth") or 9) > 1]
    R["S01"] = (OK if cat and not deep_cat else BAD, f"{len(cat) - len(deep_cat)}/{len(cat)} trang danh mục ở tầng 1" + ("\nSâu hơn: " + "\n".join(r["url"] for r in deep_cat[:6]) if deep_cat else "")) if cat else (SKIP, "Không nhận ra trang danh mục /tour-…, /combo-…, /ve-…")
    prod = [r for r in vi if "/san-pham/" in r["url"]]
    weak_prod = [r for r in prod if int(r.get("inlinks") or 0) < 5]
    R["S08"] = (OK, f"{len(prod)} trang sản phẩm đều ≥ 5 link vào") if prod and not weak_prod else \
        ((BAD, f"{len(weak_prod)}/{len(prod)} trang sản phẩm < 5 link vào:\n" + "\n".join(f"{r['inlinks']} link · {r['url']}" for r in weak_prod[:6])) if prod else (SKIP, "Không thấy trang /san-pham/"))
    weak = [r for r in vi if int(r.get("inlinks") or 0) <= 1 and r["url"].rstrip("/").count("/") > 2]
    R["S09"] = (OK, "Không có") if not weak else (BAD, f"{len(weak)} trang chỉ ≤ 1 link vào:\n" + "\n".join(r["url"] for r in weak[:6]))
    # mồ côi: đọc từ báo cáo .md cùng tên
    orphans, complete = None, False
    if reports_dir:
        import glob
        fs = sorted(glob.glob(str(Path(reports_dir) / "crawl-*.md")), key=os.path.getmtime)
        if fs:
            txt = Path(fs[-1]).read_text(encoding="utf-8")
            complete = "Chưa crawl hết" not in txt
            sec = txt.split("## Trang mồ côi", 1)[-1].split("\n## ", 1)[0] if "## Trang mồ côi" in txt else ""
            orphans = re.findall(r"^- (https?://\S+)", sec, re.M)
    if orphans is None or not complete:
        R["S07"] = (SKIP, "Cần một lần crawl quét hết site (bấm «Chạy crawl»)")
    else:
        R["S07"] = (OK, "Không có trang mồ côi") if not orphans else (BAD, f"{len(orphans)} trang mồ côi:\n" + "\n".join(orphans[:8]))
    # onsite
    from collections import Counter
    tc = Counter(r.get("title", "") for r in vi)
    dup = [t for t, c in tc.items() if t and c > 1]
    R["O01"] = (OK, "Không có title trùng") if not dup else (BAD, f"{len(dup)} nhóm title trùng, VD: " + " | ".join(dup[:4]))
    tl = [r for r in vi if 20 <= len(r.get("title", "")) <= 65]
    R["O02"] = (OK if len(tl) / max(len(vi), 1) >= 0.9 else BAD, f"{len(tl)}/{len(vi)} trang có title 20–65 ký tự ({round(len(tl) / max(len(vi), 1) * 100)}%)")
    md = [r for r in vi if 70 <= len(r.get("meta_description", "")) <= 170]
    R["O03"] = (OK if len(md) / max(len(vi), 1) >= 0.9 else BAD, f"{len(md)}/{len(vi)} trang có meta 70–170 ký tự · {sum(1 for r in vi if not r.get('meta_description'))} trang không có meta")
    h1bad = [r for r in vi if r.get("h1_count") != "1"]
    R["O04"] = (OK, "Mọi trang đúng 1 H1") if not h1bad else (BAD, f"{len(h1bad)}/{len(vi)} trang không đúng 1 H1, VD:\n" + "\n".join(f"{r.get('h1_count')} H1 · {r['url']}" for r in h1bad[:5]))
    thin = [r for r in vi if int(r.get("words") or 0) < 300]
    R["O06"] = (OK, "Không có") if not thin else (BAD, f"{len(thin)} trang < 300 từ, VD:\n" + "\n".join(r["url"] for r in thin[:5]))
    hc = Counter(r.get("h1", "").strip().lower() for r in vi if r.get("h1"))
    hdup = [h for h, c in hc.items() if c > 1]
    R["O07"] = (OK, "Không có H1 trùng") if not hdup else (BAD, f"{len(hdup)} H1 trùng giữa các trang, VD: " + " | ".join(hdup[:4]))
    # GEO audit → O05, O12
    if reports_dir:
        import glob
        gs = sorted(glob.glob(str(Path(reports_dir) / "geo-audit-*.md")), key=os.path.getmtime)
        if gs:
            sec = Path(gs[-1]).read_text(encoding="utf-8").split("## 2.", 1)[-1].split("## 3.", 1)[0]
            def row(name):
                m = re.search(rf"^\| {re.escape(name)} \| (\d+)/(\d+) \|$", sec, re.M)
                return (int(m.group(1)), int(m.group(2))) if m else (0, 0)
            a, n = row("Ít H2 dạng câu hỏi khách thật sự hỏi AI")
            R["O05"] = (OK, "H2 dạng câu hỏi đạt trên các trang mẫu") if not a else (BAD, f"{a}/{n} trang mẫu có < 30% H2 dạng câu hỏi")
            a, n = row("Khối meta chen giữa H1 và câu trả lời")
            R["O12"] = (OK, "Không thấy khối meta chen giữa") if not a else (BAD, f"{a}/{n} trang mẫu có khối tác giả/ngày/lượt xem chen giữa H1 và đoạn mở đầu")
    return R


def _crawl_tech(rows) -> dict:
    """Các mục kỹ thuật từ báo cáo crawl (T12–T16)."""
    by_url = {r["url"]: r for r in rows}
    err = [r for r in rows if r.get("status") not in ("200", "301", "302", "307", "308")]
    red = [r for r in rows if r.get("status") in ("301", "302", "307", "308")]
    chains = []
    for r in red:
        tgt = (r.get("note") or "").replace("redirect → ", "").strip()
        if tgt in by_url and by_url[tgt].get("status") in ("301", "302", "307", "308"):
            chains.append(f"{r['url']} → {tgt} → …")
    ok200 = [r for r in rows if r.get("status") == "200"]
    deep = [r for r in ok200 if int(r.get("depth") or 0) > 3]
    canon = [r for r in ok200 if r.get("canonical_self") == "False"]
    fmt = lambda rs, key="url": "\n".join(r[key] if isinstance(r, dict) else r for r in rs[:6])
    return {
        "T12": (OK, "Không có") if not err else (BAD, f"{len(err)} trang lỗi:\n" + "\n".join(f"{r['status']} · {r['url']}" for r in err[:6])),
        "T13": (OK, "Không có") if not red else (BAD, f"{len(red)} URL redirect còn được link nội bộ trỏ tới:\n" + fmt(red)),
        "T14": (OK, "Không có chuỗi redirect") if not chains else (BAD, f"{len(chains)} chuỗi:\n" + "\n".join(chains[:6])),
        "T15": (OK, "Mọi trang ≤ 3 click") if not deep else (BAD, f"{len(deep)} trang sâu > 3 click:\n" + fmt(deep)),
        "T16": (OK, "Không có") if not canon else (BAD, f"{len(canon)} trang canonical trỏ sang URL khác:\n" + fmt(canon)),
    }
