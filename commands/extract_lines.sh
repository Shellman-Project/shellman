#!/usr/bin/env bash
# 
# Extract lines that DO / DO NOT contain a string, with optional context.
# Author: Shellman project

source ./lib/utils.sh

show_help() {
  echo "Usage:"
  echo "  shellman extract_lines <file> [options]"
  echo ""
  echo "Description:"
  echo "  Prints (or saves) only the lines that contain — or do NOT contain —"
  echo "  a given text, with optional N lines of context before / after."
  echo ""
  echo "Options:"
  echo "  --contains <text>        Keep lines that contain <text>"
  echo "  --not-contains <text>    Keep lines that do NOT contain <text>"
  echo "  --before <N>             Show N lines before each match   (default 0)"
  echo "  --after <N>              Show N lines after  each match   (default 0)"
  echo "  --output <file>          Save result instead of printing  (optional)"
  echo "  --help                   Show this help message"
  echo ""
  echo "Examples:"
  echo "  shellman extract_lines sys.log --contains ERROR --before 2 --after 3"
  echo "  shellman extract_lines notes.txt --not-contains TODO --output clean.txt"
}

# -------- defaults ----------
FILE=""
CONTAINS=""
NOT_CONTAINS=""
BEFORE=0
AFTER=0
OUT_FILE=""
# -----------------------------

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --help) show_help; exit 0 ;;
    --contains)      CONTAINS="$2"; shift ;;
    --not-contains)  NOT_CONTAINS="$2"; shift ;;
    --before)        BEFORE="$2"; shift ;;
    --after)         AFTER="$2"; shift ;;
    --output)        OUT_FILE="$2"; shift ;;
    -*)
      error "Unknown option: $1"; show_help; exit 1 ;;
    *)  [[ -z "$FILE" ]] && FILE="$1" || { error "Unexpected arg: $1"; exit 1; } ;;
  esac
  shift
done

# -------- validation ---------
[[ -z "$FILE" ]]            && { error "No file given."; show_help; exit 1; }
[[ ! -f "$FILE" ]]          && { error "File not found: $FILE"; exit 1; }
[[ -n "$CONTAINS" && -n "$NOT_CONTAINS" ]] && { error "Use either --contains OR --not-contains"; exit 1; }
[[ -z "$CONTAINS" && -z "$NOT_CONTAINS" ]] && { error "Need --contains or --not-contains"; exit 1; }
[[ "$BEFORE" =~ ^[0-9]+$ ]] || { error "--before needs integer"; exit 1; }
[[ "$AFTER"  =~ ^[0-9]+$ ]] || { error "--after needs integer";  exit 1; }
# -----------------------------

# Build grep command
GREP_ARGS=(-n)                       # keep line numbers
(( BEFORE > 0 )) && GREP_ARGS+=(-B "$BEFORE")
(( AFTER  > 0 )) && GREP_ARGS+=(-A "$AFTER")

if [[ -n "$CONTAINS" ]]; then
  GREP_ARGS+=("$CONTAINS")
  CMD=(grep "${GREP_ARGS[@]}" -- "$FILE")
else
  GREP_ARGS+=( -v "$NOT_CONTAINS" )
  CMD=(grep "${GREP_ARGS[@]}" -- "$FILE")
fi

# Execute
RESULT="$("${CMD[@]}")"
if [[ -z "$OUT_FILE" ]]; then
  echo "$RESULT"
  info "Lines printed: $(echo "$RESULT" | wc -l)"
else
  echo "$RESULT" > "$OUT_FILE"
  info "Saved to $OUT_FILE  (lines: $(wc -l < "$OUT_FILE"))"
fi
