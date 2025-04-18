#!/bin/bash

source ./lib/utils.sh

show_help() {
    echo "Usage:"
    echo "  ./shellman.sh count_lines <file(s)/folder(s)> [options]"
    echo ""
    echo "Description:"
    echo "  Counts lines in one or more files. Supports recursive folder search."
    echo ""
    echo "Options:"
    echo "  --contains <text>     Count lines containing the text"
    echo "  --regex <pattern>     Count lines matching regex pattern"
    echo "  --ignore-case         Case-insensitive matching"
    echo "  --ext <extension>     Only include files with this extension (e.g. txt)"
    echo "  --summary             Show total + matched lines per file and overall"
    echo "  --percent             Show percentage of matching lines"
    echo "  --output              Save results to logs/ folder"
    echo "  --interactive         View results interactively (e.g. via 'less') "
    echo "  --show-size           Show size of file"
    echo "  --help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./shellman.sh count_lines logs --contains error --ext log --output --interactive"
}

SHOW_SIZE=false
INPUTS=()
CONTAINS=""
REGEX=""
IGNORE_CASE=false
SUMMARY=false
PERCENT=false
EXT=""
OUTPUT_TO_FILE=false
INTERACTIVE_MODE=false
OUTPUT_FILE=""

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --help) show_help; exit 0 ;;
        --contains) CONTAINS="$2"; shift ;;
        --regex) REGEX="$2"; shift ;;
        --ignore-case) IGNORE_CASE=true ;;
        --summary) SUMMARY=true ;;
        --percent) PERCENT=true ;;
        --ext) EXT="$2"; shift ;;
        --output) OUTPUT_TO_FILE=true ;;
        --interactive) INTERACTIVE_MODE=true ;;
        --show-size) SHOW_SIZE=true ;;
        -*)
            error "Unknown option: $1"
            show_help
            exit 1
            ;;
        *) INPUTS+=("$1") ;;
    esac
    shift
done

if [[ ${#INPUTS[@]} -eq 0 ]]; then
    error "No files or directories provided."
    show_help
    exit 1
fi

if [[ -n "$CONTAINS" && -n "$REGEX" ]]; then
    error "Use either --contains or --regex, not both."
    exit 1
fi

ALL_FILES=()

for INPUT in "${INPUTS[@]}"; do
    if [[ -f "$INPUT" ]]; then
        ALL_FILES+=("$INPUT")
    elif [[ -d "$INPUT" ]]; then
        while IFS= read -r -d '' file; do
            if [[ -n "$EXT" && "$file" != *.$EXT ]]; then
                continue
            fi
            ALL_FILES+=("$file")
        done < <(find "$INPUT" -type f -print0)
    else
        error "Invalid path: $INPUT"
    fi
done

if [[ ${#ALL_FILES[@]} -eq 0 ]]; then
    error "No valid files found after filtering."
    exit 1
fi
#
RESULTS=""
log_line() {
    echo "$1"
    RESULTS+="$1"$'\n'
}

TOTAL_ALL_LINES=0
TOTAL_ALL_MATCHED=0
FILE_COUNT=0

for FILE in "${ALL_FILES[@]}"; do
    if [[ ! -f "$FILE" ]]; then
        continue
    fi

    ((FILE_COUNT++))
    TOTAL_LINES=$(wc -l < "$FILE")
    MATCHED_LINES=0

    if [[ -n "$CONTAINS" ]]; then
        if [[ "$IGNORE_CASE" == true ]]; then
            MATCHED_LINES=$(grep -i -c "$CONTAINS" "$FILE")
        else
            MATCHED_LINES=$(grep -c "$CONTAINS" "$FILE")
        fi
    elif [[ -n "$REGEX" ]]; then
        if [[ "$IGNORE_CASE" == true ]]; then
            MATCHED_LINES=$(grep -i -E -c "$REGEX" "$FILE")
        else
            MATCHED_LINES=$(grep -E -c "$REGEX" "$FILE")
        fi
    else
        MATCHED_LINES="$TOTAL_LINES"
    fi

    TOTAL_ALL_LINES=$((TOTAL_ALL_LINES + TOTAL_LINES))
    TOTAL_ALL_MATCHED=$((TOTAL_ALL_MATCHED + MATCHED_LINES))

    log_line ""
    log_line "==> $FILE <=="
    if [[ "$SUMMARY" == true ]]; then
        log_line "$(info "Total lines: $TOTAL_LINES")"
        log_line "$(info "Matching lines: $MATCHED_LINES")"
    else
        log_line "$(info "Matching lines: $MATCHED_LINES")"
    fi

    if [[ "$PERCENT" == true && "$TOTAL_LINES" -gt 0 ]]; then
        PERCENTAGE=$(awk "BEGIN { printf \"%.2f\", ($MATCHED_LINES/$TOTAL_LINES)*100 }")
        log_line "$(info "Match percentage: $PERCENTAGE%")"
    fi

    if [[ "$SHOW_SIZE" == true ]]; then
       FILE_SIZE_MB=$(get_file_size_readable "$FILE")
       log_line "$(info "File size: ${FILE_SIZE_MB} ")"
    fi

done

if [[ "$FILE_COUNT" -gt 1 ]]; then
    log_line ""
    log_line "==> Summary <=="
    log_line "$(info "Total files: $FILE_COUNT")"
    log_line "$(info "Total lines: $TOTAL_ALL_LINES")"
    log_line "$(info "Total matching lines: $TOTAL_ALL_MATCHED")"
fi

if [[ "$OUTPUT_TO_FILE" == true ]]; then
    mkdir -p logs
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    OUTPUT_FILE="logs/count_lines_$TIMESTAMP.log"
    echo "$RESULTS" > "$OUTPUT_FILE"
    info "Results saved to $OUTPUT_FILE"
fi

if [[ "$INTERACTIVE_MODE" == true ]]; then
    if [[ "$OUTPUT_TO_FILE" == true ]]; then
        read -rp "Open result in 'less'? (Y/n): " CHOICE
        if [[ "$CHOICE" =~ ^[Yy]?$ ]]; then
            less "$OUTPUT_FILE"
        fi
    else
        echo ""
        echo "$RESULTS" | less
    fi
fi
