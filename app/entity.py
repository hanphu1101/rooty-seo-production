"""
Bước 8 · Tối ưu Entity: đọc NAP + schema trang chủ, quét liên kết chéo website ↔ mạng xã hội,
so NAP các hồ sơ với NAP gốc, sinh JSON-LD Organization/TravelAgency + WebSite + WebPage.
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
sys.path.insert(0, str(ROOT / "scripts"))
from geo_audit import PageParser, decode, fetch  # noqa: E402

# tên miền → tên nền tảng trong bảng Hồ sơ thương hiệu
PLATFORM_DOMAINS = [
    (r"(^|\.)facebook\.com$|(^|\.)fb\.com$|(^|\.)fb\.me$", "Facebook Page"),
    (r"(^|\.)youtube\.com$|(^|\.)youtu\.be$", "YouTube"),
    (r"(^|\.)instagram\.com$", "Instagram"),
    (r"(^|\.)tiktok\.com$", "TikTok"),
    (r"(^|\.)linkedin\.com$", "LinkedIn công ty"),
    (r"(^|\.)(x|twitter)\.com$", "X (Twitter)"),
    (r"(^|\.)pinterest\.[a-z.]+$", "Pinterest"),
    (r"(^|\.)zalo\.me$|(^|\.)oa\.zalo\.me$", "Zalo OA"),
    (r"(^|\.)tripadvisor\.[a-z.]+$", "Tripadvisor"),
    (r"(^|\.)klook\.com$", "Klook"),
    (r"(^|\.)traveloka\.com$", "Traveloka"),
    (r"^g\.page$|^maps\.app\.goo\.gl$|^(www\.)?google\.[a-z.]+$|^goo\.gl$", "Google Business Profile"),
    (r"(^|\.)trangvangvietnam\.com$", "Trang Vàng Việt Nam"),
    (r"(^|\.)wikidata\.org$", "Wikidata"),
    (r"(^|\.)foursquare\.com$", "Foursquare"),
]


def platform_of(url: str) -> str | None:
    host = urllib.parse.urlsplit(url).netloc.lower().split(":")[0]
    path = urllib.parse.urlsplit(url).path
    for pat, name in PLATFORM_DOMAINS:
        if re.search(pat, host):
            if name == "Google Business Profile" and host.startswith(("www.google", "google")) and "/maps" not in path:
                return None
            if name == "Facebook Page" and re.search(r"/(sharer|share|dialog|plugins|tr)\b", path):
                return None
            if name in ("X (Twitter)", "Pinterest") and re.search(r"/(intent|share|pin/create)", path):
                return None
            return name
    return None


def norm_url(u: str) -> str:
    u = urllib.parse.unquote((u or "").strip()).lower()
    u = re.sub(r"^https?://(www\.|m\.)?", "", u)
    return u.rstrip("/")


def profile_problem(name: str, url: str) -> str | None:
    """Link có thật sự trỏ tới hồ sơ của thương hiệu không (không phải trang chủ của nền tảng)."""
    path = urllib.parse.urlsplit(url).path.strip("/")
    if not path and name not in ("Google Business Profile",):
        return "link trỏ về trang chủ của nền tảng, không phải hồ sơ Rooty"
    if name == "TikTok" and "@" not in url:
        return "link TikTok không có @tên-kênh (đang trỏ trang chung của TikTok)"
    if name == "YouTube" and not re.search(r"/(@|channel/|c/|user/)", url):
        return "link YouTube không phải trang kênh"
    if name == "LinkedIn công ty" and "/company/" not in url:
        return "link LinkedIn là hồ sơ cá nhân (/in/), nên dùng trang công ty (/company/)"
    if name == "Zalo OA" and re.fullmatch(r"0\d{9,10}", path):
        return "link Zalo cá nhân theo số điện thoại, không phải Zalo OA"
    if re.fullmatch(r"[a-z]{2}(-[A-Za-z]{2})?", path):
        return "link chỉ là trang ngôn ngữ của nền tảng, không phải hồ sơ"
    return None


def _nodes(blocks):
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


ORG_TYPES = {"Organization", "TravelAgency", "LocalBusiness", "Corporation"}


def read_site(site: str) -> dict:
    """Đọc trang chủ: link mạng xã hội, schema tổ chức (NAP, logo, sameAs), các loại schema có mặt."""
    base = site.rstrip("/")
    st, body, hd, _ = fetch(base + "/")
    html = decode(body, hd)
    p = PageParser()
    try:
        p.feed(html)
    except Exception:
        pass
    links = list(dict.fromkeys(urllib.parse.urljoin(base + "/", h) for h in re.findall(r'href=["\']([^"\'#]+)["\']', html)))
    cands: dict[str, list] = {}
    for u in links:
        name = platform_of(u)
        if name and norm_url(u) not in {norm_url(x) for x in cands.get(name, [])}:
            cands.setdefault(name, []).append(u)
    # mỗi nền tảng: ưu tiên link là hồ sơ hợp lệ; ghi lại nếu web có nhiều link khác nhau
    social, social_all = {}, {}
    for name, us in cands.items():
        good = [u for u in us if not profile_problem(name, u)]
        social[name] = (good or us)[0]
        social_all[name] = us
    nodes = _nodes(p.jsonld)
    orgs = [n for n in nodes if set(_types(n)) & ORG_TYPES]
    org = max(orgs, key=len) if orgs else {}
    same_as = org.get("sameAs") or []
    same_as = [same_as] if isinstance(same_as, str) else same_as
    addr = org.get("address") or {}
    if isinstance(addr, list):
        addr = addr[0] if addr else {}
    if isinstance(addr, str):
        addr = {"streetAddress": addr}
    logo = org.get("logo")
    if isinstance(logo, dict):
        logo = logo.get("url") or logo.get("contentUrl")
    hours = org.get("openingHours")
    if isinstance(hours, list):
        hours = ", ".join(hours)
    if not hours and org.get("openingHoursSpecification"):
        spec = org["openingHoursSpecification"]
        spec = spec if isinstance(spec, list) else [spec]
        parts = []
        for s in spec:
            days = s.get("dayOfWeek")
            days = days if isinstance(days, list) else [days]
            codes = [str(d).split("/")[-1][:2] for d in days if d]
            short = "Mo-Su" if len(set(codes)) == 7 else ",".join(codes)
            if s.get("opens"):
                parts.append(f"{short} {s.get('opens')}-{s.get('closes')}")
        hours = ", ".join(parts) or None
    nap = {
        "Tên thương hiệu": org.get("name"), "Website": org.get("url"), "Hotline chính": org.get("telephone"),
        "Email": org.get("email"),
        "Địa chỉ": addr.get("streetAddress"), "Thành phố": addr.get("addressLocality"), "Tỉnh/thành": addr.get("addressRegion"),
        "Giờ mở cửa": hours,
        "Logo URL": logo, "Mô tả ngắn": org.get("description"),
    }
    return {"social": social, "social_all": social_all, "sameAs": same_as, "nap": {k: v for k, v in nap.items() if v},
            "org_type": "/".join(_types(org)) if org else None, "types": sorted({t for n in nodes for t in _types(n)}),
            "org": org}


def profile_links_back(url: str, domain: str) -> str:
    """Hồ sơ có nhắc/trỏ về website không. Mạng xã hội hay chặn bot → 'Chưa kiểm'."""
    try:
        st, body, hd, _ = fetch(url)
    except Exception:
        return "Chưa kiểm"
    if st != 200:
        return "Chưa kiểm"
    html = decode(body, hd).lower()
    if re.search(r"log ?in|đăng nhập|captcha", html[:20000]) and domain not in html:
        return "Chưa kiểm"
    return "Có" if domain.lower() in html else "Chưa"


# ------------------------------------------------------------------ NAP

def norm_phone(s):
    d = re.sub(r"\D", "", s or "")
    if d.startswith("84"):
        d = "0" + d[2:]
    return d


def norm_text(s):
    s = unicodedata.normalize("NFD", (s or "").lower().replace("đ", "d"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"\b(so|duong|phuong|xa|thi tran|quan|huyen|tp|thanh pho|tinh|viet nam|vn)\b", " ", s)
    return " ".join(re.findall(r"[a-z0-9]+", s))


def compare_nap(master: dict, prof: dict) -> tuple[str, str]:
    """→ (Khớp/Lệch/Chưa kiểm, ghi chú)"""
    checks, notes = [], []
    if prof.get("Tên hiển thị"):
        ok = norm_text(master.get("Tên thương hiệu")) in norm_text(prof["Tên hiển thị"]) or norm_text(prof["Tên hiển thị"]) in norm_text(master.get("Tên thương hiệu"))
        checks.append(ok)
        if not ok:
            notes.append(f"Tên «{prof['Tên hiển thị']}» ≠ «{master.get('Tên thương hiệu')}»")
    if prof.get("Hotline"):
        hp = {norm_phone(x) for x in re.split(r"[,;/|]", prof["Hotline"]) if norm_phone(x)}
        mp = {norm_phone(x) for x in re.split(r"[,;/|]", master.get("Hotline chính") or "") if norm_phone(x)}
        ok = bool(hp & mp) if mp else False
        checks.append(ok)
        if not ok:
            notes.append(f"Hotline {prof['Hotline']} ≠ {master.get('Hotline chính') or '(chưa có hotline gốc)'}")
    if prof.get("Địa chỉ"):
        a, b = set(norm_text(prof["Địa chỉ"]).split()), set(norm_text(master.get("Địa chỉ")).split())
        sim = len(a & b) / max(len(b), 1) if b else 0
        ok = sim >= 0.7
        checks.append(ok)
        if not ok:
            notes.append(f"Địa chỉ khác NAP gốc ({round(sim * 100)}% trùng)")
    if not checks:
        return "Chưa kiểm", "Chưa điền Tên hiển thị / Hotline / Địa chỉ của hồ sơ để so"
    return ("Khớp" if all(checks) else "Lệch"), ("; ".join(notes) or "Tên, hotline, địa chỉ trùng NAP gốc")


# ------------------------------------------------------------------ JSON-LD

def build_jsonld(master: dict, same_as: list[str], has_search: bool) -> dict:
    site = (master.get("Website") or "").rstrip("/")
    org = {
        "@type": ["TravelAgency", "Organization"],
        "@id": f"{site}/#organization",
        "name": master.get("Tên thương hiệu"),
        "legalName": master.get("Tên pháp lý"),
        "url": site + "/",
        "logo": {"@type": "ImageObject", "url": master.get("Logo URL")} if master.get("Logo URL") else None,
        "image": master.get("Logo URL"),
        "description": master.get("Mô tả ngắn"),
        "telephone": master.get("Hotline chính"),
        "email": master.get("Email"),
        "foundingDate": master.get("Năm thành lập"),
        "address": {"@type": "PostalAddress", "streetAddress": master.get("Địa chỉ"), "addressLocality": master.get("Thành phố"),
                    "addressRegion": master.get("Tỉnh/thành"), "addressCountry": "VN"} if master.get("Địa chỉ") else None,
        "openingHours": master.get("Giờ mở cửa"),
        "areaServed": "Phú Quốc, Kiên Giang, Việt Nam",
        "sameAs": sorted(set(u for u in same_as + ([master["Wikidata URL"]] if master.get("Wikidata URL") else []) if u)) or None,
    }
    org = {k: v for k, v in org.items() if v}
    if isinstance(org.get("address"), dict):
        org["address"] = {k: v for k, v in org["address"].items() if v}
    website = {"@type": "WebSite", "@id": f"{site}/#website", "url": site + "/", "name": master.get("Tên thương hiệu"),
               "publisher": {"@id": f"{site}/#organization"}, "inLanguage": "vi"}
    if has_search:
        website["potentialAction"] = {"@type": "SearchAction", "target": f"{site}/?s={{search_term_string}}",
                                      "query-input": "required name=search_term_string"}
    webpage = {"@type": "WebPage", "@id": f"{site}/#webpage", "url": site + "/", "name": master.get("Tên thương hiệu"),
               "isPartOf": {"@id": f"{site}/#website"}, "about": {"@id": f"{site}/#organization"}, "inLanguage": "vi"}
    return {"@context": "https://schema.org", "@graph": [org, website, webpage]}


def schema_gaps(live: dict, want: dict) -> list[str]:
    """So schema đang có trên trang chủ với bản chuẩn."""
    gaps = []
    org = live.get("org") or {}
    if not org:
        return ["Trang chủ chưa có schema Organization/TravelAgency/LocalBusiness"]
    w = want["@graph"][0]
    for k, label in (("name", "name"), ("url", "url"), ("logo", "logo"), ("telephone", "telephone"), ("address", "address"),
                     ("openingHours", "openingHours (giờ mở cửa)"), ("email", "email")):
        if k == "openingHours" and org.get("openingHoursSpecification"):
            continue
        if (k in w or k in ("name", "url", "logo", "telephone", "address")) and not org.get(k):
            gaps.append(f"Thiếu {label}")
    live_same = {norm_url(u) for u in (live.get("sameAs") or [])}
    miss = [u for u in (w.get("sameAs") or []) if norm_url(u) not in live_same]
    if miss:
        gaps.append(f"sameAs thiếu {len(miss)} hồ sơ: " + ", ".join(miss[:6]))
    if "WebSite" not in live.get("types", []):
        gaps.append("Chưa có schema WebSite")
    if "WebPage" not in live.get("types", []):
        gaps.append("Chưa có schema WebPage")
    if not set(_types(org)) & {"TravelAgency", "LocalBusiness"}:
        gaps.append(f"Loại hiện tại «{'/'.join(_types(org))}» — nên dùng TravelAgency (một loại LocalBusiness) cho công ty lữ hành")
    return gaps
