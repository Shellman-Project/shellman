#!/usr/bin/env bash
#
# Extract selected columns / rows from a CSV (any single‑char delimiter).
# Supports --skip-header and --interactive. 

# ---------------------------------------------------------------
: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
source "$SHELLMAN_HOME/lib/utils.sh"
# ---------------------------------------------------------------

show_help() {
  echo "Usage:"
  echo "  shellman csv_extract <file> [options]"
  echo ""
  echo "Description:"
  echo "  Prints or saves only chosen columns / rows of a CSV."
  echo ""
  echo "Options:"
  echo "  --cols <list>          Columns to keep, 1‑based (e.g. 1,3  or 2-4)"
  echo "  --rows <list>          Rows to keep after (optional) header (e.g. 10-20)"
  echo "  --contains <text>      Keep only rows that contain <text>"
  echo "  --not-contains <text>  Keep rows NOT containing <text>"
  echo "  --delim <char>         Field delimiter (default , )"
  echo "  --skip-header          Ignore the first line of the CSV"
  echo "  --output <file>        Save result instead of printing"
  echo "  --interactive          View result in less (can combine with --output)"
  echo "  --help                 Show this help message"
  echo ""
  echo "Examples:"
  echo "  shellman csv_extract data.csv --cols 1,4 --rows 2-100 --skip-header"
  echo "  shellman csv_extract logs.csv --contains ERROR --output errors.csv --interactive"
}

# ---------- defaults ----------
FILE=""
COLS=""
ROWS=""
CONTAINS=""
NOT_CONTAINS=""
DELIM=","
OUT_FILE=""
SKIP_HEADER=false
INTERACTIVE=false
# --------------------------------

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --help)           show_help; exit 0 ;;
    --cols)           COLS="$2"; shift ;;
    --rows)           ROWS="$2"; shift ;;
    --contains)       CONTAINS="$2"; shift ;;
    --not-contains)   NOT_CONTAINS="$2"; shift ;;
    --delim)          DELIM="$2"; shift ;;
    --output)         OUT_FILE="$2"; shift ;;
    --skip-header)    SKIP_HEADER=true ;;
    --interactive)    INTERACTIVE=true ;;
    -*)
      error "Unknown option: $1"; show_help; exit 1 ;;
    *)
      [[ -z "$FILE" ]] && FILE="$1" || { error "Unexpected arg: $1"; exit 1; }
      ;;
  esac
  shift
done

# ---------- validation ----------
[[ -z "$FILE" ]]           && { error "No file given."; show_help; exit 1; }
[[ ! -f "$FILE" ]]         && { error "File not found: $FILE"; exit 1; }
[[ -n "$CONTAINS" && -n "$NOT_CONTAINS" ]] && { error "Use --contains XOR --not-contains"; exit 1; }
[[ -z "$COLS" ]]           && { error "Missing --cols (what columns to extract?)"; exit 1; }
# --------------------------------

AWK_SCRIPT='
BEGIN{
  FS=delim; OFS=delim;
  split(cols,colArr,",");
  for(i in colArr){
    if(colArr[i] ~ /-/){ split(colArr[i],r,"-"); for(j=r[1];j<=r[2];j++) want[j]=1 }
    else want[colArr[i]]=1
  }
  split(rows,rowArr,",");
  for(i in rowArr){
    if(rowArr[i]=="") continue
    if(rowArr[i] ~ /-/){ split(rowArr[i],r,"-"); for(j=r[1];j<=r[2];j++) rowWant[j]=1 }
    else rowWant[rowArr[i]]=1
  }
}
{
  if(skip && NR==1) next
  curNR = skip ? NR-1 : NR
  if(length(rowArr[1]) && !(curNR in rowWant)) next
  line=$0
  if(lenC && index(tolower(line),tolower(cont))==0) next
  if(lenN && index(tolower(line),tolower(notc))!=0) next
  out=""
  for(i=1;i<=NF;i++) if(want[i]) out=(out==""?$i:out OFS $i)
  print out
}'

ARGS=(cols="$COLS" rows="$ROWS" cont="$CONTAINS" notc="$NOT_CONTAINS" \
      delim="$DELIM" lenC="${#CONTAINS}" lenN="${#NOT_CONTAINS}" skip="$SKIP_HEADER")

RESULT=$(awk -v "${ARGS[0]}" -v "${ARGS[1]}" -v "${ARGS[2]}" -v "${ARGS[3]}" \
               -v "${ARGS[4]}" -v "${ARGS[5]}" -v "${ARGS[6]}" -v "${ARGS[7]}" \
               "$AWK_SCRIPT" "$FILE")

if [[ -z "$OUT_FILE" ]]; then
  echo "$RESULT"
  info "Lines printed: $(echo "$RESULT" | grep -c .)"
  [[ "$INTERACTIVE" == true ]] && echo "$RESULT" | less
else
  echo "$RESULT" > "$OUT_FILE"
  info "Saved to $OUT_FILE"
  [[ "$INTERACTIVE" == true ]] && less "$OUT_FILE"
fi
