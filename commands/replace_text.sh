#!/bin/bash
#
source ./lib/utils.sh

show_help() {
    echo "Usage:"
    echo "  shellman replace_text <path> [options]"
    echo ""
    echo "Description:"
    echo "  Replaces text in multiple files with optional preview and confirmation."
    echo ""
    echo "Options:"
    echo "  --find <text>         Text to find (required)"
    echo "  --replace <text>      Text to replace with (required)"
    echo "  --ext <extension>     Only process files with this extension"
    echo "  --in-place            Write changes back to files"
    echo "  --preview             Show changes using 'diff'"
    echo "  --confirm             Ask before replacing in each file"
    echo "  --help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  shellman replace_text ./docs --find old --replace new --ext md --in-place --preview"
}

SEARCH_PATH=""
FIND_TEXT=""
REPLACE_TEXT=""
EXT=""
IN_PLACE=false
CONFIRM=false
PREVIEW=false

# Parse args
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --help) show_help; exit 0 ;;
        --find) FIND_TEXT="$2"; shift ;;
        --replace) REPLACE_TEXT="$2"; shift ;;
        --ext) EXT="$2"; shift ;;
        --in-place) IN_PLACE=true ;;
        --preview) PREVIEW=true ;;
        --confirm) CONFIRM=true ;;
        -*)
            error "Unknown option: $1"
            show_help
            exit 1
            ;;
        *) SEARCH_PATH="$1" ;;
    esac
    shift
done

# Validation
if [[ -z "$SEARCH_PATH" ]]; then error "Missing path"; show_help; exit 1; fi
if [[ -z "$FIND_TEXT" || -z "$REPLACE_TEXT" ]]; then error "Missing --find or --replace"; show_help; exit 1; fi
if [[ ! -d "$SEARCH_PATH" ]]; then error "Path does not exist: $SEARCH_PATH"; exit 1; fi

# Find matching files
FILES=()
while IFS= read -r -d '' file; do
    [[ -n "$EXT" && "${file##*.}" != "$EXT" ]] && continue
    grep -q "$FIND_TEXT" "$file" 2>/dev/null && FILES+=("$file")
done < <(find "$SEARCH_PATH" -type f -print0)

if [[ ${#FILES[@]} -eq 0 ]]; then
    MESSAGE="No files matched search criteria. "
    echo -e "\e[33m⚠️  $MESSAGE\e[0m"
    exit 0
fi

# Process files
for FILE in "${FILES[@]}"; do
    echo ""
    echo "==> $FILE"

    TMP_FILE=$(mktemp)
    sed "s/${FIND_TEXT}/${REPLACE_TEXT}/g" "$FILE" > "$TMP_FILE"

    if [[ "$PREVIEW" == true ]]; then
        diff -u "$FILE" "$TMP_FILE" || true
    fi

    if [[ "$IN_PLACE" == true ]]; then
        DO_REPLACE=true
        if [[ "$CONFIRM" == true ]]; then
            read -rp "Replace in this file? (Y/n): " CHOICE
            [[ "$CHOICE" =~ ^[Nn]$ ]] && DO_REPLACE=false
        fi

        if [[ "$DO_REPLACE" == true ]]; then
            mv "$TMP_FILE" "$FILE"
            info "Replaced in: $FILE"
        else
            rm "$TMP_FILE"
            warn "Skipped: $FILE"
        fi
    else
        rm "$TMP_FILE"
    fi
done
