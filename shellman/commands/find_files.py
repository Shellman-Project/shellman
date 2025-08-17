import importlib.resources
import os
from datetime import datetime
from pathlib import Path

import click


def print_help_md(lang="eng"):
    """Load and print help from markdown file."""
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(f"help_texts/find_files/{lang_file}")
        content = help_path.read_text(encoding="utf-8")
        click.echo(content)
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)


@click.command(
    help="Find files by name, extension or content with filtering options."
)
@click.argument("search_path", required=False, type=click.Path(exists=True, file_okay=False))
@click.option("--name","-n", "name_filter", help="Match filenames containing this fragment")
@click.option("--content","-c", "content_filter", help="Search for files containing this text")
@click.option("--ext","-e", "ext_filter", help="Only include files with this extension")
@click.option("--output","-o", is_flag=True, help="Save results to logs/find_files_<timestamp>.log")
@click.option("--show-size","-s", is_flag=True, help="Show file size next to each result")
@click.option("--lang-help","-lh", "lang", help="Show localized help (pl, eng) instead of executing the command")
def cli(search_path, name_filter, content_filter, ext_filter, output, show_size, lang):
    if lang:
        print_help_md(lang)
        return

    if not search_path:
        click.echo("❗ Missing required SEARCH_PATH\n")
        print_help_md("eng")
        return

    path = Path(search_path)
    if not path.is_dir():
        click.echo(f"Path is not a directory: {search_path}", err=True)
        raise click.Abort()

    found_files = []

    for file in path.rglob("*"):
        if not file.is_file():
            continue
        if name_filter and name_filter not in file.name:
            continue
        if ext_filter and file.suffix != f".{ext_filter}":
            continue
        if content_filter:
            try:
                if content_filter not in file.read_text(encoding="utf-8", errors="ignore"):
                    continue
            except Exception:
                continue
        found_files.append(file.resolve())

    if not found_files:
        click.echo("No files found matching criteria.", err=True)
        raise click.Abort()

    results = []
    for file in found_files:
        if show_size:
            size_bytes = os.path.getsize(file)
            if size_bytes < 1024 * 1024:                          # < 1 MiB
                size_display = f"{size_bytes / 1024:.2f} KB"
            else:
                size_display = f"{size_bytes / (1024 * 1024):.2f} MB"
            results.append(f"{file}  [{size_display}]")
        else:
            results.append(str(file))


    final_output = "\n".join(results)
    click.echo(final_output)

    if output:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/find_files_{timestamp}.log"
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(final_output)
        click.echo(f"Results saved to {log_file}")
