#!/usr/bin/env bash

UTILS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Helper function for logging
log() {
    echo "[$(date '+%Y-%m-%d %H-%M-%S')] $*"
}

# json reader
get_json_value () {
    local json_file="$1"
    python3 -c "import json; print(json.load(open('${json_file}'))$2)"
}