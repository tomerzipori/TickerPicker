#!/usr/bin/env bash
set -euo pipefail

# Helper function for logging
log() {
    echo "[$(date '+%Y-%m-%d %H-%M-%S')] $*"
}

# Error handler
error_handler() {
    log "ERROR in ${BASH_SOURCE[1]} at line ${BASH_LINENO[0]}: '${BASH_COMMAND}'"
    log "Script aborted"
    deactivate >/dev/null 2>&1 || true
    exit 1
}

trap error_handler ERR

# Configuration
VENV_DIR="stocksenv"
PYTHON_SCRIPT="scrape_and_write.py"

## Globals
STOCK2TICKER="STOCK2TICKER.json"
SHEET_ID="1XbtkMfJixvPch5RdGb4b9GXNEIAk90BKr3DTThjq-k4"
SHEET_NAME="DATA"
CELLS="F23:F26"

# Start
log "===== Starting run ====="
log "Python script: ${PYTHON_SCRIPT}"
log "Sheet target: ${SHEET_NAME}!${CELLS}"

# Install Dependencies (if needed)
if [[ ! -d "${VENV_DIR}" ]]; then
    log "Virtual environment not found, creating one at ${VENV_DIR}..."
    python3 -m venv "${VENV_DIR}"
    log "Building virtual environment..."
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
    log "Script finished successfully."
else
    log "Script encountered an error."
fi

# Deactivate Environment
deactivate
log "Deactivating virtual environment."
log "===== Finished run ====="
log "-------------------------------------------------------------------------"