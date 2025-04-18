#!/bin/bash
#
source ./lib/utils.sh

show_help() {
    echo "Usage:"
    echo "  shellman find_files <path> [options]"
    echo ""
    echo "Description:"
    echo "  Finds files by partial name, extension, or matching content."
    echo ""
    echo "Options:"
    echo "  --name <fragment>      Match filenames containing the fragment"
    echo "  --content <text>       Search for files containing this text"
    echo "  --ext <extension>      Only include files with this extension (e.g. txt)"
    echo "  --output               Save results to logs/find_files_<timestamp>.log"
    echo "  --show-size            Show file size next to each result"
    echo "  --help                 Show this help message"
    echo ""
    echo "Examples:"
    echo "  shellman find_files . --name log"
    echo "  shellman find_files ./docs --content \"error 404\" --ext md "
    echo "  shellman find_files ./src --name util --output"
}

SEARCH_PATH=""
NAME_FILTER=""
CONTENT_FILTER=""
EXT_FILTER=""
OUTPUT_TO_FILE=false
RESULTS=""
SHOW_SIZE=false

log_line() {
    echo "$1"
    RESULTS+="$1"$'\n'
}

# Argument parsing
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --help)
            show_help
            exit 0
            ;;
        --name)
            NAME_FILTER="$2"
            shift
            ;;
        --content)
            CONTENT_FILTER="$2"
            shift
            ;;
        --ext)
            EXT_FILTER="$2"
            shift
            ;;
        --output)
            OUTPUT_TO_FILE=true
            ;;
        --show-size) SHOW_SIZE=true ;;

        -*)
            error "Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            if [[ -z "$SEARCH_PATH" ]]; then
                SEARCH_PATH="$1"
            else
                error "Unexpected argument: $1"
                exit 1
            fi
            ;;
    esac
    shift
done

if [[ -z "$SEARCH_PATH" ]]; then
    error "No path provided."
    show_help
    exit 1
fi

if [[ ! -d "$SEARCH_PATH" ]]; then
    error "Path is not a directory: $SEARCH_PATH"
    exit 1
fi

FOUND=()

while IFS= read -r -d '' FILE; do
    BASENAME=$(basename "$FILE")

    [[ -n "$NAME_FILTER" && "$BASENAME" != *"$NAME_FILTER"* ]] && continue
    [[ -n "$EXT_FILTER" && "${FILE##*.}" != "$EXT_FILTER" ]] && continue
    if [[ -n "$CONTENT_FILTER" ]]; then
        if ! grep -q "$CONTENT_FILTER" "$FILE" 2>/dev/null; then
            continue
        fi
    fi

    FOUND+=("$(realpath "$FILE")")
done < <(find "$SEARCH_PATH" -type f -print0)

if [[ ${#FOUND[@]} -eq 0 ]]; then
    error "No files found matching criteria."
    exit 1
fi

for FILE in "${FOUND[@]}"; do
    if [[ "$SHOW_SIZE" == true ]]; then
        SIZE=$(get_file_size_readable "$FILE")
        log_line "$FILE  [$SIZE]"
    else
        log_line "$FILE"
    fi
done


if [[ "$OUTPUT_TO_FILE" == true ]]; then
    mkdir -p logs
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    OUTPUT_FILE="logs/find_files_$TIMESTAMP.log"
    echo "$RESULTS" > "$OUTPUT_FILE"
    info "Results saved to $OUTPUT_FILE"
fi
