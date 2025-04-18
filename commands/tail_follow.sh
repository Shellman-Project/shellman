#!/bin/bash
#
source ./lib/utils.sh

show_help() {
    echo "Usage:"
    echo "  shellman tail_follow <file> [options]"
    echo ""
    echo "Description:"
    echo "  Follows (tail -f) a single file in real time."
    echo "  Optionally filters lines containing specific text and highlights them."
    echo ""
    echo "Options:"
    echo "  --contains <text>    Show only lines containing <text>"
    echo "  --ignore-case        Ignore case when searching with --contains"
    echo "  --highlight <text>   Highlight this text in red"
    echo "  --help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  shellman tail_follow /var/log/syslog --contains error --highlight error"
}

FILE=""
CONTAINS=""
IGNORE_CASE=false
HIGHLIGHT=""

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --help)
            show_help
            exit 0
            ;;
        --contains)
            CONTAINS="$2"
            shift
            ;;
        --ignore-case)
            IGNORE_CASE=true
            ;;
        --highlight)
            HIGHLIGHT="$2"
            shift
            ;;
        -*)
            error "Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            if [[ -z "$FILE" ]]; then
                FILE="$1"
            else
                error "Unexpected argument: $1"
                exit 1
            fi
            ;;
    esac
    shift
done

if [[ -z "$FILE" ]]; then
    error "Missing file to follow."
    show_help
    exit 1
fi

if [[ ! -f "$FILE" ]]; then
    error "File not found: $FILE"
    exit 1
fi

info "Following file: $FILE (press Ctrl+C to stop) "

TAIL_CMD="tail -f \"$FILE\""
GREP_CMD="cat"
if [[ -n "$CONTAINS" ]]; then
    if [[ "$IGNORE_CASE" == true ]]; then
        GREP_CMD="grep -i \"$CONTAINS\""
    else
        GREP_CMD="grep \"$CONTAINS\""
    fi
fi

COLOR_CMD="cat"
if [[ -n "$HIGHLIGHT" ]]; then
    COLOR_CMD="sed -E 's/(${HIGHLIGHT})/\x1b[31m\1\x1b[0m/g'"
fi

# tail -f -> grep (opcjonalny) -> sed highlight (opcjonalny)
bash -c "$TAIL_CMD | $GREP_CMD | $COLOR_CMD"
