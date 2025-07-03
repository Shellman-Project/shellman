import os
from pathlib import Path
import importlib.resources
import click


def print_help_md(lang="eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(f"help_texts/change_line_end/{lang_file}")
        content = help_path.read_text(encoding="utf-8")
        click.echo(content)
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)


@click.command(
    help="Convert or check LF/CRLF line endings in files or folders."
)
@click.option("--file", "file_path", type=click.Path(exists=True, dir_okay=False), help="Path to a single file")
@click.option("--dir", "dir_path", type=click.Path(exists=True, file_okay=False), help="Path to directory (will recurse)")
@click.option("--ext", help="Only process files with this extension (requires --dir)")
@click.option("--to", "target", type=click.Choice(["lf", "crlf"]), help="Convert to specified line endings")
@click.option("--check", "check_mode", is_flag=True, help="Only check and report line ending type per file")
@click.option("--lang-help", "lang", help="Show localized help (pl, eng) instead of executing the command")
def cli(file_path, dir_path, ext, target, check_mode, lang):
    if lang:
        print_help_md(lang)
        return

    if not check_mode and not target:
        raise click.UsageError("Either --to or --check is required")
    if not file_path and not dir_path:
        raise click.UsageError("Must specify --file or --dir")

    files = []
    if file_path:
        files = [Path(file_path)]
    elif dir_path:
        ext = ext.lstrip(".") if ext else None
        path_obj = Path(dir_path)
        files = [
            f
            for f in path_obj.rglob("*")
            if f.is_file() and (not ext or f.suffix == f".{ext}")
        ]

    for f in files:
        if check_mode:
            ending = detect_endings(f)
            click.echo(f"🔍 {f} → {ending}")
        else:
            convert_endings(f, target)


def detect_endings(path: Path) -> str:
    try:
        with path.open("rb") as f:
            content = f.read()
        if b"\r\n" in content:
            if b"\n" in content.replace(b"\r\n", b""):
                return "MIXED"
            return "CRLF"
        elif b"\n" in content:
            return "LF"
        return "NONE"
    except Exception:
        return "ERROR"


def convert_endings(path: Path, to: str):
    try:
        content = path.read_bytes()
        if to == "lf":
            converted = content.replace(b"\r\n", b"\n")
            msg = "→ converted to LF"
        else:
            converted = content.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
            msg = "→ converted to CRLF"
        path.write_bytes(converted)
        click.echo(f"{msg}: {path}")
    except Exception as e:
        click.secho(f"Failed to process {path}: {e}", fg="red")
