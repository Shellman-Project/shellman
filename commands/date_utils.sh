#!/usr/bin/env bash
#
# date_utils – operate on dates: add/subtract, compare, format 

: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
source "$SHELLMAN_HOME/lib/utils.sh"

show_help() {
cat <<EOF
Usage:
  shellman date_utils [--date "YYYY-MM-DD [HH:MM:SS]"] [operation] [options]

Operations:
  --add <n><unit>      Add time (e.g. 5d, 2w, 3m, 1y, 4h, 30min, 20s)
  --sub <n><unit>      Subtract time (e.g. 10d, 1m, 2h, 15s)
  --diff <date>        Time difference between base date and another
  --format <pattern>   Format date using strftime (e.g. %A %d %B %Y %T)
  --help               Show help

Date source:
  --date "YYYY-MM-DD [HH:MM:SS]"   Use specific base datetime (defaults to now)

Examples:
  shellman date_utils --add 10d
  shellman date_utils --date "2024-12-01 13:00" --sub 2h
  shellman date_utils --date "2024-01-01" --diff "2025-04-18 09:15:00"
  shellman date_utils --format '%A, %d %B %Y, %T'
EOF
}

# --- defaults ---
BASE_DATE=""
ADD_INPUT=""
SUB_INPUT=""
DIFF_DATE=""
FORMAT_PATTERN=""

# --- parse ---
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --help) show_help; exit 0 ;;
    --date) BASE_DATE="$2"; shift ;;
    --add)  ADD_INPUT="$2"; shift ;;
    --sub)  SUB_INPUT="$2"; shift ;;
    --diff) DIFF_DATE="$2"; shift ;;
    --format) FORMAT_PATTERN="$2"; shift ;;
    *) error "Unknown option: $1"; show_help; exit 1 ;;
  esac
  shift
done

# --- determine base date ---
if [[ -z "$BASE_DATE" ]]; then
  BASE_DATE=$(date "+%Y-%m-%d %H:%M:%S")
else
  date -d "$BASE_DATE" &>/dev/null || { error "Invalid date: $BASE_DATE"; exit 1; }
fi

RESULT="$BASE_DATE"

# --- helpers ---
parse_duration() {
  local input="$1"
  local re1='^([0-9]+)([dwmqy])$'
  local re2='^([0-9]+)(h|min|s)$'

  if [[ "$input" =~ $re1 ]]; then
    local amount="${BASH_REMATCH[1]}"
    local unit="${BASH_REMATCH[2]}"
    echo "$amount $unit"
  elif [[ "$input" =~ $re2 ]]; then
    local amount="${BASH_REMATCH[1]}"
    local unit="${BASH_REMATCH[2]}"
    echo "$amount $unit"
  else
    error "Invalid duration format: $input (expected e.g. 5d, 2w, 3m, 1y, 4h, 15min, 20s)"
    exit 1
  fi
}


adjust_date() {
  local date="$1" amount="$2" unit="$3" sign="$4"
  local mod="${sign}${amount}"
  local date_epoch=$(date -d "$date" +%s)

  case "$unit" in
    d) date -d "$date ${mod} days" "+%Y-%m-%d %H:%M:%S" ;;
    w) date -d "$date ${mod} weeks" "+%Y-%m-%d %H:%M:%S" ;;
    m) date -d "$date ${mod} months" "+%Y-%m-%d %H:%M:%S" ;;
    y) date -d "$date ${mod} years" "+%Y-%m-%d %H:%M:%S" ;;
    q) date -d "$date $((amount * 3)) months" "+%Y-%m-%d %H:%M:%S" ;;
    h)
      local seconds=$((amount * 3600))
      [[ "$sign" == "-" ]] && seconds=$((-seconds))
      date -d "@$((date_epoch + seconds))" "+%Y-%m-%d %H:%M:%S"
      ;;
    min)
      local seconds=$((amount * 60))
      [[ "$sign" == "-" ]] && seconds=$((-seconds))
      date -d "@$((date_epoch + seconds))" "+%Y-%m-%d %H:%M:%S"
      ;;
    s)
      local seconds=$((amount))
      [[ "$sign" == "-" ]] && seconds=$((-seconds))
      date -d "@$((date_epoch + seconds))" "+%Y-%m-%d %H:%M:%S"
      ;;
    *)
      error "Unsupported unit: $unit"
      exit 1
      ;;
  esac
}


# --- operations ---
if [[ -n "$ADD_INPUT" ]]; then
  read -r N U <<< "$(parse_duration "$ADD_INPUT")"
  RESULT=$(adjust_date "$BASE_DATE" "$N" "$U" "+")
  info "→ $N$U after $BASE_DATE: $RESULT"
fi

if [[ -n "$SUB_INPUT" ]]; then
  read -r N U <<< "$(parse_duration "$SUB_INPUT")"
  RESULT=$(adjust_date "$BASE_DATE" "$N" "$U" "-")
  info "→ $N$U before $BASE_DATE: $RESULT"
fi

if [[ -n "$DIFF_DATE" ]]; then
  if ! date -d "$DIFF_DATE" &>/dev/null; then
    error "Invalid comparison date: $DIFF_DATE"
    exit 1
  fi
  ts1=$(date -d "$BASE_DATE" +%s)
  ts2=$(date -d "$DIFF_DATE" +%s)
  diff_sec=$((ts2 - ts1))
  days=$((diff_sec / 86400))
  hours=$(( (diff_sec % 86400) / 3600 ))
  minutes=$(( (diff_sec % 3600) / 60 ))
  seconds=$(( diff_sec % 60 ))

  info "→ Difference between $BASE_DATE and $DIFF_DATE:"
  echo "  $days days, $hours hours, $minutes minutes, $seconds seconds"
  exit 0
fi

if [[ -n "$FORMAT_PATTERN" ]]; then
  formatted_base=$(date -d "$BASE_DATE" +"$FORMAT_PATTERN")
  formatted_result=$(date -d "$RESULT" +"$FORMAT_PATTERN")

  if [[ "$RESULT" != "$BASE_DATE" ]]; then
    info "→ base:    $formatted_base"
    info "→ result:  $formatted_result"
  else
    info "→ formatted: $formatted_base"
  fi
fi
