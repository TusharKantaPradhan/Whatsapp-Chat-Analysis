import re
from datetime import datetime
import pandas as pd

# Typical WhatsApp export pattern:
# "12/25/20, 9:15 PM - Alice: Message text"
# or "25/12/2020, 21:15 - Alice: Message text" depending on locale.
DATETIME_PATTERN = r'^\[?\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4},? \d{1,2}:\d{2}(?: ?:? ?[APMapm\.]{2,4})?\]? - '

def _is_new_message(line: str):
    return re.match(DATETIME_PATTERN, line) is not None

def parse_chat(path: str, datetime_formats=None):
    """
    Parse WhatsApp exported chat text file into a DataFrame with columns:
    ['datetime','author','message']
    """
    if datetime_formats is None:
        datetime_formats = [
            "%d/%m/%y, %I:%M %p", "%d/%m/%Y, %I:%M %p",
            "%m/%d/%y, %I:%M %p", "%m/%d/%Y, %I:%M %p",
            "%d/%m/%y, %H:%M", "%d/%m/%Y, %H:%M",
            "%m/%d/%y, %H:%M", "%m/%d/%Y, %H:%M"
        ]
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    messages = []
    buffer = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if _is_new_message(line):
            # flush buffer
            if buffer:
                messages.append(buffer)
            # split datetime and rest
            try:
                dt_str, rest = line.split(" - ", 1)
            except ValueError:
                continue
            # parse datetime robustly
            dt = None
            for fmt in datetime_formats:
                try:
                    dt = datetime.strptime(dt_str.strip("[] "), fmt)
                    break
                except Exception:
                    continue
            if dt is None:
                # fallback: try iso
                try:
                    dt = datetime.fromisoformat(dt_str.strip("[] "))
                except Exception:
                    dt = None
            # author and message
            if ": " in rest:
                author, msg = rest.split(": ", 1)
            else:
                author, msg = None, rest
            buffer = {"datetime": dt, "author": author, "message": msg}
        else:
            # continuation of previous message
            if buffer:
                buffer['message'] += " " + line
    if buffer:
        messages.append(buffer)
    df = pd.DataFrame(messages)
    # attempt to fill missing datetimes with forward fill
    if df['datetime'].isnull().any():
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    return df
