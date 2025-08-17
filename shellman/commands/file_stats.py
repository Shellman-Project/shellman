import importlib.resources
import os
from datetime import datetime
from pathlib import Path

import chardet
import click


@click.command(
    help="Show full path, file size, line-count and extension for each file."
)
@click.argument("inputs", nargs=-1)
@click.option("--ext", help="Only include files with this extension")
@click.option("--meta", is_flag=True, help="Include file metadata (created, modified, type, encoding)")
@click.option("--output", is_flag=True, help="Save results to logs/file_stats_<timestamp>.log")
@click.option("--lang-help", "lang", help="Show localized help (pl, eng) instead of executing")
def cli(inputs, ext, meta, output, lang):
    if lang:
        _print_help_md(lang)
        return

    if not inputs:
        raise click.UsageError("No files or directories provided.")

    all_files = []
    for input_path in inputs:
        path = Path(input_path)
        if path.is_file():
            if ext and path.suffix != f".{ext}":
                continue
            all_files.append(path.resolve())
        elif path.is_dir():
            for file in path.rglob("*"):
                if file.is_file() and (not ext or file.suffix == f".{ext}"):
                    all_files.append(file.resolve())
        else:
            click.echo(f"Invalid path: {input_path}", err=True)

    if not all_files:
        click.echo("No valid files found after filtering.", err=True)
        raise click.Abort()

    results = []
    for file in all_files:
        try:
            line_count = sum(1 for _ in file.open("r", encoding="utf-8", errors="ignore"))
        except Exception as e:
            line_count = f"Error: {e}"

        size_bytes = os.path.getsize(file)
        size_display = (
            f"{size_bytes / 1024:.2f} KB" if size_bytes < 1024 * 1024
            else f"{size_bytes / (1024 * 1024):.2f} MB"
        )
        file_ext = file.suffix or ""

        results.append(f"\n==> {file} <==")
        results.append(f"Lines     : {line_count}")
        results.append(f"Size      : {size_display}")
        results.append(f"Extension : {file_ext}")

        if meta:
            created = datetime.fromtimestamp(file.stat().st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            modified = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            ftype, encoding = detect_file_type_and_encoding(file)
            results.append(f"Created   : {created}")
            results.append(f"Modified  : {modified}")
            results.append(f"Type      : {ftype}")
            results.append(f"Encoding  : {encoding}")

    final_output = "\n".join(results)
    click.echo(final_output)

    if output:
        Path("logs").mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/file_stats_{timestamp}.log"
        Path(log_file).write_text(final_output, encoding="utf-8")
        click.echo(f"Results saved to {log_file}")


def detect_file_type_and_encoding(path: Path) -> tuple[str, str]:
    try:
        raw = path.read_bytes()
        detected = chardet.detect(raw)
        encoding = detected["encoding"] or "unknown"
        confidence = detected["confidence"] or 0

        if confidence > 0.8 and encoding.lower() in ("ascii", "utf-8"):
            return ("Text", encoding)
        elif b"\x00" in raw:
            return ("Binary", "binary")
        else:
            return ("Text", encoding or "unknown")
    except Exception:
        return ("unknown", "unknown")


def _print_help_md(lang: str = "eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/file_stats/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
