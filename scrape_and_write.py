from __future__ import print_function
from auth import spreadsheet_service
import argparse
import json

import yfinance as yf

STOCK2TICKER = {
    'sp500': 'IS-FF702.TA',
    'europe': 'IS-FF301.TA',
    'EM': 'IS-FF101.TA',
    'TA90': 'TCH-F9.TA'
}

# sheet_id = '1XbtkMfJixvPch5RdGb4b9GXNEIAk90BKr3DTThjq-k4'

def scrape_prices(stock2ticker):
    return {stock: yf.Ticker(ticker).info['regularMarketPrice'] for stock, ticker in stock2ticker.items()}

def write_prices(sheet_id, range, prices):
    body = {
        'values': [[prices[price] / 100.0] for price in prices]
    }
    result = spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=range,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def main():
    # Parsing argumnets from bash wrapper
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock2ticker", type=str, required=True, help="Stock 2 Ticker dictionary (json file)")
    parser.add_argument("--sheet-id", type=str, required=True, help="Google Sheet ID")
    parser.add_argument("--sheet-name", type=str, required=True, help="Sheet to write data in")
    parser.add_argument("--cells", type=str, required=True, help="Cell range to write data to")

    arguments = parser.parse_args()

    stock2ticker_json = arguments.stock2ticker
    with open(stock2ticker_json, "r", encoding="utf-8") as f:
        stock2ticker_dict = json.load(f)

    sheet_id = arguments.sheet_id
    range = arguments.sheet_name + "!" + arguments.cells

    # Extract stock prices
    prices = scrape_prices(stock2ticker_dict)

    # Write stock prices to Google Sheets
    write_prices(sheet_id=sheet_id, range=range, prices=prices)

main()
