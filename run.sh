#!/usr/bin/env bash

set -euo pipefail

# Configuration
VENV_DIR="stocksenv"
PYTHON_SCRIPT="scrape_and_write.py"

## Globals
STOCK2TICKER="STOCK2TICKER.json"
SHEET_ID="1XbtkMfJixvPch5RdGb4b9GXNEIAk90BKr3DTThjq-k4"
SHEET_NAME="DATA"
CELLS="F23:F26"

# Install Dependencies (if needed)
if [[ ! -d "${VENV_DIR}" ]]; then
    echo "Virtual environment not found, creating one at ${VENV_DIR}..."
    python3 -m venv "${VENV_DIR}"
    echo "Building virtual environment..."
    source "${VENV_DIR}/bin/activate"
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
else
    echo "Virtual environment found at ${VENV_DIR}."
fi

# Activate Environment
source "${VENV_DIR}/bin/activate"

# Run Script
echo "Running script..."
python3 "${PYTHON_SCRIPT}" --stock2ticker "${STOCK2TICKER}" --sheet-id "${SHEET_ID}" --sheet-name "${SHEET_NAME}" --cells "${CELLS}"

# Deactivate Environment
deactivate
echo "Done."