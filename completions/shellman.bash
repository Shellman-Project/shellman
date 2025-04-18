_shellman_complete() {
  local cur=${COMP_WORDS[COMP_CWORD]}
  local prev=${COMP_WORDS[COMP_CWORD-1]}

  local commands="count_lines"
  local options="--contains --regex --ignore-case --summary --percent --ext --output --interactive"

  if [[ $COMP_CWORD == 1 ]]; then
    COMPREPLY=( $(compgen -W "$commands" -- "$cur") )
  else
    COMPREPLY=( $(compgen -W "$options" -- "$cur") )
  fi
}
#
complete -F _shellman_complete shellman
