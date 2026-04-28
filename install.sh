#!/bin/bash
# install.sh — register the daily wallpaper job with launchd.
#
# Reads `path`, `hour`, `minute` from config.yml, renders the plist
# template into ~/Library/LaunchAgents/, and loads it via launchctl.

set -e

# A LaunchAgent must be installed for the *current user*, never as root.
# Running this script via sudo would put a root-owned plist into the user's
# LaunchAgents folder and break later non-sudo runs of RUNME.sh.
if [ "$(id -u)" = "0" ]; then
    echo "ERROR: do NOT run install.sh with sudo." >&2
    echo "       Run it as your normal user: ./install.sh" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.yml"
TEMPLATE="$SCRIPT_DIR/com.user.bingwallpaper.plist"
LABEL="com.user.bingwallpaper"
TARGET="$HOME/Library/LaunchAgents/$LABEL.plist"
UID_NUM="$(id -u)"

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

# Prefer the modern bootstrap/bootout API (10.11+); fall back to load/unload.
if launchctl print "gui/$UID_NUM/$LABEL" >/dev/null 2>&1; then
    launchctl bootout "gui/$UID_NUM/$LABEL" 2>/dev/null || true
fi
launchctl bootstrap "gui/$UID_NUM" "$TARGET" 2>/dev/null \
    || launchctl load -w "$TARGET"
launchctl enable "gui/$UID_NUM/$LABEL" 2>/dev/null || true

echo "Installed LaunchAgent: $TARGET"
echo "Daily run time: ${HOUR}:$(printf '%02d' "$MINUTE")"
echo "Trigger now with: launchctl kickstart -k gui/$UID_NUM/$LABEL"
