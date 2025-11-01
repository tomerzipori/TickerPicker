#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root and absolute path from location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Load config values from config.json
CONFIG="${ROOT_DIR}/configs/config.json"

# Source utils.sh for functions
source "${SCRIPT_DIR}/utils.sh"

RETENTION_DAYS="$(get_json_value ${CONFIG} "['logging']['retention_days']")"

log "Deleting archived logs older than ${RETENTION_DAYS} days in logs/"
find "${ROOT_DIR}/logs" -type f -name "log-*.txt" -mtime +"${RETENTION_DAYS}" -print -delete || true
log "Completed deleting."