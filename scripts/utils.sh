#!/usr/bin/env bash

UTILS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Helper function for logging
log() {
    echo "[$(date '+%Y-%m-%d %H-%M-%S')] $*"
}

# json reader
get_json_value () {
    local json_file="$1"
    local field="$2"
    python3 -c "
import json
dict = json.load(open('${json_file}'))
try:
    res = dict${field}
except Exception:
    res = None
print(res)
"
}