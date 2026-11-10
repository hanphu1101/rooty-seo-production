"""
Giá & dữ kiện: một chỗ lưu giá/giờ/lịch "chuẩn" (có nguồn + ngày kiểm), lịch sử đổi giá,
và dò toàn bộ bài blog xem bài nào đang ghi giá khác giá hiện tại → việc sửa.
Giá gốc lấy từ chính trang sản phẩm của Rooty (schema Offer.price) hoặc người nhập tay có nguồn.
"""
from __future__ import annotations

import html
import json
import re
import unicodedata
import urllib.parse

MONEY = re.compile(
    r"(?<![\d.,])(\d{1,3}(?:[.,]\d{3})+|\d{4,9})\s*(?:đ|₫|vnđ|vnd|đồng)(?![a-zà-ỹ])"          # 1.550.000đ · 1550000 VNĐ
    r"|(?:đ|₫|vnđ|vnd)\s*(\d{1,3}(?:[.,]\d{3})+)"                                               # đ 1,550,000
    r"|(?<![\d.,])(\d{1,4}(?:[.,]\d{1,3})?)\s*(k|nghìn|ngàn|tr|triệu)(?![a-zà-ỹ])"              # 650k · 1,55 triệu · 1tr5
    r"(\d{1,3})?",
    re.I)


def strip_accents(s):
    s = unicodedata.normalize("NFD", s or "").replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def money_values(text):
    """→ [(chuỗi gốc, số VND)]"""
    out = []
    for m in MONEY.finditer(text or ""):
        raw = m.group(0).strip()
        try:
            if m.group(1) or m.group(2):
                v = int(re.sub(r"\D", "", m.group(1) or m.group(2)))
            else:
                num, unit, tail = m.group(3), m.group(4).lower(), m.group(5)
                base = float(num.replace(",", "."))
                if unit in ("k", "nghìn", "ngàn"):
                    v = int(round(base * 1000))
                else:
                    v = int(round(base * 1_000_000))
                    if tail:   # 1tr5 → 1.500.000
                        v += int(tail.ljust(3, "0")[:3]) * 1000
        except ValueError:
            continue
        if 10_000 <= v <= 500_000_000:
            out.append((raw, v))
    return out


def fmt(v):
    return f"{v:,}".replace(",", ".") + "đ" if isinstance(v, int) else str(v)


def to_int(s):
    vals = money_values(str(s or "")) or ([(str(s), int(re.sub(r"\D", "", str(s))))] if re.sub(r"\D", "", str(s or "")) else [])
    return vals[0][1] if vals else None


# ------------------------------------------------------------------ giá gốc từ trang sản phẩm

def product_price(url, fetch, decode):
    st, body, hd, _ = fetch(url)
    if st != 200:
        return None
    h = decode(body, hd)
    name = ""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S | re.I)
    if m:
        name = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split())
    prices = []
    for blk in re.findall(r'<script[^>]+ld\+json[^>]*>(.*?)</script>', h, re.S | re.I):
        try:
            data = json.loads(blk)
        except Exception:
            continue
        stack = [data]
        while stack:
            n = stack.pop()
            if isinstance(n, dict):
                for k in ("price", "lowPrice"):
                    if n.get(k) not in (None, "") and str(n.get(k)).replace(".", "").isdigit():
                        prices.append(int(float(n[k])))
                stack.extend(n.values())
            elif isinstance(n, list):
                stack.extend(n)
    prices = [p for p in prices if p >= 10_000]
    if not prices:
        return None
    return {"name": name, "url": url, "price": min(prices)}


def default_phrases(name, url):
    """Cụm để dò trong bài: tên sản phẩm (bỏ phần sau dấu – : |) + slug."""
    core = re.split(r"\s[–\-:|]\s|\s–|:", name or "")[0].strip()
    slug = urllib.parse.urlsplit(url).path.strip("/").split("/")[-1].replace("-", " ")
    out = [core] if core else []
    if slug and strip_accents(slug) != strip_accents(core):
        out.append(slug)
    return "\n".join(out)


# ------------------------------------------------------------------ dò bài đang dùng giá

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?…])\s+|\n+", text or "") if s.strip()]


def _tokens(phrase_ascii):
    return [t for t in re.findall(r"[a-z0-9]+", phrase_ascii) if (len(t) > 1 or t.isdigit()) and t not in STOPT and not re.fullmatch(r"20\d\d", t)]


STOPT = {"phu", "quoc", "tour", "va", "o", "tai", "gia", "tot", "trai", "nghiem", "kham", "pha", "chuan", "lich", "trinh", "tron", "goi", "the", "of"}


def find_usage(fact, posts, window=15):
    """fact: dict bảng Giá & dữ kiện. posts: [{link, text}].
    Một con số tiền được coi là giá của dữ kiện khi MỌI từ chính của một cụm dò nằm trong `window` chữ ngay trước con số đó
    (bắt được khung giới thiệu tour gắn trong bài và câu kiểu «Tour 3 đảo … giá 800.000đ»). → (dòng dùng giá, số bài ghi khác)."""
    cur = to_int(fact.get("Giá trị"))
    phrases = [toks for toks in (_tokens(strip_accents(p)) for p in (fact.get("Từ khoá tìm trong bài") or "").splitlines()) if len(toks) >= 2]
    rows, wrong_posts = [], set()
    if not phrases:
        return rows, 0
    for p in posts:
        text = p.get("text") or ""
        path = urllib.parse.urlsplit(p["link"]).path
        seen = set()
        for m in MONEY.finditer(text):
            vals = money_values(m.group(0))
            if not vals:
                continue
            raw, v = vals[0]
            seg = text[max(0, m.start() - 160): m.start()]
            cut = max([x.end() for x in re.finditer(r"[.!?;](?=\s)|\n", seg)] + [x.end() for x in MONEY.finditer(seg)] + [0])
            before = strip_accents(seg[cut:])   # chỉ trong cùng câu, sau con số tiền trước đó
            win = set(re.findall(r"[a-z0-9]+", before)[-window:])
            if not any(all(t in win for t in toks) for toks in phrases):
                continue
            s0 = max(text.rfind(". ", 0, m.start()), text.rfind("! ", 0, m.start()), m.start() - 160) + 1
            sent = text[s0: m.end() + 60].strip()
            key = (raw, path)
            if key in seen:
                continue
            seen.add(key)
            ok = cur is not None and v == cur
            rows.append({"url": path, "ok": ok, "written": raw, "sentence": sent[:240]})
            if not ok and cur is not None:
                wrong_posts.add(path)
    return rows, len(wrong_posts)
