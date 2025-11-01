from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pathlib import Path
import json

with open(Path(__file__).resolve().parents[1] / "configs" / "config.json", "r") as f:
    config = json.load(f)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_file(config["credentials"])

spreadsheet_service = build('sheets', 'v4', credentials=credentials)
drice_service = build('drive', 'v3', credentials=credentials)