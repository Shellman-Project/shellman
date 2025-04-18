#!/bin/bash
#
source ./lib/utils.sh

show_help() {
    echo "Usage:"
    echo "  shellman zip_batch [options]"
    echo ""
    echo "Description:"
    echo "  Creates zip archives from files or folders."
    echo ""
    echo "Options:"
    echo "  --path <directory>       Source directory (default: .)"
    echo "  --ext <extension>        Only include files with this extension (e.g. txt) "
    echo "  --per-folder             Create one archive per subfolder"
    echo "  --name <prefix>          Archive name prefix (default: batch_)"
    echo "  --output <directory>     Output directory (default: ./zips)"
    echo "  --password <string>      Set password for zip (optional)"
    echo "  --help                   Show this help message"
    echo ""
    echo "Examples:"
    echo "  shellman zip_batch --path ./src --ext log --output ./archives"
    echo "  shellman zip_batch --path ./projects --per-folder --password secret --name backup_"
}

SRC_PATH="."
EXT=""
PER_FOLDER=false
OUT_DIR="./zips"
NAME_PREFIX="batch_"
PASSWORD=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --help) show_help; exit 0 ;;
        --path) SRC_PATH="$2"; shift ;;
        --ext) EXT="$2"; shift ;;
        --per-folder) PER_FOLDER=true ;;
        --output) OUT_DIR="$2"; shift ;;
        --name) NAME_PREFIX="$2"; shift ;;
        --password) PASSWORD="$2"; shift ;;
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

# Validate source
if [[ ! -d "$SRC_PATH" ]]; then
    error "Invalid directory: $SRC_PATH"
    exit 1
fi

mkdir -p "$OUT_DIR"

if [[ "$PER_FOLDER" == true ]]; then
    for dir in "$SRC_PATH"/*/; do
        [[ ! -d "$dir" ]] && continue
        BASENAME=$(basename "$dir")
        ZIPFILE="$OUT_DIR/${NAME_PREFIX}${BASENAME}.zip"

        CMD=(zip -r "$ZIPFILE" "$dir")
        [[ -n "$PASSWORD" ]] && CMD+=("-P" "$PASSWORD")

        echo "📦 Archiving folder: $dir → $ZIPFILE"
        "${CMD[@]}" > /dev/null
        info "Created: $ZIPFILE"
    done
else
    TMP_LIST=()
    while IFS= read -r -d '' file; do
        [[ -n "$EXT" && "${file##*.}" != "$EXT" ]] && continue
        TMP_LIST+=("$file")
    done < <(find "$SRC_PATH" -type f -print0)

    if [[ ${#TMP_LIST[@]} -eq 0 ]]; then
        warn "No matching files found to zip."
        exit 0
    fi

    ZIPFILE="$OUT_DIR/${NAME_PREFIX}files_$(date +%Y%m%d_%H%M%S).zip"
    CMD=(zip "$ZIPFILE")
    [[ -n "$PASSWORD" ]] && CMD+=("-P" "$PASSWORD")
    CMD+=("${TMP_LIST[@]}")

    echo "📦 Creating archive: $ZIPFILE"
    "${CMD[@]}" > /dev/null
    info "Created: $ZIPFILE"
fi
