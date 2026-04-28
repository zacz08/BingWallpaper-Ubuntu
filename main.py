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


def is_same_image(new_data: bytes, picture_path: str) -> bool:
    if not os.path.exists(picture_path):
        return False
    with open(picture_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest() == hashlib.md5(new_data).hexdigest()


def notify(message: str, title: str = "Bing Wallpaper") -> None:
    """Show a macOS notification via osascript (no extra deps)."""
    safe_msg = message.replace('"', "'")
    safe_title = title.replace('"', "'")
    script = f'display notification "{safe_msg}" with title "{safe_title}"'
    subprocess.run(["/usr/bin/osascript", "-e", script],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def set_wallpaper(picture_path: str) -> None:
    """Set the wallpaper on every desktop/space using AppleScript."""
    abs_path = os.path.abspath(picture_path)
    script = (
        'tell application "System Events" to tell every desktop '
        f'to set picture to "{abs_path}"'
    )
    subprocess.run(["/usr/bin/osascript", "-e", script], check=True)


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
    picture_path = os.path.join(picture_dir, "background.jpg")

    if not wait_for_network():
        notify("No network, will retry on next schedule")
        return 1

    try:
        img_data = get_bing_wallpaper(index=mode)
        if not img_data:
            notify("Failed to fetch image from Bing")
            return 1
        if is_same_image(img_data, picture_path):
            return 0
        with open(picture_path, "wb") as f:
            f.write(img_data)
        set_wallpaper(picture_path)
        notify("Wallpaper updated successfully")
        return 0
    except Exception as e:
        notify(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
