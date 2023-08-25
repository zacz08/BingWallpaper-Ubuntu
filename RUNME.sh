#!/bin/bash

CONFIG_FILE="config.yml"
PROJECT_PATH=$(grep "path" "$CONFIG_FILE" | awk -F: '{print $2}' | tr -d '[:space:]')
MODE=$(grep "mode" "$CONFIG_FILE" | awk -F: '{print $2}' | tr -d '[:space:]')
MAIN_PY="$PROJECT_PATH/main.py"

python3 "$MAIN_PY" "$PROJECT_PATH" "$MODE"
