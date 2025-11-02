# 📈 TickerPicker
![GitHub repo size](https://img.shields.io/github/repo-size/tomerzipori/TickerPicker)

Fetching stock prices from international stock exchages, and writing them in a Google Sheet. This repo can run fairly good on a RapsberryPi Zero 2 W.

# 📁 Repository Structure
```
├── configs <--- Add credentials.json here
│   ├── config.json
│   ├── STOCK2TICKER.json
|   └── bonds.json
├── scripts
│   ├── auth.py
|   ├── main.py
|   ├── prune_logs.sh
|   └── rotate_logs.sh
├── requirements.txt
└── run.sh
```

# 💿 Setup

## ♊ Google Cloud Console (GCP) and service accounts
Nice tutorial found [here](https://www.youtube.com/watch?v=-vBbkrk9sdA&t=29s). \
Add your credentials.json for Google service account to the `config` directory.

## 👩‍🔧 Prerequisites (checked only on these, very likely to work on other versions)
- Python 3.13.5/3.12.3
- git 2.47.3/2.43.0

## 💾 Installation
```bash
git clone git@github.com:tomerzipori/TickerPicker.git
```

## Customize Configuration
Rename `config_example.json` to `config.json` and edit it to match your Google Sheet: main variables for customiztion are:
- `stock2ticker` - A json file in the `configs` directory mapping stocks names (keys) to tickers (values).
- `bonds` - A json file in the `configs` directory mapping bonds (or any other stock listed online) to a dictionary with URL and XPATH fields - *Optional*.
- `sheet` - Three variables specifying the destination Google Sheet:
  - `id` - Google Sheet ID (appearing in the URL at "...spreadsheets/d/<SHEET_ID>/..."
  - `name` - Sheet name in the destination file.
  - `cells` - Range of cells to write the data to. In a Google Sheets/Excel format (e.g "F23:F26").
 
## 🚀 Run at least once manually:
```bash
./run.sh
```
Required virtual environment and dependencies are built and installed on initial run.

# ⏲️ Cron Jobs
The script is meant to be scheduled, currently tested on Linux's cron only. Add those lines to `crontab`:
```bash
# Run hourly, Sun-Thu, 9:00-18:00
0 9-18 * * 0-4 cd /absolute/path/to/root && ./run.sh
```

## 🗒️ Logging
Logging is recommended for scheduled tasks, this repo has support for it. First, create a `logs` directory in the project's root:
```bash
mkdir logs
```

Add these lines to `crontab`:
```bash
# Run hourly, Sun-Thu, 9:00-18:00
0 9-18 * * 0-4 cd /absolute/path/to/root && ./run.sh >> /absolute/path/to/root/logs/current.log 2>&1

# Rotate logs Sun-Thu at 18:10
10 18 * * 0-4 cd /absolute/path/to/root/scripts && ./rotate_logs.sh >> /absolute/path/to/root/logs/current.log 2>&1

# Delete old logs daily
20 18 * * * cd /absolute/path/to/root/scripts && ./prune_logs.sh >> /absolute/path/to/root/logs/current.log 2>&1
```

Logs from each run are saved to `current.log`. The second line takes each `current.log` file at the end of the day, converts it to a txt file with the following name structure: `log-YYYY-MM-DD.txt`, and creates a new `current.log` file. The third line deletes each day any logs older then X amount of days (specified in the `logging:retention_days` field on `config.json`).

### Example log for a successful run
```
[2025-11-01 12-50-58] ===== Starting run =====
[2025-11-01 12-50-58] Python script: scripts/main.py
[2025-11-01 12-50-58] Sheet target: DATA!F23:F26
[2025-11-01 12-50-58] Virtual environment found at stocksenv.
[2025-11-01 12-50-58] Activating virtual environment...
[2025-11-01 12-50-58] Running scripts/main.py...
[2025-11-01 12:50:59] Starting Python script...
[2025-11-01 12:50:59] Loading stock mapping from configs/STOCK2TICKER.json
[2025-11-01 12:50:59] Fetching stock prices...
[2025-11-01 12:51:00] sp500 (IS-FF702.TA) = 239140.0
[2025-11-01 12:51:01] europe (IS-FF301.TA) = 34260.0
[2025-11-01 12:51:01] EM (IS-FF101.TA) = 14640.0
[2025-11-01 12:51:02] TA90 (TCH-F9.TA) = 3284.0
[2025-11-01 12:51:02] Fetched 4 prices.
[2025-11-01 12:51:02] Writing prices to Google Sheet range 'DATA!F23:F26'...
[2025-11-01 12:51:03] 4 cells updated successfully.
[2025-11-01 12:51:03] Python script completed successfully.
[2025-11-01 12-51-03] Bash script completed successfully.
[2025-11-01 12-51-03] Deactivating virtual environment.
[2025-11-01 12-51-03] ===== Finished run =====
[2025-11-01 12-51-03] -------------------------------------------------------------------------
```

# 🗺️ Things left to do
- Add some kind of `build` or `verify` script to "compile" and check repo before run. For example, if number of stocks extracted fits in the cell range on destination.
- Additional functionalities like time-series of stock prices etc...
- Create dashboard for checking logs more conveniently (?)
