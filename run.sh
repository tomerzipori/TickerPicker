#!/usr/bin/env bash
set -euo pipefail

# Get the path to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source utils.sh for functions
source "${SCRIPT_DIR}/scripts/utils.sh"

# Error handler
error_handler() {
    log "ERROR in ${BASH_SOURCE[1]} at line ${BASH_LINENO[0]}: '${BASH_COMMAND}'"
    log "Script aborted"
    deactivate >/dev/null 2>&1 || true
    exit 1
}

trap error_handler ERR

# Load config values from config.json
CONFIG="configs/config.json"

# General Configuration
VENV_DIR=$(get_json_value ${CONFIG} "['venv_dir']")
PYTHON_SCRIPT=$(get_json_value ${CONFIG} "['python_script']")

## Python Arguments
STOCK2TICKER=$(get_json_value ${CONFIG} "['stock2ticker']")
SHEET_ID=$(get_json_value ${CONFIG} "['sheet']['id']")
SHEET_NAME=$(get_json_value ${CONFIG} "['sheet']['name']")
CELLS=$(get_json_value ${CONFIG} "['sheet']['cells']")

# Start
log "===== Starting run ====="
log "Python script: ${PYTHON_SCRIPT}"
log "Sheet target: ${SHEET_NAME}!${CELLS}"

# Install Dependencies (if needed)
if [[ ! -d "${VENV_DIR}" ]]; then
    log "Virtual environment not found, creating one at ${VENV_DIR}..."
    python3 -m venv "${VENV_DIR}"
    log "Installing dependencies..."
    source "${VENV_DIR}/bin/activate"
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
    log "Virtual environment created successfully."
else
    log "Virtual environment found at ${VENV_DIR}."
fi

# Activate Environment
log "Activating virtual environment..."
source "${VENV_DIR}/bin/activate"

# Run Script
log "Running ${PYTHON_SCRIPT}..."
if python3 "${PYTHON_SCRIPT}" \
    --stock2ticker "${STOCK2TICKER}" \
    --sheet-id "${SHEET_ID}" \
    --sheet-name "${SHEET_NAME}" \
    --cells "${CELLS}"; then
    log "Bash script completed successfully."
else
    log "Script encountered an error."
fi

# Deactivate Environment
deactivate
log "Deactivating virtual environment."
log "===== Finished run ====="
log "-------------------------------------------------------------------------"