#!/bin/bash
# RUNME.sh — fetch today's Bing image and set it as the macOS wallpaper.
# Uses the system Python 3 shipped with macOS (no virtualenv, no pip).

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.yml"

# Tiny YAML reader: only handles `key: value` lines.
read_cfg() {
    grep -E "^\s*$1\s*:" "$CONFIG_FILE" | head -n1 | awk -F: '{print $2}' | tr -d '[:space:]'
}

PROJECT_PATH="$(read_cfg path)"
MODE="$(read_cfg mode)"

# Fall back to the script directory if `path` is not set.
[ -z "$PROJECT_PATH" ] && PROJECT_PATH="$SCRIPT_DIR"
[ -z "$MODE" ] && MODE="0"

exec /usr/bin/python3 "$PROJECT_PATH/main.py" "$PROJECT_PATH" "$MODE"
