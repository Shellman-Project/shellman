# ----  SHELLMAN BASH COMPLETION  ----
# Requires bash-completion >= 1.3

_shellman() {
  local cur prev words cword
  _init_completion || return    # sets $cur $prev $words $cword

  # ------ helpers ------
  _filedir_custom() {           # 1 arg = ext mask, "" = all
    COMPREPLY=( $(compgen -f -- "$cur") )
    [[ -n "$1" ]] && COMPREPLY=( ${COMPREPLY[@]/*.$1/} )
  }

  local cmd_dir="${SHELLMAN_HOME:-/usr/local/lib/shellman}/commands"
  local cmds="$(basename -s .sh "$cmd_dir"/*.sh 2>/dev/null)"

  _flags_for() {                # dynamic flags from --help
    shellman "$1" --help 2>/dev/null | grep -oE -- '--[a-zA-Z0-9\-]+' | tr '\n' ' '
  }

  # ---------- stage 0 :  komenda bez spacji ----------
  if [[ $cword -eq 0 ]]; then
    COMPREPLY=( $(compgen -W "$cmds" -- "$cur") )
    compopt -o nospace
    return
  fi

  # ---------- które sub‑polecenie? ----------
  local sub="${words[1]}"

  # ---------- stage 1 : global + lokalne flagi ----------
  if [[ "$cur" == --* ]]; then
    local global="--help --version"
    if [[ $cword -eq 1 ]]; then        # jeszcze przed nazwą komendy
      COMPREPLY=( $(compgen -W "$global" -- "$cur") )
    else                               # po nazwie komendy
      COMPREPLY=( $(compgen -W "$(_flags_for "$sub") $global" -- "$cur") )
    fi
    return
  fi

  # ---------- stage 2 : pliki / katalogi dla opcji ----------
  case "$prev" in
    --path)   _filedir ;;      # dowolny plik/katalog
    --output) _filedir ;;      # pliki w bieżącym kat.
  esac
}
complete -F _shellman shellman
