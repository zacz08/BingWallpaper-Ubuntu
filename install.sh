#!/bin/bash
# install.sh — register the daily wallpaper job with launchd.
#
# Reads `path`, `hour`, `minute` from config.yml, renders the plist
# template into ~/Library/LaunchAgents/, and loads it via launchctl.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.yml"
TEMPLATE="$SCRIPT_DIR/com.user.bingwallpaper.plist"
LABEL="com.user.bingwallpaper"
TARGET="$HOME/Library/LaunchAgents/$LABEL.plist"

read_cfg() {
    grep -E "^\s*$1\s*:" "$CONFIG_FILE" | head -n1 | awk -F: '{print $2}' | tr -d '[:space:]'
}

PROJECT_PATH="$(read_cfg path)"
HOUR="$(read_cfg hour)"
MINUTE="$(read_cfg minute)"

[ -z "$PROJECT_PATH" ] && PROJECT_PATH="$SCRIPT_DIR"
[ -z "$HOUR" ] && HOUR="9"
[ -z "$MINUTE" ] && MINUTE="0"

chmod +x "$SCRIPT_DIR/RUNME.sh"
mkdir -p "$HOME/Library/LaunchAgents" "$PROJECT_PATH/picture"

# Render the template.
sed -e "s|__PROJECT_PATH__|$PROJECT_PATH|g" \
    -e "s|__HOUR__|$HOUR|g" \
    -e "s|__MINUTE__|$MINUTE|g" \
    "$TEMPLATE" > "$TARGET"

# Reload (unload first, ignore errors when not yet loaded).
launchctl unload "$TARGET" 2>/dev/null || true
launchctl load -w "$TARGET"

echo "Installed LaunchAgent: $TARGET"
echo "Daily run time: ${HOUR}:$(printf '%02d' "$MINUTE")"
echo "Trigger now with: launchctl start $LABEL"
