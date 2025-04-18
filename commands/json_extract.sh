#!/usr/bin/env bash
#
# json_extract – simple wrapper around jq for extracting JSON data
#
# Dependencies: jq (install via 'shellman doctor --fix') 

: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
source "$SHELLMAN_HOME/lib/utils.sh"

show_help() {
  echo "Usage:"
  echo "  shellman json_extract <file.json> [options]"
  echo ""
  echo "Description:"
  echo "  Extracts and filters JSON using jq expressions, selecting fields and saving or viewing the result."
  echo ""
  echo "Options:"
  echo "  --path <jq_expr>      jq path/expression to apply (e.g. '.[]')"
  echo "  --filter <jq_expr>    filter expression (requires array input)"
  echo "  --fields <list>       comma-separated list of fields to select"
  echo "  --output <file>       save output to file (disables interactive)"
  echo "  --interactive         pipe output through less (default when no --output)"
  echo "  --help                show this help message"
  echo ""
  echo "Examples:"
  echo "  shellman json_extract data.json --path '.items[]' --fields id,name"
  echo "  shellman json_extract data.json --filter '.[] | select(.status==\"ERROR\")' --fields id,msg --output errors.json"
}

# Defaults
FILE=""
PATH_EXPR=""
FILTER_EXPR=""
FIELDS=""
OUTPUT_FILE=""
INTERACTIVE=true

# Parse arguments
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --help)
      show_help; exit 0
      ;;
    --path)
      PATH_EXPR="$2"; shift
      ;;
    --filter)
      FILTER_EXPR="$2"; shift
      ;;
    --fields)
      FIELDS="$2"; shift
      ;;
    --output)
      OUTPUT_FILE="$2"; INTERACTIVE=false; shift
      ;;
    --interactive)
      INTERACTIVE=true
      ;;
    -* )
      error "Unknown option: $1"; show_help; exit 1
      ;;
    *)
      if [[ -z "$FILE" ]]; then
        FILE="$1"
      else
        error "Unexpected argument: $1"; show_help; exit 1
      fi
      ;;
  esac
  shift
done

# Validation
if [[ -z "$FILE" ]]; then
  error "No JSON file provided."; show_help; exit 1
fi
if [[ ! -f "$FILE" ]]; then
  error "File not found: $FILE"; exit 1
fi
if ! command -v jq &>/dev/null; then
  error "jq is required. Install it or run 'shellman doctor --fix'."; exit 1
fi

# Build jq filter
JQ_FILTER="."
if [[ -n "$PATH_EXPR" ]]; then
  JQ_FILTER="$PATH_EXPR"
elif [[ -n "$FILTER_EXPR" ]]; then
  JQ_FILTER="$FILTER_EXPR"
fi

if [[ -n "$FIELDS" ]]; then
  IFS=',' read -ra FIELD_ARR <<< "$FIELDS"
  SELECT="{"
  for f in "${FIELD_ARR[@]}"; do
    SELECT+="\"$f\": .$f, "
  done
  SELECT=${SELECT%, }"}"
  # inline the SELECT object into the filter
  JQ_FILTER="$JQ_FILTER | $SELECT"
fi

# Prepare command
CMD=(jq -c "$JQ_FILTER" "$FILE")

# Execute
if [[ -n "$OUTPUT_FILE" ]]; then
  "${CMD[@]}" > "$OUTPUT_FILE"
  info "Saved to $OUTPUT_FILE"
else
  if [[ "$INTERACTIVE" == true ]]; then
    "${CMD[@]}" | less -S
  else
    "${CMD[@]}"
  fi
fi
