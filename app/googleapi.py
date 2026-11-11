"""
Lấy số liệu Google Search Console + GA4 qua API bằng tài khoản dịch vụ (service account) — chỉ cần Python, không cài thêm thư viện.
Kết quả trả về đúng dạng bảng như file CSV xuất tay (dòng tiêu đề + dữ liệu) để đi qua cùng đường nhập ở B10.

.env:  GOOGLE_SA_KEY=đường dẫn file JSON khoá service account  (trên Render: GOOGLE_SA_JSON = dán nguyên nội dung file)
       GSC_SITE=sc-domain:rootytrip.com   (hoặc https://rootytrip.com/ nếu là thuộc tính tiền tố URL)
       GA4_PROPERTY=123456789             (Mã thuộc tính GA4 — số, không phải G-XXXX)
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

SCOPES = "https://www.googleapis.com/auth/webmasters.readonly https://www.googleapis.com/auth/analytics.readonly"
TOKEN_URL = "https://oauth2.googleapis.com/token"
GSC_URL = "https://searchconsole.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query"
GA4_URL = "https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport"


class GoogleError(Exception):
    pass


# ------------------------------------------------------------------ ký JWT RS256 bằng Python thuần

def _der(buf, i):
    """Đọc một phần tử DER tại i → (tag, nội dung, vị trí kế tiếp)."""
    tag, ln = buf[i], buf[i + 1]
    i += 2
    if ln & 0x80:
        n = ln & 0x7F
        ln = int.from_bytes(buf[i:i + n], "big")
        i += n
    return tag, buf[i:i + ln], i + ln


def _rsa_key(pem: str):
    """PEM PKCS#8 (file JSON của Google) → (n, d)."""
    body = re.sub(r"-----[^-]+-----|\s", "", pem)
    der = base64.b64decode(body)
    _, seq, _ = _der(der, 0)                      # PrivateKeyInfo
    _, _, i = _der(seq, 0)                        # version
    _, _, i = _der(seq, i)                        # algorithm
    _, octet, _ = _der(seq, i)                    # privateKey OCTET STRING
    _, rsa, _ = _der(octet, 0)                    # RSAPrivateKey
    vals, i = [], 0
    while i < len(rsa) and len(vals) < 4:         # version, n, e, d
        _, v, i = _der(rsa, i)
        vals.append(int.from_bytes(v, "big"))
    return vals[1], vals[3]


def _sign(msg: bytes, n: int, d: int) -> bytes:
    # PKCS#1 v1.5 + SHA-256
    k = (n.bit_length() + 7) // 8
    t = bytes.fromhex("3031300d060960864801650304020105000420") + hashlib.sha256(msg).digest()
    em = b"\x00\x01" + b"\xff" * (k - len(t) - 3) + b"\x00" + t
    return pow(int.from_bytes(em, "big"), d, n).to_bytes(k, "big")


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _post(url, body, token=None, form=False):
    data = urllib.parse.urlencode(body).encode() if form else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded" if form else "application/json")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode())
            msg = (msg.get("error") or {}).get("message") if isinstance(msg.get("error"), dict) else msg.get("error_description") or msg.get("error")
        except Exception:
            msg = e.reason
        raise GoogleError(f"Google báo lỗi {e.code}: {msg}")


def access_token(key: str) -> tuple[str, str]:
    """key: đường dẫn file JSON khoá, hoặc chính nội dung JSON (biến GOOGLE_SA_JSON trên Render) → (token, email service account)"""
    try:
        sa = json.loads(key if key.lstrip().startswith("{") else open(key, encoding="utf-8").read())
    except OSError:
        raise GoogleError(f"Không mở được file khoá {key} — kiểm GOOGLE_SA_KEY trong .env")
    except ValueError:
        raise GoogleError("Nội dung khoá Google không phải JSON hợp lệ — kiểm GOOGLE_SA_JSON")
    now = int(time.time())
    head = _b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    claim = _b64(json.dumps({"iss": sa["client_email"], "scope": SCOPES, "aud": TOKEN_URL, "iat": now, "exp": now + 3600}).encode())
    n, d = _rsa_key(sa["private_key"])
    jwt = f"{head}.{claim}." + _b64(_sign(f"{head}.{claim}".encode(), n, d))
    r = _post(TOKEN_URL, {"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt}, form=True)
    return r["access_token"], sa["client_email"]


# ------------------------------------------------------------------ Search Console

def _gsc(token, site, start, end, dims):
    url = GSC_URL.format(site=urllib.parse.quote(site, safe=""))
    out, row = [], 0
    while True:
        r = _post(url, {"startDate": start, "endDate": end, "dimensions": dims, "rowLimit": 25000, "startRow": row, "dataState": "final"}, token)
        rows = r.get("rows") or []
        out += rows
        if len(rows) < 25000:
            return out
        row += 25000


def gsc_tables(token, site, days=28, today=None):
    """4 bảng giống CSV xuất từ GSC: Ngày (16 tháng) · Trang · Truy vấn · Truy vấn × Trang (28 ngày)."""
    today = today or dt.date.today()
    end = today - dt.timedelta(days=3)  # số liệu GSC trễ ~2–3 ngày
    start = end - dt.timedelta(days=days - 1)
    s, e = start.isoformat(), end.isoformat()
    m = lambda x: [x["clicks"], x["impressions"], f'{x["ctr"] * 100:.2f}%', f'{x["position"]:.1f}']
    cols = ["Clicks", "Impressions", "CTR", "Position"]
    dates = _gsc(token, site, (end - dt.timedelta(days=480)).isoformat(), e, ["date"])
    pages = _gsc(token, site, s, e, ["page"])
    queries = _gsc(token, site, s, e, ["query"])
    qp = _gsc(token, site, s, e, ["query", "page"])
    period = f"{start:%d/%m}–{end:%d/%m/%Y}"
    return period, {
        "gsc_dates": [["Date"] + cols] + [[x["keys"][0]] + m(x) for x in dates],
        "gsc_pages": [["Page"] + cols] + [[x["keys"][0]] + m(x) for x in pages],
        "gsc_queries": [["Query"] + cols] + [[x["keys"][0]] + m(x) for x in queries],
        "gsc_query_page": [["Query", "Page"] + cols] + [x["keys"] + m(x) for x in qp],
    }


# ------------------------------------------------------------------ GA4

def ga4_pages(token, prop, days=28, today=None):
    """Trang đích, chỉ kênh Organic Search: phiên, tỷ lệ tương tác, sự kiện chính — giống CSV GA4 → Tương tác → Trang đích."""
    today = today or dt.date.today()
    end = today - dt.timedelta(days=1)
    start = end - dt.timedelta(days=days - 1)
    body = {"dateRanges": [{"startDate": start.isoformat(), "endDate": end.isoformat()}],
            "dimensions": [{"name": "landingPage"}],
            "metrics": [{"name": "sessions"}, {"name": "engagementRate"}, {"name": "keyEvents"}],
            "dimensionFilter": {"filter": {"fieldName": "sessionDefaultChannelGroup", "stringFilter": {"value": "Organic Search"}}},
            "limit": 10000}
    r = _post(GA4_URL.format(prop=prop), body, token)
    rows = [["Landing page", "Sessions", "Engagement rate", "Key events"]]
    for x in r.get("rows") or []:
        rows.append([x["dimensionValues"][0]["value"]] + [v["value"] for v in x["metricValues"]])
    return f"{start:%d/%m}–{end:%d/%m/%Y}", rows


def ga4_months(token, prop, months=17, today=None):
    """Theo tháng (yearMonth): kênh Organic Search + tổng phiên mọi kênh → {"2026-10": {cột Đánh giá tháng: giá trị}}."""
    today = today or dt.date.today()
    end = today - dt.timedelta(days=1)
    start = (end.replace(day=1) - dt.timedelta(days=31 * (months - 1))).replace(day=1)
    rng = [{"startDate": start.isoformat(), "endDate": end.isoformat()}]
    org = _post(GA4_URL.format(prop=prop), {
        "dateRanges": rng, "dimensions": [{"name": "yearMonth"}],
        "metrics": [{"name": n} for n in ("sessions", "totalUsers", "engagementRate", "bounceRate", "userEngagementDuration", "keyEvents", "sessionKeyEventRate")],
        "dimensionFilter": {"filter": {"fieldName": "sessionDefaultChannelGroup", "stringFilter": {"value": "Organic Search"}}}}, token)
    tot = _post(GA4_URL.format(prop=prop), {"dateRanges": rng, "dimensions": [{"name": "yearMonth"}], "metrics": [{"name": "sessions"}]}, token)
    out = {}
    for x in org.get("rows") or []:
        ym = x["dimensionValues"][0]["value"]
        ses, users, eng, bounce, dur, kev, kevr = (float(v["value"]) for v in x["metricValues"])
        out[f"{ym[:4]}-{ym[4:]}"] = {"Phiên organic": int(ses), "Người dùng organic": int(users),
                                     "Tỷ lệ tương tác %": round(eng * 100, 1), "Tỷ lệ thoát %": round(bounce * 100, 1),
                                     "Thời gian tương tác TB (giây)": round(dur / ses) if ses else None,
                                     "Chuyển đổi organic": int(kev), "Tỷ lệ chuyển đổi %": round(kevr * 100, 2)}
    for x in tot.get("rows") or []:
        ym = x["dimensionValues"][0]["value"]
        out.setdefault(f"{ym[:4]}-{ym[4:]}", {})["Phiên (mọi kênh)"] = int(float(x["metricValues"][0]["value"]))
    return out
