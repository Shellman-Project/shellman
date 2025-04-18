#!/bin/bash
#
source ./lib/utils.sh

show_help() {
    echo "Usage:"
    echo "  shellman encrypt_files --mode <encrypt|decrypt> --password <string> [options]"
    echo ""
    echo "Description:"
    echo "  Encrypts or decrypts files using AES-256 with OpenSSL."
    echo ""
    echo "Options:"
    echo "  --mode <encrypt|decrypt>   Required. Operation mode."
    echo "  --password <string>        Required. Password to encrypt/decrypt."
    echo "  --ext <extension>          Only process files with this extension (e.g. txt)"
    echo "  --path <directory>         Directory to scan (default: current)"
    echo "  --out <directory>          Output directory (default: ./encrypted or ./decrypted)"
    echo "  --help                     Show this help message"
    echo ""
    echo "Examples:"
    echo "  shellman encrypt_files --mode encrypt --password mypass --ext log --path ./logs --out ./secure"
    echo "  shellman encrypt_files --mode decrypt --password mypass --ext enc --path ./secure --out ./plain "
}

MODE=""
PASSWORD=""
EXT=""
SCAN_PATH="."
OUT_DIR=""

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --help) show_help; exit 0 ;;
        --mode) MODE="$2"; shift ;;
        --password) PASSWORD="$2"; shift ;;
        --ext) EXT="$2"; shift ;;
        --path) SCAN_PATH="$2"; shift ;;
        --out) OUT_DIR="$2"; shift ;;
        -*)
            error "Unknown option: $1"
            show_help
            exit 1
            ;;
        *) error "Unexpected argument: $1"; exit 1 ;;
    esac
    shift
done

if [[ -z "$MODE" || -z "$PASSWORD" ]]; then
    error "Both --mode and --password are required."
    show_help
    exit 1
fi

if [[ "$MODE" != "encrypt" && "$MODE" != "decrypt" ]]; then
    error "Invalid mode: $MODE (expected 'encrypt' or 'decrypt')"
    exit 1
fi

if [[ -z "$OUT_DIR" ]]; then
    OUT_DIR="./${MODE}ed"
fi
mkdir -p "$OUT_DIR"

FILES=()
while IFS= read -r -d '' file; do
    [[ -n "$EXT" && "${file##*.}" != "$EXT" ]] && continue
    FILES+=("$file")
done < <(find "$SCAN_PATH" -type f -print0)

if [[ ${#FILES[@]} -eq 0 ]]; then
    warn "No matching files found."
    exit 0
fi

for FILE in "${FILES[@]}"; do
    BASENAME=$(basename "$FILE")
    if [[ "$MODE" == "encrypt" ]]; then
        OUT_FILE="$OUT_DIR/${BASENAME}.enc"
        openssl enc -aes-256-cbc -salt -in "$FILE" -out "$OUT_FILE" -k "$PASSWORD" 2>/dev/null
        info "Encrypted: $FILE → $OUT_FILE"
    else
        NAME="${BASENAME%.enc}"
        OUT_FILE="$OUT_DIR/${NAME}"
        openssl enc -d -aes-256-cbc -in "$FILE" -out "$OUT_FILE" -k "$PASSWORD" 2>/dev/null
        info "Decrypted: $FILE → $OUT_FILE"
    fi
done
