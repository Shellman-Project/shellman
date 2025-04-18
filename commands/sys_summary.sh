#!/usr/bin/env bash
#
# sys_summary – show system and shell environment info
# Works on Linux, macOS, WSL 

: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
source "$SHELLMAN_HOME/lib/utils.sh"

echo "📋  System Summary"
echo "────────────────────────────────────────"

# ---------- System Info ----------
OS_NAME="$(uname -s)"
OS_VER="$(uname -r)"
ARCH="$(uname -m)"
DISTRO=""
WSL="No"

if [[ -f /etc/os-release ]]; then
  . /etc/os-release
  DISTRO="$NAME $VERSION_ID"
fi

if grep -qi microsoft /proc/version 2>/dev/null; then
  WSL="Yes"
fi

HOST=$(hostname)

echo "🖥️  OS & Host"
echo "────────────────────────────────────────"
printf "System       : %s\n" "$OS_NAME"
[[ -n "$DISTRO" ]] && printf "Distro       : %s\n" "$DISTRO"
printf "Version      : %s\n" "$OS_VER"
printf "Architecture : %s\n" "$ARCH"
printf "WSL          : %s\n" "$WSL"
printf "Hostname     : %s\n" "$HOST"
echo

# ---------- Shell ----------
SHELL_NAME=$(basename "$SHELL")
SHELL_VER="$($SHELL --version 2>&1 | head -n1)"
BASH_VER="${BASH_VERSION:-N/A}"

echo "🐚  Shell"
echo "────────────────────────────────────────"
printf "Shell        : %s\n" "$SHELL_NAME"
printf "Shell Ver.   : %s\n" "$SHELL_VER"
[[ "$SHELL_NAME" == "bash" ]] && printf "Bash Ver.    : %s\n" "$BASH_VER"
echo

# ---------- Tools ----------
PYTHON_VER="$(python3 --version 2>/dev/null || echo 'not found')"
JQ_VER="$(jq --version 2>/dev/null || echo 'not found')"
XLSX2CSV_VER="$(xlsx2csv --version 2>/dev/null || echo 'not found')"

echo "🛠  Tools"
echo "────────────────────────────────────────"
printf "python3      : %s\n" "$PYTHON_VER"
printf "jq           : %s\n" "$JQ_VER"
printf "xlsx2csv     : %s\n" "$XLSX2CSV_VER"
echo

# ---------- Memory ----------
echo "🧠  Memory"
echo "────────────────────────────────────────"
free -h | awk 'NR==1 || NR==2 || NR==3 {printf "%-10s %-10s %-10s %-10s\n", $1, $2, $3, $4}'
echo

# ---------- Uptime & Load ----------
echo "⏱  Uptime & Load"
echo "────────────────────────────────────────"
uptime -p | sed 's/^/Uptime       : /'
uptime | awk -F'load average:' '{print "Load Avg.    :" $2}'
echo

# ---------- Disk ----------
echo "💽  Disks"
echo "────────────────────────────────────────"
df -h -x tmpfs -x devtmpfs | awk 'NR==1 || /\/$/ {printf "%-20s %-8s %-8s %-8s %-8s\n", $1, $2, $3, $4, $5}'
echo

# ---------- Network ----------
IP_LOCAL=$(hostname -I | awk '{print $1}')
IP_PUBLIC=$(curl -s ifconfig.me 2>/dev/null || echo "unavailable")

echo "🌐  Network"
echo "────────────────────────────────────────"
printf "Local IP     : %s\n" "$IP_LOCAL"
printf "Public IP    : %s\n" "$IP_PUBLIC"
echo

# ---------- Packages ----------
detect_pkg_mgr() {
  if   command -v apt-get &>/dev/null;  then echo apt
  elif command -v dnf     &>/dev/null;  then echo dnf
  elif command -v pacman  &>/dev/null;  then echo pacman
  elif command -v brew    &>/dev/null;  then echo brew
  elif command -v choco   &>/dev/null;  then echo choco
  else echo none; fi
}

PKG_MGR=$(detect_pkg_mgr)
case "$PKG_MGR" in
  apt)    PKG_COUNT=$(dpkg -l | grep '^ii' | wc -l) ;;
  pacman) PKG_COUNT=$(pacman -Q | wc -l) ;;
  dnf)    PKG_COUNT=$(dnf list installed | wc -l) ;;
  brew)   PKG_COUNT=$(brew list | wc -l) ;;
  choco)  PKG_COUNT=$(choco list -l | wc -l) ;;
  *)      PKG_COUNT="unknown" ;;
esac

echo "📦  Packages"
echo "────────────────────────────────────────"
printf "Pkg Manager  : %s\n" "$PKG_MGR"
printf "Total pkgs   : %s\n" "$PKG_COUNT"
echo
