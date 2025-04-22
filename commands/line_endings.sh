#!/usr/bin/env bash
#
# line_endings – convert file line endings (CRLF ↔ LF), or check them
#
# Examples:
#   shellman line_endings --file script.sh --to lf
#   shellman line_endings --dir src --ext .txt --to crlf
#   shellman line_endings --dir src --check

: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
source "$SHELLMAN_HOME/lib/utils.sh"

show_help() {
cat <<EOF
Usage:
  shellman line_endings [--file path | --dir path] [--ext .ext] (--to lf|crlf | --check)

Options:
  --file <path>       Path to a single file
  --dir <dir>         Path to directory (will recurse)
  --ext <.ext>        Only files with this extension (requires --dir)
  --to <lf|crlf>      Convert to specified line endings
  --check             Only check and report line ending type per file
  --help              Show help

Examples:
  shellman line_endings --file script.sh --to lf
  shellman line_endings --dir src --ext .py --to crlf
  shellman line_endings --dir src --check
EOF
}

# Defaults
TARGET=""
FILE=""
DIR=""
EXT=""
CHECK_MODE=false

# Parse args
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --file) FILE="$2"; shift ;;
    --dir)  DIR="$2"; shift ;;
    --ext)  EXT="$2"; shift ;;
    --to)   TARGET="$2"; shift ;;
    --check) CHECK_MODE=true ;;
    --help) show_help; exit 0 ;;
    *) error "Unknown option: $1"; show_help; exit 1 ;;
  esac
  shift
done

# Validation
[[ "$CHECK_MODE" == false && -z "$TARGET" ]] && { error "Either --to or --check is required"; exit 1; }
[[ -n "$TARGET" && "$TARGET" != "lf" && "$TARGET" != "crlf" ]] && { error "--to must be 'lf' or 'crlf'"; exit 1; }

# Normalize extension (remove leading dot if exists)
[[ -n "$EXT" ]] && EXT="${EXT#.}"

# Tool detection
USE_DOS2UNIX=false
command -v dos2unix &>/dev/null && command -v unix2dos &>/dev/null && USE_DOS2UNIX=true

detect_endings() {
  local path="$1"
  [[ ! -f "$path" ]] && return

  if grep -q $'\r$' "$path"; then
    if grep -qv $'\r$' "$path"; then
      echo "MIXED"
    else
      echo "CRLF"
    fi
  else
    if grep -q $'\n' "$path"; then
      echo "LF"
    else
      echo "NONE"
    fi
  fi
}

convert_file() {
  local path="$1"
  [[ ! -f "$path" ]] && return

  if [[ "$CHECK_MODE" == true ]]; then
    local type
    type=$(detect_endings "$path")
    echo "🔍 $path → $type"
    return
  fi

  if [[ "$USE_DOS2UNIX" == true ]]; then
    if [[ "$TARGET" == "lf" ]]; then
      dos2unix "$path" &>/dev/null && info "→ converted to LF (dos2unix): $path"
    else
      unix2dos "$path" &>/dev/null && info "→ converted to CRLF (unix2dos): $path"
    fi
  else
    if [[ "$TARGET" == "lf" ]]; then
      sed -i 's/\r$//' "$path"
      info "→ converted to LF (sed): $path"
    else
      sed -i 's/$/\r/' "$path"
      sed -i 's/\([^\r]\)\r$/\1\r/' "$path"
      info "→ converted to CRLF (sed): $path"
    fi
  fi
}

# Process
if [[ -n "$FILE" ]]; then
  convert_file "$FILE"
elif [[ -n "$DIR" ]]; then
  FIND_ARGS=(-type f)
  [[ -n "$EXT" ]] && FIND_ARGS+=(-iname "*.${EXT}")
  while IFS= read -r -d '' file; do
    convert_file "$file"
  done < <(find "$DIR" "${FIND_ARGS[@]}" -print0 2>/dev/null)
else
  error "Must specify --file or --dir"
  exit 1
fi
