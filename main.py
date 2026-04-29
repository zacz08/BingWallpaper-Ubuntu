#!/usr/bin/env python3
"""
Bing daily wallpaper for macOS.

Uses only the Python standard library, so it runs with the
system /usr/bin/python3 — no pip packages required.
Sets the desktop wallpaper through AppleScript via `osascript`.
"""

from __future__ import annotations  # allow `X | None` on system Python 3.9

import hashlib
import json
import os
import ssl
import subprocess
import sys
import time
from urllib.request import Request, urlopen


BING_API = "https://www.bing.com/HPImageArchive.aspx?format=js&idx={idx}&n=1&mkt=zh-CN"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X) BingWallpaper/1.0"


def _http_get(url: str, timeout: int = 20) -> bytes:
    req = Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    with urlopen(req, timeout=timeout, context=ctx) as resp:
        return resp.read()


def get_bing_wallpaper(index: str = "0", resolution: str = "UHD") -> bytes | None:
    """Fetch Bing wallpaper image bytes for the given archive index."""
    meta = json.loads(_http_get(BING_API.format(idx=index)).decode("utf-8"))
    if not meta.get("images"):
        return None
    raw_url = meta["images"][0]["url"]
    url_no_params = raw_url.split("&")[0]
    url_base = url_no_params.rsplit("_", 1)[0]
    return _http_get(f"https://www.bing.com{url_base}_{resolution}.jpg")


def is_same_image(new_data: bytes, picture_dir: str) -> str | None:
    """Return the path of an existing wallpaper file with identical bytes,
    or None. We compare against any *.jpg in `picture_dir` so that the
    timestamp-based filenames still de-duplicate correctly.
    """
    new_md5 = hashlib.md5(new_data).hexdigest()
    if not os.path.isdir(picture_dir):
        return None
    for name in os.listdir(picture_dir):
        if not name.lower().endswith(".jpg"):
            continue
        path = os.path.join(picture_dir, name)
        try:
            with open(path, "rb") as f:
                if hashlib.md5(f.read()).hexdigest() == new_md5:
                    return path
        except OSError:
            continue
    return None


def notify(message: str, title: str = "Bing Wallpaper") -> None:
    """Show a macOS notification via osascript (no extra deps)."""
    safe_msg = message.replace('"', "'")
    safe_title = title.replace('"', "'")
    script = f'display notification "{safe_msg}" with title "{safe_title}"'
    subprocess.run(["/usr/bin/osascript", "-e", script],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def set_wallpaper(picture_path: str) -> None:
    """Set the wallpaper on every desktop/space using AppleScript.

    Uses `POSIX file` form which is the most reliable across recent
    macOS releases. Captures stderr so AppleScript permission errors
    surface as a notification instead of failing silently.
    """
    abs_path = os.path.abspath(picture_path)
    safe_path = abs_path.replace('"', '\\"')
    script = (
        'tell application "System Events" to tell every desktop '
        f'to set picture to POSIX file "{safe_path}"'
    )
    result = subprocess.run(
        ["/usr/bin/osascript", "-e", script],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        err = (result.stderr or "").strip() or "osascript failed"
        raise RuntimeError(f"set wallpaper failed: {err}")


def wait_for_network(timeout: int = 60) -> bool:
    """Wait until Bing is reachable (helps when fired right after wake)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            _http_get("https://www.bing.com/", timeout=5)
            return True
        except Exception:
            time.sleep(3)
    return False


def read_config(config_path: str) -> dict:
    """Tiny `key: value` parser so we don't depend on PyYAML."""
    cfg = {}
    if not os.path.exists(config_path):
        return cfg
    with open(config_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if not line or ":" not in line:
                continue
            k, v = line.split(":", 1)
            cfg[k.strip()] = v.strip()
    return cfg


def main() -> int:
    if len(sys.argv) != 3:
        notify("Argument error: expected <project_path> <mode>")
        return 1

    project_path, mode = sys.argv[1], sys.argv[2]
    picture_dir = os.path.join(project_path, "picture")
    os.makedirs(picture_dir, exist_ok=True)

    if not wait_for_network():
        notify("No network, please retry")
        return 1

    try:
        img_data = get_bing_wallpaper(index=mode)
        if not img_data:
            notify("Failed to fetch image from Bing")
            return 1

        # macOS caches wallpapers by file PATH: re-setting the same path
        # with new content does NOT refresh the desktop. Workaround: save
        # each new image under a unique timestamped filename, point the
        # wallpaper at that new path, then prune old files.
        existing = is_same_image(img_data, picture_dir)
        if existing:
            # Same content as something we already have — but maybe it
            # isn't the currently-set wallpaper. Force a re-set anyway.
            picture_path = existing
        else:
            picture_path = os.path.join(
                picture_dir, f"background_{int(time.time())}.jpg"
            )
            with open(picture_path, "wb") as f:
                f.write(img_data)

        set_wallpaper(picture_path)

        # Keep only the file we just used; delete the rest.
        for name in os.listdir(picture_dir):
            if not name.lower().endswith(".jpg"):
                continue
            p = os.path.join(picture_dir, name)
            if p != picture_path:
                try:
                    os.remove(p)
                except OSError:
                    pass

        notify("Wallpaper updated successfully")
        return 0
    except Exception as e:
        notify(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
