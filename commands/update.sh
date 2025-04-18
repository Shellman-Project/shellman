#!/usr/bin/env bash
#
# Update Shellman from the local clone   (default)
# or pull newest code from GitHub first  (--remote). 

source ./lib/utils.sh

REPO_URL="https://github.com/JakubMarciniak93/shellman.git"   # change if you fork

# --- parse optional flag ----------------------------------------------------
REMOTE=false
if [[ "$1" == "--remote" ]]; then
  REMOTE=true
  shift
fi
[[ "$1" == "--help" ]] && {
cat <<EOF
Usage:  shellman update [--remote]

  (no flag)   – copy current working tree to the system install
  --remote    – git‑pull newest code from GitHub first, then copy

EOF
exit 0
}

# --- versions --------------------------------------------------------------- 
SHELLMAN_HOME="${SHELLMAN_HOME:-/usr/local/lib/shellman}"
CURRENT_VERSION=$(cat "$SHELLMAN_HOME/VERSION" 2>/dev/null || echo "unknown")
LOCAL_VERSION=$(cat ./VERSION 2>/dev/null || echo "unknown")

echo "🔁  Updating Shellman ..."
echo "Installed version : $CURRENT_VERSION"
echo "Local clone        : $LOCAL_VERSION"

# --- fetch remote if requested ---------------------------------------------
if $REMOTE; then
  echo "🌐  Checking remote repository ..."
  REMOTE_VERSION=$(curl -fsSL "$REPO_URL/raw/main/VERSION" 2>/dev/null || echo "unknown")
  echo "GitHub version     : $REMOTE_VERSION"

  if [[ "$REMOTE_VERSION" == "$LOCAL_VERSION" ]]; then
    info "Local clone already at latest revision."
  else
    if [[ -d .git ]]; then
      git pull --quiet || { fail "git pull failed"; exit 1; }
      LOCAL_VERSION=$(cat ./VERSION)
      ok "Pulled newest code: $LOCAL_VERSION"
    else
      fail "This directory is not a git clone – cannot --remote pull."
      exit 1
    fi
  fi
fi

echo ""
read -rp "Proceed with install/update? (Y/n): " yn
[[ "$yn" =~ ^[Nn]$ ]] && { echo "❌  Cancelled."; exit 0; }

# --- copy files to system location -----------------------------------------
echo "📁  Installing to $SHELLMAN_HOME ..."
sudo cp -r bin commands lib VERSION contrib completions "$SHELLMAN_HOME"

echo "🔓  Setting permissions ..."
sudo chmod +x "$SHELLMAN_HOME/bin/shellman"

echo "🔗  Refreshing symlink in /usr/local/bin ..."
sudo ln -sf "$SHELLMAN_HOME/bin/shellman" /usr/local/bin/shellman

echo "✅  Done."
shellman --version
