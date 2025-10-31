from __future__ import print_function
from auth import spreadsheet_service

import argparse
import json
from typing import Dict
from datetime import datetime

import yfinance as yf

# Helper function for logging
def log(message: str) -> None:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def scrape_prices(stock2ticker: Dict) -> Dict:
    log("Fetching stock prices...")
    prices = {}
    for stock, ticker in stock2ticker.items():
        try:
            data = yf.Ticker(ticker)
            price = data.info.get("regularMarketPrice")
            if price is None:
                raise ValueError("No regularMarketPrice field found.")
            prices[stock] = price
            log(f"{stock} ({ticker}) = {price}")
        except Exception as e:
            log(f"Failed to fetch {stock} ({ticker}): {e}")
    log(f"Fetched {len(prices)} prices.")
    return prices

def write_prices(sheet_id: str, range: str, prices: Dict) -> None:
    log(f"Writing prices to Google Sheet range '{range}'...")
    body = {
        'values': [[prices[price] / 100.0] for price in prices]
    }
    try:
        result = spreadsheet_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=range,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        log(f"{result.get('updatedCells')} cells updated successfully.")
    except Exception as e:
        log(f"Error while writing to sheet: {e}")


def main():
    log("Starting script...")
    # Parsing argumnets from bash wrapper
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock2ticker", type=str, required=True, help="Stock 2 Ticker dictionary (json file)")
    parser.add_argument("--sheet-id", type=str, required=True, help="Google Sheet ID")
    parser.add_argument("--sheet-name", type=str, required=True, help="Sheet to write data in")
    parser.add_argument("--cells", type=str, required=True, help="Cell range to write data to")

    arguments = parser.parse_args()

    log(f"Loading stock mapping from {arguments.stock2ticker}")
    with open(arguments.stock2ticker, "r", encoding="utf-8") as f:
        stock2ticker_dict = json.load(f)

    sheet_id = arguments.sheet_id
    range = arguments.sheet_name + "!" + arguments.cells

    # Extract stock prices
    prices = scrape_prices(stock2ticker_dict)

    # Write stock prices to Google Sheets
    write_prices(sheet_id=sheet_id, range=range, prices=prices)
    log("Script completed successfully.")

if __name__ == "__main__":
    main()