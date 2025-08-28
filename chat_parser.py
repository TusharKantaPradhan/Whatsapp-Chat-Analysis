import pandas as pd
import re

def parse_chat(file):
    text = file.read().decode('utf-8')
    lines = text.split('\n')
    data = []
    for line in lines:
        match = re.match(r'(\d+/\d+/\d+, \d+:\d+ [APM]+) - (.*?): (.*)', line)
        if match:
            date, user, msg = match.groups()
            data.append([date, user, msg])
    return pd.DataFrame(data, columns=['datetime', 'user', 'message'])
