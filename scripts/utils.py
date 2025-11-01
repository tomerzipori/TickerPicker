from datetime import datetime
import re

# Log helper
def log(message: str) -> None:
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

# Check if a Google Sheets range is a row or a column
def iscol(range: str) -> bool:
  start_col = re.search(r"!(\S)", range).group(1) # first character after  "!"
  end_col = re.search(r":(\S)", range).group(1) # first character after ":"
  return start_col.casefold() == end_col.casefold()