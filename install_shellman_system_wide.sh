#!/usr/bin/env bash
set -e

REPO="https://github.com/JakubMarciniak93/shellman"
PREFIX="/usr/local"
LIBDIR="$PREFIX/lib/shellman"
BINLINK="$PREFIX/bin/shellman"

echo "🔧  Installing Shellman system‑wide …"

# 1. required tools 
for cmd in git zip openssl; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "▶ Installing missing dependency: $cmd"
    sudo apt update -qq && sudo apt install -y "$cmd"
  fi
done

# 2. maple or pull
if [[ -d "$LIBDIR/.git" ]]; then
  echo "🔄  Updating existing repo in $LIBDIR"
  sudo git -C "$LIBDIR" pull --quiet
else
  echo "🌐  Cloning Shellman to $LIBDIR"
  sudo git clone --depth 1 "$REPO" "$LIBDIR"
fi

# 3. run built-in install.sh (copies files, makes symlink) 
sudo chmod +x "$LIBDIR/install.sh"
sudo "$LIBDIR/install.sh"

# 4. check installation
if command -v shellman &>/dev/null; then
  echo -e "\n✅  Shellman installed!  Try:  shellman --help"
else
  echo "⚠️  Something went wrong – /usr/local/bin/shellman not found."
  exit 1
fi
