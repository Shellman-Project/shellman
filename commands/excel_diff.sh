#!/usr/bin/env bash
#
# excel_diff – show cell‑level differences between two Excel sheets
#
# Needs: python3 + pandas + openpyxl   (→ shellman doctor --fix)
# Works with .xlsx  .xlsm  .xlsb  .xltx  .xltm 
# ----------------------------------------------------------------------

: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
source "$SHELLMAN_HOME/lib/utils.sh"
PY_SCRIPT="$SHELLMAN_HOME/lib/py/excel_diff.py"

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

# ---------- call python script -----------------------------------------
PY_SCRIPT="$SHELLMAN_HOME/lib/py/excel_diff.py"
RES="$(python3 "$PY_SCRIPT" "$OLD" "$NEW" "$SHEET" "$FMT" "$IGNORE_CASE" 2>&1)"
STATUS=$?

if [[ $STATUS -ne 0 ]]; then
  error "$RES"
  exit "$STATUS"
fi


if [[ -n "$OUT" ]]; then
  echo "$RES" > "$OUT"
  info "Diff saved to $OUT"
else
  echo "$RES"
fi

exit 0
