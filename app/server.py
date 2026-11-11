#!/usr/bin/env python3
"""
Rooty SEO Production — trang theo dõi dây chuyền, lưu dữ liệu trên Lark Base.

Chạy:  python app/server.py            → mở http://localhost:8010
Cấu hình Lark trong file .env ở thư mục rooty-seo-production (xem .env.example).
Chưa có .env → chạy chế độ DEMO, dữ liệu lưu tạm ở app/demo-data.json.

Chỉ dùng thư viện chuẩn của Python.
"""
from __future__ import annotations

import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

APP_DIR = Path(os.path.abspath(__file__)).parent
ROOT = APP_DIR.parent
sys.path.insert(0, str(APP_DIR))
import tables as TB  # noqa: E402  — 10 bảng theo 10 bước SEO
STATIC = APP_DIR / "static"
PORT = int(os.environ.get("PORT", "8010"))

# ------------------------------------------------------------------ cấu hình dây chuyền

STAGES = [
    "Hàng đợi", "1 · Nghiên cứu", "2 · Dàn ý", "3 · Viết nháp",
    "4 · Kiểm chứng", "5 · Brief ảnh", "6 · Chuốt giọng", "Đã đăng",
]
STATUSES = ["Đang làm", "Bị trả về", "Cần người", "Chờ duyệt", "Đã đăng"]
PAGE_TYPES = ["Cẩm nang địa điểm", "Bảng giá", "So sánh", "Lịch trình", "Danh sách", "Trang tour/combo", "Trang thương hiệu"]
GATE_RESULTS = ["Chưa chấm", "PASS", "FAIL"]
INTENTS = ["Thông tin", "Điều hướng", "Cân nhắc", "Mua"]
# Định dạng phù hợp theo ý định tìm kiếm (Bước 6)
INTENT_FORMATS = {
    "Thông tin": ["Bài blog / cẩm nang", "Hướng dẫn từng bước", "Checklist"],
    "Điều hướng": ["Trang thương hiệu / giới thiệu", "Trang liên hệ"],
    "Cân nhắc": ["Bài so sánh", "Review / đánh giá", "Top list"],
    "Mua": ["Trang tour / sản phẩm", "Trang danh mục", "Landing page"],
}
FORMATS = [f for fs in INTENT_FORMATS.values() for f in fs]
SERP_FEATURES = ["Featured Snippet", "People Also Ask", "Local Pack (bản đồ)", "Video", "Hình ảnh", "Quảng cáo", "AI Overview", "Sitelinks"]
# Muốn rời trạm (key) thì cổng (value) phải PASS
GATE_TO_LEAVE = {"2 · Dàn ý": "Cổng 1", "3 · Viết nháp": "Cổng 2", "4 · Kiểm chứng": "Cổng 3", "6 · Chuốt giọng": "Cổng 4"}
GATE_FILES = {
    "Cổng 1": "cong-1-dan-y.md", "Cổng 2": "cong-2-ban-nhap.md",
    "Cổng 3": "cong-3-kiem-chung.md", "Cổng 4": "cong-4-nguoi-duyet.md",
}

T_BAI = "Bài viết"
T_LOG = "Nhật ký"
T_VIEC = "Việc SEO"

QT_DIR = ROOT / "quy-trinh"
try:
    QT = json.loads((QT_DIR / "cong-doan.json").read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    QT = {"mang": {}, "pha": [], "cong_doan": []}
MANG = list(QT["mang"].keys())
PHA = QT["pha"]
VIEC_STATUS = ["Chưa làm", "Đang làm", "Xong", "Bị chặn", "Không áp dụng"]

# Kiểu trường Lark Base: 1 văn bản · 3 chọn một · 5 ngày
def _sel(opts):
    return {"options": [{"name": o} for o in opts]}

SCHEMA = {
    T_BAI: [
        ("Từ khoá", 1, None),          # trường đầu tiên = trường chính
        ("Slug", 1, None),
        ("Trạm", 3, _sel(STAGES)),
        ("Trạng thái", 3, _sel(STATUSES)),
        ("Loại trang", 3, _sel(PAGE_TYPES)),
        ("Người phụ trách", 1, None),
        ("Hạn", 5, {"date_formatter": "yyyy/MM/dd"}),
        ("Cổng 1", 3, _sel(GATE_RESULTS)),
        ("Cổng 2", 3, _sel(GATE_RESULTS)),
        ("Cổng 3", 3, _sel(GATE_RESULTS)),
        ("Cổng 4", 3, _sel(GATE_RESULTS)),
        ("Chi tiết cổng", 1, None),
        ("Link bài", 1, None),
        ("Ghi chú", 1, None),
        ("Cập nhật lúc", 5, {"date_formatter": "yyyy/MM/dd HH:mm"}),
        # Bước 6 · Search Intent & SERP
        ("Ý định", 3, _sel(INTENTS)),
        ("Định dạng", 3, _sel(FORMATS)),
        ("SERP: loại trang top 10", 1, None),
        ("SERP: tính năng", 1, None),
        ("Câu hỏi khách hay hỏi", 1, None),
        ("Kiểm nội dung", 1, None),
        ("Điểm nội dung", 2, {"formatter": "0"}),
        # GEO · AI Search
        ("Điểm GEO", 2, {"formatter": "0"}),
        ("Chấm GEO", 1, None),
    ],
    T_VIEC: [
        ("Công đoạn", 1, None),        # trường chính
        ("Mã", 1, None),
        ("Mảng", 3, _sel(MANG)),
        ("Pha", 3, _sel(PHA)),
        ("Từ tháng", 2, {"formatter": "0"}),
        ("Đến tháng", 2, {"formatter": "0"}),
        ("Cửa chặn", 3, _sel(["Có", "Không"])),
        ("Trạng thái", 3, _sel(VIEC_STATUS)),
        ("Người phụ trách", 1, None),
        ("Hạn", 5, {"date_formatter": "yyyy/MM/dd"}),
        ("Đầu ra", 1, None),
        ("Kết quả / link", 1, None),
        ("Ghi chú", 1, None),
        ("Cập nhật lúc", 5, {"date_formatter": "yyyy/MM/dd HH:mm"}),
    ],
    T_LOG: [
        ("Nội dung", 1, None),
        ("Slug", 1, None),
        ("Trạm", 1, None),
        ("Kết quả", 1, None),
        ("Thời gian", 5, {"date_formatter": "yyyy/MM/dd HH:mm"}),
    ],
}


for _k, _t in TB.TABLES.items():
    SCHEMA[_t["name"]] = TB.lark_fields(_k)


def load_env() -> dict:
    env = {}
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("LARK_APP_ID", "LARK_APP_SECRET", "LARK_BASE_TOKEN", "LARK_DOMAIN", "PROJECT_START", "SITE_URL", "PAGESPEED_API_KEY",
              "GOOGLE_SA_KEY", "GOOGLE_SA_JSON", "GSC_SITE", "GA4_PROPERTY"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    # Chạy trong Marketing Hub: LARK_BASE_TOKEN là biến chung của các app khác trong Hub,
    # nên Base của app SEO khai bằng tên riêng SEO_LARK_BASE_TOKEN.
    if os.environ.get("SEO_LARK_BASE_TOKEN"):
        env["LARK_BASE_TOKEN"] = os.environ["SEO_LARK_BASE_TOKEN"]
    return env


def parse_gates() -> dict:
    """Đọc tiêu chí từng cổng từ gates/*.md → {Cổng N: [{id, text, required}]}"""
    out = {}
    for gate, fname in GATE_FILES.items():
        items = []
        p = ROOT / "gates" / fname
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                m = re.match(r"^\s*(\d+)\.\s+(\(B\)\s*)?(.+)$", line)
                if m:
                    items.append({"id": f"{gate}-{m.group(1)}", "text": m.group(3).strip(), "required": bool(m.group(2))})
                    continue
                m = re.match(r"^\s*\[ \]\s+(.+)$", line)
                if m:  # cổng 4 (người duyệt): mọi dòng đều bắt buộc
                    items.append({"id": f"{gate}-{len(items)+1}", "text": m.group(1).strip(), "required": True})
        out[gate] = items
    return out


# ------------------------------------------------------------------ kho dữ liệu

class StoreError(Exception):
    pass


class LocalStore:
    """Chế độ demo: lưu vào file JSON, cùng giao diện với LarkStore."""
    mode = "demo"

    def __init__(self, path: Path):
        self.path = path
        self.lock = threading.Lock()
        if not path.exists():
            self._save({T_BAI: [], T_LOG: []})
            self._seed()

    def _load(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, data):
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    def _seed(self):
        now = int(time.time() * 1000)
        demo = [
            ("tour 4 đảo phú quốc nên đi 3 đảo hay 4 đảo", "tour-3-dao-hay-4-dao-phu-quoc", "2 · Dàn ý", "Đang làm", "So sánh", {"Cổng 1": "FAIL"}),
            ("chi phí du lịch phú quốc 3 ngày 2 đêm", "chi-phi-du-lich-phu-quoc-3n2d", "1 · Nghiên cứu", "Đang làm", "Bảng giá", {}),
            ("thị trấn hoàng hôn phú quốc", "thi-tran-hoang-hon-phu-quoc", "6 · Chuốt giọng", "Chờ duyệt", "Cẩm nang địa điểm", {"Cổng 1": "PASS", "Cổng 2": "PASS", "Cổng 3": "PASS"}),
            ("du lịch phú quốc với trẻ nhỏ", "du-lich-phu-quoc-voi-tre-nho", "Hàng đợi", "Đang làm", "Lịch trình", {}),
            ("chính sách huỷ đổi tour rooty trip", "chinh-sach-huy-doi-tour", "3 · Viết nháp", "Cần người", "Trang thương hiệu", {"Cổng 1": "PASS", "Cổng 2": "FAIL"}),
        ]
        for kw, slug, stage, status, ptype, gates in demo:
            f = {"Từ khoá": kw, "Slug": slug, "Trạm": stage, "Trạng thái": status, "Loại trang": ptype,
                 "Người phụ trách": "", "Cập nhật lúc": now}
            for g in GATE_FILES:
                f[g] = gates.get(g, "Chưa chấm")
            self.create(T_BAI, f)
        self.create(T_LOG, {"Nội dung": "Khởi tạo dữ liệu demo", "Slug": "", "Trạm": "", "Kết quả": "", "Thời gian": now})

    def setup(self):
        return {"ok": True, "message": "Chế độ demo không cần khởi tạo bảng."}

    def list(self, table):
        with self.lock:
            return self._load().get(table, [])

    def create(self, table, fields):
        with self.lock:
            data = self._load()
            rec = {"record_id": f"rec{int(time.time()*1e6)}", "fields": fields}
            data.setdefault(table, []).append(rec)
            self._save(data)
            return rec

    def update(self, table, record_id, fields):
        with self.lock:
            data = self._load()
            for r in data.get(table, []):
                if r["record_id"] == record_id:
                    r["fields"].update(fields)
                    self._save(data)
                    return r
        raise StoreError("Không tìm thấy bản ghi")

    def create_many(self, table, records):
        with self.lock:
            data = self._load()
            base = int(time.time() * 1e6)
            out = [{"record_id": f"rec{base + i}", "fields": f} for i, f in enumerate(records)]
            data.setdefault(table, []).extend(out)
            self._save(data)
            return out

    def update_many(self, table, updates: dict):
        with self.lock:
            data = self._load()
            for r in data.get(table, []):
                if r["record_id"] in updates:
                    r["fields"].update(updates[r["record_id"]])
            self._save(data)
            return len(updates)

    def delete(self, table, record_id):
        with self.lock:
            data = self._load()
            before = len(data.get(table, []))
            data[table] = [r for r in data.get(table, []) if r["record_id"] != record_id]
            if len(data[table]) == before:
                raise StoreError("Không tìm thấy bản ghi")
            self._save(data)
            return {"ok": True}


class LarkStore:
    """Đọc/ghi Lark Base (Bitable) qua Open API."""
    mode = "lark"

    def __init__(self, env: dict):
        self.app_id = env["LARK_APP_ID"]
        self.app_secret = env["LARK_APP_SECRET"]
        self.base = env["LARK_BASE_TOKEN"]
        self.domain = env.get("LARK_DOMAIN") or "https://open.larksuite.com"
        self._token, self._token_exp = None, 0
        self._tables: dict[str, str] = {}
        self.lock = threading.Lock()
        # Bộ nhớ tạm cho list(): bảng lớn (Từ khoá ~16 nghìn dòng) đọc từ Lark mất ~25 giây,
        # quá sát mốc 30 giây Marketing Hub cắt yêu cầu. Ghi qua app thì xoá ngay; người sửa
        # thẳng trên Lark thì thấy sau tối đa CACHE_TTL giây.
        self._cache: dict[str, tuple[float, list]] = {}
        self._cache_lock: dict[str, threading.Lock] = {}

    # -- HTTP
    def _req(self, method, path, body=None, auth=True):
        url = self.domain.rstrip("/") + path
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if auth:
            headers["Authorization"] = "Bearer " + self._tenant_token()
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                res = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            try:
                res = json.loads(e.read().decode())
            except Exception:
                raise StoreError(f"Lark trả lỗi HTTP {e.code}")
        except urllib.error.URLError as e:
            raise StoreError(f"Không kết nối được Lark: {e.reason}")
        if res.get("code", 0) != 0:
            raise StoreError(f"Lark lỗi {res.get('code')}: {res.get('msg')}")
        return res.get("data", res)

    def _tenant_token(self):
        if self._token and time.time() < self._token_exp - 60:
            return self._token
        url = self.domain.rstrip("/") + "/open-apis/auth/v3/tenant_access_token/internal"
        body = json.dumps({"app_id": self.app_id, "app_secret": self.app_secret}).encode()
        req = urllib.request.Request(url, data=body, method="POST", headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                res = json.loads(r.read().decode())
        except urllib.error.URLError as e:
            raise StoreError(f"Không lấy được token Lark: {e}")
        if res.get("code") != 0:
            raise StoreError(f"Sai App ID/App Secret? Lark lỗi {res.get('code')}: {res.get('msg')}")
        self._token = res["tenant_access_token"]
        self._token_exp = time.time() + int(res.get("expire", 7200))
        return self._token

    # -- bảng
    def _list_tables(self):
        out, page = {}, None
        while True:
            q = "?page_size=100" + (f"&page_token={page}" if page else "")
            d = self._req("GET", f"/open-apis/bitable/v1/apps/{self.base}/tables{q}")
            for t in d.get("items", []):
                out[t["name"]] = t["table_id"]
            if not d.get("has_more"):
                return out
            page = d.get("page_token")

    def _table_id(self, name):
        if name not in self._tables:
            self._tables = self._list_tables()
        if name not in self._tables:
            raise StoreError(f"Chưa có bảng «{name}» trong Base. Bấm «Khởi tạo bảng Lark» trên trang.")
        return self._tables[name]

    def setup(self):
        with self.lock:
            existing = self._list_tables()
            created, added = [], []
            for name, fields in SCHEMA.items():
                if name not in existing:
                    payload = {"table": {"name": name, "default_view_name": "Tất cả",
                                         "fields": [self._field_def(f) for f in fields]}}
                    d = self._req("POST", f"/open-apis/bitable/v1/apps/{self.base}/tables", payload)
                    existing[name] = d.get("table_id")
                    created.append(name)
                else:
                    tid = existing[name]
                    d = self._req("GET", f"/open-apis/bitable/v1/apps/{self.base}/tables/{tid}/fields?page_size=100")
                    have = {f["field_name"] for f in d.get("items", [])}
                    for f in fields:
                        if f[0] not in have:
                            self._req("POST", f"/open-apis/bitable/v1/apps/{self.base}/tables/{tid}/fields", self._field_def(f))
                            added.append(f"{name}.{f[0]}")
            self._tables = existing
            msg = []
            if created:
                msg.append("Đã tạo bảng: " + ", ".join(created))
            if added:
                msg.append("Đã thêm trường: " + ", ".join(added))
            return {"ok": True, "message": "; ".join(msg) or "Base đã đủ bảng và trường."}

    @staticmethod
    def _field_def(f):
        name, ftype, prop = f
        d = {"field_name": name, "type": ftype}
        if prop:
            d["property"] = prop
        return d

    # -- bản ghi
    CACHE_TTL = 600

    def list(self, table):
        with self._cache_lock.setdefault(table, threading.Lock()):  # hai yêu cầu cùng lúc: đọc Lark một lần
            hit = self._cache.get(table)
            if hit and time.time() - hit[0] < self.CACHE_TTL:
                rows = hit[1]
            else:
                rows = self._list_lark(table)
                self._cache[table] = (time.time(), rows)
        # bản sao từng dòng: nơi gọi sửa fields cũng không làm hỏng bộ nhớ tạm
        return [{"record_id": r["record_id"], "fields": dict(r["fields"])} for r in rows]

    def _list_lark(self, table):
        tid = self._table_id(table)
        out, page = [], None
        while True:
            q = "?page_size=500" + (f"&page_token={page}" if page else "")
            d = self._req("GET", f"/open-apis/bitable/v1/apps/{self.base}/tables/{tid}/records{q}")
            for it in d.get("items") or []:
                out.append({"record_id": it["record_id"], "fields": self._flatten(it.get("fields", {}), table)})
            if not d.get("has_more"):
                return out
            page = d.get("page_token")

    def create(self, table, fields):
        self._cache.pop(table, None)
        tid = self._table_id(table)
        d = self._req("POST", f"/open-apis/bitable/v1/apps/{self.base}/tables/{tid}/records", {"fields": self._clean(fields)})
        r = d.get("record", {})
        return {"record_id": r.get("record_id"), "fields": self._flatten(r.get("fields", {}), table)}

    def update(self, table, record_id, fields):
        self._cache.pop(table, None)
        tid = self._table_id(table)
        # khi sửa: chuỗi rỗng → null để xoá giá trị trong Lark
        body = {k: (None if v == "" else v) for k, v in fields.items()}
        d = self._req("PUT", f"/open-apis/bitable/v1/apps/{self.base}/tables/{tid}/records/{record_id}", {"fields": body})
        r = d.get("record", {})
        return {"record_id": r.get("record_id", record_id), "fields": self._flatten(r.get("fields", {}), table)}

    def create_many(self, table, records):
        self._cache.pop(table, None)
        tid = self._table_id(table)
        out = []
        for i in range(0, len(records), 450):  # Lark giới hạn 500 bản ghi / lần
            chunk = [{"fields": self._clean(f)} for f in records[i:i + 450]]
            d = self._req("POST", f"/open-apis/bitable/v1/apps/{self.base}/tables/{tid}/records/batch_create", {"records": chunk})
            for r in d.get("records", []):
                out.append({"record_id": r.get("record_id"), "fields": self._flatten(r.get("fields", {}), table)})
        return out

    def update_many(self, table, updates: dict):
        self._cache.pop(table, None)
        tid = self._table_id(table)
        items = [{"record_id": rid, "fields": {k: (None if v == "" else v) for k, v in f.items()}} for rid, f in updates.items()]
        for i in range(0, len(items), 450):
            self._req("POST", f"/open-apis/bitable/v1/apps/{self.base}/tables/{tid}/records/batch_update", {"records": items[i:i + 450]})
        return len(items)

    def delete(self, table, record_id):
        self._cache.pop(table, None)
        tid = self._table_id(table)
        self._req("DELETE", f"/open-apis/bitable/v1/apps/{self.base}/tables/{tid}/records/{record_id}")
        return {"ok": True}

    @staticmethod
    def _clean(fields):
        # Lark không nhận chuỗi rỗng cho trường chọn/ngày → bỏ đi
        return {k: v for k, v in fields.items() if v not in ("", None)}

    @staticmethod
    def _flatten(fields, table=None):
        # Văn bản có thể trả về dạng [{"type":"text","text":"..."}]
        # Trường số có định dạng (formatter) Lark trả về chuỗi "44" → đổi lại thành số
        nums = {n for n, t, _ in SCHEMA.get(table, []) if t == 2}
        out = {}
        for k, v in fields.items():
            if isinstance(v, list) and v and isinstance(v[0], dict) and "text" in v[0]:
                out[k] = "".join(x.get("text", "") for x in v)
            elif k in nums and isinstance(v, str):
                try:
                    f = float(v.replace(",", ""))
                    out[k] = int(f) if f.is_integer() else f
                except ValueError:
                    out[k] = v
            else:
                out[k] = v
        return out


def make_store():
    env = load_env()
    if all(env.get(k) for k in ("LARK_APP_ID", "LARK_APP_SECRET", "LARK_BASE_TOKEN")):
        return LarkStore(env)
    return LocalStore(APP_DIR / "demo-data.json")


STORE = make_store()


def _prewarm():
    """Đọc sẵn mọi bảng vào bộ nhớ tạm lúc khởi động, để người mở trang đầu tiên không phải chờ."""
    for t in TB.TABLES.values():
        try:
            STORE.list(t["name"])
        except Exception:
            pass


if STORE.mode == "lark":
    threading.Thread(target=_prewarm, daemon=True).start()
GATES = parse_gates()
ENV = load_env()


def project_start() -> str:
    """Tháng bắt đầu dự án dạng YYYY-MM (PROJECT_START trong .env), mặc định tháng hiện tại."""
    v = ENV.get("PROJECT_START", "")
    if re.match(r"^\d{4}-\d{2}$", v):
        return v
    return time.strftime("%Y-%m")


def current_month_index() -> int:
    y, m = map(int, project_start().split("-"))
    now = time.localtime()
    return (now.tm_year - y) * 12 + (now.tm_mon - m) + 1


# ------------------------------------------------------------------ nghiệp vụ

def now_ms():
    return int(time.time() * 1000)


def log(content, slug="", stage="", result=""):
    try:
        STORE.create(T_LOG, {"Nội dung": content, "Slug": slug, "Trạm": stage, "Kết quả": result, "Thời gian": now_ms()})
    except StoreError:
        pass


def find_bai(record_id):
    for r in STORE.list(T_BAI):
        if r["record_id"] == record_id:
            return r
    raise StoreError("Không tìm thấy bài")


def slugify(s):
    s = s.lower().strip()
    table = str.maketrans("àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ",
                          "aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd")
    s = s.translate(table)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:80]


def gate_verdict(gate, checked: list[str]):
    items = GATES.get(gate, [])
    if not items:
        return "Chưa chấm", 0, 0
    req = [i for i in items if i["required"]]
    opt = [i for i in items if not i["required"]]
    req_ok = all(i["id"] in checked for i in req)
    opt_ok = (sum(i["id"] in checked for i in opt) / len(opt) >= 0.8) if opt else True
    passed = sum(i["id"] in checked for i in items)
    return ("PASS" if req_ok and opt_ok else "FAIL"), passed, len(items)


def api_create(body):
    kw = (body.get("Từ khoá") or "").strip()
    if not kw:
        raise StoreError("Cần nhập từ khoá")
    fields = {
        "Từ khoá": kw,
        "Slug": body.get("Slug") or slugify(kw),
        "Trạm": "Hàng đợi",
        "Trạng thái": "Đang làm",
        "Loại trang": body.get("Loại trang") or "",
        "Người phụ trách": body.get("Người phụ trách") or "",
        "Ghi chú": body.get("Ghi chú") or "",
        "Cập nhật lúc": now_ms(),
        "Ý định": body.get("Ý định") or KW.guess_intent(kw),
    }
    fields["Định dạng"] = INTENT_FORMATS[fields["Ý định"]][0] if fields["Ý định"] in INTENT_FORMATS else ""
    if body.get("Hạn"):
        fields["Hạn"] = int(body["Hạn"])
    for g in GATE_FILES:
        fields[g] = "Chưa chấm"
    rec = STORE.create(T_BAI, fields)
    log(f"Thêm bài mới: {kw}", fields["Slug"], "Hàng đợi")
    return rec


def api_update(record_id, body):
    rec = find_bai(record_id)
    f = rec["fields"]
    changes = {}
    for k in ("Từ khoá", "Loại trang", "Người phụ trách", "Ghi chú", "Link bài", "Trạng thái", "Hạn",
              "Ý định", "Định dạng", "SERP: loại trang top 10", "SERP: tính năng", "Câu hỏi khách hay hỏi"):
        if k in body:
            changes[k] = body[k]

    # chuyển trạm — kiểm cổng
    if "Trạm" in body and body["Trạm"] != f.get("Trạm"):
        cur, new = f.get("Trạm", "Hàng đợi"), body["Trạm"]
        if new not in STAGES:
            raise StoreError("Trạm không hợp lệ")
        if STAGES.index(new) > STAGES.index(cur):
            # đi tới: mọi cổng của các trạm bị vượt qua phải PASS
            for s in STAGES[STAGES.index(cur):STAGES.index(new)]:
                g = GATE_TO_LEAVE.get(s)
                if g and f.get(g) != "PASS":
                    raise StoreError(f"Chưa qua {g} — chưa thể rời trạm «{s}».")
        changes["Trạm"] = new
        if new == "Đã đăng":
            changes["Trạng thái"] = "Đã đăng"
        elif STAGES.index(new) < STAGES.index(cur):
            changes["Trạng thái"] = "Bị trả về"
        elif new == "6 · Chuốt giọng":
            changes["Trạng thái"] = "Chờ duyệt"
        else:
            changes["Trạng thái"] = "Đang làm"
        log(f"Chuyển trạm: {cur} → {new}", f.get("Slug", ""), new, changes.get("Trạng thái", ""))

    # chấm cổng
    if "gate" in body:
        gate = body["gate"]
        if gate not in GATE_FILES:
            raise StoreError("Cổng không hợp lệ")
        checked = body.get("checked", [])
        verdict, passed, total = gate_verdict(gate, checked)
        detail = {}
        try:
            detail = json.loads(f.get("Chi tiết cổng") or "{}")
        except json.JSONDecodeError:
            pass
        detail[gate] = {"checked": checked, "note": body.get("note", ""), "at": now_ms()}
        changes[gate] = verdict
        changes["Chi tiết cổng"] = json.dumps(detail, ensure_ascii=False)
        if verdict == "FAIL":
            changes["Trạng thái"] = "Bị trả về"
        elif f.get("Trạng thái") in ("Bị trả về", "Cần người"):
            changes["Trạng thái"] = "Chờ duyệt" if gate == "Cổng 4" else "Đang làm"
        log(f"Chấm {gate}: {verdict} ({passed}/{total})", f.get("Slug", ""), f.get("Trạm", ""), verdict)

    if not changes:
        return rec
    changes["Cập nhật lúc"] = now_ms()
    return STORE.update(T_BAI, record_id, changes)


def api_viec_seed():
    existing = {r["fields"].get("Mã") for r in STORE.list(T_VIEC)}
    added = 0
    for c in QT["cong_doan"]:
        if c["ma"] in existing:
            continue
        STORE.create(T_VIEC, {
            "Công đoạn": c["ten"], "Mã": c["ma"], "Mảng": c["mang"], "Pha": PHA[c["pha"] - 1],
            "Từ tháng": c["tu"], "Đến tháng": c["den"], "Cửa chặn": "Có" if c["cua"] else "Không",
            "Trạng thái": "Chưa làm", "Đầu ra": c.get("dau_ra", ""), "Cập nhật lúc": now_ms(),
        })
        added += 1
    if added:
        log(f"Nạp {added} công đoạn SEO vào bảng Việc SEO")
    return {"ok": True, "message": f"Đã nạp {added} công đoạn" if added else "Đã đủ công đoạn, không nạp thêm."}


def api_viec_update(record_id, body):
    rec = next((r for r in STORE.list(T_VIEC) if r["record_id"] == record_id), None)
    if not rec:
        raise StoreError("Không tìm thấy công đoạn")
    changes = {k: body[k] for k in ("Trạng thái", "Người phụ trách", "Hạn", "Kết quả / link", "Ghi chú") if k in body}
    if "Trạng thái" in changes and changes["Trạng thái"] not in VIEC_STATUS:
        raise StoreError("Trạng thái không hợp lệ")
    if not changes:
        return rec
    changes["Cập nhật lúc"] = now_ms()
    if "Trạng thái" in changes and changes["Trạng thái"] != rec["fields"].get("Trạng thái"):
        f = rec["fields"]
        log(f"Việc SEO {f.get('Mã')}: {f.get('Trạng thái')} → {changes['Trạng thái']}", "", f.get("Mảng", ""), changes["Trạng thái"])
    return STORE.update(T_VIEC, record_id, changes)


# ------------------------------------------------------------------ 10 bảng theo 10 bước

def _tname(key):
    if key not in TB.TABLES:
        raise StoreError("Bảng không tồn tại")
    return TB.TABLES[key]["name"]


def _clean_fields(key, body):
    """Chỉ giữ trường có trong schema, ép kiểu số/ngày."""
    kinds = {f["n"]: f["k"] for f in TB.TABLES[key]["fields"]}
    out = {}
    for k, v in (body or {}).items():
        if k not in kinds:
            continue
        if kinds[k] in ("num", "dec", "date"):
            if v in ("", None):
                v = None
            else:
                try:
                    v = float(v)
                    v = int(v) if kinds[k] in ("num", "date") else round(v, 2)
                except (TypeError, ValueError):
                    raise StoreError(f"«{k}» phải là số")
        elif v is None:
            v = ""
        else:
            v = str(v)
        out[k] = v
    return out


def t_create(key, body):
    f = _clean_fields(key, body)
    if not str(f.get(TB.primary(key), "")).strip():
        raise StoreError(f"Cần nhập «{TB.primary(key)}»")
    return STORE.create(_tname(key), {k: v for k, v in f.items() if v not in ("", None)})


def t_update(key, rid, body):
    f = _clean_fields(key, body)
    if key == "sualoi":
        f = loi_on_update(rid, f)
    if key == "giadukien":
        f = gia_on_update(rid, f)
    if TB.primary(key) in f and not str(f[TB.primary(key)]).strip():
        raise StoreError(f"«{TB.primary(key)}» không được để trống")
    return STORE.update(_tname(key), rid, f)


def t_bulk(key, body):
    recs = [_clean_fields(key, r) for r in (body or {}).get("records", [])]
    recs = [{k: v for k, v in r.items() if v not in ("", None)} for r in recs if str(r.get(TB.primary(key), "")).strip()]
    if not recs:
        raise StoreError("Không có dòng hợp lệ để nhập")
    # bỏ dòng trùng giá trị trường chính với dữ liệu đã có
    have = {str(r["fields"].get(TB.primary(key), "")).strip().lower() for r in STORE.list(_tname(key))}
    seen, new = set(), []
    for r in recs:
        k = str(r[TB.primary(key)]).strip().lower()
        if k in have or k in seen:
            continue
        seen.add(k)
        new.append(r)
    if new:
        STORE.create_many(_tname(key), new)
    log(f"Nhập {len(new)} dòng vào bảng {_tname(key)} (bỏ {len(recs) - len(new)} trùng)")
    return {"ok": True, "message": f"Đã nhập {len(new)} dòng, bỏ qua {len(recs) - len(new)} dòng trùng."}


def t_seed(key):
    if key not in TB.SEEDS:
        raise StoreError("Bảng này không có dữ liệu mẫu")
    return t_bulk(key, {"records": TB.SEEDS[key]})


def import_crawl():
    rows, src = TB.crawl_rows(ROOT / "reports")
    have = {r["fields"].get("URL") for r in STORE.list(_tname("trang"))}
    recs = TB.trang_from_crawl(rows, have)
    if recs:
        STORE.create_many(_tname("trang"), recs)
    log(f"Nạp {len(recs)} trang từ {src} vào Trang đích")
    return {"ok": True, "message": f"Đã nạp {len(recs)} trang từ {src}" if recs else "Không có trang mới để nạp."}


def import_audit():
    """Đồng bộ Audit với báo cáo mới nhất: thêm vấn đề mới, cập nhật số trang,
    mở lại vấn đề 'Đã sửa' nếu vẫn còn, tự đóng vấn đề từ crawl không còn xuất hiện."""
    rows, src = TB.crawl_rows(ROOT / "reports")
    existing = {r["fields"].get("Vấn đề"): r for r in STORE.list(_tname("audit"))}
    found = TB.audit_from_reports(rows, src, ROOT / "reports", set())
    found_names = {f["Vấn đề"] for f in found}
    today = time.strftime("%d/%m/%Y")
    new, upd, reopened, closed = [], 0, 0, 0
    for f in found:
        old = existing.get(f["Vấn đề"])
        if not old:
            new.append(f)
            continue
        ch = {"Số trang": f["Số trang"], "URL ví dụ": f["URL ví dụ"], "Nguồn": f["Nguồn"]}
        if old["fields"].get("Trạng thái") == "Đã sửa":
            ch["Trạng thái"] = "Mới"
            ch["Ghi chú"] = (old["fields"].get("Ghi chú") or "") + f"\n{today}: mở lại — báo cáo {src} vẫn thấy {f['Số trang']} trang."
            reopened += 1
        STORE.update(_tname("audit"), old["record_id"], ch)
        upd += 1
    complete = TB.crawl_complete(ROOT / "reports")  # crawl dừng giữa chừng thì không tự đóng
    for name, old in existing.items():
        fo = old["fields"]
        if complete and name not in found_names and str(fo.get("Nguồn", "")).startswith("crawl-") and fo.get("Trạng thái") not in ("Đã sửa", "Bỏ qua"):
            STORE.update(_tname("audit"), old["record_id"], {"Trạng thái": "Đã sửa", "Số trang": 0,
                         "Ghi chú": (fo.get("Ghi chú") or "") + f"\n{today}: tự đóng — báo cáo {src} không còn thấy."})
            closed += 1
    if new:
        STORE.create_many(_tname("audit"), new)
    msg = f"Audit: {len(new)} vấn đề mới · cập nhật {upd} · mở lại {reopened} · tự đóng {closed}"
    if not complete:
        msg += " (crawl chưa quét hết site nên không tự đóng vấn đề nào)"
    log(msg)
    return {"ok": True, "message": msg}


# ------------------------------------------------------------------ Technical SEO: kiểm tự động + chạy crawl
import subprocess  # noqa: E402
import techcheck  # noqa: E402


def site_url():
    return (ENV.get("SITE_URL") or "https://rootytrip.com").rstrip("/")


def sync_checklist():
    """Đưa bảng Checklist audit về đúng danh sách mới nhất (thêm mục mới, cập nhật tên/hạng mục), giữ nguyên kết quả đã chấm."""
    tname = _tname("kythuat")
    recs = STORE.list(tname)
    by_code = {r["fields"].get("Mã"): r for r in recs}
    new, ups = [], {}
    for c, m, a, g, lv, auto, how in TB.TECH_CHECKLIST:
        want = {"Mục kiểm": m, "Hạng mục": a, "Nhóm": g, "Mức độ": lv, "Kiểm tự động": "Có" if auto else "Không", "Cách kiểm / cách sửa": how}
        r = by_code.get(c)
        if not r:
            new.append({**want, "Mã": c, "Kết quả": "Chưa kiểm"})
        elif any(r["fields"].get(k) != v for k, v in want.items()):
            ups[r["record_id"]] = want
    if new:
        STORE.create_many(tname, new)
    if ups:
        STORE.update_many(tname, ups)
    return len(new), len(ups)


def _apply_tech(results: dict):
    tname = _tname("kythuat")
    sync_checklist()
    recs = STORE.list(tname)
    by_code = {r["fields"].get("Mã"): r for r in recs}
    now = now_ms()
    STORE.update_many(tname, {by_code[c]["record_id"]: {"Kết quả": res, "Chi tiết kết quả": detail, "Lần kiểm": now}
                              for c, (res, detail) in results.items() if c in by_code})
    ok = sum(1 for v in results.values() if v[0] == "Đạt")
    bad = sum(1 for v in results.values() if v[0] == "Chưa đạt")
    return ok, bad, len(results)


def tech_check():
    key = ENV.get("PAGESPEED_API_KEY")
    results = techcheck.check_site(site_url(), key)
    try:
        rows, _ = TB.crawl_rows(ROOT / "reports")
    except FileNotFoundError:
        rows = []
    results.update(techcheck.check_crawl(rows, ROOT / "reports"))
    results.update(techcheck.check_extra(site_url(), rows, key))
    results.update(techcheck.check_tables({k: [r["fields"] for r in STORE.list(_tname(k))] for k in ("trang", "tukhoa", "hoso", "lienket")}))
    ok, bad, n = _apply_tech(results)
    msg = f"Kiểm tự động {n} mục (5 hạng mục): {ok} đạt · {bad} chưa đạt · {n - ok - bad} chưa kiểm được"
    log(msg)
    return {"ok": True, "message": msg}


CRAWL = {"running": False, "lines": [], "started": 0, "finished": 0, "rc": None, "result": ""}


def _crawl_worker(max_pages):
    cmd = [sys.executable, "-X", "utf8", str(ROOT / "scripts" / "crawl_site.py"), site_url(),
           "--max-pages", str(max_pages), "--delay", "0.15"]
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                             encoding="utf-8", errors="replace", cwd=str(ROOT))
        for line in p.stdout:
            CRAWL["lines"] = (CRAWL["lines"] + [line.rstrip()])[-8:]
        CRAWL["rc"] = p.wait()
        if CRAWL["rc"] == 0:
            parts = [import_crawl()["message"], import_audit()["message"]]
            rows, _ = TB.crawl_rows(ROOT / "reports")
            _apply_tech(techcheck.check_crawl(rows, ROOT / "reports"))
            parts.append("đã chấm lại các mục kiểm từ crawl trong Checklist audit")
            parts.append(onpage_rescore()["message"].split(" (")[0])
            CRAWL["result"] = " · ".join(parts)
        else:
            CRAWL["result"] = f"Crawl lỗi (mã {CRAWL['rc']}): " + " / ".join(CRAWL["lines"][-3:])
    except Exception as e:
        CRAWL["result"] = f"Crawl lỗi: {e}"
    finally:
        CRAWL["running"] = False
        CRAWL["finished"] = now_ms()
        log("Chạy crawl xong: " + CRAWL["result"][:300])


# ------------------------------------------------------------------ B2–B4: từ khoá, topic cluster, đối thủ
import kwtools as KW  # noqa: E402

JOBS: dict[str, dict] = {}


def run_job(name, fn):
    if JOBS.get(name, {}).get("running"):
        raise StoreError("Việc này đang chạy, đợi xong đã.")
    st = JOBS[name] = {"running": True, "lines": [], "result": "", "started": now_ms(), "finished": 0}

    def say(m):
        st["lines"] = (st["lines"] + [m])[-8:]

    def work():
        try:
            st["result"] = fn(say) or "Xong"
        except Exception as e:
            st["result"] = f"Lỗi: {e}"
        finally:
            st["running"] = False
            st["finished"] = now_ms()
            log(f"{name}: {st['result'][:300]}")
    threading.Thread(target=work, daemon=True).start()
    return {"ok": True, "message": "Đã bắt đầu — chạy nền, trang tự cập nhật khi xong."}


def kw_expand(body):
    if (body or {}).get("__invalid__"):
        raise StoreError("Dữ liệu gửi lên không phải JSON hợp lệ")
    ids = set((body or {}).get("ids") or [])

    def job(say):
        seeds = [r for r in STORE.list(_tname("tukhoagoc"))
                 if (r["record_id"] in ids) or (not ids and r["fields"].get("Mở rộng") != "Đã mở rộng")]
        if not seeds:
            return "Không có từ khoá gốc nào cần mở rộng (đều đã mở rộng)."
        total_new = 0
        for i, s in enumerate(seeds, 1):
            f = s["fields"]
            seed = f.get("Từ khoá gốc", "").strip()
            say(f"[{i}/{len(seeds)}] Mở rộng «{seed}»…")
            kws = KW.expand_seed(seed, say)
            before = len(STORE.list(_tname("tukhoa")))
            recs = [{"Từ khoá": k, "Ý định": KW.guess_intent(k), "Giai đoạn": KW.INTENT_STAGE[KW.guess_intent(k)],
                     "Nguồn": "Gợi ý Google", "Từ khoá gốc": seed, "Cụm chủ đề": f.get("Cụm dự kiến", ""), "Trạng thái": "Mới"} for k in kws]
            if recs:
                try:
                    t_bulk("tukhoa", {"records": recs})
                except StoreError:
                    pass
            added = len(STORE.list(_tname("tukhoa"))) - before
            total_new += added
            STORE.update(_tname("tukhoagoc"), s["record_id"], {"Mở rộng": "Đã mở rộng", "Số từ khoá tìm được": len(kws),
                                                               "Ghi chú": f"{time.strftime('%d/%m/%Y')}: {len(kws)} gợi ý, thêm mới {added}"})
        return f"Mở rộng {len(seeds)} từ khoá gốc → thêm {total_new} từ khoá mới vào bảng Từ khoá"
    return run_job("expand", job)


def kw_group():
    rows = STORE.list(_tname("tukhoa"))
    ups = KW.suggest_groups(rows)
    if ups:
        STORE.update_many(_tname("tukhoa"), ups)
    groups = {u.get("Nhóm URL") for u in ups.values() if u.get("Nhóm URL")}
    msg = f"Gợi ý gom nhóm: điền {len(ups)} từ khoá vào {len(groups)} nhóm URL (chỉ điền ô trống — kiểm lại bằng SERP)"
    log(msg)
    return {"ok": True, "message": msg}


def kw_create_posts():
    rows = [r for r in STORE.list(_tname("tukhoa")) if r["fields"].get("Trạng thái") != "Bỏ"]
    groups: dict[str, list] = {}
    for r in rows:
        g = r["fields"].get("Nhóm URL")
        if g:
            groups.setdefault(g, []).append(r)
    have_slugs = {r["fields"].get("Slug") for r in STORE.list(T_BAI)}
    created, marked = 0, {}
    for g, rs in groups.items():
        if any(r["fields"].get("Trang đích") for r in rs):
            continue
        slug = KW.slugify(g)
        if slug not in have_slugs:
            kws = ", ".join(r["fields"].get("Từ khoá", "") for r in rs[:15])
            api_create({"Từ khoá": g, "Slug": slug, "Ghi chú": f"Tạo từ nhóm URL (B3). Từ khoá trong nhóm: {kws}"})
            have_slugs.add(slug)
            created += 1
        for r in rs:
            if r["fields"].get("Trạng thái") in (None, "", "Mới"):
                marked[r["record_id"]] = {"Trạng thái": "Cần viết"}
    if marked:
        STORE.update_many(_tname("tukhoa"), marked)
    return {"ok": True, "message": f"Tạo {created} bài mới trong tab Content cho các nhóm chưa có trang; đánh dấu {len(marked)} từ khoá «Cần viết»."}


def bai_intent(rid):
    """Suy ý định cho bài từ các từ khoá trong nhóm URL (B3), hoặc từ chính từ khoá bài."""
    rec = find_bai(rid)
    kw = rec["fields"].get("Từ khoá", "")
    group = [r["fields"] for r in STORE.list(_tname("tukhoa"))
             if (r["fields"].get("Nhóm URL") or "").lower() == kw.lower() and r["fields"].get("Trạng thái") != "Bỏ"]
    if group:
        cnt = {}
        for f in group:
            it = f.get("Ý định") or KW.guess_intent(f.get("Từ khoá", ""))
            cnt[it] = cnt.get(it, 0) + (f.get("Lượng tìm") or f.get("Hiển thị") or 1)
        intent = max(cnt, key=cnt.get)
        why = f"theo {len(group)} từ khoá trong nhóm URL (" + ", ".join(f"{k}: {v}" for k, v in cnt.items()) + ")"
    else:
        intent = KW.guess_intent(kw)
        why = "đoán từ từ khoá chính"
    fmt = INTENT_FORMATS[intent][0]
    STORE.update(T_BAI, rid, {"Ý định": intent, "Định dạng": rec["fields"].get("Định dạng") or fmt, "Cập nhật lúc": now_ms()})
    return {"ok": True, "message": f"Ý định: {intent} ({why}) · định dạng gợi ý: {', '.join(INTENT_FORMATS[intent])}"}


def bai_questions(rid):
    rec = find_bai(rid)
    qs = KW.suggest_questions(rec["fields"].get("Từ khoá", ""))
    if not qs:
        return {"ok": True, "message": "Google không gợi ý câu hỏi nào cho từ khoá này."}
    STORE.update(T_BAI, rid, {"Câu hỏi khách hay hỏi": "\n".join(qs), "Cập nhật lúc": now_ms()})
    return {"ok": True, "message": f"Lấy được {len(qs)} câu hỏi — dùng làm H2/FAQ"}


def bai_check(rid):
    rec = find_bai(rid)
    f = rec["fields"]
    url = (f.get("Link bài") or "").strip()
    if not url.startswith("http"):
        raise StoreError("Cần điền «Link bài» (URL bài đã đăng) trước khi chấm")
    score, detail = KW.content_check(url, f.get("Từ khoá", ""), f.get("Ý định") or KW.guess_intent(f.get("Từ khoá", "")))
    STORE.update(T_BAI, rid, {"Kiểm nội dung": f"{time.strftime('%d/%m/%Y')} · {detail}", "Điểm nội dung": score, "Cập nhật lúc": now_ms()})
    log(f"Chấm nội dung {score}/100", f.get("Slug", ""), f.get("Trạm", ""))
    return {"ok": True, "message": f"Điểm nội dung {score}/100"}



# ------------------------------------------------------------------ GEO · AI Search (Checklist GEO của GTV)
import geocheck as GEO  # noqa: E402


def sync_geo():
    """Đưa bảng Checklist GEO về đúng 32 việc của GTV (thêm việc thiếu, cập nhật nội dung), giữ trạng thái đã ghi."""
    tname = _tname("geo")
    have = {int(r["fields"].get("Số") or 0): r for r in STORE.list(tname)}
    new, ups = [], {}
    for it in TB.SEEDS["geo"]:
        r = have.get(it["Số"])
        want = {k: v for k, v in it.items() if k != "Trạng thái"}
        if not r:
            new.append(it)
        elif any(r["fields"].get(k) != v for k, v in want.items()):
            ups[r["record_id"]] = want
    if new:
        STORE.create_many(tname, new)
    if ups:
        STORE.update_many(tname, ups)
    return len(new), len(ups)


def _geo_fields(res):
    return {"Điểm GEO": res["score"], "Chấm GEO": f"{time.strftime('%d/%m/%Y')} · " + GEO.render(res)}


def bai_geo(rid):
    rec = find_bai(rid)
    f = rec["fields"]
    url = (f.get("Link bài") or "").strip()
    if not url.startswith("http"):
        raise StoreError("Cần điền «Link bài» (URL bài đã đăng) trước khi chấm GEO")
    res = GEO.check(url, f.get("Từ khoá", ""), f.get("Ý định") or KW.guess_intent(f.get("Từ khoá", "")))
    if res.get("error"):
        raise StoreError(res["error"])
    STORE.update(T_BAI, rid, {**_geo_fields(res), "Cập nhật lúc": now_ms()})
    log(f"Chấm GEO {res['score']}/100 · G3 {res['g3']}", f.get("Slug", ""), f.get("Trạm", ""))
    return {"ok": True, "message": f"Điểm GEO {res['score']}/100 · G3 đạt {res['g3']} · " + ("qua cửa chặn" if res["gate_ok"] else "CHƯA qua cửa chặn")}


def trang_geo(rid, kw_rows=None):
    rec = next((r for r in STORE.list(_tname("trang")) if r["record_id"] == rid), None)
    if not rec:
        raise StoreError("Không tìm thấy trang")
    f = rec["fields"]
    kw, _ = page_keyword(f, kw_rows)
    intent = KW.guess_intent(kw) if kw else ""
    res = GEO.check(f["URL"], kw or "", intent)
    if res.get("error"):
        raise StoreError(res["error"])
    STORE.update(_tname("trang"), rid, {**_geo_fields(res), "Qua cửa chặn GEO": "Đạt" if res["gate_ok"] else "Chưa đạt",
                                        "Lần chấm GEO": now_ms()})
    return {"ok": True, "message": f"Điểm GEO {res['score']}/100 · G3 đạt {res['g3']}"}


def geo_batch(body):
    """Chấm GEO hàng loạt các bài viết (ưu tiên bài nhiều hiển thị GSC / nhiều link vào, chưa chấm)."""
    limit = int((body or {}).get("limit") or 30)
    ids = set((body or {}).get("ids") or [])

    def job(say):
        kw_rows = STORE.list(_tname("tukhoa"))
        rows = [r for r in STORE.list(_tname("trang")) if (r["record_id"] in ids) or (
            not ids and r["fields"].get("Loại trang") == "Bài viết" and (r["fields"].get("Số từ") or 0) >= 300
            and not r["fields"].get("Lần chấm GEO"))]
        rows.sort(key=lambda r: (-(r["fields"].get("GSC hiển thị") or 0), -(r["fields"].get("Link vào") or 0)))
        rows = rows[:limit]
        done, errs = 0, 0
        for i, r in enumerate(rows, 1):
            say(f"[{i}/{len(rows)}] {r['fields'].get('URL')}")
            try:
                trang_geo(r["record_id"], kw_rows)
                done += 1
            except Exception:
                errs += 1
        res = geo_sync()["message"]
        return f"Chấm GEO {done} trang" + (f" · bỏ qua {errs} trang (quá ít chữ, không phải bài, hoặc không tải được)" if errs else "") + " · " + res
    return run_job("geo", job)


GEO_LINE = re.compile(r"^(✅|❌) #(\d+)", re.M)


def _page_crit(texts):
    """Từ cột «Chấm GEO» của các trang → {số tiêu chí: [số trang đạt, số trang đo]}."""
    agg = {}
    for t in texts:
        per = {}
        for mark, no in GEO_LINE.findall(t or ""):
            per[int(no)] = per.get(int(no), True) and mark == "✅"
        for no, ok in per.items():
            a = agg.setdefault(no, [0, 0])
            a[0] += ok
            a[1] += 1
    return agg


def geo_sync():
    """Tự điền «Kết quả tự kiểm» cho Checklist GEO từ: Checklist audit (B5), điểm GEO từng bài, đo hiện diện AI, GSC."""
    sync_geo()
    tname = _tname("geo")
    recs = {int(r["fields"].get("Số") or 0): r for r in STORE.list(tname)}
    tech = {r["fields"].get("Mã"): r["fields"] for r in STORE.list(_tname("kythuat"))}
    trang = [r["fields"] for r in STORE.list(_tname("trang"))]
    bai = [r["fields"] for r in STORE.list(T_BAI)]
    crit = _page_crit([f.get("Chấm GEO") for f in trang + bai if f.get("Chấm GEO")])
    q = STORE.list(_tname("cauhoiai"))
    runs = [r["fields"] for r in STORE.list(_tname("aihien"))]
    summ = GEO.presence_summary(runs, len(q))
    out = {}

    for n, codes in TB.GEO_TECH.items():
        got = [(c, tech.get(c, {}).get("Kết quả") or "Chưa kiểm") for c in codes]
        checked = [k for _, k in got if k != "Chưa kiểm"]
        st = None
        if checked:
            st = "Chưa đạt" if "Chưa đạt" in checked else ("Đạt" if len(checked) == len(got) else None)
        out[n] = (st, "B5 · " + " · ".join(f"{c}: {k}" for c, k in got))
    for n in sorted(TB.GEO_AUTO_PAGE):
        if n in crit:
            ok, tot = crit[n]
            pct = round(ok / tot * 100)
            prev_st, prev_txt = out.get(n, (None, ""))
            st = "Chưa đạt" if prev_st == "Chưa đạt" or pct < 80 else "Đạt"
            out[n] = (st, (prev_txt + " · " if prev_txt else "") + f"Chấm bài: {ok}/{tot} trang đạt ({pct}%)")
    gsc = [f for f in trang if f.get("GSC vị trí")]
    if gsc:
        top = sum(1 for f in gsc if f["GSC vị trí"] <= 10)
        out[1] = ("Đạt" if top else "Chưa đạt", f"{top}/{len(gsc)} trang có số liệu GSC đang ở top 10 (vị trí TB)")
    else:
        out[1] = (None, "Chưa có số liệu GSC — nhập ở tab B10")
    base = [f for f in runs if f.get("Ngày chạy") and f.get("Phiên bản mô hình")]
    out[3] = ("Đạt" if len(q) >= 28 and base else ("Đang làm" if q else None),
              f"Bộ câu hỏi {len(q)} câu (GTV: 28–40 cho ngành dịch vụ) · {len(base)} lượt đo có ghi ngày + phiên bản mô hình")
    if runs:
        out[30] = ("Đạt" if summ["pairsUnder3"] == 0 else "Chưa đạt",
                   f"{summ['pairs']} cặp câu × máy AI · {summ['pairsUnder3']} cặp chạy chưa đủ 3 lần")
        eng = ", ".join(f"{e}: nhắc {d['mentionPct']}%" for e, d in summ["engines"].items())
        alert = summ["concentrationAlert"]
        out[31] = ("Chưa đạt" if alert else ("Đạt" if len(summ["engines"]) >= 2 else "Đang làm"),
                   eng + (f" · ⚠ lượt nhắc tập trung > 70% ở {', '.join(alert)}" if alert else ""))
    now = now_ms()
    ups = {}
    for n, (st, txt) in out.items():
        r = recs.get(n)
        if not r:
            continue
        ch = {"Kết quả tự kiểm": txt, "Lần kiểm": now}
        if st and r["fields"].get("Trạng thái") != "Không áp dụng":
            ch["Trạng thái"] = st
        ups[r["record_id"]] = ch
    if ups:
        STORE.update_many(tname, ups)
    done = sum(1 for st, _ in out.values() if st == "Đạt")
    return {"ok": True, "message": f"Tự kiểm {len(ups)}/32 việc từ dữ liệu đã đo · {done} đạt — các việc còn lại chị tự đánh dấu"}


def geo_answer(body):
    """Dán câu trả lời của một máy AI → tự nhận diện Rooty có được nhắc tên / trích link, đối thủ nào xuất hiện."""
    b = body or {}
    if b.get("__invalid__"):
        raise StoreError("Dữ liệu gửi lên không phải JSON hợp lệ")
    text = (b.get("text") or "").strip()
    if len(text) < 20:
        raise StoreError("Dán toàn bộ câu trả lời của AI vào ô «Câu trả lời»")
    if not b.get("engine"):
        raise StoreError("Chọn máy AI")
    qs = {r["fields"].get("Mã câu"): r["fields"] for r in STORE.list(_tname("cauhoiai"))}
    qf = qs.get(b.get("code")) or {}
    question = qf.get("Câu hỏi") or (b.get("question") or "").strip()
    if not question:
        raise StoreError("Chọn câu hỏi trong bộ câu hỏi (hoặc gõ câu hỏi)")
    comps = [r["fields"].get("Đối thủ") for r in STORE.list(_tname("doithu")) if r["fields"].get("Đối thủ")]
    comps = list(dict.fromkeys(comps + GEO.DEFAULT_COMPETITORS))
    _, brand = brand_master()
    a = GEO.analyze_answer(text, comps, brand)
    key = b.get("code") or question
    same = [r for r in STORE.list(_tname("aihien"))
            if (r["fields"].get("Mã câu") or r["fields"].get("Câu hỏi")) == key and r["fields"].get("Máy AI") == b["engine"]]
    n = len(same) + 1
    rec = {"Câu hỏi": question, "Mã câu": b.get("code") or "", "Chủ đề": qf.get("Chủ đề") or "", "Máy AI": b["engine"],
           "Phiên bản mô hình": (b.get("model") or "").strip(), "Ngày chạy": now_ms(), "Lần chạy": n, "Câu trả lời": text[:20000],
           "Nhắc tên Rooty": "Có" if a["mention"] else "Không", "Trích link Rooty": "Có" if a["link"] else "Không",
           "URL được trích": "\n".join(a["urls"][:20]), "Đối thủ xuất hiện": ", ".join(a["competitors"]),
           "Thông tin đúng": ("Sai" if a["issues"] else "Đúng") if a["mention"] else "Không nhắc", "Lỗi sai": "\n".join(a["issues"])}
    if a["rank"]:
        rec["Thứ tự Rooty"] = a["rank"]
    STORE.create_many(_tname("aihien"), [rec])
    msg = (f"Lần {n} · {b['engine']}: " + (("✅ có nhắc Rooty" + (f" (thứ {a['rank']} trong các thương hiệu được nêu)" if a["rank"] else ""))
                                           if a["mention"] else "❌ không nhắc Rooty")
           + (" · có trích link rootytrip.com" if a["link"] else "")
           + (f" · đối thủ: {', '.join(a['competitors'][:6])}" if a["competitors"] else "")
           + (" · ⚠ " + "; ".join(a["issues"]) if a["issues"] else "")
           + (f" · chạy thêm {3 - n} lần nữa cho đủ 3 lần/câu/máy" if n < 3 else "")
           + ("" if rec["Phiên bản mô hình"] else " · nhớ ghi phiên bản mô hình"))
    return {"ok": True, "message": msg}


def geo_summary():
    sync_geo()
    items = [r["fields"] for r in STORE.list(_tname("geo"))]
    by_point = {}
    for f in items:
        p = (f.get("Điểm chạm") or "?").split(" · ")[0]
        d = by_point.setdefault(p, {"name": f.get("Điểm chạm"), "total": 0, "done": 0, "bad": 0, "gate": 0, "gateDone": 0})
        d["total"] += 1
        d["done"] += f.get("Trạng thái") in ("Đạt", "Không áp dụng")
        d["bad"] += f.get("Trạng thái") == "Chưa đạt"
        if f.get("Cửa chặn") == "Có":
            d["gate"] += 1
            d["gateDone"] += f.get("Trạng thái") == "Đạt"
    pages = [r["fields"] for r in STORE.list(_tname("trang")) if r["fields"].get("Điểm GEO") is not None]
    scores = [f["Điểm GEO"] for f in pages]
    runs = [r["fields"] for r in STORE.list(_tname("aihien"))]
    return {"points": dict(sorted(by_point.items())), "pages": len(pages), "avg": round(sum(scores) / len(scores)) if scores else None,
            "gatePass": sum(1 for f in pages if f.get("Qua cửa chặn GEO") == "Đạt"),
            "crit": {str(k): v for k, v in sorted(_page_crit([f.get("Chấm GEO") for f in pages]).items())},
            "presence": GEO.presence_summary(runs, len(STORE.list(_tname("cauhoiai"))))}



# ------------------------------------------------------------------ Theo dõi sửa lỗi từng trang (lỗi × URL × trạng thái × thứ hạng trước/sau)
import base64  # noqa: E402

import fixtrack as FX  # noqa: E402
from geo_audit import decode, fetch  # noqa: E402


def _pages_by_path():
    return {FX.norm_path(r["fields"].get("URL") or ""): r["fields"] for r in STORE.list(_tname("trang"))}


def _gsc_snap(p, prefix):
    """Số liệu GSC hiện có của trang → các cột «… trước» / «… sau»."""
    if not p or p.get("GSC lượt nhấp") is None:
        return {}
    return {f"Nhấp {prefix}": p.get("GSC lượt nhấp"), f"Hiển thị {prefix}": p.get("GSC hiển thị"),
            f"Vị trí {prefix}": p.get("GSC vị trí"), f"Kỳ số liệu {prefix}": p.get("Kỳ số liệu") or ""}


def _level(ket_luan):
    k = (ket_luan or "").upper()
    if "NẶNG" in k:
        return "🔴 Cao"
    if "SUY LUẬN" in k or "KHÔNG ĐÚNG" in k:
        return "🟢 Thấp"
    return "🟡 Vừa"


def loi_import(body):
    b = body or {}
    if b.get("__invalid__") or not b.get("b64"):
        raise StoreError("Chọn file .xlsx (Google Sheets → Tệp → Tải xuống → Microsoft Excel)")
    try:
        sheets = FX.read_xlsx(base64.b64decode(b["b64"]))
    except Exception as e:
        raise StoreError(f"Không đọc được file Excel: {e}")
    items, overview = FX.parse_report(sheets)
    if not items:
        raise StoreError("Không thấy tab nào có cột «URL» hoặc «Các URL»")
    batch = (b.get("name") or "báo cáo").rsplit(".", 1)[0]
    return loi_apply(items, overview, batch)


def _cluster_urls(detail):
    m = re.search(r"Các URL:\s*(.+)$", detail or "")
    return {FX.norm_path(x) for x in re.split(r"\s*·\s*", m.group(1)) if x.strip().startswith("/")} if m else set()


def loi_apply(items, overview, batch, close_kinds=None):
    """Nạp danh sách lỗi × trang vào bảng «Sửa lỗi từng trang». close_kinds: loại lỗi được tự đóng khi không còn thấy
    (mặc định: mọi loại có trong đợt này). Cụm «Trùng từ khóa» khớp cụm cũ nếu trùng ≥ 50% URL."""
    tname = _tname("sualoi")
    have = {r["fields"].get("Lỗi trên trang"): r for r in STORE.list(tname)}
    old_clusters = [(k, _cluster_urls(r["fields"].get("Chi tiết lỗi"))) for k, r in have.items() if r["fields"].get("Loại lỗi") == "Trùng từ khóa"]
    for it in items:
        if it["type"] == "Trùng từ khóa":
            mine = _cluster_urls(it["detail"])
            best = max(old_clusters, key=lambda kc: len(kc[1] & mine), default=None)
            if best and mine and len(best[1] & mine) >= 0.5 * min(len(mine), len(best[1])):
                it["url"] = best[0].split(" · ", 1)[1]
    pages = _pages_by_path()
    now = now_ms()
    new, ups, seen = [], {}, set()
    cnt = {"new": 0, "again": 0, "upd": 0, "gone": 0}
    for it in items:
        k = FX.key(it["type"], it["url"])
        if k in seen:
            continue
        seen.add(k)
        ov = overview.get(it["type"], {})
        r = have.get(k)
        if not r:
            rec = {"Lỗi trên trang": k, "Loại lỗi": it["type"], "URL": site_url() + it["url"], "Ngôn ngữ": it["lang"],
                   "Chi tiết lỗi": it["detail"], "Cần sửa gì": FX.fix_hint(it["type"], it["detail"]), "Mô tả loại lỗi": " · ".join(str(x) for x in (it["note"], ov.get("ket_luan") and f"Kết luận: {ov['ket_luan']}") if x),
                   "Mức độ": _level(ov.get("ket_luan")), "Trạng thái": "Mới", "Ngày phát hiện": now, "Đợt quét": batch,
                   "Hiệu quả": "Chờ đo", **_gsc_snap(pages.get(it["url"]), "trước")}
            new.append(rec)
            cnt["new"] += 1
        else:
            f = r["fields"]
            ch = {"Chi tiết lỗi": it["detail"], "Đợt quét": batch}
            # gợi ý tự động chưa ai sửa tay → làm mới theo chi tiết mới
            if not f.get("Cần sửa gì") or f.get("Cần sửa gì") == FX.fix_hint(it["type"], f.get("Chi tiết lỗi") or ""):
                ch["Cần sửa gì"] = FX.fix_hint(it["type"], it["detail"])
            if f.get("Trạng thái") in FX.FIXED:
                ch.update({"Trạng thái": "Tái phát", "Kiểm lại": f"{time.strftime('%d/%m/%Y')} · đợt «{batch}» vẫn thấy lỗi này"})
                cnt["again"] += 1
            else:
                cnt["upd"] += 1
            ups[r["record_id"]] = ch
    kinds = set(close_kinds) if close_kinds is not None else {it["type"] for it in items}
    for k, r in have.items():
        f = r["fields"]
        if f.get("Loại lỗi") in kinds and k not in seen and f.get("Trạng thái") in FX.OPEN:
            ups[r["record_id"]] = {"Trạng thái": "Hết lỗi (quét lại)", "Ngày sửa": f.get("Ngày sửa") or now,
                                   "Kiểm lại": f"{time.strftime('%d/%m/%Y')} · đợt «{batch}» không còn thấy lỗi này",
                                   **({} if f.get("Nhấp trước") is not None else _gsc_snap(pages.get(FX.norm_path(f.get("URL") or "")), "trước"))}
            cnt["gone"] += 1
    if new:
        STORE.create_many(tname, new)
    if ups:
        STORE.update_many(tname, ups)
    # một dòng tổng cho mỗi loại lỗi ở bảng Audit (danh sách lỗi cấp site)
    aud = {r["fields"].get("Vấn đề"): r for r in STORE.list(_tname("audit"))}
    a_new, a_up = [], {}
    by_kind = {}
    for it in items:
        by_kind.setdefault(it["type"], set()).add(it["url"])
    for kind, urls in by_kind.items():
        ov = overview.get(kind, {})
        name = f"{kind} — {ov['ten']}" if ov.get("ten") else kind
        rec = {"Số trang": len(urls), "Nguồn": batch, "URL ví dụ": "\n".join(sorted(urls)[:5]),
               "Cách sửa": " · ".join(str(x) for x in (ov.get("ket_luan") and f"Kết luận: {ov['ket_luan']}", ov.get("cach_do")) if x)
               + " · Theo dõi từng trang ở mục «Sửa lỗi từng trang»"}
        if name in aud:
            a_up[aud[name]["record_id"]] = rec
        else:
            a_new.append({"Vấn đề": name, "Hạng mục": "Onsite", "Mức độ": _level(ov.get("ket_luan")), "Trạng thái": "Mới", **rec})
    if a_new:
        STORE.create_many(_tname("audit"), a_new)
    if a_up:
        STORE.update_many(_tname("audit"), a_up)
    msg = (f"Đợt «{batch}»: {len(items)} lỗi × trang ({len(by_kind)} loại) · thêm mới {cnt['new']} · cập nhật {cnt['upd']}"
           + (f" · tái phát {cnt['again']}" if cnt["again"] else "") + (f" · hết lỗi {cnt['gone']}" if cnt["gone"] else "")
           + ("" if any(p.get("GSC lượt nhấp") is not None for p in pages.values()) else " · chưa có số liệu GSC theo trang (nhập ở B10) nên chưa ghi được thứ hạng «trước»"))
    log(msg)
    return {"ok": True, "message": msg}


def loi_fill_hints():
    """Điền «Cần sửa gì» cho dòng lỗi còn trống (dòng nhập trước khi có cột này)."""
    ups = {r["record_id"]: {"Cần sửa gì": FX.fix_hint(r["fields"].get("Loại lỗi") or "", r["fields"].get("Chi tiết lỗi") or "")}
           for r in STORE.list(_tname("sualoi")) if not r["fields"].get("Cần sửa gì")}
    if ups:
        STORE.update_many(_tname("sualoi"), ups)
    return len(ups)


def loi_on_update(rid, f):
    """Đổi trạng thái sang «Đã sửa» → ghi ngày sửa + chụp số liệu GSC lúc sửa làm mốc «trước»."""
    if f.get("Trạng thái") not in FX.FIXED:
        return f
    cur = next((r["fields"] for r in STORE.list(_tname("sualoi")) if r["record_id"] == rid), {})
    if cur.get("Trạng thái") in FX.FIXED:
        return f
    out = dict(f)
    out.setdefault("Ngày sửa", now_ms())
    snap = _gsc_snap(_pages_by_path().get(FX.norm_path(cur.get("URL") or "")), "trước")
    if snap:
        out.update(snap)
    out.setdefault("Hiệu quả", "Chờ đo")
    return out


def loi_recheck(body):
    """Mở lại từng trang để kiểm lỗi còn hay hết (máy kiểm được: link tự thân, đổi năm giả)."""
    ids = set((body or {}).get("ids") or [])
    only_fixed = bool((body or {}).get("onlyFixed"))

    def job(say):
        rows = [r for r in STORE.list(_tname("sualoi")) if (r["record_id"] in ids) or (not ids and (
            r["fields"].get("Trạng thái") in ({"Đã sửa"} if only_fixed else FX.OPEN | {"Đã sửa"})))]
        pages = _pages_by_path()
        now = now_ms()
        ok = still = manual = 0
        ups = {}
        for i, r in enumerate(rows, 1):
            f = r["fields"]
            say(f"[{i}/{len(rows)}] {f.get('URL')}")
            try:
                bad, detail = FX.recheck(f.get("Loại lỗi") or "", f.get("URL") or "", lambda u: fetch(u, follow=False), decode, f.get("Chi tiết lỗi") or "")
            except Exception as e:
                bad, detail = None, f"lỗi khi tải: {e}"
            ch = {"Kiểm lại": f"{time.strftime('%d/%m/%Y')} · {detail}", "Lần kiểm lại": now}
            if bad is None:
                manual += 1
                continue
            if bad:
                still += 1
                if f.get("Trạng thái") == "Đã sửa":
                    ch["Trạng thái"] = "Sửa chưa đạt"
            else:
                ok += 1
                if f.get("Trạng thái") not in FX.FIXED:
                    ch.update({"Trạng thái": "Đã sửa", "Ngày sửa": f.get("Ngày sửa") or now, "Hiệu quả": f.get("Hiệu quả") or "Chờ đo"})
                    ch.update(_gsc_snap(pages.get(FX.norm_path(f.get("URL") or "")), "trước"))
            ups[r["record_id"]] = ch
        if ups:
            STORE.update_many(_tname("sualoi"), ups)
        return f"Kiểm lại {ok + still} trang: {ok} đã hết lỗi · {still} còn lỗi" + (f" · {manual} dòng loại lỗi phải kiểm tay (bỏ qua)" if manual else "")
    return run_job("loicheck", job)


def loi_measure():
    """Đo hiệu quả: trang đã sửa ≥ 28 ngày + có số liệu GSC kỳ mới hơn kỳ «trước» → ghi «sau» và Tốt lên / Không đổi / Giảm.
    Trang chưa sửa cũng được ghi «sau» để làm nhóm đối chứng."""
    pages = _pages_by_path()
    now = now_ms()
    ups, cnt = {}, {}
    for r in STORE.list(_tname("sualoi")):
        f = r["fields"]
        p = pages.get(FX.norm_path(f.get("URL") or ""))
        if not p or p.get("GSC lượt nhấp") is None:
            continue
        ch = {}
        if f.get("Nhấp trước") is None:
            ch = _gsc_snap(p, "trước")
        elif (p.get("Kỳ số liệu") or "") != (f.get("Kỳ số liệu trước") or ""):
            fixed = f.get("Trạng thái") in FX.FIXED
            if fixed and (now - (f.get("Ngày sửa") or now)) / 864e5 < 28:
                continue
            ch = _gsc_snap(p, "sau")
            if fixed:
                b0, a0 = f.get("Nhấp trước") or 0, p.get("GSC lượt nhấp") or 0
                pb, pa = f.get("Vị trí trước"), p.get("GSC vị trí")
                up = a0 > b0 * 1.1 or (pb and pa and pa <= pb - 1 and a0 >= b0 * 0.9)
                down = a0 < b0 * 0.9 or (pb and pa and pa >= pb + 1 and a0 <= b0 * 1.1)
                ch["Hiệu quả"] = "Tốt lên" if up else ("Giảm" if down else "Không đổi")
                cnt[ch["Hiệu quả"]] = cnt.get(ch["Hiệu quả"], 0) + 1
            else:
                cnt["đối chứng"] = cnt.get("đối chứng", 0) + 1
        if ch:
            ups[r["record_id"]] = ch
            if "Nhấp trước" in ch:
                cnt["ghi mốc trước"] = cnt.get("ghi mốc trước", 0) + 1
    if ups:
        STORE.update_many(_tname("sualoi"), ups)
    return {"ok": True, "message": ("Đo lại: " + " · ".join(f"{k} {v}" for k, v in cnt.items())) if cnt else
            "Chưa có dòng nào đủ điều kiện đo — cần nhập GSC Trang ở B10 (mỗi kỳ một lần), trang đã sửa ≥ 28 ngày"}


def loi_summary():
    rows = [r["fields"] for r in STORE.list(_tname("sualoi"))]
    out = {}

    def delta(f):
        b, a = f.get("Nhấp trước"), f.get("Nhấp sau")
        pb, pa = f.get("Vị trí trước"), f.get("Vị trí sau")
        return (a - b if a is not None and b is not None else None, pa - pb if pa and pb else None)
    for f in rows:
        k = f.get("Loại lỗi") or "?"
        d = out.setdefault(k, {"total": 0, "open": 0, "fixed": 0, "skip": 0, "status": {}, "effect": {},
                               "fixClicks": [], "fixPos": [], "ctlClicks": [], "ctlPos": []})
        st = f.get("Trạng thái") or "Mới"
        d["total"] += 1
        d["status"][st] = d["status"].get(st, 0) + 1
        d["open"] += st in FX.OPEN
        d["fixed"] += st in FX.FIXED
        d["skip"] += st in ("Không phải lỗi", "Bỏ qua")
        if f.get("Hiệu quả") and f.get("Hiệu quả") != "Chờ đo":
            d["effect"][f["Hiệu quả"]] = d["effect"].get(f["Hiệu quả"], 0) + 1
        dc, dp = delta(f)
        grp = "fix" if st in FX.FIXED else ("ctl" if st in FX.OPEN else None)
        if grp and dc is not None:
            d[grp + "Clicks"].append(dc)
        if grp and dp is not None:
            d[grp + "Pos"].append(dp)
    med = lambda xs: sorted(xs)[len(xs) // 2] if xs else None
    for d in out.values():
        for k in ("fixClicks", "fixPos", "ctlClicks", "ctlPos"):
            xs = d.pop(k)
            d[k] = {"n": len(xs), "median": med(xs)}
    return {"kinds": out, "total": len(rows)}



# ------------------------------------------------------------------ Thuật toán Google (nguồn chính thức) + chính sách spam
import algo as AL  # noqa: E402

ALGO_STATE = ROOT / "reports" / "du-lieu" / "algo-last.json"


def _iso_ms(d):
    try:
        return int(time.mktime(time.strptime(d, "%Y-%m-%d")) * 1000) if d else None
    except ValueError:
        return None


def algo_refresh():
    """Lấy các đợt cập nhật từ Google Search Status Dashboard + tin blog Search Central, đo ảnh hưởng bằng GSC theo ngày."""
    try:
        ups = AL.fetch_updates()
    except Exception as e:
        raise StoreError(f"Không đọc được Google Search Status Dashboard: {e}")
    try:
        posts = AL.fetch_blog()
    except Exception:
        posts = []
    daily = json.loads(DAILY_FILE.read_text(encoding="utf-8")) if DAILY_FILE.exists() else []
    t = _tname("thuattoan")
    have = {r["fields"].get("Tên đợt"): r for r in STORE.list(t)}
    new, upd, fresh = [], {}, []
    for u in ups:
        im = AL.impact(daily, u["begin"], u["end"])
        rec = {"Loại": u["kind"], "Bắt đầu": _iso_ms(u["begin"]), "Kết thúc": _iso_ms(u["end"]),
               "Trạng thái": "Đã xong" if u["done"] else "Đang triển khai", "Nguồn": u["url"], "Thông báo của Google": u["note"],
               "Ảnh hưởng tới Rooty": im["status"], "Chi tiết ảnh hưởng": im["text"]}
        if im.get("clicks") is not None:
            rec.update({"Lượt nhấp/ngày trước": im["before"], "Lượt nhấp/ngày sau": im["after"], "Thay đổi lượt nhấp %": im["clicks"],
                        "Thay đổi hiển thị %": im["impr"]})
        r = have.get(u["name"])
        if not r:
            new.append({"Tên đợt": u["name"], **rec, "Việc cần làm": AL.TODO.get(u["kind"], AL.TODO["Khác"]), "Đã review": "Chưa"})
            fresh.append(u["name"])
        else:
            ch = {k: v for k, v in rec.items() if r["fields"].get(k) != v}
            if ch:
                upd[r["record_id"]] = ch
    if new:
        STORE.create_many(t, new)
    if upd:
        STORE.update_many(t, upd)
    tb = _tname("tinseo")
    have_p = {r["fields"].get("Tiêu đề") for r in STORE.list(tb)}
    new_p = [{"Tiêu đề": p["title"], "Ngày": _iso_ms(p["date"]), "Link": p["link"], "Tóm tắt": p["desc"],
              "Mức liên quan": p["rel"], "Đã đọc": "Chưa"} for p in posts if p["title"] not in have_p]
    if new_p:
        STORE.create_many(tb, new_p)
    ALGO_STATE.parent.mkdir(parents=True, exist_ok=True)
    ALGO_STATE.write_text(json.dumps({"at": now_ms(), "updates": len(ups), "posts": len(posts)}), encoding="utf-8")
    active = [u["name"] for u in ups if not u["done"]]
    msg = (f"Google Search Status: {len(ups)} đợt · mới {len(new)}" + (f" ({', '.join(fresh[:3])})" if fresh else "")
           + (f" · ⚠ ĐANG TRIỂN KHAI: {', '.join(active)}" if active else " · không có đợt nào đang triển khai")
           + f" · blog Search Central: {len(new_p)} tin mới"
           + ("" if daily else " · chưa có GSC theo ngày nên chưa đo được ảnh hưởng (nhập file Ngày ở B10)"))
    log(msg)
    return {"ok": True, "message": msg}


def algo_auto_refresh():
    """Tự lấy lại nếu lần trước đã quá 24 giờ (chạy nền khi mở app)."""
    try:
        last = json.loads(ALGO_STATE.read_text(encoding="utf-8")).get("at", 0) if ALGO_STATE.exists() else 0
        if now_ms() - last > 24 * 3600 * 1000:
            algo_refresh()
    except Exception as e:
        print("Bỏ qua tự cập nhật thuật toán Google:", e)


def policy_check():
    """Chấm rủi ro theo chính sách spam của Google từ dữ liệu đã có trong app; mục không đo được giữ nguyên để kiểm tay."""
    t = _tname("chinhsach")
    if not STORE.list(t):
        STORE.create_many(t, AL.policy_seed())
    rows = {r["fields"].get("Mã"): r for r in STORE.list(t)}
    loi = [r["fields"] for r in STORE.list(_tname("sualoi"))]
    open_ = lambda kind: [f for f in loi if f.get("Loại lỗi") == kind and f.get("Trạng thái") in FX.OPEN]
    res = {}
    if loi:
        x = open_("Thiếu trải nghiệm")
        res["scaled-content"] = ("Có rủi ro" if x else "An toàn",
                                 f"{len(x)} bài nghi thiếu trải nghiệm thật còn mở (B5 · Sửa lỗi từng trang)" if x else "Không còn bài nghi thiếu trải nghiệm")
        x = open_("Trùng từ khóa")
        res["doorways"] = ("Có rủi ro" if x else "An toàn", f"{len(x)} cụm bài trùng từ khoá chưa xử lý" if x else "Không còn cụm trùng")
        x = open_("Đổi năm giả")
        res["fake-freshness"] = ("Có rủi ro" if x else "An toàn", f"{len(x)} bài chỉ đổi năm trên tiêu đề còn chưa sửa" if x else "Đã sửa hết")
        x = open_("Thương mại")
        if x:
            res["thin-affiliate-pages"] = ("Chưa kiểm", f"{len(x)} bài mật độ link đặt tour/CTA cao — chỉ là nghi vấn (báo cáo kiểm chứng: phần lớn không đúng), đọc lại rồi chọn trạng thái")
    geo = [r["fields"].get("Chấm GEO") or "" for r in STORE.list(_tname("trang")) if r["fields"].get("Chấm GEO")]
    if geo:
        fail20 = sum(1 for g in geo if re.search(r"^❌ #20", g, re.M))
        cur = res.get("scaled-content")
        extra = f" · GEO #20: {fail20}/{len(geo)} bài đã chấm chưa có thông tin riêng Rooty"
        res["scaled-content"] = (("Có rủi ro" if (fail20 / len(geo) > 0.3 or (cur and cur[0] == "Có rủi ro")) else (cur[0] if cur else "An toàn")),
                                 (cur[1] if cur else "") + extra)
    links = [r["fields"] for r in STORE.list(_tname("lienket")) if r["fields"].get("Loại") != "Nội bộ"]
    if links:
        paid = [f for f in links if (f.get("Chi phí") or 0) > 0 and f.get("Thuộc tính") == "Dofollow"]
        res["link-spam"] = ("Có rủi ro" if paid else "An toàn",
                            f"{len(paid)} backlink trả tiền đang dofollow (phải gắn rel=sponsored/nofollow)" if paid else f"{len(links)} backlink, không có link trả tiền dofollow")
    now = now_ms()
    ups = {rows[c]["record_id"]: {"Trạng thái": st, "Kết quả tự kiểm": txt, "Lần kiểm": now} for c, (st, txt) in res.items() if c in rows}
    if ups:
        STORE.update_many(t, ups)
    bad = sum(1 for st, _ in res.values() if st in ("Có rủi ro", "Vi phạm — cần sửa"))
    return {"ok": True, "message": f"Tự kiểm {len(ups)} chính sách từ dữ liệu app: {bad} có rủi ro/vi phạm · {len(rows) - len(ups)} mục kiểm tay"}


def algo_summary():
    last = json.loads(ALGO_STATE.read_text(encoding="utf-8")) if ALGO_STATE.exists() else {}
    ups = [r["fields"] for r in STORE.list(_tname("thuattoan"))]
    return {"last": last.get("at"), "active": [u["Tên đợt"] for u in ups if u.get("Trạng thái") == "Đang triển khai"],
            "unreviewed": sum(1 for u in ups if u.get("Đã review") != "Đã" and u.get("Loại") in ("Core update", "Spam update")),
            "unread": sum(1 for r in STORE.list(_tname("tinseo")) if r["fields"].get("Đã đọc") != "Đã" and r["fields"].get("Mức liên quan") == "Cao"),
            "hasDaily": DAILY_FILE.exists()}



# ------------------------------------------------------------------ Kiểm nhiều website / nhiều trang cùng lúc
from concurrent.futures import ThreadPoolExecutor  # noqa: E402

TECH_NAMES = {c: m for c, m, *_ in TB.TECH_CHECKLIST}


def _norm_line(s):
    s = (s or "").strip().strip(",;")
    if not s or s.startswith("#"):
        return None
    if not re.match(r"^https?://", s, re.I):
        s = "https://" + s
    p = urllib.parse.urlsplit(s)
    if not p.netloc or "." not in p.netloc:
        return None
    path = p.path if p.path not in ("", "/") else ""
    return f"{p.scheme.lower()}://{p.netloc.lower()}{path}" + (f"?{p.query}" if p.query and path else "")


def _check_one(target):
    """Cả site (chỉ tên miền) → 34 mục kỹ thuật/UX/onsite/entity như B5. Một trang (có đường dẫn) → chấm GEO + onpage."""
    path = urllib.parse.urlsplit(target).path
    if not path or path == "/":
        R = techcheck.check_site(target, ENV.get("PAGESPEED_API_KEY"))
        R.update(techcheck.check_extra(target, [], ENV.get("PAGESPEED_API_KEY")))
        ok = [c for c, v in R.items() if v[0] == "Đạt"]
        bad = [c for c, v in R.items() if v[0] == "Chưa đạt"]
        skip = [c for c, v in R.items() if v[0] not in ("Đạt", "Chưa đạt")]
        score = round(len(ok) / max(len(ok) + len(bad), 1) * 100)
        lv = {c: lvl for c, _, _, _, lvl, *_ in TB.TECH_CHECKLIST}
        bad.sort(key=lambda c: {"🔴 Cao": 0, "🟡 Vừa": 1}.get(lv.get(c), 2))
        fix = "\n".join(f"{lv.get(c, '')} {c} {TECH_NAMES.get(c, c)} — {str(R[c][1])[:160]}" for c in bad)
        detail = "\n".join(f"{'✅' if v[0] == 'Đạt' else '❌' if v[0] == 'Chưa đạt' else '·'} {c} {TECH_NAMES.get(c, c)} — {str(v[1])[:200]}"
                           for c, v in sorted(R.items()))
        return {"Loại kiểm": "Toàn site", "Điểm %": score, "Đạt": len(ok), "Chưa đạt": len(bad), "Chưa kiểm": len(skip),
                "Lỗi cần sửa": fix or "Không có lỗi trong các mục kiểm tự động", "Chi tiết": detail}
    res = GEO.check(target, "", "")
    if res.get("error"):
        raise StoreError(res["error"])
    op = OP.deep(target, None)
    bad = [c for c in res["checks"] if c["ok"] is False]
    fix = "\n".join(f"{'🔒' if c['gate'] else '•'} GEO #{c['no']} {c['name'][:90]} — {c['detail'][:140]}" for c in bad)
    if not op.get("error"):
        fix += ("\n" if fix else "") + "\n".join("• Onpage: " + l.strip()[2:] for l in (op.get("detail") or "").splitlines() if l.strip().startswith("❌"))[:1500]
    n_ok = res["passed"] + (sum(1 for l in (op.get("detail") or "").splitlines() if l.strip().startswith("✅")) if not op.get("error") else 0)
    n_bad = len(bad) + (sum(1 for l in (op.get("detail") or "").splitlines() if l.strip().startswith("❌")) if not op.get("error") else 0)
    return {"Loại kiểm": "Một trang", "Điểm %": round(n_ok / max(n_ok + n_bad, 1) * 100), "Đạt": n_ok, "Chưa đạt": n_bad,
            "Chưa kiểm": sum(1 for c in res["checks"] if c["ok"] is None),
            "Lỗi cần sửa": fix or "Không có lỗi trong các mục kiểm tự động",
            "Chi tiết": GEO.render(res) + ("\n\n— Onpage —\n" + op["detail"] if not op.get("error") else "")}


def multi_check(body):
    b = body or {}
    if b.get("__invalid__"):
        raise StoreError("Dữ liệu gửi lên không phải JSON hợp lệ")
    t = _tname("kiemweb")
    have = {r["fields"].get("Website"): r for r in STORE.list(t)}
    ids = set(b.get("ids") or [])
    targets = []
    for line in re.split(r"[\s,;]+", b.get("text") or ""):
        x = _norm_line(line)
        if x and x not in targets:
            targets.append(x)
    targets += [r["fields"]["Website"] for r in have.values() if r["record_id"] in ids and r["fields"]["Website"] not in targets]
    if not targets:
        raise StoreError("Dán danh sách website (mỗi dòng một tên miền, VD rootytrip.com) hoặc link từng trang")
    if len(targets) > 50:
        raise StoreError(f"{len(targets)} địa chỉ — tối đa 50 mỗi lần")
    group = (b.get("group") or "").strip()
    new = [{"Website": x, "Nhóm": group, "Trạng thái": "Đang chờ"} for x in targets if x not in have]
    if new:
        STORE.create_many(t, new)
    have = {r["fields"].get("Website"): r for r in STORE.list(t)}
    STORE.update_many(t, {have[x]["record_id"]: {"Trạng thái": "Đang chờ", **({"Nhóm": group} if group else {})} for x in targets})

    def job(say):
        done = [0]
        errs = []

        def one(x):
            rid = have[x]["record_id"]
            STORE.update(t, rid, {"Trạng thái": "Đang kiểm"})
            try:
                ch = _check_one(x)
                ch.update({"Trạng thái": "Xong", "Lần kiểm": now_ms()})
            except Exception as e:
                ch = {"Trạng thái": "Lỗi", "Lần kiểm": now_ms(), "Lỗi cần sửa": f"Không kiểm được: {e}"}
                errs.append(x)
            STORE.update(t, rid, ch)
            done[0] += 1
            say(f"[{done[0]}/{len(targets)}] xong {x}" + (f" · {ch.get('Điểm %')}%" if ch.get("Điểm %") is not None else " · lỗi"))
        with ThreadPoolExecutor(max_workers=4) as ex:
            list(ex.map(one, targets))
        return f"Kiểm xong {len(targets) - len(errs)}/{len(targets)} địa chỉ" + (f" · không kiểm được: {', '.join(errs[:5])}" if errs else "")
    return run_job("kiemweb", job)



# ------------------------------------------------------------------ Chẩn đoán rớt top (1 câu → 4 bước)
import blogscan as BS  # noqa: E402
import chandoan as CD  # noqa: E402

CD_LAST = ROOT / "reports" / "du-lieu" / "chandoan-last.json"


def chandoan_run(body):
    b = body or {}
    if b.get("__invalid__"):
        raise StoreError("Dữ liệu gửi lên không phải JSON hợp lệ")
    site = (_norm_line(b.get("site") or "") or site_url()).rstrip("/")
    own = urllib.parse.urlsplit(site).netloc.replace("www.", "") == urllib.parse.urlsplit(site_url()).netloc.replace("www.", "")

    def job(say):
        say("① Đọc số liệu GSC theo ngày…")
        daily = json.loads(DAILY_FILE.read_text(encoding="utf-8")) if (own and DAILY_FILE.exists()) else []
        tr = CD.trend(daily)
        say("② Lấy các đợt cập nhật thuật toán từ Google Search Status…")
        try:
            updates = AL.fetch_updates()
        except Exception:
            updates = [{"name": f.get("Tên đợt"), "kind": f.get("Loại"), "begin": time.strftime("%Y-%m-%d", time.localtime(f["Bắt đầu"] / 1000)) if f.get("Bắt đầu") else "",
                        "end": time.strftime("%Y-%m-%d", time.localtime(f["Kết thúc"] / 1000)) if f.get("Kết thúc") else ""}
                       for f in (r["fields"] for r in STORE.list(_tname("thuattoan")))]
        hits = CD.overlap(tr.get("start"), updates)
        say("③ Quét toàn bộ bài blog…")
        prods = [FX.norm_path(r["fields"].get("URL") or "") for r in STORE.list(_tname("trang"))
                 if r["fields"].get("Loại trang") in ("Trang tour/sản phẩm", "Danh mục")] if own else []
        items, overview, st = BS.scan(site, prods, say=say)
        if not st["posts"]:
            raise StoreError(f"Không đọc được bài viết qua {site}/wp-json/wp/v2/posts (site không phải WordPress hoặc đã tắt REST API)")
        conf = {k: v[0] for k, v in BS.KINDS.items()}
        loi_msg = ""
        geo = None
        policy = []
        if own:
            say("Nạp kết quả vào B5 · Sửa lỗi từng trang…")
            loi_msg = loi_apply(items, overview, f"Quét tự động {time.strftime('%d/%m/%Y')}",
                                close_kinds={k for k, v in BS.KINDS.items() if v[0] == "ĐÃ KIỂM" and k not in ("Đa ngôn ngữ", "Tác giả")})["message"]
            policy_check()
            policy = [(r["fields"].get("Chính sách"), r["fields"].get("Trạng thái")) for r in STORE.list(_tname("chinhsach"))
                      if r["fields"].get("Trạng thái") in ("Có rủi ro", "Vi phạm — cần sửa")]
            pages = [r["fields"] for r in STORE.list(_tname("trang")) if r["fields"].get("Điểm GEO") is not None]
            if pages:
                crit = _page_crit([f.get("Chấm GEO") for f in pages])
                weak = sorted(crit.items(), key=lambda kv: kv[1][0] / kv[1][1])[:3]
                geo = {"pages": len(pages), "avg": round(sum(f["Điểm GEO"] for f in pages) / len(pages)),
                       "gate": sum(1 for f in pages if f.get("Qua cửa chặn GEO") == "Đạt"),
                       "weak": ", ".join(f"#{n} ({a}/{t} đạt)" for n, (a, t) in weak)}
        ranked = CD.rank(st["counts"], conf, hits)
        md = CD.report(site, tr, updates, hits, st, conf, ranked, geo, policy)
        host = urllib.parse.urlsplit(site).netloc.replace("www.", "")
        out = ROOT / "reports" / f"chan-doan-rot-top-{host}-{time.strftime('%Y-%m-%d')}.md"
        out.write_text(md, encoding="utf-8")
        CD_LAST.parent.mkdir(parents=True, exist_ok=True)
        CD_LAST.write_text(json.dumps({"md": md, "at": now_ms(), "site": site, "file": str(out.relative_to(ROOT)), "counts": st["counts"]},
                                      ensure_ascii=False), encoding="utf-8")
        top = ", ".join(f"{r['kind']} {r['count']}" for r in ranked[:3])
        return (f"Chẩn đoán xong {site}: {st['posts']} bài · " + ("RỚT từ " + tr["start"] if tr.get("drop") else ("chưa có GSC" if not tr["ok"] else "không thấy rớt mạnh"))
                + (f" · trùng {', '.join(u['name'] for u in hits)}" if hits else "") + f" · ưu tiên: {top}"
                + (f" · {loi_msg}" if loi_msg else "") + f" · báo cáo: {out.relative_to(ROOT)}")
    return run_job("chandoan", job)


def chandoan_last():
    return json.loads(CD_LAST.read_text(encoding="utf-8")) if CD_LAST.exists() else {}



# ------------------------------------------------------------------ Giá & dữ kiện (giá gốc + lịch sử đổi giá + dò bài ghi giá cũ)
import factbook as FB  # noqa: E402


def _hist_line(old, new):
    return f"{time.strftime('%d/%m/%Y')}: {old or '—'} → {new}"


def gia_on_update(rid, f):
    """Đổi «Giá trị» → lưu giá cũ + thêm dòng lịch sử + nhắc dò lại bài."""
    if "Giá trị" not in f:
        return f
    cur = next((r["fields"] for r in STORE.list(_tname("giadukien")) if r["record_id"] == rid), {})
    old = (cur.get("Giá trị") or "").strip()
    new = str(f.get("Giá trị") or "").strip()
    if not old or old == new:
        return f
    out = dict(f)
    out["Giá cũ"] = old
    out["Lịch sử"] = ((cur.get("Lịch sử") or "") + "\n" + _hist_line(old, new)).strip()
    out.setdefault("Ngày kiểm", now_ms())
    out["Trạng thái"] = "Đã đổi — dò lại bài"
    return out


def gia_from_site():
    """Lấy giá từ trang sản phẩm của chính Rooty (schema Offer). Giá khác lần trước → ghi lịch sử đổi giá."""
    urls = [r["fields"]["URL"] for r in STORE.list(_tname("trang")) if r["fields"].get("Loại trang") == "Trang tour/sản phẩm" and r["fields"].get("URL")]
    if not urls:
        raise StoreError("Chưa có trang tour/sản phẩm trong bảng Trang đích — chạy crawl ở tab B5 trước")

    def job(say):
        t = _tname("giadukien")
        have = {(r["fields"].get("Nguồn") or "").rstrip("/"): r for r in STORE.list(t)}
        found = []
        with ThreadPoolExecutor(max_workers=6) as ex:
            for i, res in enumerate(ex.map(lambda u: FB.product_price(u, fetch, decode), urls), 1):
                if i % 10 == 0:
                    say(f"Đọc giá trang sản phẩm {i}/{len(urls)}")
                if res:
                    found.append(res)
        now = now_ms()
        new, ups, changed = [], {}, []
        for x in found:
            val = FB.fmt(x["price"])
            r = have.get(x["url"].rstrip("/"))
            if not r:
                new.append({"Dữ kiện": x["name"] or x["url"], "Loại": "Giá tour/combo/vé", "Sản phẩm / địa điểm": x["name"], "Giá trị": val,
                            "Nguồn": x["url"], "Nguồn từ": "Trang sản phẩm Rooty (schema Offer)", "Ngày kiểm": now, "Kiểm lại sau (ngày)": 30,
                            "Từ khoá tìm trong bài": FB.default_phrases(x["name"], x["url"]), "Trạng thái": "Đúng",
                            "Lịch sử": _hist_line("", val)})
            else:
                f = r["fields"]
                ch = {"Ngày kiểm": now}
                if FB.to_int(f.get("Giá trị")) != x["price"]:
                    ch.update({"Giá cũ": f.get("Giá trị"), "Giá trị": val, "Trạng thái": "Đã đổi — dò lại bài",
                               "Lịch sử": ((f.get("Lịch sử") or "") + "\n" + _hist_line(f.get("Giá trị"), val)).strip()})
                    changed.append(f"{f.get('Dữ kiện')}: {f.get('Giá trị')} → {val}")
                ups[r["record_id"]] = ch
        if new:
            STORE.create_many(t, new)
        if ups:
            STORE.update_many(t, ups)
        msg = f"Đọc {len(found)}/{len(urls)} trang sản phẩm có giá · thêm {len(new)} dữ kiện · " + (
            f"ĐỔI GIÁ {len(changed)}: " + "; ".join(changed[:5]) if changed else "không có giá nào đổi")
        log(msg)
        return msg
    return run_job("giasite", job)


def gia_usage(body):
    """Dò toàn bộ bài blog: bài nào nhắc dữ kiện này kèm giá, giá đó có khớp giá hiện tại không. Bài ghi khác → việc «Giá cũ» ở B5."""
    ids = set((body or {}).get("ids") or [])

    def job(say):
        t = _tname("giadukien")
        facts = [r for r in STORE.list(t) if (not ids or r["record_id"] in ids) and r["fields"].get("Trạng thái") != "Ngừng bán"]
        if not facts:
            return "Chưa có dữ kiện nào — bấm «Lấy giá từ trang sản phẩm» hoặc «+ Thêm»"
        say("Đọc toàn bộ bài blog…")
        posts = BS.fetch_posts(site_url(), say)
        for p in posts:
            p["text"] = BS.text_of(p["html"])
        now = now_ms()
        ups, items, total_wrong = {}, [], 0
        for i, r in enumerate(facts, 1):
            f = r["fields"]
            say(f"[{i}/{len(facts)}] dò «{(f.get('Dữ kiện') or '')[:50]}»")
            rows, n_wrong = FB.find_usage(f, posts)
            total_wrong += n_wrong
            lines = [f"{'✅' if x['ok'] else '❌'} {x['url']} — ghi «{x['written']}» — «{x['sentence']}»" for x in rows]
            ch = {"Bài đang dùng": "\n".join(lines[:60]) or "Không bài nào nhắc dữ kiện này kèm giá",
                  "Số bài ghi khác giá": n_wrong, "Lần dò bài": now}
            if f.get("Trạng thái") == "Đã đổi — dò lại bài":
                ch["Trạng thái"] = "Có bài cần sửa" if n_wrong else "Đúng"
            elif n_wrong:
                ch["Trạng thái"] = "Có bài cần sửa"
            ups[r["record_id"]] = ch
            seen = set()
            for x in rows:
                if x["ok"] or x["url"] in seen:
                    continue
                seen.add(x["url"])
                items.append({"type": "Giá cũ", "url": x["url"], "lang": "VI",
                              "detail": f"Dữ kiện: {f.get('Dữ kiện')} · Giá hiện tại: {f.get('Giá trị')} · Bài đang ghi: {x['written']} · "
                                        f"Câu: {x['sentence']} · Nguồn giá: {f.get('Nguồn') or '—'} · Kiểm ngày: {time.strftime('%d/%m/%Y', time.localtime((f.get('Ngày kiểm') or now) / 1000))}",
                              "note": "Bài ghi giá khác giá hiện tại trong bảng Giá & dữ kiện (có thể là giá cũ, hoặc giá gói/đối tượng khác — người xem lại)."})
        if ups:
            STORE.update_many(t, ups)
        merged = {}
        for it in items:   # một bài nhiều dữ kiện sai → gộp một dòng
            m = merged.setdefault(it["url"], dict(it))
            if m is not it and it["detail"] not in m["detail"]:
                m["detail"] += " ‖ " + it["detail"]
        items = list(merged.values())
        msg = f"Dò {len(posts)} bài cho {len(facts)} dữ kiện: {total_wrong} lượt bài ghi khác giá hiện tại"
        if items or not ids:
            msg += " · " + loi_apply(items, {"Giá cũ": {"ket_luan": "ĐÃ KIỂM"}}, f"Dò giá {time.strftime('%d/%m/%Y')}",
                                     close_kinds={"Giá cũ"} if not ids else set())["message"]
        log(msg)
        return msg
    return run_job("giausage", job)



# ------------------------------------------------------------------ Kế hoạch link cho một trang đích (silo kim tự tháp)
import linkplan as LP  # noqa: E402

LP_LAST = ROOT / "reports" / "du-lieu" / "linkplan-last.json"


def _vi_texts(say):
    out, page = {}, 1
    while True:
        try:
            body, hd = BS._get(f"{site_url()}/wp-json/wp/v2/posts?per_page=100&page={page}&status=publish&_fields=link,content")
            data = json.loads(body)
        except Exception:
            break
        if not data:
            break
        for p in data:
            out[p["link"].rstrip("/") + "/"] = BS.text_of(p["content"]["rendered"])
        say(f"Đọc bài tiếng Việt: trang {page}")
        if page >= int(hd.get("X-WP-TotalPages") or hd.get("x-wp-totalpages") or 1):
            break
        page += 1
    return out


def linkplan_run(body):
    b = body or {}
    url = (b.get("url") or "").strip()
    kw = (b.get("keyword") or "").strip()
    if not url.startswith("http") or not kw:
        raise StoreError("Chọn trang đích và nhập từ khoá cần lên top")
    extra = [x.strip() for x in re.split(r"[,\n;]", b.get("terms") or "") if x.strip()]

    def job(say):
        edges = LB.load_edges(ROOT / "reports")
        if not edges:
            return "Chưa có bản đồ link nội bộ — chạy crawl ở tab B5 trước."
        pages = [r["fields"] for r in STORE.list(_tname("trang"))]
        kw_rows = [r["fields"] for r in STORE.list(_tname("tukhoa"))]
        texts = _vi_texts(say)
        t = url.rstrip("/") + "/"
        if t not in texts:
            texts[t] = LB.page_text(t)
        say("Dựng kim tự tháp & tìm câu đặt link…")
        plan = LP.build(t, kw, pages, edges, kw_rows, texts, extra)
        plan["at"] = now_ms()
        LP_LAST.parent.mkdir(parents=True, exist_ok=True)
        LP_LAST.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        have = {(r["fields"].get("Từ URL"), r["fields"].get("Đến URL")) for r in STORE.list(_tname("lienket"))}
        recs = [{"Anchor": L["anchor"], "Loại": "Nội bộ", "Chiến lược": "Liên kết nội bộ", "Từ URL": L["from"], "Đến URL": L["to"],
                 "Thuộc tính": "Dofollow", "Vị trí đặt": "Trong nội dung", "Trạng thái": "Kế hoạch", "Câu gắn link": L.get("sentence", ""),
                 "Ghi chú": f"Kế hoạch silo «{kw}» · {L['role']} · anchor {L['kind']} · {L['why']}"}
                for L in plan["links"] if not L["has"] and (L["from"], L["to"]) not in have]
        if recs:
            STORE.create_many(_tname("lienket"), recs)
        miss = sum(1 for L in plan["links"] if not L["has"])
        return (f"Kế hoạch «{kw}»: {len(plan['satellites'])} bài vệ tinh · trụ: {(plan['pillar'] or {}).get('url', 'chưa có')} · "
                f"{len(plan['links'])} link cần có, {len(plan['links']) - miss} đã có, thêm {len(recs)} việc vào bảng Liên kết · "
                f"link vào hiện tại: {plan['inbound_content']} trong nội dung, {plan['generic']} anchor chung chung")
    return run_job("linkplan", job)


def linkplan_last():
    return json.loads(LP_LAST.read_text(encoding="utf-8")) if LP_LAST.exists() else {}



# ------------------------------------------------------------------ Chuyển dữ liệu demo (máy) → Lark Base
def migrate_to_lark():
    if STORE.mode != "lark":
        raise StoreError("Chưa nối Lark — điền LARK_APP_ID, LARK_APP_SECRET, LARK_BASE_TOKEN vào .env rồi chạy lại server")
    src = APP_DIR / "demo-data.json"
    if not src.exists():
        raise StoreError("Không có file dữ liệu trên máy (app/demo-data.json) để chuyển")
    data = json.loads(src.read_text(encoding="utf-8"))

    def job(say):
        STORE.setup()
        done, skipped, total = [], [], 0
        for name, fields in SCHEMA.items():
            rows = data.get(name) or []
            if not rows:
                continue
            if STORE.list(name):
                skipped.append(name)      # bảng trên Lark đã có dữ liệu → không ghi đè, không nhân đôi
                continue
            names = {f[0] for f in fields}
            recs = [{k: v for k, v in (r.get("fields") or {}).items() if k in names} for r in rows]
            recs = [r for r in recs if r]
            say(f"Chuyển «{name}»: {len(recs)} dòng…")
            STORE.create_many(name, recs)
            done.append(f"{name} {len(recs)}")
            total += len(recs)
        msg = f"Đã chuyển {total} dòng lên Lark ({len(done)} bảng)" + (f" · bỏ qua {len(skipped)} bảng đã có dữ liệu trên Lark: {', '.join(skipped)}" if skipped else "")
        log(msg)
        return msg
    return run_job("migrate", job)


# ------------------------------------------------------------------ Bước 10 · Review
import review as RV  # noqa: E402

DAILY_FILE = ROOT / "reports" / "du-lieu" / "gsc-daily.json"


def review_import(body):
    rows = [r for r in (body or {}).get("rows") or [] if r and not str(r[0]).lstrip().startswith("#")]
    name = (body or {}).get("name") or "file"
    period = (body or {}).get("period") or ""
    hi, kind, c = -1, "unknown", {}
    for i, r in enumerate(rows[:15]):
        k, cc = RV.detect(r)
        if k != "unknown":
            hi, kind, c = i, k, cc
            break
    if hi < 0:
        raise StoreError("Không nhận ra file. Hỗ trợ: GSC (Ngày / Trang / Truy vấn / Truy vấn × Trang) và GA4 (Trang đích có cột Phiên).")
    data = rows[hi + 1:]
    stamp = time.strftime("%d/%m/%Y")
    site = site_url()
    if kind == "gsc_dates":
        months, daily = RV.months_from_dates(data, c)
        DAILY_FILE.parent.mkdir(parents=True, exist_ok=True)
        DAILY_FILE.write_text(json.dumps(daily), encoding="utf-8")
        have = {r["fields"].get("Tháng"): r for r in STORE.list(_tname("danhgia"))}
        new, ups = [], {}
        for m, v in months.items():
            v = {k: x for k, x in v.items() if x is not None}
            v["Nguồn số liệu"] = f"GSC {name} ({stamp})"
            if m in have:
                ups[have[m]["record_id"]] = v
            else:
                new.append({"Tháng": m, **v})
        if new:
            STORE.create_many(_tname("danhgia"), new)
        if ups:
            STORE.update_many(_tname("danhgia"), ups)
        msg = f"GSC theo ngày: {len(daily)} ngày → {len(months)} tháng (thêm {len(new)}, cập nhật {len(ups)})"
    elif kind in ("gsc_pages", "ga4_pages"):
        idx = {RV.norm_url(r["fields"].get("URL"), site): r for r in STORE.list(_tname("trang"))}
        ups, miss = {}, 0
        for r in data:
            if c["page"] >= len(r):
                continue
            rec = idx.get(RV.norm_url(r[c["page"]], site))
            if not rec:
                miss += 1
                continue
            if kind == "gsc_pages":
                v = {"GSC lượt nhấp": RV.num(r[c["clicks"]]) if c["clicks"] >= 0 else None,
                     "GSC hiển thị": RV.num(r[c["impr"]]) if c["impr"] >= 0 else None,
                     "GSC CTR %": RV.num(r[c["ctr"]], True) if c["ctr"] >= 0 else None,
                     "GSC vị trí": RV.num(r[c["pos"]], True) if c["pos"] >= 0 else None}
            else:
                eng = RV.num(r[c["eng"]], True) if c["eng"] >= 0 else None
                if eng is not None and eng <= 1:
                    eng = round(eng * 100, 1)
                v = {"GA4 phiên": RV.num(r[c["sessions"]]), "GA4 tương tác %": eng,
                     "GA4 chuyển đổi": RV.num(r[c["conv"]]) if c["conv"] >= 0 else None}
            v = {k: (int(x) if k in ("GSC lượt nhấp", "GSC hiển thị", "GA4 phiên", "GA4 chuyển đổi") and x is not None else x) for k, x in v.items() if x is not None}
            v["Kỳ số liệu"] = (period + " · " if period else "") + f"{name} ({stamp})"
            ups[rec["record_id"]] = {**ups.get(rec["record_id"], {}), **v}
        if ups:
            STORE.update_many(_tname("trang"), ups)
        msg = f"{'GSC' if kind == 'gsc_pages' else 'GA4'} theo trang: cập nhật {len(ups)} trang" + (f" · {miss} URL không có trong bảng Trang đích (chạy crawl để thêm)" if miss else "")
    elif kind == "gsc_queries":
        have = {(r["fields"].get("Từ khoá") or "").strip().lower(): r for r in STORE.list(_tname("tukhoa"))}
        ups, new = {}, []
        for r in data:
            q = (r[c["query"]] or "").strip().lower()
            if not q:
                continue
            v = {"Lượt nhấp": RV.num(r[c["clicks"]]) if c["clicks"] >= 0 else None, "Hiển thị": RV.num(r[c["impr"]]) if c["impr"] >= 0 else None,
                 "Vị trí": RV.num(r[c["pos"]], True) if c["pos"] >= 0 else None}
            v = {k: (int(x) if k != "Vị trí" else x) for k, x in v.items() if x is not None}
            if q in have:
                ups[have[q]["record_id"]] = v
            else:
                it = KW.guess_intent(q)
                new.append({"Từ khoá": q, **v, "Nguồn": "Search Console", "Ý định": it, "Giai đoạn": KW.INTENT_STAGE[it], "Trạng thái": "Mới"})
        if ups:
            STORE.update_many(_tname("tukhoa"), ups)
        if new:
            STORE.create_many(_tname("tukhoa"), new)
        msg = f"GSC truy vấn: cập nhật thứ hạng {len(ups)} từ khoá, thêm {len(new)} từ khoá mới"
    else:  # gsc_query_page
        found = RV.cannibalization(data, c, site)
        have = {r["fields"].get("Từ khoá"): r for r in STORE.list(_tname("cannib"))}
        new, ups = [], {}
        for f in found:
            if f["Từ khoá"] in have:
                ups[have[f["Từ khoá"]]["record_id"]] = {k: v for k, v in f.items() if k != "Từ khoá"}
            else:
                new.append({**f, "Trạng thái": "Mới"})
        if new:
            STORE.create_many(_tname("cannib"), new)
        if ups:
            STORE.update_many(_tname("cannib"), ups)
        msg = f"Xung đột từ khoá: {len(found)} từ khoá có ≥ 2 trang Rooty cùng cạnh tranh (thêm {len(new)}, cập nhật {len(ups)})"
    log("Nhập số liệu: " + msg)
    return {"ok": True, "kind": kind, "message": msg}


import googleapi as GAPI  # noqa: E402


def google_ready():
    """Đủ cấu hình .env để lấy số qua API chưa → (gsc?, ga4?)"""
    key = ENV.get("GOOGLE_SA_JSON") or ENV.get("GOOGLE_SA_KEY")
    return bool(key and ENV.get("GSC_SITE")), bool(key and ENV.get("GA4_PROPERTY"))


def _month_upsert(by_month, src):
    """Ghi {"2026-10": {cột: giá trị}} vào bảng Đánh giá tháng (theo cột Tháng), giữ cột khác nguyên."""
    have = {r["fields"].get("Tháng"): r for r in STORE.list(_tname("danhgia"))}
    new, ups = [], {}
    for m, v in sorted(by_month.items()):
        v = {k: x for k, x in v.items() if x is not None}
        if m in have:
            old = have[m]["fields"].get("Nguồn số liệu") or ""
            ups[have[m]["record_id"]] = {**v, "Nguồn số liệu": old if src in old else (old + " · " if old else "") + src}
        else:
            new.append({"Tháng": m, **v, "Nguồn số liệu": src})
    if new:
        STORE.create_many(_tname("danhgia"), new)
    if ups:
        STORE.update_many(_tname("danhgia"), ups)
    return f"{src} theo tháng: thêm {len(new)}, cập nhật {len(ups)} tháng"


SALES_KINDS = ("Form đặt dịch vụ", "Form tư vấn", "Đơn đặt online", "Email khách trực tiếp")  # bỏ Email đại lý B2B, Đơn thanh toán lỗi


def sales_leads():
    """Đếm khách đăng ký qua sales@rootytrip.com theo tháng từ bảng «Mail khách sales@ — T…» của chị (chỉ đọc)."""
    if STORE.mode != "lark":
        return "Mail sales@: chỉ có khi nối Lark"
    names = [n for n in STORE._list_tables() if n.startswith("Mail khách sales@") and "So sánh" not in n]
    if not names:
        return "Mail sales@: không thấy bảng «Mail khách sales@ — …» trong Base"
    cnt = {}
    for r in STORE.list(names[0]):
        f = r["fields"]
        kind, ts = f.get("Nguồn"), f.get("Ngày gửi")
        kind = kind[0] if isinstance(kind, list) else kind
        if kind not in SALES_KINDS or not ts:
            continue
        m = time.strftime("%Y-%m", time.localtime(int(ts) / 1000))
        cnt.setdefault(m, {k: 0 for k in SALES_KINDS})[kind] += 1
    phien = {r["fields"].get("Tháng"): r["fields"].get("Phiên (mọi kênh)") for r in STORE.list(_tname("danhgia"))}
    by = {}
    for m, c in cnt.items():
        total = sum(c.values())
        by[m] = {"Khách đăng ký sales@": total, "Đặt dịch vụ / tư vấn / đơn online / email khách": " / ".join(str(c[k]) for k in SALES_KINDS),
                 "Tỷ lệ đăng ký %": round(total / phien[m] * 100, 2) if phien.get(m) else None}
    return _month_upsert(by, f"Mail sales@ ({names[0]})")


def google_sync():
    gsc, ga4 = google_ready()
    if not (gsc or ga4):
        raise StoreError("Chưa cấu hình — điền GOOGLE_SA_KEY (hoặc GOOGLE_SA_JSON) và GSC_SITE / GA4_PROPERTY vào .env rồi chạy lại server (xem app/README.md)")

    def job(say):
        key = ENV.get("GOOGLE_SA_JSON") or ENV["GOOGLE_SA_KEY"]  # nội dung JSON (Render) hoặc đường dẫn file (máy)
        if not key.lstrip().startswith("{") and not os.path.isabs(key):
            key = str(ROOT / key)
        say("Đăng nhập Google bằng service account…")
        token, email = GAPI.access_token(key)
        done = []
        if gsc:
            say("Lấy Search Console: theo ngày (16 tháng), trang, truy vấn, truy vấn × trang (28 ngày)…")
            try:
                period, tables = GAPI.gsc_tables(token, ENV["GSC_SITE"])
            except GAPI.GoogleError as e:
                raise GAPI.GoogleError(f"{e} — kiểm GSC_SITE và đã thêm {email} vào Search Console chưa")
            for kind, rows in tables.items():
                say(f"Nạp {kind}: {len(rows) - 1} dòng")
                done.append(review_import({"rows": rows, "name": "GSC API", "period": period})["message"])
        if ga4:
            say("Lấy GA4: trang đích, kênh Organic Search (28 ngày)…")
            try:
                period, rows = GAPI.ga4_pages(token, ENV["GA4_PROPERTY"])
            except GAPI.GoogleError as e:
                raise GAPI.GoogleError(f"{e} — kiểm GA4_PROPERTY và đã thêm {email} vào GA4 (quyền Người xem) chưa")
            done.append(review_import({"rows": rows, "name": "GA4 API organic", "period": period})["message"])
            say("Lấy GA4 theo tháng: phiên, tương tác, tỷ lệ thoát, thời gian, chuyển đổi…")
            done.append(_month_upsert(GAPI.ga4_months(token, ENV["GA4_PROPERTY"]), "GA4 API"))
        say("Đếm khách đăng ký qua sales@ theo tháng…")
        done.append(sales_leads())
        return " · ".join(done)
    return run_job("google", job)


def review_classify():
    rows = [r for r in STORE.list(_tname("trang")) if r["fields"].get("Loại trang") != "Ngôn ngữ khác"]
    h1c = {}
    for r in rows:
        h = (r["fields"].get("H1") or "").strip().lower()
        if h:
            h1c[h] = h1c.get(h, 0) + 1
    dup = {h for h, n in h1c.items() if n > 1}
    ups, cnt = {}, {}
    for r in rows:
        d, why = RV.classify(r["fields"], dup)
        ups[r["record_id"]] = {"Đề xuất audit": d, "Lý do đề xuất": why}
        cnt[d] = cnt.get(d, 0) + 1
    STORE.update_many(_tname("trang"), ups)
    return {"ok": True, "message": "Content audit: " + " · ".join(f"{k} {v}" for k, v in sorted(cnt.items(), key=lambda x: -x[1]))}


def review_tasks():
    rows = [r["fields"] for r in STORE.list(_tname("trang"))
            if (r["fields"].get("Quyết định") or r["fields"].get("Đề xuất audit")) == "Cập nhật / viết lại"
            and r["fields"].get("Quyết định") != "Chưa quyết"]
    rows.sort(key=lambda f: -(f.get("GSC hiển thị") or 0))
    have = {(r["fields"].get("Link bài") or "").rstrip("/") for r in STORE.list(T_BAI)}
    made = 0
    for f in rows[:15]:
        if f["URL"].rstrip("/") in have:
            continue
        kw, _ = page_keyword(f)
        rec = api_create({"Từ khoá": kw or f.get("H1") or f.get("Tiêu đề") or f["URL"], "Slug": KW.slugify(urllib.parse.urlsplit(f["URL"]).path.strip("/").split("/")[-1] or "trang-chu"),
                          "Ghi chú": f"Cập nhật bài cũ (content audit B10): {f.get('Lý do đề xuất', '')}"})
        STORE.update(T_BAI, rec["record_id"], {"Link bài": f["URL"]})
        made += 1
    return {"ok": True, "message": f"Tạo {made} việc cập nhật bài cũ trong tab Content (ưu tiên trang nhiều hiển thị nhất)"}


def review_remeasure():
    pages = {RV.norm_url(r["fields"].get("URL"), site_url()): r["fields"] for r in STORE.list(_tname("trang"))}
    now = now_ms()
    ups, cnt = {}, {}
    for r in STORE.list(_tname("changelog")):
        f = r["fields"]
        p = pages.get(RV.norm_url(f.get("URL") or "", site_url()))
        if not p or p.get("GSC lượt nhấp") is None:
            continue
        ch = {}
        age_days = (now - (f.get("Ngày") or now)) / 864e5
        if f.get("Lượt nhấp trước") is None and age_days <= 7:
            ch = {"Lượt nhấp trước": p.get("GSC lượt nhấp"), "Vị trí trước": p.get("GSC vị trí"), "Kết quả": "Chờ đo"}
        elif f.get("Lượt nhấp trước") is not None and age_days >= 28:
            before, after = f["Lượt nhấp trước"] or 0, p.get("GSC lượt nhấp") or 0
            res = "Tốt lên" if after > before * 1.1 else ("Giảm" if after < before * 0.9 else "Không đổi")
            ch = {"Lượt nhấp sau": after, "Vị trí sau": p.get("GSC vị trí"), "Kết quả": res}
        if ch:
            ups[r["record_id"]] = ch
            cnt[ch["Kết quả"]] = cnt.get(ch["Kết quả"], 0) + 1
    if ups:
        STORE.update_many(_tname("changelog"), ups)
    return {"ok": True, "message": ("Đo lại: " + " · ".join(f"{k} {v}" for k, v in cnt.items())) if cnt else
            "Chưa có thay đổi nào đủ điều kiện đo (cần số liệu GSC theo trang; ghi «trước» trong 7 ngày đầu, đo «sau» từ tuần thứ 4)"}


def review_summary():
    daily = json.loads(DAILY_FILE.read_text(encoding="utf-8")) if DAILY_FILE.exists() else []
    return {"week": RV.week_alert(daily), "days": len(daily),
            "lastDay": daily[-1][0] if daily else None}


# ------------------------------------------------------------------ Bước 9 · Link building
import linkbuild as LB  # noqa: E402


def links_stats():
    edges = LB.load_edges(ROOT / "reports")
    if not edges:
        return {"ready": False, "message": "Chưa có bản đồ link nội bộ — bấm «Chạy crawl» ở tab B5 (crawl mới ghi thêm file .links.tsv)"}
    st = LB.internal_stats(edges)
    pages = {r["fields"].get("URL"): r["fields"] for r in STORE.list(_tname("trang"))}
    imp = [u for u, f in pages.items() if f.get("Loại trang") in ("Trang tour/sản phẩm", "Danh mục") or f.get("Vai trò silo") == "Pillar (trụ cột)"]
    weak_imp = sorted(((u, st["in_content"].get(u, 0)) for u in imp), key=lambda x: x[1])
    return {"ready": True, "total": st["total"], "content": st["content"], "menuFooter": st["menu_footer"], "zones": st["zones"],
            "generic": len(st["generic"]), "genericEx": [f"«{e['anchor']}» · {e['from']} → {e['to']}" for e in st["generic"][:8]],
            "empty": len(st["empty"]), "heavy": st["heavy"][:5],
            "weakImportant": [{"url": u, "n": n} for u, n in weak_imp[:12]],
            "weakImportantCount": sum(1 for _, n in weak_imp if n < 3), "importantCount": len(imp),
            "file": os.path.basename(LB.latest_links(ROOT / "reports"))}


def links_suggest(body):
    limit = int((body or {}).get("targets") or 25)

    def job(say):
        edges = LB.load_edges(ROOT / "reports")
        if not edges:
            return "Chưa có bản đồ link nội bộ — chạy crawl trước (tab B5)."
        existing = {(e["from"], e["to"]) for e in edges}
        in_content = LB.internal_stats(edges)["in_content"]
        trang = STORE.list(_tname("trang"))
        kw_rows = STORE.list(_tname("tukhoa"))
        tg = []
        for r in trang:
            f = r["fields"]
            if f.get("Loại trang") in ("Trang tour/sản phẩm", "Danh mục") or f.get("Vai trò silo") == "Pillar (trụ cột)":
                kw, _ = page_keyword(f, kw_rows)
                ph = LB.phrases_for({**f, "Từ khoá chính": kw or f.get("Từ khoá chính")})
                if ph:
                    tg.append({"url": f["URL"], "phrases": ph, "n": in_content.get(f["URL"], 0), "kw": bool(kw)})
        # cụm mà nhiều trang cùng có (VD "tour phú quốc trọn gói" của danh mục và của 1 tour 4N3Đ) → chỉ giao cho
        # trang có cụm đó là từ khoá chính, hoặc trang có URL ngắn nhất (thường là danh mục)
        owners: dict[str, list] = {}
        for t in tg:
            for p in t["phrases"]:
                owners.setdefault(p, []).append(t)
        for p, ts in owners.items():
            if len(ts) > 1:
                keep = min(ts, key=lambda t: (not t["kw"], len(t["url"])))
                for t in ts:
                    if t is not keep:
                        t["phrases"] = [x for x in t["phrases"] if x != p]
        tg = [t for t in tg if t["phrases"]]
        tg.sort(key=lambda t: t["n"])
        tg = tg[:limit]
        sources = [r["fields"]["URL"] for r in trang if r["fields"].get("Loại trang") == "Bài viết" and (r["fields"].get("Số từ") or 0) > 500]
        sources.sort(key=lambda u: -(in_content.get(u, 0)))
        say(f"{len(tg)} trang đích cần thêm link · {len(sources)} bài viết nguồn")
        sug = LB.suggest_internal(tg, sources, existing, say)
        have = {(r["fields"].get("Từ URL"), r["fields"].get("Đến URL")) for r in STORE.list(_tname("lienket"))}
        recs = [{"Anchor": s["anchor"], "Loại": "Nội bộ", "Chiến lược": "Liên kết nội bộ", "Từ URL": s["from"], "Đến URL": s["to"],
                 "Thuộc tính": "Dofollow", "Vị trí đặt": "Trong nội dung", "Trạng thái": "Kế hoạch", "Câu gắn link": s["sentence"],
                 "Ghi chú": f"Gợi ý tự động {time.strftime('%d/%m/%Y')}: bài nguồn đã nhắc «{s['anchor']}» nhưng chưa gắn link"}
                for s in sug if (s["from"], s["to"]) not in have]
        if recs:
            STORE.create_many(_tname("lienket"), recs)
        return f"Gợi ý {len(recs)} link nội bộ cho {len({r['Đến URL'] for r in recs})} trang đích (tour, danh mục, Pillar ít link nhất)"
    return run_job("linksuggest", job)


def links_check():
    def job(say):
        rows = [r for r in STORE.list(_tname("lienket")) if r["fields"].get("Loại") != "Nội bộ" and r["fields"].get("Từ URL")
                and r["fields"].get("Trạng thái") in ("Đã gắn", "Đang live", "Mất link")]
        if not rows:
            return "Chưa có backlink nào ở trạng thái Đã gắn / Đang live để kiểm."
        ups, cnt = {}, {}
        for i, r in enumerate(rows, 1):
            f = r["fields"]
            say(f"[{i}/{len(rows)}] {f['Từ URL']}")
            res = LB.check_backlink(f["Từ URL"], f.get("Đến URL") or site_url())
            ch = {"Kiểm lần cuối": now_ms(), "Kết quả kiểm": res["detail"]}
            if res["status"] == "Đang live":
                ch.update({"Trạng thái": "Đang live", "Thuộc tính": res["attr"], "Vị trí đặt": res["zone"] if res["zone"] in ("Trong nội dung", "Sidebar", "Footer", "Menu/header") else f.get("Vị trí đặt")})
                if not f.get("Anchor"):
                    ch["Anchor"] = res["anchor"]
            elif res["status"] == "Mất link":
                ch["Trạng thái"] = "Mất link"
            if not f.get("Domain nguồn"):
                ch["Domain nguồn"] = urllib.parse.urlsplit(f["Từ URL"]).netloc.replace("www.", "")
            ch["Điểm chất lượng"] = LB.quality({**f, **ch})
            ups[r["record_id"]] = ch
            cnt[res["status"]] = cnt.get(res["status"], 0) + 1
        STORE.update_many(_tname("lienket"), ups)
        return "Kiểm backlink: " + " · ".join(f"{k} {v}" for k, v in cnt.items())
    return run_job("linkcheck", job)


def links_broken(body):
    url = ((body or {}).get("url") or "").strip()
    if not url.startswith("http"):
        raise StoreError("Nhập URL trang cần tìm link gãy (bắt đầu bằng http)")
    try:
        res = LB.find_broken(url)
    except Exception as e:
        raise StoreError(f"Không đọc được trang: {e}")
    return {"ok": True, "page": url, "broken": res,
            "message": f"Tìm thấy {len(res)} link gãy trên trang" if res else "Không thấy link gãy (đã kiểm tối đa 80 link ra ngoài)"}


def links_rescore():
    ups = {r["record_id"]: {"Điểm chất lượng": LB.quality(r["fields"]),
                            **({"Domain nguồn": urllib.parse.urlsplit(r["fields"]["Từ URL"]).netloc.replace("www.", "")}
                               if r["fields"].get("Từ URL") and not r["fields"].get("Domain nguồn") else {})}
           for r in STORE.list(_tname("lienket")) if r["fields"].get("Loại") != "Nội bộ"}
    if ups:
        STORE.update_many(_tname("lienket"), ups)
    return {"ok": True, "message": f"Tính lại điểm chất lượng {len(ups)} backlink"}


# ------------------------------------------------------------------ Bước 8 · Entity
import entity as EN  # noqa: E402


def sync_hoso():
    """Thêm nền tảng còn thiếu vào bảng Hồ sơ thương hiệu và điền cột Nhóm cho dòng cũ."""
    tname = _tname("hoso")
    rows = STORE.list(tname)
    if not rows:
        return 0
    have = {r["fields"].get("Nền tảng"): r for r in rows}
    groups = dict(TB.PROFILES)
    new = [s for s in TB.SEEDS["hoso"] if s["Nền tảng"] not in have]
    ups = {r["record_id"]: {"Nhóm": groups[n]} for n, r in have.items() if n in groups and not r["fields"].get("Nhóm")}
    if new:
        STORE.create_many(tname, new)
    if ups:
        STORE.update_many(tname, ups)
    return len(new)


def brand_master() -> tuple[dict | None, dict]:
    rows = STORE.list(_tname("brand"))
    if not rows:
        t_seed("brand")
        rows = STORE.list(_tname("brand"))
    return rows[0]["record_id"], rows[0]["fields"]


def entity_from_site():
    rid, master = brand_master()
    live = EN.read_site(site_url())
    ch = {k: v for k, v in live["nap"].items() if not master.get(k) and k in {f["n"] for f in TB.TABLES["brand"]["fields"]}}
    if ch:
        STORE.update(_tname("brand"), rid, ch)
    return {"ok": True, "message": f"Lấy từ schema trang chủ ({live['org_type'] or 'không thấy schema tổ chức'}): điền {len(ch)} ô — " + (", ".join(ch) or "không có ô trống cần điền")}


def entity_scan():
    """Liên kết chéo: website có link tới hồ sơ không, hồ sơ có trong sameAs không, hồ sơ có trỏ về website không."""
    sync_hoso()
    live = EN.read_site(site_url())
    domain = urllib.parse.urlsplit(site_url()).netloc.replace("www.", "")
    rows = STORE.list(_tname("hoso"))
    by_name = {r["fields"].get("Nền tảng"): r for r in rows}
    same_by_platform = {}
    for u in live["sameAs"]:
        n = EN.platform_of(u)
        if n:
            same_by_platform.setdefault(n, []).append(u)
    ups, notes = {}, []
    for name, r in by_name.items():
        f, ch, note = r["fields"], {}, []
        if name.startswith("Website"):
            ch = {"URL": f.get("URL") or site_url(), "Trạng thái": "Đã có", "Web trỏ tới hồ sơ": "Có", "Hồ sơ trỏ về web": "Có", "Đã xác minh": "Không áp dụng"}
            ups[r["record_id"]] = ch
            continue
        web_link = live["social"].get(name)
        all_links = live["social_all"].get(name, [])
        same = same_by_platform.get(name, [])
        url = web_link or f.get("URL") or (same[0] if same else "")
        if url and EN.norm_url(url) != EN.norm_url(f.get("URL") or ""):
            ch["URL"] = url
        if url:
            prob = EN.profile_problem(name, url)
            if prob:
                note.append(f"⚠ {prob} ({url})")
            for u in all_links:
                if EN.norm_url(u) != EN.norm_url(url):
                    p2 = EN.profile_problem(name, u)
                    note.append(f"⚠ Website còn link {name} khác: {u}" + (f" — {p2}" if p2 else ""))
            same_bad = [u for u in same if EN.profile_problem(name, u)]
            for u in same_bad:
                note.append(f"⚠ sameAs: {EN.profile_problem(name, u)} ({u})")
            ch["Trạng thái"] = "Cần sửa" if (prob or same_bad) else "Đã có"
        ch["Web trỏ tới hồ sơ"] = "Có" if web_link else "Chưa"
        ch["Trong sameAs"] = "Có" if same else "Chưa"
        if web_link and same and EN.norm_url(web_link) not in {EN.norm_url(x) for x in same}:
            note.append(f"⚠ Link trên web ({web_link}) khác link trong schema sameAs ({same[0]})")
        if not web_link and same:
            note.append("Có trong sameAs nhưng website chưa đặt link/biểu tượng tới hồ sơ này")
        if web_link and not same:
            note.append("Website có link nhưng schema sameAs chưa khai báo")
        if note:
            ch["Ghi chú"] = time.strftime("%d/%m/%Y") + ": " + " · ".join(note)
            notes += [f"{name}: {x}" for x in note]
        ups[r["record_id"]] = ch
    # hồ sơ trỏ về web (mạng xã hội hay chặn bot → «Chưa kiểm»)
    targets = []
    for r in rows:
        if r["fields"].get("Nền tảng", "").startswith("Website"):
            continue
        u = ups.get(r["record_id"], {}).get("URL") or r["fields"].get("URL")
        if u:
            targets.append((r["record_id"], u))
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(6) as ex:
        backs = dict(zip([t[0] for t in targets], ex.map(lambda t: EN.profile_links_back(t[1], domain), targets)))
    for rid, v in backs.items():
        ups.setdefault(rid, {})["Hồ sơ trỏ về web"] = v
    # hồ sơ có trong sameAs/website mà bảng chưa có dòng
    extra = [u for u in live["sameAs"] if not EN.platform_of(u)]
    if ups:
        STORE.update_many(_tname("hoso"), ups)
    log("Quét liên kết chéo thương hiệu: " + (" | ".join(notes[:5]) or "không có cảnh báo"))
    msg = f"Website có link tới {len(live['social'])} hồ sơ · sameAs khai báo {len(live['sameAs'])} URL · {len(notes)} cảnh báo"
    if extra:
        msg += f" · sameAs có thêm: {', '.join(extra[:4])}"
    return {"ok": True, "message": msg}


def entity_nap():
    _, master = brand_master()
    if not master.get("Hotline chính") and not master.get("Địa chỉ"):
        raise StoreError("Chưa có NAP gốc — bấm «Lấy từ website» hoặc điền Thông tin thương hiệu trước")
    ups, cnt = {}, {}
    for r in STORE.list(_tname("hoso")):
        f = r["fields"]
        if f.get("Nền tảng", "").startswith("Website"):
            continue
        res, note = EN.compare_nap(master, f)
        if res == "Chưa kiểm" and f.get("Khớp NAP") in ("Khớp", "Lệch"):
            continue
        cnt[res] = cnt.get(res, 0) + 1
        ups[r["record_id"]] = {"Khớp NAP": res, **({"Ghi chú": time.strftime("%d/%m/%Y") + " NAP: " + note} if res != "Chưa kiểm" else {})}
    if ups:
        STORE.update_many(_tname("hoso"), ups)
    return {"ok": True, "message": "Kiểm NAP: " + " · ".join(f"{k} {v}" for k, v in cnt.items()) + " (hồ sơ «Chưa kiểm» = chưa điền Tên/Hotline/Địa chỉ của hồ sơ)"}


def entity_schema():
    _, master = brand_master()
    rows = [r["fields"] for r in STORE.list(_tname("hoso"))]
    same = [f["URL"] for f in rows if f.get("URL") and f.get("Trạng thái") in ("Đã có",) and not f.get("Nền tảng", "").startswith("Website")
            and not EN.profile_problem(f.get("Nền tảng", ""), f["URL"])]
    live = EN.read_site(site_url())
    want = EN.build_jsonld({**live["nap"], **{k: v for k, v in master.items() if v}}, same, "SearchAction" in live["types"])
    return {"jsonld": json.dumps(want, ensure_ascii=False, indent=2), "gaps": EN.schema_gaps(live, want),
            "liveType": live["org_type"], "liveSameAs": live["sameAs"]}


# ------------------------------------------------------------------ Bước 7 · Onpage
import onpage as OP  # noqa: E402


def page_keyword(f: dict, kw_rows=None) -> tuple[str | None, list[str]]:
    """Từ khoá chính của trang: cột «Từ khoá chính», hoặc từ khoá trong bảng Từ khoá trỏ về URL này."""
    url = (f.get("URL") or "").rstrip("/")
    rel = [r["fields"] for r in (kw_rows if kw_rows is not None else STORE.list(_tname("tukhoa")))
           if (r["fields"].get("Trang đích") or "").rstrip("/") == url and r["fields"].get("Trạng thái") != "Bỏ"]
    rel.sort(key=lambda x: (x.get("Vai trò") != "Từ khoá chính", -(x.get("Lượng tìm") or x.get("Hiển thị") or 0)))
    main = (f.get("Từ khoá chính") or "").strip() or (rel[0]["Từ khoá"] if rel else None)
    return main, [x["Từ khoá"] for x in rel if x["Từ khoá"] != main][:15]


def onpage_rescore():
    """Chấm nhanh lại mọi trang từ báo cáo crawl mới nhất (Title, Meta, Heading, URL) — không ghi đè trang đã chấm chi tiết."""
    rows, src = TB.crawl_rows(ROOT / "reports")
    by_url = {r["url"]: r for r in TB.crawl_pages(rows)}
    kw_rows = STORE.list(_tname("tukhoa"))
    ups = {}
    for r in STORE.list(_tname("trang")):
        f = r["fields"]
        c = by_url.get(f.get("URL"))
        if not c or f.get("Lần chấm onpage"):
            continue
        kw, _ = page_keyword(f, kw_rows)
        res, score = OP.quick(c, kw)
        ups[r["record_id"]] = {**res, "Điểm onpage": score}
    if ups:
        STORE.update_many(_tname("trang"), ups)
    return {"ok": True, "message": f"Chấm nhanh {len(ups)} trang từ {src} (Title, Meta, Heading, URL). Hình ảnh cần «Chấm chi tiết»."}


def onpage_deep(rid):
    rec = next((r for r in STORE.list(_tname("trang")) if r["record_id"] == rid), None)
    if not rec:
        raise StoreError("Không tìm thấy trang")
    f = rec["fields"]
    kw, related = page_keyword(f)
    r = OP.deep(f["URL"], kw, related)
    if r.get("error"):
        raise StoreError(r["error"])
    ch = {**r["res"], "Điểm onpage": r["score"], "Chi tiết onpage": r["detail"], "Gợi ý Title": r["sug_title"],
          "Gợi ý Meta": r["sug_meta"], "Lần chấm onpage": now_ms()}
    if not f.get("Từ khoá chính") and kw:
        ch["Từ khoá chính"] = kw
    if f.get("Onpage") in (None, "", "Chưa làm") and r["score"] < 100:
        ch["Onpage"] = "Đang làm"
    STORE.update(_tname("trang"), rid, ch)
    return {"ok": True, "message": f"Onpage {r['score']}/100 · " + " · ".join(f"{k}: {v}" for k, v in r["res"].items())}


def onpage_deep_batch(body):
    """Chấm chi tiết các trang quan trọng: Pillar, trang sản phẩm, danh mục (tối đa N trang)."""
    limit = int((body or {}).get("limit") or 40)

    def job(say):
        rows = [r for r in STORE.list(_tname("trang")) if not r["fields"].get("Lần chấm onpage") and (
            r["fields"].get("Vai trò silo") == "Pillar (trụ cột)" or r["fields"].get("Loại trang") in ("Trang tour/sản phẩm", "Danh mục", "Trang chủ"))]
        rows.sort(key=lambda r: -(r["fields"].get("Link vào") or 0))
        rows = rows[:limit]
        done = 0
        for i, r in enumerate(rows, 1):
            say(f"[{i}/{len(rows)}] {r['fields'].get('URL')}")
            try:
                onpage_deep(r["record_id"])
                done += 1
            except Exception as e:
                say(f"  lỗi: {e}")
            time.sleep(0.3)
        return f"Chấm chi tiết {done} trang quan trọng (trang chủ, danh mục, Pillar, tour)"
    return run_job("onpage", job)


def dt_scan(body):
    rid = (body or {}).get("id")

    def job(say):
        rows = [r for r in STORE.list(_tname("doithu")) if r["fields"].get("Website") and (not rid or r["record_id"] == rid)]
        if not rows:
            return "Chưa có đối thủ nào có Website."
        for i, r in enumerate(rows, 1):
            say(f"[{i}/{len(rows)}] Soi {r['fields'].get('Website')}…")
            try:
                txt = KW.scan_site(r["fields"]["Website"])
            except Exception as e:
                txt = f"Không soi được: {e}"
            STORE.update(_tname("doithu"), r["record_id"], {"Chỉ số kỹ thuật": txt, "Ngày soi": now_ms()})
        return f"Đã soi {len(rows)} website đối thủ"
    return run_job("scan", job)


def dt_classify():
    ups = KW.classify_competitor_kw(STORE.list(_tname("dtkw")), STORE.list(_tname("tukhoa")))
    if ups:
        STORE.update_many(_tname("dtkw"), ups)
    c = {}
    for u in ups.values():
        c[u["Phân loại"]] = c.get(u["Phân loại"], 0) + 1
    return {"ok": True, "message": "Phân loại: " + (" · ".join(f"{k}: {v}" for k, v in c.items()) or "không có dòng nào")}


def dt_to_keywords():
    rows = [r for r in STORE.list(_tname("dtkw")) if str(r["fields"].get("Phân loại", "")).startswith("Gap") and r["fields"].get("Đã thêm vào Từ khoá") != "Đã thêm"]
    if not rows:
        return {"ok": True, "message": "Không có từ khoá Gap nào chưa chuyển (bấm «Phân loại» trước)."}
    recs = []
    for r in rows:
        f = r["fields"]
        k = f.get("Từ khoá", "")
        it = KW.guess_intent(k)
        recs.append({"Từ khoá": k, "Lượng tìm": f.get("Lượng tìm"), "Nguồn": "Đối thủ", "Ý định": it, "Giai đoạn": KW.INTENT_STAGE[it],
                     "Trạng thái": "Mới", "Ghi chú": f"Gap: {f.get('Đối thủ', '')} đứng vị trí {f.get('Vị trí đối thủ', '?')} · {f.get('URL đối thủ', '')}"})
    msg = t_bulk("tukhoa", {"records": recs})["message"]
    STORE.update_many(_tname("dtkw"), {r["record_id"]: {"Đã thêm vào Từ khoá": "Đã thêm"} for r in rows})
    return {"ok": True, "message": f"Chuyển {len(rows)} từ khoá Gap sang bảng Từ khoá — {msg}"}


def crawl_start(body):
    if CRAWL["running"]:
        raise StoreError("Crawl đang chạy, đợi xong đã.")
    mp = int((body or {}).get("maxPages") or 1200)
    CRAWL.update(running=True, lines=[f"Bắt đầu crawl {site_url()} (tối đa {mp} trang)…"], started=now_ms(), finished=0, rc=None, result="")
    threading.Thread(target=_crawl_worker, args=(mp,), daemon=True).start()
    return {"ok": True, "message": "Đã bắt đầu crawl — mất vài phút, trang tự cập nhật khi xong."}


def t_meta():
    return {k: {"name": t["name"], "fields": t["fields"], "seed": k in TB.SEEDS} for k, t in TB.TABLES.items()}


# ------------------------------------------------------------------ HTTP

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.command, self.path))

    def _json(self, obj, status=200):
        data = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        raw = self.rfile.read(n)
        try:
            return json.loads(raw.decode("utf-8-sig") or "{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {"__invalid__": True}

    def handle_one_request(self):
        # dữ liệu gửi lên không phải JSON hợp lệ → trả 400 thay vì đứt kết nối
        try:
            super().handle_one_request()
        except (ConnectionResetError, BrokenPipeError):
            pass

    def _guard(self, fn):
        try:
            self._json(fn())
        except json.JSONDecodeError:
            self._json({"error": "Dữ liệu gửi lên không phải JSON hợp lệ"}, 400)
        except StoreError as e:
            self._json({"error": str(e)}, 400)
        except Exception as e:  # lỗi không lường trước
            self._json({"error": f"Lỗi máy chủ: {e}"}, 500)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/api/config":
            return self._json({"mode": STORE.mode, "stages": STAGES, "statuses": STATUSES,
                               "pageTypes": PAGE_TYPES, "gates": GATES, "gateToLeave": GATE_TO_LEAVE,
                               "intents": INTENTS, "intentFormats": INTENT_FORMATS, "serpFeatures": SERP_FEATURES, "site": site_url(),
                               "mang": QT["mang"], "pha": PHA, "viecStatus": VIEC_STATUS,
                               "projectStart": project_start(), "currentMonth": current_month_index(),
                               "google": dict(zip(("gsc", "ga4"), google_ready())),
                               "tables": t_meta()})
        m = re.match(r"^/api/t/(\w+)$", path)
        if m:
            return self._guard(lambda: STORE.list(_tname(m.group(1))))
        if path == "/api/entity/schema":
            return self._guard(entity_schema)
        if path == "/api/links/stats":
            return self._guard(links_stats)
        if path == "/api/linkplan/last":
            return self._guard(linkplan_last)
        if path == "/api/chandoan/last":
            return self._guard(chandoan_last)
        if path == "/api/algo/summary":
            return self._guard(algo_summary)
        if path == "/api/loi/summary":
            return self._guard(loi_summary)
        if path == "/api/geo/summary":
            return self._guard(geo_summary)
        if path == "/api/review/summary":
            return self._guard(review_summary)
        m = re.match(r"^/api/job/(\w+)$", path)
        if m:
            return self._json(JOBS.get(m.group(1), {"running": False, "lines": [], "result": "", "finished": 0}))
        if path == "/api/run/status":
            last = TB.latest(str(ROOT / "reports" / "crawl-*.csv"))
            return self._json({**CRAWL, "site": site_url(),
                               "lastReport": os.path.basename(last) if last else None,
                               "lastReportAt": int(os.path.getmtime(last) * 1000) if last else None})
        if path == "/api/bai":
            return self._guard(lambda: STORE.list(T_BAI))
        if path == "/api/viec":
            return self._guard(lambda: STORE.list(T_VIEC))
        if path.startswith("/docs/"):
            name = urllib.parse.unquote(path[len("/docs/"):])
            f = QT_DIR / name
            if not re.match(r"^[\w.-]+\.md$", name) or not f.exists():
                return self.send_error(404)
            data = f.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            return self.wfile.write(data)
        if path == "/api/log":
            return self._guard(lambda: sorted(STORE.list(T_LOG), key=lambda r: -(r["fields"].get("Thời gian") or 0))[:60])
        # file tĩnh
        f = STATIC / ("index.html" if path in ("/", "") else path.lstrip("/"))
        try:
            f = f.resolve()
            if STATIC.resolve() not in f.parents and f != STATIC.resolve() / "index.html":
                raise FileNotFoundError
            data = f.read_bytes()
        except (FileNotFoundError, IsADirectoryError, OSError):
            self.send_error(404)
            return
        ctype = {"html": "text/html", "js": "text/javascript", "css": "text/css"}.get(f.suffix.lstrip("."), "application/octet-stream")
        self.send_response(200)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        if ctype == "text/html" and os.environ.get("HUB"):
            # Chạy trong Marketing Hub: xin Hub không chèn bộ CSS/JS dùng chung, giữ giao diện riêng của app
            self.send_header("X-Hub-Khong-Chen", "1")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/api/bai":
            return self._guard(lambda: api_create(self._body()))
        if path == "/api/setup":
            return self._guard(STORE.setup)
        if path == "/api/migrate":
            return self._guard(migrate_to_lark)
        if path == "/api/viec/seed":
            return self._guard(api_viec_seed)
        if path == "/api/import/crawl":
            return self._guard(import_crawl)
        if path == "/api/import/audit":
            return self._guard(import_audit)
        if path == "/api/tech/check":
            return self._guard(tech_check)
        simple = {"/api/kw/group": kw_group, "/api/kw/create-posts": kw_create_posts,
                  "/api/dtkw/classify": dt_classify, "/api/dtkw/to-keywords": dt_to_keywords}
        if path in simple:
            return self._guard(simple[path])
        if path == "/api/review/import":
            body = self._body()
            return self._guard(lambda: review_import(body))
        if path == "/api/google/sync":
            return self._guard(google_sync)
        rv = {"/api/review/classify": review_classify, "/api/review/tasks": review_tasks, "/api/review/remeasure": review_remeasure}
        if path in rv:
            return self._guard(rv[path])
        if path in ("/api/links/suggest", "/api/links/broken"):
            body = self._body()
            return self._guard(lambda: (links_suggest if path.endswith("suggest") else links_broken)(body))
        if path == "/api/links/check":
            return self._guard(links_check)
        if path == "/api/links/rescore":
            return self._guard(links_rescore)
        entity_api = {"/api/entity/from-site": entity_from_site, "/api/entity/scan": entity_scan, "/api/entity/nap": entity_nap}
        if path in entity_api:
            return self._guard(entity_api[path])
        if path == "/api/onpage/rescore":
            return self._guard(onpage_rescore)
        if path == "/api/onpage/batch":
            body = self._body()
            return self._guard(lambda: onpage_deep_batch(body))
        m = re.match(r"^/api/onpage/([\w-]+)/check$", path)
        if m:
            return self._guard(lambda: onpage_deep(m.group(1)))
        if path in ("/api/loi/import", "/api/loi/recheck"):
            body = self._body()
            return self._guard(lambda: (loi_import if path.endswith("import") else loi_recheck)(body))
        if path == "/api/linkplan/run":
            body = self._body()
            return self._guard(lambda: linkplan_run(body))
        if path == "/api/gia/from-site":
            return self._guard(gia_from_site)
        if path == "/api/gia/usage":
            body = self._body()
            return self._guard(lambda: gia_usage(body))
        if path == "/api/chandoan/run":
            body = self._body()
            return self._guard(lambda: chandoan_run(body))
        if path == "/api/kiemweb/run":
            body = self._body()
            return self._guard(lambda: multi_check(body))
        if path == "/api/algo/refresh":
            return self._guard(algo_refresh)
        if path == "/api/policy/check":
            return self._guard(policy_check)
        if path == "/api/loi/measure":
            return self._guard(loi_measure)
        if path in ("/api/geo/answer", "/api/geo/batch"):
            body = self._body()
            return self._guard(lambda: (geo_answer if path.endswith("answer") else geo_batch)(body))
        if path == "/api/geo/sync":
            return self._guard(geo_sync)
        m = re.match(r"^/api/geo/page/([\w-]+)$", path)
        if m:
            return self._guard(lambda: trang_geo(m.group(1)))
        m = re.match(r"^/api/bai/([\w-]+)/(intent|questions|check|geo)$", path)
        if m:
            fn = {"intent": bai_intent, "questions": bai_questions, "check": bai_check, "geo": bai_geo}[m.group(2)]
            return self._guard(lambda: fn(m.group(1)))
        if path in ("/api/kw/expand", "/api/doithu/scan"):
            body = self._body()
            return self._guard(lambda: (kw_expand if path == "/api/kw/expand" else dt_scan)(body))
        if path == "/api/run/crawl":
            body = self._body()
            return self._guard(lambda: crawl_start(body))
        m = re.match(r"^/api/t/(\w+)(/bulk|/seed)?$", path)
        if m:
            key, act = m.group(1), m.group(2)
            body = self._body() if act != "/seed" else None
            fn = {None: lambda: t_create(key, body), "/bulk": lambda: t_bulk(key, body), "/seed": lambda: t_seed(key)}[act]
            return self._guard(fn)
        self.send_error(404)

    def do_PATCH(self):
        path = urllib.parse.urlparse(self.path).path
        m = re.match(r"^/api/t/(\w+)/([\w-]+)$", path)
        if m:
            body = self._body()
            return self._guard(lambda: t_update(m.group(1), m.group(2), body))
        m = re.match(r"^/api/(bai|viec)/([\w-]+)$", path)
        if not m:
            return self.send_error(404)
        body = self._body()
        fn = api_update if m.group(1) == "bai" else api_viec_update
        self._guard(lambda: fn(m.group(2), body))

    def do_DELETE(self):
        m = re.match(r"^/api/t/(\w+)/([\w-]+)$", urllib.parse.urlparse(self.path).path)
        if not m:
            return self.send_error(404)
        self._guard(lambda: STORE.delete(_tname(m.group(1)), m.group(2)))


def main():
    try:
        n = sync_hoso()
        if n:
            print(f"Hồ sơ thương hiệu: thêm {n} nền tảng")
    except StoreError as e:
        print("Bỏ qua đồng bộ hồ sơ:", e)
    try:  # bảng checklist đã có → cập nhật theo danh sách mới nhất (thêm mục, giữ kết quả)
        if STORE.list(_tname("kythuat")):
            n, u = sync_checklist()
            if n or u:
                print(f"Checklist audit: thêm {n} mục, cập nhật {u} mục")
    except StoreError as e:
        print("Bỏ qua đồng bộ checklist:", e)
    try:  # Checklist GEO (GTV) đã có → cập nhật theo bản mới nhất, giữ trạng thái
        if STORE.list(_tname("geo")):
            n, u = sync_geo()
            if n or u:
                print(f"Checklist GEO: thêm {n} việc, cập nhật {u} việc")
    except StoreError as e:
        print("Bỏ qua đồng bộ Checklist GEO:", e)
    try:
        n = loi_fill_hints()
        if n:
            print(f"Sửa lỗi từng trang: điền «Cần sửa gì» cho {n} dòng")
    except StoreError as e:
        print("Bỏ qua điền «Cần sửa gì»:", e)
    threading.Thread(target=algo_auto_refresh, daemon=True).start()   # tin thuật toán Google: tự lấy lại mỗi 24 giờ
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Rooty SEO Production · chế độ: {STORE.mode.upper()} · http://localhost:{PORT}")
    srv.serve_forever()


if __name__ == "__main__":
    main()
