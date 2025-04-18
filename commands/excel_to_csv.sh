#!/usr/bin/env bash
#
# excel_to_csv – export one or more sheets (or slices) to CSV
# 
# Needs: python3 + xlsx2csv      (→ shellman doctor --fix)
# Works with: .xlsx .xlsm .xlsb .xltx .xltm
# -------------------------------------------------------------------------

: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
source "$SHELLMAN_HOME/lib/utils.sh"

show_help() { cat <<'EOF'
Usage:
  shellman excel_to_csv <file.xlsx> [options]

Options:
  --sheets <list>   Sheet names / numbers (comma)          [ALL]
  --rows <a-b>      Keep only rows a‑b                     [ALL]
  --columns A,C‑E   Keep only chosen columns               [ALL]
  --out <dir>       Output directory                       [./csv]
  --overwrite       Replace files even with timestamp
  --help            This help screen
EOF
}

# ------ defaults --------------------------------------------------------
FILE=""; SHEETS=""; ROW_RANGE=""; COL_SPEC=""; OUT_DIR="./csv"; OVERWRITE=false
# ------------------------------------------------------------------------

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --help) show_help; exit 0 ;;
    --sheets)  shift; SHEETS=""; while [[ $# -gt 0 && "$1" != --* ]]; do
                 SHEETS+="${SHEETS:+ }$1"; shift; done; continue ;;
    --rows)    ROW_RANGE="$2"; shift ;;
    --columns) COL_SPEC="$2"; shift ;;
    --out)     OUT_DIR="$2"; shift ;;
    --overwrite) OVERWRITE=true ;;
    -* ) error "Unknown option: $1"; show_help; exit 1 ;;
    *  ) [[ -z "$FILE" ]] && FILE="$1" || { error "Unexpected arg: $1"; exit 1; } ;;
  esac; shift
done

[[ -z "$FILE" ]] && { error "No Excel file given."; exit 1; }
[[ ! -f "$FILE" ]] && { error "File not found: $FILE"; exit 1; }
command -v xlsx2csv >/dev/null || { error "xlsx2csv not installed. Run: shellman doctor --fix"; exit 1; }
mkdir -p "$OUT_DIR"

# ------ helpers ---------------------------------------------------------
sanitize() { echo "$1" | tr ' /' '__' | tr -cd '[:alnum:]_-' ; }
letter_to_num() { local s="${1^^}" n=0; for ((i=0;i<${#s};i++)); do
  n=$(( n*26 + $(printf '%d' "'${s:i:1}") - 64 )); done; echo "$n"; }
build_num_list() { local list=""; IFS=',' read -ra p <<< "$1"
  for part in "${p[@]}"; do
    if [[ "$part" == *-* ]]; then
      local a=$(letter_to_num "${part%-*}") b=$(letter_to_num "${part#*-}")
      for ((i=a;i<=b;i++)); do list+="${list:+,}$i"; done
    else list+="${list:+,}$(letter_to_num "$part")"; fi; done; echo "$list"; }

# ------ sheet list ------------------------------------------------------
declare -a TODO
if [[ -z "$SHEETS" ]]; then
  while IFS=$'\t' read -r idx name; do [[ $idx =~ ^[0-9]+$ ]] && TODO+=("$idx::$name"); done < <(xlsx2csv -i "$FILE")
else IFS=',' read -ra parts <<< "$SHEETS"; for p in "${parts[@]}"; do TODO+=("$(echo "$p" | xargs)"); done; fi
[[ ${#TODO[@]} -eq 0 ]] && { error "No sheets matched."; exit 1; }

# ------ optional filters ------------------------------------------------
ROW_AWK=""
if [[ -n "$ROW_RANGE" ]]; then
  [[ "$ROW_RANGE" =~ ^([0-9]+)-([0-9]+)$ ]] \
    || { error "--rows expects <from>-<to>"; exit 1; }
  start="${BASH_REMATCH[1]}"; end="${BASH_REMATCH[2]}"
  ROW_AWK="NR>=$start && NR<=$end"
fi

COL_AWK=""; NUMS=""
if [[ -n "$COL_SPEC" ]]; then
  NUMS=$(build_num_list "$COL_SPEC")
  COL_AWK='{
    out=""; split(num,K,",");
    for(i=1;i<=NF;i++) if(K[i]) out=(out==""?$i:out OFS $i);
    print out
  }'
fi

STAMP="$(date +%Y%m%d_%H%M%S)"

# ------ export loop -----------------------------------------------------
for item in "${TODO[@]}"; do
  if [[ "$item" == *::* ]]; then idx="${item%%::*}"; name="${item##*::}"
  else idx="$item"; name="$item"; fi

  target="${OUT_DIR}/$(sanitize "$name")_${STAMP}.csv"
  [[ -f $target && $OVERWRITE == false ]] && { warn "Skip existing: $(basename "$target")"; continue; }

  CMD=(xlsx2csv) ; [[ $idx =~ ^[0-9]+$ ]] && CMD+=(-s "$idx") || CMD+=(--sheetname "$idx") ; CMD+=("$FILE")

  { "${CMD[@]}" |
    { [[ -n "$ROW_AWK" ]] && awk "$ROW_AWK" || cat; } |
    { [[ -n "$COL_AWK" ]] && awk -v num="$NUMS" -F, -v OFS=',' "$COL_AWK" || cat; }
  } > "$target"

  info "Created: $target"
done
