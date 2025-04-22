#!/usr/bin/env bash
#
# shellman update – update Shellman from local or remote source
# -------------------------------------------------------------

: "${SHELLMAN_HOME:=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
source "$SHELLMAN_HOME/lib/utils.sh"

REPO_URL="https://github.com/JakubMarciniak93/shellman"
RAW_VERSION_URL="https://raw.githubusercontent.com/JakubMarciniak93/shellman/main/VERSION"
INSTALL_DIR="/usr/local/lib/shellman"

show_help() {
cat <<EOF
Usage:
  shellman update [--remote | --local]

Options:
  --remote      Download and install the latest version from GitHub
  --local       Install from current local files (default if no option)
  --help        Show this help screen
EOF
}

# ---------- parse args ----------
[[ "$1" == "--help" ]] && { show_help; exit 0; }

USE_REMOTE=false
[[ "$1" == "--remote" ]] && USE_REMOTE=true
[[ "$1" == "--local" ]] && USE_REMOTE=false

# ---------- update info ----------
echo "🔁  Updating Shellman ..."

INSTALLED_VERSION="$(shellman --version 2>/dev/null)"
CLONE_VERSION="$(cat "$SHELLMAN_HOME/VERSION" 2>/dev/null || echo unknown)"

echo "Installed version : $INSTALLED_VERSION"
echo "Local clone        : $CLONE_VERSION"

if [[ "$USE_REMOTE" == true ]]; then
  echo "🌐  Checking remote repository ..."
  REMOTE_VERSION="$(curl -fsSL "$RAW_VERSION_URL" 2>/dev/null || echo unknown)"
  echo "GitHub version     : $REMOTE_VERSION"
  [[ "$REMOTE_VERSION" == "unknown" ]] && warn "Could not fetch remote version from GitHub"
fi

# ---------- confirmation ----------
echo ""
read -p "Proceed with install/update? (Y/n): " confirm
[[ "$confirm" =~ ^[Nn]$ ]] && { echo "❌  Aborted."; exit 0; }

echo "📁  Installing to $INSTALL_DIR ..."
sudo mkdir -p "$INSTALL_DIR"

if [[ "$USE_REMOTE" == true ]]; then
  TMP_DIR=$(mktemp -d)
  git clone --quiet "$REPO_URL" "$TMP_DIR"
  sudo cp -r "$TMP_DIR"/* "$INSTALL_DIR"
  rm -rf "$TMP_DIR"
else
  sudo cp -r "$SHELLMAN_HOME"/* "$INSTALL_DIR"
fi

# ---------- dos2unix install ----------
if ! command -v dos2unix &>/dev/null; then
  echo "🔧  Installing dos2unix ..."
  if command -v apt-get &>/dev/null; then
    sudo apt-get install -y dos2unix
  elif command -v dnf &>/dev/null; then
    sudo dnf install -y dos2unix
  elif command -v pacman &>/dev/null; then
    sudo pacman -Sy --noconfirm dos2unix
  elif command -v brew &>/dev/null; then
    brew install dos2unix
  elif command -v choco &>/dev/null; then
    choco install -y dos2unix
  else
    warn "Could not auto-install dos2unix (no known package manager)"
  fi
fi

# ---------- normalize line endings ----------
if command -v dos2unix &>/dev/null; then
  echo "🧹  Converting script line endings to LF ..."
  sudo find "$INSTALL_DIR" -name "*.sh" -exec dos2unix {} + &>/dev/null
fi

# ---------- set permissions & symlink ----------
echo "🔓  Setting permissions ..."
sudo chmod -R a+rX "$INSTALL_DIR"

echo "🔗  Refreshing symlink in /usr/local/bin ..."
sudo ln -sf "$INSTALL_DIR/bin/shellman" /usr/local/bin/shellman

VERSION_MSG="Shellman is now up-to-date"
[[ "$USE_REMOTE" == true ]] && VERSION_MSG+=" (v$REMOTE_VERSION)" || VERSION_MSG+=" from local clone (v$CLONE_VERSION)"
echo "✅  $VERSION_MSG"
 
# ---------- post-check ----------
echo ""
echo "🩺  Running shellman doctor ..."
shellman doctor
