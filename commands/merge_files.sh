#!/bin/bash
#
source ./lib/utils.sh

show_help() {
    echo "Usage:"
    echo "  shellman merge_files [options]"
    echo ""
    echo "Description:"
    echo "  Merges multiple text files into a single file."
    echo ""
    echo "Options:"
    echo "  --ext <extension>     Only include files with this extension (e.g. txt)"
    echo "  --out <filename>      Output file name (default: merged_<timestamp>.txt)"
    echo "  --path <directory>    Directory to scan (default: current directory)"
    echo "  --header              Add filename headers before each file's content"
    echo "  --sort                Sort files alphabetically before merging"
    echo "  --help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  shellman merge_files --ext log --out all_logs.txt --header --sort"
}

EXT=""
OUT=""
PATH_TO_SCAN="."
HEADER=false
SORT=false

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --help)
            show_help
            exit 0
            ;;
        --ext)
            EXT="$2"
            shift
            ;;
        --out)
            OUT="$2"
            shift
            ;;
        --path)
            PATH_TO_SCAN="$2"
            shift
            ;;
        --header)
            HEADER=true
            ;;
        --sort)
            SORT=true
            ;;
        -*)
            error "Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            error "Unexpected argument: $1"
            exit 1
            ;;
    esac
    shift
done

if [[ ! -d "$PATH_TO_SCAN" ]]; then
    error "Invalid directory: $PATH_TO_SCAN"
    exit 1
fi

# Szukanie plików
FILES=()
while IFS= read -r -d '' file; do
    [[ -n "$EXT" && "${file##*.}" != "$EXT" ]] && continue
    FILES+=("$file")
done < <(find "$PATH_TO_SCAN" -type f -print0)

if [[ ${#FILES[@]} -eq 0 ]]; then
    warn "No files found to merge. "
    exit 0
fi

# Sortowanie opcjonalne
if [[ "$SORT" == true ]]; then
    IFS=$'\n' FILES=($(sort <<<"${FILES[*]}"))
    unset IFS
fi

# Wyjściowy plik
mkdir -p logs
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUT_FILE="${OUT:-logs/merged_$TIMESTAMP.txt}"

echo "🔀 Merging ${#FILES[@]} file(s) into: $OUT_FILE"
> "$OUT_FILE"

for FILE in "${FILES[@]}"; do
    if [[ "$HEADER" == true ]]; then
        echo -e "\n=== $(realpath "$FILE") ===" >> "$OUT_FILE"
    fi
    cat "$FILE" >> "$OUT_FILE"
done

info "Merge complete: $OUT_FILE"
