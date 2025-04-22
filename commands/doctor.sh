#!/usr/bin/env bash
#
# Shellman doctor – diagnose & optionally fix installation 
# --------------------------------------------------------

: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
source "$SHELLMAN_HOME/lib/utils.sh"

export PATH="$HOME/.local/bin:$PATH"

FIX_MODE=false
[[ "$1" == "--fix" ]] && FIX_MODE=true

mkdir -p logs
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="logs/doctor_${TIMESTAMP}.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "🩺  Running Shellman diagnostics…  (log: $LOG_FILE)"

ok()   { echo -e "\e[32m✔︎ $1\e[0m"; }
warn() { echo -e "\e[33m⚠️  $1\e[0m"; }
fail() { echo -e "\e[31m✖ $1\e[0m"; }

# ---------- system summary -----------------------------------------------
echo ""
echo "📋  System summary:"
OS="$(uname -s)"
KERNEL="$(uname -r)"
ARCH="$(uname -m)"
DISTRO="unknown"
WSL_VERSION=""

if [[ -f /etc/os-release ]]; then
  . /etc/os-release
  DISTRO="$NAME $VERSION"
elif command -v lsb_release &>/dev/null; then
  DISTRO="$(lsb_release -ds)"
fi

if grep -qi microsoft /proc/version 2>/dev/null; then
  if grep -q "WSL2" /proc/version; then
    WSL_VERSION="WSL2"
  else
    WSL_VERSION="WSL1"
  fi
  DISTRO+=" (under $WSL_VERSION)"
fi

echo "  OS:        $OS"
echo "  Distro:    $DISTRO"
echo "  Kernel:    $KERNEL"
echo "  Arch:      $ARCH"
echo ""

# ---------- package‑manager helpers -------------------------------------
detect_pkg_mgr() {
  if   command -v apt-get &>/dev/null;  then echo apt
  elif command -v dnf     &>/dev/null;  then echo dnf
  elif command -v pacman  &>/dev/null;  then echo pacman
  elif command -v brew    &>/dev/null;  then echo brew
  elif command -v choco   &>/dev/null;  then echo choco
  else echo none; fi
}
pkg_install() {
  case "$1" in
    apt)    sudo apt-get update -qq && sudo apt-get install -y -qq "$2" ;;
    dnf)    sudo dnf -y install -q "$2" ;;
    pacman) sudo pacman --noconfirm -S "$2" &>/dev/null ;;
    brew)   brew install "$2" &>/dev/null ;;
    choco)  choco install -y "$2" &>/dev/null ;;
  esac
}

# ---------- remote version ----------------------------------------------
check_remote_version() {
  local url="https://raw.githubusercontent.com/JakubMarciniak93/shellman/main/VERSION"
  local local_v="$(/usr/local/bin/shellman --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo unknown)"
  local remote_v="$(curl -fsSL "$url" 2>/dev/null || echo unknown)"
  echo "  Shellman version: $local_v"
  if [[ $local_v != unknown && $remote_v != unknown && $local_v != $remote_v ]]; then
    warn "Newer version available ($remote_v). Run: shellman update --remote"
  else
    ok "Shellman up‑to‑date ($local_v)"
  fi
}

# ---------- bash‑completion ---------------------------------------------
check_completion() {
  local mgr=$(detect_pkg_mgr)
  local dst="/etc/bash_completion.d/shellman_completion.bash"

  if ! dpkg -s bash-completion &>/dev/null; then
    warn "bash-completion package not installed"
    if $FIX_MODE && [[ "$mgr" == "apt" ]]; then
      pkg_install apt bash-completion && ok "bash-completion installed via apt"
    fi
  else
    ok "bash-completion package present"
  fi

  if $FIX_MODE; then
    for old in /etc/bash_completion.d/_shellman /etc/bash_completion.d/shellman.bash; do
      [[ -f "$old" ]] && sudo rm -f "$old" && warn "Removed legacy completion file: $old"
    done
  fi

  if [[ -f "$dst" ]]; then
    grep -q '_shellman()' "$dst" && ok "Shellman completion file present" || warn "Completion file present but not valid"
  else
    warn "Shellman completion file missing"
    if $FIX_MODE && [[ -f "$SHELLMAN_HOME/contrib/shellman_completion.bash" ]]; then
      normalize_line_endings "$SHELLMAN_HOME/contrib/shellman_completion.bash"
      sudo cp "$SHELLMAN_HOME/contrib/shellman_completion.bash" "$dst" && ok "Completion file installed → $dst"
    fi
  fi
}

normalize_line_endings() {
  local file="$1"
  if file "$file" | grep -q "CRLF"; then
    sed -i 's/\r$//' "$file" && ok "Normalized line endings to LF: $file"
  fi
}


ensure_completion_loaded() {
  local line='[[ -f /etc/bash_completion.d/shellman_completion.bash ]] && source /etc/bash_completion.d/shellman_completion.bash'
  grep -Fxq "$line" ~/.bashrc || echo "$line" >> ~/.bashrc
}

# ---------- Python libs --------------------------------------------------
check_python_pkg() {
  python3 - "$1" <<'PY' >/dev/null 2>&1
import importlib, sys
sys.exit(0 if importlib.util.find_spec(sys.argv[1]) else 1)
PY
}
pip_install_break() {
  if ! command -v pip3 &>/dev/null; then
    warn "pip3 is not available — skipping pip install of $1"
    return
  fi
  sudo python3 -m pip install --break-system-packages --upgrade "$1"
}
install_python_lib() {
  local mgr=$(detect_pkg_mgr)
  case "$mgr" in
    apt|dnf|pacman) pkg_install "$mgr" "$2" && ok "$1 installed ($mgr)" && return ;;
    brew|choco)     pkg_install "$mgr" "$1" && ok "$1 installed ($mgr)" && return ;;
  esac
  pip_install_break "$1" && ok "$1 installed (pip)"
}
check_or_install_pip() {
  if command -v pip3 &>/dev/null; then
    ok "pip3 present"
  else
    warn "pip3 not found"
    if $FIX_MODE; then
      pkg_install "$(detect_pkg_mgr)" python3-pip && ok "pip3 installed"
    fi
  fi
}
ensure_user_bin_path() {
  local line='export PATH="$HOME/.local/bin:$PATH"'
  grep -qxF "$line" ~/.bashrc || echo "$line" >> ~/.bashrc
}
 
# ---------- Python requirements ------------------------------------------
check_openpyxl()  { check_python_pkg openpyxl || { warn "openpyxl missing";  $FIX_MODE && install_python_lib openpyxl python3-openpyxl; } }
check_pandas()    { check_python_pkg pandas   || { warn "pandas missing";    $FIX_MODE && install_python_lib pandas python3-pandas; } }
check_xlsx2csv() {
  if command -v xlsx2csv &>/dev/null; then
    ok "xlsx2csv present"
  else
    warn "xlsx2csv missing"
    if $FIX_MODE; then
      if command -v pip3 &>/dev/null; then
        python3 -m pip install --user --break-system-packages --upgrade xlsx2csv && ok "xlsx2csv installed (user pip)"
      else
        warn "pip3 not available — cannot install xlsx2csv"
      fi
    fi
  fi
}
check_toml()      { check_python_pkg toml     || { warn "toml missing";      $FIX_MODE && install_python_lib toml python3-toml; } }
check_pyyaml() {
  local version
  version=$(python3 -c 'import yaml; print(yaml.__version__)' 2>/dev/null || echo "not found")
  if [[ "$version" == "not found" ]]; then
    warn "PyYAML missing"
    $FIX_MODE && install_python_lib PyYAML python3-yaml
  elif [[ "$version" =~ ^[0-5]\. ]]; then
    warn "PyYAML version too old ($version) – 6.0+ recommended"
    $FIX_MODE && install_python_lib PyYAML python3-yaml
  else
    ok "PyYAML present ($version)"
  fi
}

# ---------- CLI deps -----------------------------------------------------
check_or_install_cli() {
  if command -v "$1" &>/dev/null; then
    ok "$1 present"
  else
    warn "$1 missing"
    $FIX_MODE && pkg_install "$(detect_pkg_mgr)" "$2" && ok "$1 installed"
  fi
}
check_line_end_tools() {
  local has_dos2unix=false
  local has_unix2dos=false
  local has_sed=false

  command -v dos2unix &>/dev/null && has_dos2unix=true
  command -v unix2dos &>/dev/null && has_unix2dos=true
  command -v sed &>/dev/null && has_sed=true

  if $has_dos2unix && $has_unix2dos; then
    ok "dos2unix / unix2dos present"
  else
    warn "dos2unix or unix2dos missing"
    if $FIX_MODE; then
      pkg_install "$(detect_pkg_mgr)" dos2unix && ok "dos2unix installed"
    fi
  fi

  if ! $has_dos2unix || ! $has_unix2dos; then
    if $has_sed; then
      warn "Using fallback: sed-based CRLF/LF conversion (less reliable)"
    else
      fail "Neither dos2unix/unix2dos nor sed found – line_endings may not work"
    fi
  fi
}

# ---------- filesystem structure -----------------------------------------
check_or_create()  { [[ -e $1 ]] && ok "$2" || { $FIX_MODE && { mkdir -p "$1"; warn "$2 created"; } || fail "$2 missing"; } }
check_file_or_warn() { [[ -f $1 ]] && ok "$2" || warn "$2 missing"; }

check_or_create bin      "bin/ directory"
check_or_create commands "commands/ directory"
check_or_create lib      "lib/ directory"
check_or_create logs     "logs/ directory"

check_file_or_warn VERSION     "VERSION file"
check_file_or_warn lib/utils.sh "utils.sh"
check_file_or_warn bin/shellman "launcher script"

[[ -x bin/shellman ]] || { $FIX_MODE && chmod +x bin/shellman && warn "launcher made executable" || warn "launcher not executable"; }

[[ -L /usr/local/bin/shellman ]] && ok "symlink present" \
  || { $FIX_MODE && sudo ln -sf "$(realpath bin/shellman)" /usr/local/bin/shellman && ok "symlink created" || warn "symlink missing"; }

# ---------- commands list ------------------------------------------------
for cmd in count_lines file_stats find_files replace_text merge_files encrypt_files \
           zip_batch clean_files extract_lines csv_extract checksum_files \
           json_extract excel_info excel_preview excel_to_csv excel_diff \
           file_convert sys_summary tail_follow update doctor date_utils \
           line_endings; do
  [[ -f "commands/$cmd.sh" ]] && ok "command $cmd found" || warn "command $cmd missing"
done

# ---------- dependencies -------------------------------------------------
check_or_install_cli jq jq
check_or_install_cli zip zip
check_or_install_cli bats bats
check_or_install_pip
check_openpyxl
check_pandas
check_xlsx2csv
check_toml
check_pyyaml
check_completion
ensure_completion_loaded
check_line_end_tools
check_remote_version
ensure_user_bin_path

$FIX_MODE && echo -e "\n🛠️  Fix mode: repairs applied where possible.\n"
