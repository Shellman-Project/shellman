import importlib.resources
from pathlib import Path

import click


def print_help_md(lang="eng"):
    """Print localized help text for the `change_line_end` command."""
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
@click.option("--file", "-f", "file_path", type=click.Path(exists=True, dir_okay=False), help="Path to a single file")
@click.option("--dir", "-d", "dir_path", type=click.Path(exists=True, file_okay=False), help="Path to directory (will recurse)")
@click.option("--ext", "-x", help="Only process files with this extension (requires --dir)")
@click.option("--to", "-t", "target", type=click.Choice(["lf", "crlf"]), help="Convert to specified line endings")
@click.option("--check", "-c", "check_mode", is_flag=True, help="Only check and report line ending type per file")
@click.option("--lang-help", "-lh", "lang", help="Show localized help (pl, eng) instead of executing the command")
def cli(file_path, dir_path, ext, target, check_mode, lang):
    """
    Command-line interface for converting or checking line endings (LF/CRLF).

    Supports scanning a single file or recursively processing a directory.
    Can either convert line endings to the specified style or check/report
    the current type per file.

    Args:
        file_path (str | None): Path to a single file (exclusive with `dir_path`).
        dir_path (str | None): Path to a directory (recursive search).
        ext (str | None): Only process files with this extension (requires `--dir`).
        target (str | None): Desired line endings ("lf" or "crlf").
            Required unless `check_mode` is used.
        check_mode (bool): If True, only report detected line endings per file.
        lang (str | None): Print localized help ("pl", "eng") instead of executing.

    Raises:
        click.UsageError: If neither `--to` nor `--check` is provided,
            or if neither `--file` nor `--dir` is specified.

    Examples:
        Check endings in a file:
            $ shellman change_line_end --file script.py --check

        Convert all `.txt` files in a folder to LF:
            $ shellman change_line_end --dir ./docs --ext txt --to lf
    """
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
    """
    Detect the type of line endings in a file.

    Reads the file as bytes and determines whether the file uses:
    - LF (`\n`)
    - CRLF (`\r\n`)
    - MIXED (both LF and CRLF in the same file)
    - NONE (no line endings found)
    - ERROR (if the file could not be read)

    Args:
        path (Path): Path to the file to inspect.

    Returns:
        str: One of {"LF", "CRLF", "MIXED", "NONE", "ERROR"}.
    """
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
    """
    Convert the line endings of a file to LF or CRLF.

    Reads the file in binary mode, normalizes its line endings, and writes
    the converted result back to the same file.

    Args:
        path (Path): Path to the file to convert.
        to (str): Target format, either "lf" or "crlf".

    Effects:
        - Overwrites the file with converted line endings.
        - Prints a success message or error to the console.

    Raises:
        Exception: If the file cannot be read or written.
    """
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
