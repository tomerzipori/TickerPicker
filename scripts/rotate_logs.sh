#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root and absolute path from location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*";
}

CURRENT_LOG="${ROOT_DIR}/logs/current.log"
ARCHIVE="${ROOT_DIR}/logs/log-$(date +\%Y-\%m-\%d).txt"

if [[ -f "${CURRENT_LOG}" && -s "${CURRENT_LOG}" ]]; then
    log "Rotating ${CURRENT_LOG} to logs/log-$(date +\%Y-\%m-\%d).txt"

    # Moving ang renaming the current log
    mv "${CURRENT_LOG}" "${ARCHIVE}"
else
    log "No rotation needed."
fi

# Create new log file
touch "${CURRENT_LOG}"
log "Created fresh ${CURRENT_LOG}."