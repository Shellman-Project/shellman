import fnmatch
import importlib.resources
from pathlib import Path

import click


@click.command(
    help="Prints a visual tree of directories (like 'tree')."
)
@click.argument("path", default=".", type=click.Path(exists=True, file_okay=False))
@click.option("--files", "-f", is_flag=True, help="Include files, not just folders")
@click.option("--depth", "-d", type=int, help="Limit recursion depth")
@click.option("--output", "-o", type=click.Path(), help="Save result to file")
@click.option("--hidden", "-hd", is_flag=True, help="Include hidden files/folders")
@click.option("--ascii", "-a", is_flag=True, help="Use ASCII instead of Unicode box lines")
@click.option(
    "--exclude",
    "-x",
    multiple=True,
    help="Exclude patterns (folder names, file names, or extensions, e.g. __pycache__, *.txt, *.pyc)"
)
@click.option("--lang-help", "lang", help="Show localized help (pl, eng)")
@click.option("--ascii", "-a", "use_ascii", is_flag=True, help="Use ASCII instead of Unicode box lines")
def cli(path, files, depth, output, hidden, use_ascii, exclude, lang):
    """
    Print a visual tree of directories and (optionally) files.

    Supports configurable recursion depth, exclusion patterns, hidden files,
    ASCII/Unicode output styles, and saving results to a file.

    Args:
        path (str): Root directory to start from. Defaults to current dir.
        files (bool): If True, include files as well as folders.
        depth (int | None): Limit recursion depth (None = no limit).
        output (str | None): Save tree output to this file instead of printing.
        hidden (bool): If True, include hidden files/folders (starting with ".").
        ascii (bool): If True, use ASCII characters instead of Unicode box drawing.
        exclude (list[str]): Glob patterns of files/folders to exclude
            (e.g., `__pycache__`, `*.pyc`, `*.log`).
        lang (str | None): Show localized help ("pl", "eng") instead of executing.

    Effects:
        - Prints directory tree to stdout or writes to file.

    Examples:
        Show directory tree including files:
            $ shellman dir_tree ./src -f

        Limit depth to 2 and use ASCII lines:
            $ shellman dir_tree ./project -d 2 -a

        Exclude cache and .log files:
            $ shellman dir_tree ./data -x __pycache__ -x "*.log"

        Save tree to file:
            $ shellman dir_tree ./src -o tree.txt
    """
    if lang:
        _print_help_md(lang)
        return

    default_excludes = ["__pycache__", "*.pyc"]
    exclude_patterns = list(default_excludes) + list(exclude)

    root = Path(path).resolve()
    tree = _build_tree(root, files, depth, hidden, use_ascii, exclude_patterns)
    if output:
        Path(output).write_text(tree, encoding="utf-8")
        click.echo(f"Saved to {output}")
    else:
        click.echo(tree)


def _build_tree(root: Path, include_files: bool, max_depth: int, show_hidden: bool, ascii_mode: bool, exclude_patterns):
    """
    Recursively build a directory tree representation.

    Args:
        root (Path): Root directory to traverse.
        include_files (bool): Whether to include files in output.
        max_depth (int | None): Maximum recursion depth (None = unlimited).
        show_hidden (bool): If True, include hidden files/folders.
        ascii_mode (bool): If True, use ASCII characters instead of Unicode.
        exclude_patterns (list[str]): Glob patterns of files/folders to skip.

    Returns:
        str: The formatted directory tree as a multi-line string.

    Notes:
        - Always starts with the root folder as the top node.
        - Exclusion is checked by both name and full path.

    Example:
        >>> from pathlib import Path
        >>> print(_build_tree(Path("."), True, 1, False, False, []))
        project/
        ├── README.md
        └── src/
    """
    lines = []

    def is_excluded(entry: Path) -> bool:
        """Check if the entry matches any exclude pattern."""
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(entry.name, pattern) or fnmatch.fnmatch(str(entry), pattern):
                return True
        return False

    def walk(dir_path, prefix="", level=0):
        if max_depth is not None and level > max_depth:
            return
        try:
            entries = sorted(
                [e for e in dir_path.iterdir()
                 if (show_hidden or not e.name.startswith(".")) and not is_excluded(e)],
                key=lambda e: (e.is_file(), e.name.lower())
            )
        except PermissionError:
            lines.append(f"{prefix}[access denied] {dir_path.name}/")
            return

        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            if ascii_mode:
                connector = "+-- " if is_last else "|-- "
            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                ext_prefix = "    " if is_last else ("│   " if not ascii_mode else "|   ")
                walk(entry, prefix + ext_prefix, level + 1)

    lines.append(f"{root.name}/")
    walk(root)
    return "\n".join(lines)


def _print_help_md(lang: str):
    """Print localized help text for the `dir_tree` command."""
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/dir_tree/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
