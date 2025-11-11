import fnmatch
import importlib.resources
from collections.abc import Iterable
from pathlib import Path
from typing import Optional

import click


@click.command(help="Prints a visual tree of directories (like 'tree').")
@click.argument("path", default=".", type=click.Path(exists=True, file_okay=False))
@click.option("--files", "-f", is_flag=True, help="Include files, not just folders")
@click.option("--depth", "-d", type=int, help="Limit recursion depth (0 = root only)")
@click.option("--output", "-o", type=click.Path(), help="Save result to file")
@click.option("--hidden", "-hd", is_flag=True, help="Include hidden files/folders")
@click.option(
    "--exclude",
    "-x",
    multiple=True,
    help="Exclude patterns (folder names, file names, or extensions, e.g. __pycache__, *.txt, *.pyc)",
)
@click.option("--lang-help", "lang", help="Show localized help (pl, eng)")
@click.option(
    "--ascii",
    "-a",
    "use_ascii",
    is_flag=True,
    help="Use ASCII instead of Unicode box lines",
)
def cli(path, files, depth, output, hidden, use_ascii, exclude, lang):
    """
    Print a visual tree of directories and (optionally) files.

    Supports configurable recursion depth, exclusion patterns, hidden files,
    ASCII/Unicode output styles, and saving results to a file.

    Args:
        path (str): Root directory to start from. Defaults to current dir.
        files (bool): If True, include files as well as folders.
        depth (int | None): Limit recursion depth (None = no limit). 0 = root only.
        output (str | None): Save tree output to this file instead of printing.
        hidden (bool): If True, include hidden files/folders (starting with ".").
        use_ascii (bool): If True, use ASCII characters instead of Unicode.
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
    tree = _build_tree(
        root=root,
        include_files=files,
        max_depth=depth,
        show_hidden=hidden,
        ascii_mode=use_ascii,
        exclude_patterns=exclude_patterns,
    )
    if output:
        Path(output).write_text(tree, encoding="utf-8")
        click.echo(f"Saved to {output}")
    else:
        click.echo(tree)


def _build_tree(
    *,
    root: Path,
    include_files: bool,
    max_depth: Optional[int],
    show_hidden: bool,
    ascii_mode: bool,
    exclude_patterns: Iterable[str],
) -> str:
    """Recursively build a directory tree representation.

    - `max_depth` semantics:
        * None  -> unlimited depth
        * 0     -> show only the root directory name
        * N>0   -> show up to N levels below root
    """
    # Select drawing characters based on chosen style
    if ascii_mode:
        elbow = "+-- "
        tee = "|-- "
        pipe = "|   "
        space = "    "
    else:
        elbow = "└── "
        tee = "├── "
        pipe = "│   "
        space = "    "

    lines: list[str] = []

    def is_excluded(entry: Path) -> bool:
        """Return True if entry matches any of the exclude patterns."""
        name = entry.name
        path_str = str(entry)
        for pattern in exclude_patterns:
            # Match by name and by full path
            if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(path_str, pattern):
                return True
        return False

    def list_entries(dir_path: Path) -> list[Path]:
        """List directory entries honoring hidden/exclude/include_files flags."""
        try:
            items = list(dir_path.iterdir())
        except PermissionError:
            # Cannot read directory contents
            return []

        # Hide "dot" items unless requested
        if not show_hidden:
            items = [e for e in items if not e.name.startswith(".")]

        # Apply exclude filters
        items = [e for e in items if not is_excluded(e)]

        # If files are not requested, keep only directories
        if not include_files:
            items = [e for e in items if e.is_dir()]

        # Sort: directories first, then files; alphabetical (case-insensitive)
        items.sort(key=lambda e: (e.is_file(), e.name.lower()))
        return items

    def walk(dir_path: Path, prefix: str, level: int) -> None:
        """Depth-first traversal that appends pretty lines to `lines`.

        `level` counts how deep we are *below* the root:
            root children -> level=0, grandchildren -> level=1, etc.
        We stop descending once `level >= max_depth` (if limited).
        """
        # If max_depth is set and we've reached it, stop here (no children)
        if max_depth is not None and level >= max_depth:
            return

        entries = list_entries(dir_path)
        if not entries and max_depth is not None and level < max_depth:
            return

        for idx, entry in enumerate(entries):
            last = idx == len(entries) - 1
            connector = elbow if last else tee
            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                child_prefix = prefix + (space if last else pipe)
                walk(entry, child_prefix, level + 1)

    # Always start with the root folder as the top node
    lines.append(f"{root.name}/")

    # If depth is None -> unlimited; if depth == 0 -> only root (no children)
    if max_depth is None or max_depth > 0:
        walk(root, prefix="", level=0)

    return "\n".join(lines)


def _print_help_md(lang: str) -> None:
    """Print localized help text for the `dir_tree` command."""
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/dir_tree/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
