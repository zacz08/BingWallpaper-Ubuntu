#!/bin/bash
# uninstall.sh — remove the launchd LaunchAgent for Bing Wallpaper.

set -e

LABEL="com.user.bingwallpaper"
TARGET="$HOME/Library/LaunchAgents/$LABEL.plist"

if [ -f "$TARGET" ]; then
    launchctl unload "$TARGET" 2>/dev/null || true
    rm -f "$TARGET"
    echo "Removed $TARGET"
else
    echo "Not installed."
fi
