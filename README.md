# :chart_with_upwards_trend: TickerPicker
Fetch stock prices from the Tel Aviv stock exchage, and write them in a Google Sheet.

# Structure
```
├── configs <--- Add credentials.json here
│   ├── config.json
│   └── STOCK2TICKER.json
├── scripts
│   ├── auth.py
|   ├── main.py
|   ├── prune_logs.sh
|   └── rotate_logs.sh
├── requirements.txt
└── run.sh
```

# Setup
```bash
git clone git@github.com:tomerzipori/TickerPicker.git
```

## Google Cloud Console (GCP) and service accounts
Nice tutorial found here: https://www.youtube.com/watch?v=-vBbkrk9sdA&t=29s \
Add your credentials.json for Google service account to the `config` directory.

## Prerequisites (checked only on these, very likely to work on other versions)
- Python 3.13.5/3.12.3
- git 2.47.3/2.43.0

## Customize Configuration
Edit `configs/config.json` to match your Google Sheet: main variables for customiztion are:
- `stock2ticker` - A json file in the `configs` directory mapping stocks names (keys) to tickers (values).
- `sheet` - Three variables specifying the destination Google Sheet:
  - `id` - Google Sheet ID (appearing in the URL at "...spreadsheets/d/<SHEET_ID>/..."
  - `name` - Sheet name in the destination file.
  - `cells` - Range of cells to write the data to. In a Google Sheets/Excel format (e.g "F23:F26").
 
## Run once manually:
```bash
./run.sh
```
On the initial run it will build the required virtual environment and install dependencies.

# Cron Jobs
The script is meant to be schduled, currently tested on Linux's cron. Add those lines to `crontab`:
```bash
# Run hourly, Sun-Thu, 9:00-18:00
0 9-18 * * 0-4 /absolute/path/to/run.sh
```

## Logging
Logging is recommended for scheduled tasks, this repo has supprt for it. First, create a `logs` directory in the project's root:
```bash
mkdir logs
```

Add these lines to `crontab`:
```bash
# Run hourly, Sun-Thu, 9:00-18:00
0 9-18 * * 0-4 /absolute/path/to/root/run.sh >> /absolute/path/to/root/logs/current.log 2>&1

# Rotate logs Sun-Thu at 18:10
10 18 * * 0-4 /absolute/path/to/root/scripts/rotate_logs.sh >> /absolute/path/to/root/logs/current.log 2>&1

# Delete old logs daily
20 18 * * * /absolute/path/to/root/scripts/prune_logs.sh >> /absolute/path/to/root/logs/current.log 2>&1
```

Logs from each run are saved to `current.log`. The second line takes each `current.log` file at the end of the day, converts it to a txt file with the following name structure: `log-YYYY-MM-DD.txt`, and creates a new `current.log` file. The third line deletes each day any logs older then X amount of days (specified in the `logging:retention_days` field on `config.json`).





