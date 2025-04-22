# ----  SHELLMAN BASH COMPLETION  ----
# Requires bash-completion >= 1.3

_shellman() {
  local cur prev words cword
  _init_completion || return

  # ------ helpers ------
  _filedir_custom() {           # 1 arg = ext mask, "" = all
    COMPREPLY=( $(compgen -f -- "$cur") )
    [[ -n "$1" ]] && COMPREPLY=( ${COMPREPLY[@]/*.$1/} )
  }

  local cmd_dir="${SHELLMAN_HOME:-/usr/local/lib/shellman}/commands"
  local cmds="$(basename -s .sh "$cmd_dir"/*.sh 2>/dev/null)"

  _flags_for() {
    shellman "$1" --help 2>/dev/null | grep -oE -- '--[a-zA-Z0-9\-]+' | tr '\n' ' '
  }

  # ---------- commands after "shellman [TAB]" ----------
  if [[ $cword -eq 1 && "$cur" != --* ]]; then
    COMPREPLY=( $(compgen -W "$cmds" -- "$cur") )
    return
  fi

  # ---------- global and local flags ----------
  if [[ "$cur" == --* ]]; then
    local global="--help --version"
    if [[ $cword -eq 1 ]]; then
      COMPREPLY=( $(compgen -W "$global" -- "$cur") )
    else
      local sub="${words[1]}"
      COMPREPLY=( $(compgen -W "$(_flags_for "$sub") $global" -- "$cur") )
    fi
    return
  fi

  # ---------- files and directories for options ----------
  case "$prev" in
    --path)   _filedir ;;
    --output) _filedir ;;
  esac
}

complete -F _shellman shellman
