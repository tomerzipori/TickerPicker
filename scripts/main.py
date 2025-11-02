from __future__ import print_function
from auth import spreadsheet_service
from utils import log, iscol

import argparse
import json
from typing import Dict
import requests
from lxml import html

import yfinance as yf

def get_bond_prices(bonds: Dict) -> Dict:
    log("Fetching bond prices...")
    prices = {}
    for bond_name, bond_data in bonds.items():
        try:
            req = requests.get(bond_data["url"])
            tree = html.fromstring(req.text)
            price = float(tree.xpath(bond_data["xpath"])[0].text_content())
            prices[bond_name] = price
            log(f"{bond_name} = {price}")
        except Exception as e:
            log(f"Failed to fetch {bond_name}): {e}")
    log(f"Fetched {len(prices)} prices.")
    return prices


def get_stock_prices(stock2ticker: Dict) -> Dict:
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
        'values': [[prices[price] / 100.0] for price in prices] if iscol(range) else [prices[price] / 100.0 for price in prices]
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
    log("Starting Python script...")
    # Parsing argumnets from bash wrapper
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock2ticker", type=str, required=True, help="Stock 2 Ticker dictionary (json file)")
    parser.add_argument("--bonds", type=str, required=False, default=None, help="Dictionary with data about bonds to fetch with 'requests'")
    parser.add_argument("--sheet-id", type=str, required=True, help="Google Sheet ID")
    parser.add_argument("--sheet-name", type=str, required=True, help="Sheet to write data in")
    parser.add_argument("--cells", type=str, required=True, help="Cell range to write data to")

    arguments = parser.parse_args()

    log(f"Loading stock mapping from {arguments.stock2ticker}")
    with open(arguments.stock2ticker, "r", encoding="utf-8") as f:
        stock2ticker_dict = json.load(f)

    sheet_id = arguments.sheet_id
    range = arguments.sheet_name + "!" + arguments.cells

    # Extract stock prices from Yahoo Finance
    stock_prices = get_stock_prices(stock2ticker_dict)

    # Extract bond prices (if found)
    if arguments.bonds != 'None':
        with open(arguments.bonds, "r", encoding="utf-8") as f:
            bonds_dict = json.load(f)

        bond_prices = get_bond_prices(bonds_dict)
        prices = stock_prices | bond_prices

    elif arguments.bonds == 'None':
        prices = stock_prices
    
    # Write stock prices to Google Sheets
    write_prices(sheet_id=sheet_id, range=range, prices=prices)
    log("Python script completed successfully.")

if __name__ == "__main__":
    main()