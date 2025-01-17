"""
Steps:
1. Run on CSV to produce <name>_temporal.csv
2. Run Layer->Add layer->Add Delimited Text Layer
3. Apply
4. <name>_temporal->Properties->Temporal
5. Enable "Dynamic Temporal Control"
6. Configuration->Single Fields with Date/Time
7. Enable "Accumulate features over time"
8. Apply
9. Temporal Control Panel
10. Enable "Animated temporal navigation"
11. Click "Set to Full Range"
12. Pan through times
"""

import argparse
import csv
from datetime import datetime
import os

parser = argparse.ArgumentParser()
parser.add_argument('src', type=str)
args = parser.parse_args()

src = args.src
dst = format(os.path.splitext(src)[0]) + "_temporal.csv"

with open(src, 'r') as src, open(dst, 'w', newline='') as dst:
    reader = csv.DictReader(src, delimiter=';')
    writer = csv.DictWriter(dst, fieldnames=['time', 'x', 'y', 'ignited'])
    writer.writeheader()
    for row in reader:
        time = int(row['data'].split(':')[0].split(':')[0])
        time = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        data = row['data'].split(':')
        x = data[0]
        y = data[1]
        ignited = data[2]
        if int(ignited) == 0:
            continue
        writer.writerow({'time': time, 'x': x, 'y': y, 'ignited': ignited})