#!/bin/bash
# uninstall.sh — remove the launchd LaunchAgent for Bing Wallpaper.

set -e

if [ "$(id -u)" = "0" ]; then
    echo "ERROR: do NOT run uninstall.sh with sudo." >&2
    exit 1
fi

LABEL="com.user.bingwallpaper"
TARGET="$HOME/Library/LaunchAgents/$LABEL.plist"
UID_NUM="$(id -u)"

launchctl bootout "gui/$UID_NUM/$LABEL" 2>/dev/null || \
    launchctl unload "$TARGET" 2>/dev/null || true

if [ -f "$TARGET" ]; then
    rm -f "$TARGET"
    echo "Removed $TARGET"
else
    echo "Not installed."
fi
