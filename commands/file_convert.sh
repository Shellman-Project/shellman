#!/usr/bin/env bash
# 
# file_convert – convert between JSON, YAML, TOML formats
# Requires: python3 + PyYAML + toml + rich (→ shellman doctor --fix)

: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

source "$SHELLMAN_HOME/lib/utils.sh"

show_help() {
cat <<EOF
Usage:
  shellman file_convert <file> --from json --to yaml [options]

Options:
  --from <format>     Input format: json | yaml | toml
  --to   <format>     Output format: json | yaml | toml
  --output <file>     Save to file instead of stdout
  --pretty            Pretty print output (if supported)
  --interactive       Pipe output to less (if no --output)
  --help              Show help

Examples:
  shellman file_convert config.json --from json --to yaml
  shellman file_convert config.toml --from toml --to json --pretty --output out.json
EOF
}

# -------- defaults --------
IN_FILE=""; FROM=""; TO=""
OUT_FILE=""; PRETTY=""; INTERACTIVE=true
# --------------------------

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --help) show_help; exit 0 ;;
    --from) FROM="$2"; shift ;;
    --to)   TO="$2"; shift ;;
    --output) OUT_FILE="$2"; INTERACTIVE=false; shift ;;
    --pretty) PRETTY="--pretty" ;;
    --interactive) INTERACTIVE=true ;;
    -* ) error "Unknown option: $1"; show_help; exit 1 ;;
    *  ) [[ -z "$IN_FILE" ]] && IN_FILE="$1" || { error "Unexpected arg: $1"; exit 1; } ;;
  esac
  shift
done

[[ -z "$IN_FILE" || -z "$FROM" || -z "$TO" ]] && { error "Missing required argument"; show_help; exit 1; }
[[ ! -f "$IN_FILE" ]] && { error "File not found: $IN_FILE"; exit 1; }

# ---------------- execute ------------------
PY_SCRIPT="$SHELLMAN_HOME/lib/py/file_converter.py"
OUT_PATH="${OUT_FILE:-/dev/stdout}"

if [[ ! -f "$PY_SCRIPT" ]]; then
  error "Missing Python script: $PY_SCRIPT"
  exit 1
fi

python3 "$PY_SCRIPT" "$IN_FILE" "$FROM" "$TO" "$PRETTY" > "$OUT_PATH"

[[ -n "$OUT_FILE" ]] && info "Saved to $OUT_FILE"
[[ -n "$OUT_FILE" && "$INTERACTIVE" == true ]] && less -S "$OUT_FILE"

