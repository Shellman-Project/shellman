#!/bin/bash

source ./lib/utils.sh

echo "🐚 Installing BATS (Bash Automated Testing System)..."

#  
if command -v bats >/dev/null 2>&1; then
    info "BATS is already installed. ✔️"
    bats --version
    exit 0
fi

# Instalacja
git clone https://github.com/bats-core/bats-core.git /tmp/bats-core
cd /tmp/bats-core || exit
sudo ./install.sh /usr/local

# Weryfikacja
if command -v bats >/dev/null 2>&1; then
    info "BATS installed successfully!"
    bats --version
else
    error "BATS installation failed."
    exit 1
fi
