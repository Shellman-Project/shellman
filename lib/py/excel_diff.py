import sys
import pandas as pd
import numpy as np
import re

if len(sys.argv) < 6:
    sys.exit("Usage: excel_diff.py old.xlsx new.xlsx sheet format ignore_case")

old, new, sheet_arg, fmt, ign = sys.argv[1:6]
sheet = int(sheet_arg) if re.fullmatch(r'\d+', sheet_arg) else sheet_arg
ignore_case = (ign.lower() == 'true')

def load(path):
    return pd.read_excel(path, sheet_name=sheet, dtype=str, header=None)

try:
    df_old, df_new = load(old), load(new)
except Exception as e:
    sys.exit(f"Error reading sheets: {e}")

max_rows = max(df_old.shape[0], df_new.shape[0])
max_cols = max(df_old.shape[1], df_new.shape[1])
df_old = df_old.reindex(index=range(max_rows), columns=range(max_cols))
df_new = df_new.reindex_like(df_old)

mask = (df_old != df_new)
if ignore_case:
    casemask = (df_old.fillna('').str.lower() != df_new.fillna('').str.lower())
    mask = mask | casemask

diffs = np.where(mask)
if len(diffs[0]) == 0:
    print("✅  Sheets are identical.")
    sys.exit(0)

def excel_col(n):  # 0‑based -> letters 
    s = ''
    while n >= 0:
        s = chr(n % 26 + 65) + s
        n = n // 26 - 1
    return s

rows = []
for r, c in zip(*diffs):
    cell = f"{excel_col(c)}{r+1}"
    rows.append((str(sheet), cell,
                 '' if pd.isna(df_old.iat[r, c]) else str(df_old.iat[r, c]),
                 '' if pd.isna(df_new.iat[r, c]) else str(df_new.iat[r, c])))


if fmt == 'csv':
    import csv, io
    out = io.StringIO()
    csv.writer(out).writerows([("Sheet", "Cell", "Old", "New"), *rows])
    print(out.getvalue(), end='')
else:  # markdown
    col_widths = [max(map(len, col)) for col in zip(*([("Sheet", "Cell", "Old", "New")] + rows))]
    def fmtrow(r): return "| " + " | ".join(f"{v:{col_widths[i]}}" for i, v in enumerate(r)) + " |"
    print(fmtrow(("Sheet", "Cell", "Old", "New")))
    print(fmtrow(['-'*w for w in col_widths]))
    for r in rows: print(fmtrow(r))
