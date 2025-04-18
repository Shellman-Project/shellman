#!/usr/bin/env bash
#
# excel_info – quick overview of an Excel file 
# Supports .xlsx .xlsm .xltx .xltm .xlsb   (openpyxl backend)

: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
source "$SHELLMAN_HOME/lib/utils.sh"

show_help() {
  cat <<EOF
Usage:
  shellman excel_info <workbook.xlsx>

Description:
  Prints a table with sheet name, rows and columns for a given Excel file.

Requires:
  python3 + openpyxl   (install via: shellman doctor --fix)

Examples:
  shellman excel_info report.xlsx
  shellman excel_info data.xlsb
EOF
}

FILE="$1"
[[ "$1" == "--help" || -z "$FILE" ]] && { show_help; exit 0; }
[[ ! -f "$FILE" ]] && { error "File not found: $FILE"; exit 1; }

# -------- run embedded Python ---------------------------------
python3 - "$FILE" <<'PY'
import sys, openpyxl
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
print(f"{'Sheet':<20} {'Rows':>7} {'Cols':>6}")
print('-'*34)
for ws in wb.worksheets:
    print(f"{ws.title[:20]:<20} {ws.max_row:>7} {ws.max_column:>6}")
PY
status=$?

if [[ $status -ne 0 ]]; then
  error "Python/openpyxl problem. Run: shellman doctor --fix"
  exit 1
fi
