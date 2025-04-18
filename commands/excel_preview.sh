#!/usr/bin/env bash
#
# excel_preview – quick view of selected rows/columns from an Excel sheet
# 
# Needs: python3 + xlsx2csv   (install via `shellman doctor --fix`)
# Supports .xlsx  .xlsm  .xlsb  .xltx  .xltm
# ----------------------------------------------------------------------

: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
source "$SHELLMAN_HOME/lib/utils.sh"

show_help() {
cat <<EOF
Usage:
  shellman excel_preview <file.xlsx> [options]

Options:
  --sheet <n|name>   Sheet number (1‑based) or sheet name       [1]
  --rows  <N>        Show only first N rows                     [20]
  --columns A,C-E    Show only chosen columns (letters/ranges)  [all]
  --output <csv>     Save result to CSV (no live preview)
  --interactive      Pipe preview to less -S  (auto ON unless --output)
  --help             This help screen
EOF
}

# ---------- defaults --------------------------------------------------
FILE=""; SHEET="1"; ROWS="20"; COL_SPEC=""; OUT_FILE=""; INTERACTIVE=true
# ----------------------------------------------------------------------

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --help) show_help; exit 0 ;;
    --sheet) shift; SHEET=""
             while [[ $# -gt 0 && "$1" != --* ]]; do
               SHEET+="${SHEET:+ }$1"; shift; done; continue ;;
    --rows)      ROWS="$2"; shift ;;
    --columns)   COL_SPEC="$2"; shift ;;
    --output)    OUT_FILE="$2"; INTERACTIVE=false; shift ;;
    --interactive) INTERACTIVE=true ;;
    -* ) error "Unknown option: $1"; show_help; exit 1 ;;
    *  ) [[ -z "$FILE" ]] && FILE="$1" || { error "Unexpected arg: $1"; exit 1; } ;;
  esac; shift
done

[[ -z "$FILE" ]]      && { error "No Excel file given."; exit 1; }
[[ ! -f "$FILE" ]]    && { error "File not found: $FILE"; exit 1; }
command -v xlsx2csv >/dev/null || { error "xlsx2csv not installed. Run: shellman doctor --fix"; exit 1; }

# ---------- xlsx2csv command -----------------------------------------
CMD=(xlsx2csv)
if [[ "$SHEET" =~ ^[0-9]+$ ]]; then
  CMD+=(-s "$SHEET")           # numeric id
else
  CMD+=(--sheetname "$SHEET")  # name
fi
CMD+=("$FILE")

# ---------- helpers for columns --------------------------------------
letter_to_num() { local s="${1^^}" n=0; for ((i=0;i<${#s};i++)); do
  n=$(( n*26 + $(printf '%d' "'${s:i:1}") - 64 )); done; echo "$n"; }

build_num_list() {                   # A,C-E → 1,3,5
  local spec="$1" part list=""
  IFS=',' read -ra parts <<< "$spec"
  for part in "${parts[@]}"; do
    if [[ "$part" == *-* ]]; then
      local a=${part%-*} b=${part#*-}
      a=$(letter_to_num "$a"); b=$(letter_to_num "$b")
      for ((i=a;i<=b;i++)); do list+="${list:+,}$i"; done
    else list+="${list:+,}$(letter_to_num "$part")"
    fi
  done; echo "$list"
}

AWK_FILTER=''
if [[ -n "$COL_SPEC" ]]; then
  NUMS=$(build_num_list "$COL_SPEC")          # e.g. 1,3,5
  read -r -d '' AWK_FILTER <<'AWK'
BEGIN{FS=OFS=","; split(num,k,","); for(i in k) keep[k[i]]=1}
{
  out="";
  for(i=1;i<=NF;i++) if(keep[i]) out = (out=="" ? $i : out OFS $i);
  print out
}
AWK
fi

# ---------- run -------------------------------------------------------
TMP=$(mktemp)

# run pipeline: xlsx2csv | head | (optional awk) -> TMP
if [[ -z "$AWK_FILTER" ]]; then
  "${CMD[@]}" | head -n "$ROWS" > "$TMP"
else
  "${CMD[@]}" | head -n "$ROWS" | awk -v num="$NUMS" "$AWK_FILTER" > "$TMP"
fi

# ---------- output / preview -----------------------------------------
if [[ -n "$OUT_FILE" ]]; then
  mv "$TMP" "$OUT_FILE"
  info "Saved to $OUT_FILE"
  $INTERACTIVE && less -S "$OUT_FILE"
else
  $INTERACTIVE && less -S "$TMP" || cat "$TMP"
  rm -f "$TMP"
fi

