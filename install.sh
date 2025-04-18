#!/usr/bin/env bash

set -e

INSTALL_DIR="/usr/local/lib/shellman"
BIN_LINK="/usr/local/bin/shellman"
SOURCE_BIN="./bin/shellman"

echo "🔧 Installing Shellman (local/offline mode)..."

# --- Weryfikacja struktury katalogu ---
if [[ ! -f "$SOURCE_BIN" || ! -d "./commands" || ! -d "./lib" ]]; then
  echo "❌ Error: Please run this script from inside the Shellman project root." >&2
  echo "🛠️  Missing expected files: bin/shellman, commands/, lib/" >&2
  exit 1
fi

# --- Kopiowanie plików do instalacji --- 
echo "📁 Copying files to $INSTALL_DIR..."
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r bin commands lib VERSION "$INSTALL_DIR"

# --- Uprawnienia ---
echo "🔓 Setting executable permission on bin/shellman..."
sudo chmod +x "$INSTALL_DIR/bin/shellman"

# --- Tworzenie symlinku ---
echo "🔗 Creating symlink at $BIN_LINK ..."
sudo ln -sf "$INSTALL_DIR/bin/shellman" "$BIN_LINK"

# --- Walidacja instalacji ---
if command -v shellman >/dev/null 2>&1; then
  echo "✅ Shellman installed successfully!"
  echo "ℹ️  Version: $("$BIN_LINK" --version 2>/dev/null || echo 'unknown')"
else
  echo "⚠️  Shellman was installed, but is not in your PATH."
  echo "👉 Add /usr/local/bin to your PATH, or use: $BIN_LINK"
fi
