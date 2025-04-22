#!/bin/bash
# 
info() {
  echo -e "\e[32m[INFO]\e[0m $1"
}

error() {
  echo -e "\e[31m[ERROR]\e[0m $1"
}

ok() {
  echo -e "\e[32m✔︎ $1\e[0m"
}

warn() {
  echo -e "\e[33m⚠️  $1\e[0m"
}
 
get_file_size_readable() {
  local file="$1"
  if [[ -f "$file" ]]; then
    local size_bytes
    size_bytes=$(wc -c < "$file")

    if (( size_bytes < 1024 )); then
      echo "${size_bytes} B"
    elif (( size_bytes < 1024 * 1024 )); then
      awk "BEGIN { printf \"%.2f KB\", $size_bytes / 1024 }"
    else
      awk "BEGIN { printf \"%.2f MB\", $size_bytes / 1024 / 1024 }"
    fi
  else
    echo "0 B"
  fi
}
 