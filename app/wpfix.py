"""
Sửa lỗi trên WordPress qua REST API (cần Mật khẩu ứng dụng của một tài khoản Biên tập viên trở lên).

Hiện có: gỡ LINK TỰ THÂN — thẻ <a> trong thân bài trỏ về chính URL của bài (không tính link mục lục #).
Gỡ thẻ link, GIỮ NGUYÊN chữ. WordPress tự lưu bản sửa đổi (Revisions) nên mỗi bài đều quay lại được.
"""
from __future__ import annotations

import base64
import json
import re
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; RootySEO/1.0)"
A_TAG = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.I | re.S)
HREF = re.compile(r"""\bhref\s*=\s*(["'])(.*?)\1""", re.I | re.S)


class WPError(Exception):
    pass


def _path(u):
    p = urllib.parse.urlsplit(u)
    return (p.netloc.lower().removeprefix("www."), p.path.rstrip("/").lower())


def _req(method, url, auth=None, body=None, timeout=40):
    h = {"User-Agent": UA, "Accept": "application/json"}
    data = None
    if auth:
        h["Authorization"] = h["X-Rooty-Auth"] = "Basic " + base64.b64encode(f"{auth[0]}:{auth[1]}".encode()).decode()
        # X-Rooty-Auth: dự phòng khi hosting cắt header Authorization (cài scripts/wordpress/rooty-app-password-header.php)
    if body is not None:
        data = json.dumps(body).encode()
        h["Content-Type"] = "application/json; charset=utf-8"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method, headers=h), timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode("utf-8", "replace")).get("message", "")
        except Exception:
            msg = ""
        raise WPError(f"WordPress trả {e.code}: {re.sub('<[^>]+>', '', msg)[:200]}")


def find_item(url, auth=None):
    """URL bài/trang → (gốc REST, loại 'posts'|'pages', id). Thử cả gốc có tiền tố ngôn ngữ (/en/…) như blogscan."""
    sp = urllib.parse.urlsplit(url)
    site = f"{sp.scheme}://{sp.netloc}"
    parts = [x for x in sp.path.split("/") if x]
    if not parts:
        return None
    slug = urllib.parse.unquote(parts[-1])
    bases = [site]
    if len(parts) > 1 and re.fullmatch(r"[a-z]{2}(-[a-z]+)?", parts[0]):
        bases.insert(0, f"{site}/{parts[0]}")
    want = _path(url)
    for base in bases:
        for kind in ("posts", "pages"):
            try:
                items = _req("GET", f"{base}/wp-json/wp/v2/{kind}?slug={urllib.parse.quote(slug)}&status=publish&_fields=id,link", auth)
            except WPError:
                continue
            for it in items if isinstance(items, list) else []:
                if _path(it.get("link", "")) == want:
                    return base, kind, it["id"]
    return None


def who_am_i(base, auth):
    """Bị từ chối sửa bài → hỏi WordPress tài khoản đang đăng nhập là ai, để nói đúng lý do."""
    try:
        me = _req("GET", f"{base}/wp-json/wp/v2/users/me?context=edit&_fields=name,username,roles", auth)
    except WPError as e:
        return ("WordPress không nhận tài khoản (" + str(e)[:120] + "): kiểm WP_USER = tên đăng nhập, WP_APP_PASSWORD = Mật khẩu ứng dụng "
                "(không phải mật khẩu đăng nhập); nếu đúng cả hai thì plugin bảo mật/hosting đang chặn đăng nhập kiểu Mật khẩu ứng dụng")
    roles = ", ".join(me.get("roles") or []) or "không rõ"
    return (f"Đăng nhập được bằng «{me.get('username') or me.get('name')}» (vai trò: {roles}) nhưng không đủ quyền sửa bài này — "
            "cần vai trò Biên tập viên (editor) hoặc Quản trị viên")


def strip_self_links(html, page_url):
    """Gỡ <a> trỏ về chính trang (bỏ qua #mục lục) → (html mới, [anchor đã gỡ])."""
    me = _path(page_url)
    removed = []

    def sub(m):
        hm = HREF.search(m.group(1))
        if not hm:
            return m.group(0)
        href = hm.group(2).strip()
        if not href or href.startswith("#"):
            return m.group(0)
        full = urllib.parse.urljoin(page_url, href)
        if "#" in href or _path(full.split("#")[0]) != me:
            return m.group(0)
        removed.append(re.sub(r"<[^>]+>", "", m.group(2)).strip()[:80])
        return m.group(2)
    return A_TAG.sub(sub, html), removed


def fix_self_links(url, auth, apply=True):
    """Một bài: đọc nội dung gốc (context=edit), gỡ link tự thân, ghi lại nếu apply. → dict kết quả."""
    found = find_item(url, auth)
    if not found:
        raise WPError("Không tìm thấy bài/trang trên WordPress REST (có thể là trang sản phẩm/WooCommerce hoặc đã đổi URL)")
    base, kind, pid = found
    if not auth:   # chưa có mật khẩu ứng dụng → chỉ xem trước trên nội dung hiển thị công khai
        item = _req("GET", f"{base}/wp-json/wp/v2/{kind}/{pid}?_fields=id,link,content")
        _, removed = strip_self_links((item.get("content") or {}).get("rendered") or "", item.get("link") or url)
        return {"id": pid, "kind": kind, "removed": removed, "applied": False}
    try:
        item = _req("GET", f"{base}/wp-json/wp/v2/{kind}/{pid}?context=edit&_fields=id,link,content", auth)
    except WPError as e:
        if " 401" in str(e) or " 403" in str(e):
            raise WPError(who_am_i(base, auth))
        raise
    raw = ((item.get("content") or {}).get("raw")) or ""
    if not raw:
        raise WPError("Không đọc được nội dung gốc (tài khoản cần quyền Biên tập viên trở lên)")
    new, removed = strip_self_links(raw, item.get("link") or url)
    if removed and apply:
        _req("POST", f"{base}/wp-json/wp/v2/{kind}/{pid}", auth, {"content": new})
    return {"id": pid, "kind": kind, "removed": removed, "applied": bool(removed and apply)}
