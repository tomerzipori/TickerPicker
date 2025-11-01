#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root and absolute path from location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Load config values from config.json
CONFIG="${ROOT_DIR}/configs/config.json"

# Log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*";
}

# json reader
get_json_value () {
    python3 -c "import json; print(json.load(open('${CONFIG}'))$1)"
}

RETENTION_DAYS="$(get_json_value "['logging']['retention_days']")"

log "Deleting archived logs older than ${RETENTION_DAYS} days in logs/"
find "${ROOT_DIR}/logs" -type f -name "log-*.txt" -mtime +"${RETENTION_DAYS}" -print -delete || true
log "Completed deleting."