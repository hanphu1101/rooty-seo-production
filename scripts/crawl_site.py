#!/usr/bin/env python3
"""
Crawl website theo link nội bộ (giống Googlebot) → kiểm kê URL, độ sâu click, link trỏ vào, trang mồ côi.

Chạy:
    python -X utf8 scripts/crawl_site.py https://rootytrip.com
    python -X utf8 scripts/crawl_site.py https://rootytrip.com --max-pages 800 --delay 0.3

Đầu ra:
    reports/crawl-<domain>-<ngày>.csv   — mỗi URL một dòng (dùng cho content audit, liên kết nội bộ)
    reports/crawl-<domain>-<ngày>.md    — tóm tắt: lỗi, trang mồ côi, trang sâu, title/H1 trùng
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import os
import re
import sys
import time
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo_audit import PageParser, decode, fetch, sitemap_urls  # noqa: E402

SKIP_EXT = re.compile(r"\.(jpe?g|png|gif|webp|svg|pdf|zip|mp4|mp3|css|js|xml|ico|woff2?)(\?|$)", re.I)
SKIP_PATH = re.compile(r"/(wp-admin|wp-json|wp-login|feed|cart|checkout|my-account)(/|$)|[?&](replytocom|share|s)=", re.I)


class LinkParser(HTMLParser):
    """Lấy link + anchor text + rel + vùng (nội dung / menu-header / footer / sidebar)."""
    ZONES = {"nav": "menu", "header": "menu", "footer": "footer", "aside": "sidebar"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []          # link dofollow để đi tiếp
        self.items: list[dict] = []         # mọi link: href, anchor, rel, zone
        self._zone: list[str] = []
        self._a = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.ZONES:
            self._zone.append(self.ZONES[tag])
        elif tag in ("div", "section") and re.search(r"\b(footer|sidebar|widget|menu|navbar|breadcrumb)\b", (a.get("class") or "") + " " + (a.get("id") or ""), re.I):
            z = re.search(r"footer|sidebar|widget|menu|navbar|breadcrumb", (a.get("class") or "") + " " + (a.get("id") or ""), re.I).group(0).lower()
            self._zone.append({"widget": "sidebar", "navbar": "menu", "breadcrumb": "menu"}.get(z, z))
        elif tag in ("div", "section"):
            self._zone.append("")
        if tag == "a":
            href = (a.get("href") or "").strip()
            rel = (a.get("rel") or "").lower()
            if href:
                if "nofollow" not in rel:
                    self.links.append(href)
                zone = next((z for z in reversed(self._zone) if z), "nội dung")
                self._a = {"href": href, "rel": rel, "zone": zone, "anchor": "", "alt": ""}
        elif tag == "img" and self._a is not None:
            self._a["alt"] = a.get("alt") or ""

    def handle_endtag(self, tag):
        if tag in self.ZONES or tag in ("div", "section"):
            if self._zone:
                self._zone.pop()
        if tag == "a" and self._a is not None:
            self._a["anchor"] = " ".join(self._a["anchor"].split()) or (f"[ảnh] {self._a['alt']}" if self._a["alt"] else "")
            self.items.append(self._a)
            self._a = None

    def handle_data(self, data):
        if self._a is not None:
            self._a["anchor"] += data


def norm(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    path = p.path or "/"
    return urllib.parse.urlunsplit((p.scheme, p.netloc.lower(), path, p.query, ""))


def main() -> int:
    ap = argparse.ArgumentParser(description="Crawl website theo link nội bộ")
    ap.add_argument("site")
    ap.add_argument("--max-pages", type=int, default=500)
    ap.add_argument("--delay", type=float, default=0.25, help="Nghỉ giữa 2 request (giây), để không làm nặng máy chủ")
    args = ap.parse_args()

    start = norm(args.site if args.site.startswith("http") else "https://" + args.site)
    host = urllib.parse.urlsplit(start).netloc.lower()
    hosts = {host, host[4:] if host.startswith("www.") else "www." + host}

    queue = collections.deque([(start, 0)])
    depth: dict[str, int] = {start: 0}
    inlinks: dict[str, set] = collections.defaultdict(set)
    rows: dict[str, dict] = {}
    edges: list[dict] = []   # bản đồ link nội bộ: từ → đến, anchor, rel, vùng

    print(f"→ Crawl {start} (tối đa {args.max_pages} trang)")
    while queue and len(rows) < args.max_pages:
        url, d = queue.popleft()
        if url in rows:
            continue
        try:
            status, body, headers, ttfb = fetch(url, follow=False)
        except Exception as e:
            rows[url] = {"url": url, "status": "ERR", "depth": d, "note": str(e)[:80]}
            continue
        row = {"url": url, "status": status, "depth": d, "ttfb_ms": round(ttfb * 1000),
               "html_kb": round(len(body) / 1024)}
        ctype = headers.get("content-type", "")
        if status == 200 and "html" in ctype:
            html = decode(body, headers)
            p, lp = PageParser(), LinkParser()
            try:
                p.feed(html)
                lp.feed(html)
            except Exception:
                pass
            h1 = [t for tag, t in p.headings if tag == "h1"]
            robots = p.meta.get("robots", "").lower() + " " + headers.get("x-robots-tag", "").lower()
            canon = urllib.parse.urljoin(url, p.canonical) if p.canonical else ""
            mod = p.meta.get("article:modified_time") or (re.search(r'"dateModified"\s*:\s*"([^"]+)"', html) or [None, ""])[1]
            row.update({
                "title": " ".join(p.title.split()),
                "h1": h1[0] if h1 else "",
                "h1_count": len(h1),
                "words": len(" ".join(p.body_text).split()),
                "noindex": "noindex" in robots,
                "canonical": canon,
                "canonical_self": (canon.rstrip("/") == url.rstrip("/")) if canon else "",
                "date_modified": mod or "",
                "meta_description": p.meta.get("description", "")[:200],
            })
            for href in lp.links:
                if href.startswith(("#", "mailto:", "tel:", "javascript:", "zalo:")):
                    continue
                u = norm(urllib.parse.urljoin(url, href))
                if urllib.parse.urlsplit(u).netloc.lower() not in hosts or SKIP_EXT.search(u) or SKIP_PATH.search(u):
                    continue
                if u != url:
                    inlinks[u].add(url)
                if u not in depth:
                    depth[u] = d + 1
                    queue.append((u, d + 1))
            seen_edge = set()
            for it in lp.items:
                h = it["href"]
                if h.startswith(("#", "mailto:", "tel:", "javascript:", "zalo:")):
                    continue
                u = norm(urllib.parse.urljoin(url, h))
                if urllib.parse.urlsplit(u).netloc.lower() not in hosts or SKIP_EXT.search(u) or u == url:
                    continue
                key = (u, it["anchor"].lower(), it["zone"])
                if key in seen_edge:
                    continue
                seen_edge.add(key)
                edges.append({"from": url, "to": u, "anchor": it["anchor"][:120], "rel": it["rel"], "zone": it["zone"]})
        elif status in (301, 302, 307, 308):
            target = norm(urllib.parse.urljoin(url, headers.get("location", "")))
            row["note"] = "redirect → " + target
            # vẫn crawl tiếp URL đích (để không bỏ sót trang), nhưng URL redirect giữ nguyên trong báo cáo
            if urllib.parse.urlsplit(target).netloc.lower() in hosts and target not in depth:
                depth[target] = d
                queue.appendleft((target, d))
        rows[url] = row
        if len(rows) % 25 == 0:
            print(f"  … {len(rows)} trang")
        time.sleep(args.delay)

    for u, r in rows.items():
        r["inlinks"] = len(inlinks.get(u, ()))

    # trang có trong sitemap nhưng crawl không tìm thấy link → mồ côi
    print("→ Đọc sitemap để tìm trang mồ côi ...")
    try:
        sm = [norm(u) for u in sitemap_urls(start, "", 5000)]
    except Exception:
        sm = []
    complete = not queue  # crawl hết site thì mới kết luận được trang mồ côi
    orphans = [u for u in sm if u not in depth] if complete else []
    not_reached = len([u for u in sm if u not in rows])

    today = dt.date.today().isoformat()
    out_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent / "reports"
    out_dir.mkdir(exist_ok=True)
    stem = f"crawl-{host}-{today}"
    csv_path, md_path = out_dir / (stem + ".csv"), out_dir / (stem + ".md")
    cols = ["url", "status", "depth", "inlinks", "title", "h1", "h1_count", "words", "noindex",
            "canonical_self", "canonical", "date_modified", "meta_description", "ttfb_ms", "html_kb", "note"]
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in sorted(rows.values(), key=lambda r: (r.get("depth", 99), r["url"])):
            w.writerow(r)
    links_path = out_dir / (stem + ".links.tsv")   # đuôi .tsv để không lẫn với báo cáo crawl-*.csv
    with open(links_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["from", "to", "anchor", "rel", "zone"], delimiter="\t")
        w.writeheader()
        w.writerows(edges)

    pages = [r for r in rows.values() if r.get("status") == 200 and "title" in r]
    errors = [r for r in rows.values() if r.get("status") not in (200, 301, 302, 307, 308)]
    redirects = [r for r in rows.values() if r.get("status") in (301, 302, 307, 308)]
    deep = [r for r in pages if r["depth"] > 3]
    weak = [r for r in pages if r["inlinks"] <= 1 and r["url"] != start]
    thin = [r for r in pages if r.get("words", 0) < 300]
    dup_title = {t: us for t, us in _group(pages, "title").items() if t and len(us) > 1}
    no_canon_self = [r for r in pages if r.get("canonical_self") is False]
    depth_hist = collections.Counter(r["depth"] for r in pages)

    L = [f"# Crawl {host} — {today}", "",
         f"Đã crawl **{len(rows)}** URL ({len(pages)} trang HTML 200) · giới hạn {args.max_pages}. "
         f"Sitemap có {len(sm)} URL.", "",
         ("✅ Đã crawl hết các trang tìm được qua link nội bộ." if complete else
          f"⚠ **Chưa crawl hết** (dừng ở giới hạn {args.max_pages}); còn {not_reached} URL trong sitemap chưa tới. "
          "Mục «trang mồ côi» bị bỏ qua — chạy lại với --max-pages lớn hơn số URL sitemap để kết luận."), "",
         "## Tóm tắt", "",
         "| Hạng mục | Số lượng |", "|---|---|",
         f"| Trang lỗi (4xx/5xx) | {len(errors)} |",
         f"| URL redirect được link nội bộ trỏ tới | {len(redirects)} |",
         f"| Trang mồ côi (có trong sitemap, crawl không thấy link) | {len(orphans) if complete else 'chưa kết luận'} |",
         f"| Trang sâu > 3 click | {len(deep)} |",
         f"| Trang chỉ có ≤ 1 link nội bộ trỏ vào | {len(weak)} |",
         f"| Trang mỏng (< 300 từ) | {len(thin)} |",
         f"| Nhóm title trùng | {len(dup_title)} |",
         f"| Canonical trỏ sang URL khác | {len(no_canon_self)} |", "",
         "## Phân bố độ sâu click", "", "| Độ sâu | Số trang |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in sorted(depth_hist.items())]

    def section(title, items, fmt, limit=40):
        L.extend(["", f"## {title}", ""])
        if not items:
            L.append("Không có.")
        for it in items[:limit]:
            L.append("- " + fmt(it))
        if len(items) > limit:
            L.append(f"- … và {len(items) - limit} mục nữa (xem file CSV)")

    section("Trang lỗi", errors, lambda r: f"{r['status']} · {r['url']} · được trỏ từ {r['inlinks']} trang")
    section("URL redirect còn được link nội bộ trỏ tới — sửa link về URL đích", redirects, lambda r: f"{r['url']} {r.get('note', '')}")
    section("Trang mồ côi", orphans, lambda u: u)
    section("Trang sâu > 3 click", sorted(deep, key=lambda r: -r["depth"]), lambda r: f"độ sâu {r['depth']} · {r['url']}")
    section("Trang ít link nội bộ trỏ vào (≤ 1)", weak, lambda r: f"{r['inlinks']} link · {r['url']}")
    section("Title trùng", list(dup_title.items()), lambda kv: f"«{kv[0]}» — " + ", ".join(kv[1][:4]))
    section("Trang mỏng (< 300 từ)", sorted(thin, key=lambda r: r.get("words", 0)), lambda r: f"{r.get('words')} từ · {r['url']}")

    md_path.write_text("\n".join(L), encoding="utf-8")
    orphan_txt = f"{len(orphans)} mồ côi" if complete else "chưa crawl hết nên chưa kết luận mồ côi"
    print(f"\nXong. {len(pages)} trang · {len(errors)} lỗi · {orphan_txt} · {len(deep)} sâu > 3 click")
    print(f"CSV: {csv_path}")
    print(f"Bản đồ link nội bộ: {links_path} ({len(edges)} link)")
    print(f"Báo cáo: {md_path}")
    return 0


def _group(rows, key):
    g = collections.defaultdict(list)
    for r in rows:
        g[r.get(key, "")].append(r["url"])
    return g


if __name__ == "__main__":
    sys.exit(main())
