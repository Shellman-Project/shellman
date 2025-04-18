#!/bin/bash
#
source ./lib/utils.sh

show_help() {
    echo "Usage:"
    echo "  shellman file_stats <file(s)/folder(s)> [options]"
    echo ""
    echo "Description:"
    echo "  Shows full path, file size, number of lines, and extension for each file."
    echo ""
    echo "Options:"
    echo "  --ext <extension>   Only include files with this extension (e.g. txt)"
    echo "  --output            Save the result to logs/file_stats_<timestamp>.log"
    echo "  --help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  shellman file_stats myfile.txt"
    echo "  shellman file_stats ./src --ext sh --output"
}

INPUTS=()
EXT=""
OUTPUT_TO_FILE=false
RESULTS=""

log_line() {
    echo "$1"
    RESULTS+="$1"$'\n'
}

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
        --output)
            OUTPUT_TO_FILE=true
            ;;
        -*)
            error "Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            INPUTS+=("$1")
            ;;
    esac
    shift
done

if [[ ${#INPUTS[@]} -eq 0 ]]; then
    error "No files or directories provided. "
    show_help
    exit 1
fi

ALL_FILES=()

for INPUT in "${INPUTS[@]}"; do
    if [[ -f "$INPUT" ]]; then
        [[ -n "$EXT" && "${INPUT##*.}" != "$EXT" ]] && continue
        ALL_FILES+=("$(realpath "$INPUT")")
    elif [[ -d "$INPUT" ]]; then
        while IFS= read -r -d '' file; do
            [[ -n "$EXT" && "${file##*.}" != "$EXT" ]] && continue
            [[ -f "$file" ]] && ALL_FILES+=("$(realpath "$file")")
        done < <(find "$INPUT" -type f -print0)
    else
        error "Invalid path: $INPUT"
    fi
done

if [[ ${#ALL_FILES[@]} -eq 0 ]]; then
    error "No valid files found after filtering."
    exit 1
fi

for FILE in "${ALL_FILES[@]}"; do
    LINE_COUNT=$(wc -l < "$FILE")
    FILE_SIZE=$(get_file_size_readable "$FILE")
    EXTENSION="${FILE##*.}"

    log_line ""
    log_line "==> $FILE <=="
    log_line "$(info "Lines: $LINE_COUNT")"
    log_line "$(info "Size: $FILE_SIZE")"
    log_line "$(info "Extension: .$EXTENSION")"
done

if [[ "$OUTPUT_TO_FILE" == true ]]; then
    mkdir -p logs
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    OUTPUT_FILE="logs/file_stats_$TIMESTAMP.log"
    echo "$RESULTS" > "$OUTPUT_FILE"
    info "Results saved to $OUTPUT_FILE"
fi
