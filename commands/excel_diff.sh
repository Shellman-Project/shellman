#!/usr/bin/env bash
#
# excel_diff – show cell‑level differences between two Excel sheets
#
# Needs: python3 + pandas + openpyxl   (→ shellman doctor --fix)
# Works with .xlsx  .xlsm  .xlsb  .xltx  .xltm 
# ----------------------------------------------------------------------

: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
source "$SHELLMAN_HOME/lib/utils.sh"

show_help() {
cat <<'EOF'
Usage:
  shellman excel_diff <old.xlsx> <new.xlsx> [options]

Options:
  --sheet <n|name>   Compare only this sheet     (default: first sheet)
  --format csv|md    Output format               (default: md = Markdown)
  --out <file>       Save result instead of printing
  --ignore-case      Ignore text‑case differences
  --help             This help screen

Result columns:
  Sheet | Cell | Old value | New value
EOF
}

# ---------- defaults ----------------------------------------------------
OLD=""; NEW=""; SHEET="0"; OUT=""; FMT="md"; IGNORE_CASE=false
# ------------------------------------------------------------------------

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --help) show_help; exit 0 ;;
    --sheet)       SHEET="$2"; shift ;;
    --format)      FMT="$2"; shift ;;
    --out)         OUT="$2"; shift ;;
    --ignore-case) IGNORE_CASE=true ;;
    -* ) error "Unknown option: $1"; show_help; exit 1 ;;
    *  ) [[ -z "$OLD" ]] && OLD="$1" || { [[ -z "$NEW" ]] && NEW="$1" || { error "Too many positional args"; exit 1; }; } ;;
  esac; shift
done

[[ -z "$OLD" || -z "$NEW" ]] && { error "Need <old.xlsx> and <new.xlsx>"; exit 1; }
[[ ! -f $OLD || ! -f $NEW ]] && { error "File missing."; exit 1; }
case "$FMT" in csv|md) ;; *) error "--format must be csv or md"; exit 1 ;; esac
command -v python3 >/dev/null || { error "python3 not found"; exit 1; }

# ---------- run embedded python ----------------------------------------
RES="$(python3 - "$OLD" "$NEW" "$SHEET" "$FMT" "$IGNORE_CASE" 2>&1)" || {
  error "$RES"; exit 1; }

if [[ -n "$OUT" ]]; then
  echo "$RES" > "$OUT"
  info "Diff saved to $OUT"
else
  echo "$RES"
fi

exit 0
##########################################################################
python <<'PY'
import sys, pandas as pd, numpy as np, openpyxl, re, itertools
old, new, sheet_arg, fmt, ign = sys.argv[1:6]
sheet = int(sheet_arg) if re.fullmatch(r'\d+', sheet_arg) else sheet_arg
ignore_case = (ign.lower() == 'true')

def load(path):
    df = pd.read_excel(path, sheet_name=sheet, dtype=str, header=None)
    return df

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
    rows.append((sheet, cell,
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
PY
