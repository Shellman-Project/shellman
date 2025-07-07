import os
from pathlib import Path
import click
import importlib.resources


@click.command(
    help="Prints a visual tree of directories (like 'tree')."
)
@click.argument("path", default=".", type=click.Path(exists=True, file_okay=False))
@click.option("--files", is_flag=True, help="Include files, not just folders")
@click.option("--depth", type=int, help="Limit recursion depth")
@click.option("--output", type=click.Path(), help="Save result to file")
@click.option("--hidden", is_flag=True, help="Include hidden files/folders")
@click.option("--ascii", is_flag=True, help="Use ASCII instead of Unicode box lines")
@click.option("--lang-help", "lang", help="Show localized help (pl, eng)")
def cli(path, files, depth, output, hidden, ascii, lang):
    if lang:
        _print_help_md(lang)
        return

    root = Path(path).resolve()
    tree = _build_tree(root, files, depth, hidden, ascii)
    if output:
        Path(output).write_text(tree, encoding="utf-8")
        click.echo(f"Saved to {output}")
    else:
        click.echo(tree)


def _build_tree(root: Path, include_files: bool, max_depth: int, show_hidden: bool, ascii_mode: bool):
    lines = []

    def walk(dir_path, prefix="", level=0):
        try:
            entries = [
                e for e in dir_path.iterdir()
                if show_hidden or not e.name.startswith(".")
            ]
        except PermissionError:
            print(f"{prefix}{dir_path.name} [access denied]")
            return
        print(f"{prefix}{dir_path.name}/")
        for entry in entries:
            if entry.is_dir():
                walk(entry, prefix + "    ", level + 1)
            else:
                print(f"{prefix}    {entry.name}")
        if max_depth is not None and level > max_depth:
            return
        entries = sorted(
            [e for e in dir_path.iterdir() if show_hidden or not e.name.startswith(".")],
            key=lambda e: (e.is_file(), e.name.lower())
        )
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            if ascii_mode:
                connector = "+-- " if is_last else "|-- "
            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                ext_prefix = "    " if is_last else ("│   " if not ascii_mode else "|   ")
                walk(entry, prefix + ext_prefix, level + 1)
            elif include_files:
                continue

    lines.append(f"{root.name}/")
    walk(root)
    return "\n".join(lines)


def _print_help_md(lang: str):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/dir_tree/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
