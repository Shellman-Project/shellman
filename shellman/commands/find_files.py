import os
from datetime import datetime
from pathlib import Path

import click


@click.command(
    help="""Finds files by partial name, extension, or matching content.

Examples:
  shellman find_files . --name log
  shellman find_files ./docs --content "error 404" --ext md
  shellman find_files ./src --name util --output --show-size
"""
)
@click.argument("search_path", type=click.Path(exists=True, file_okay=False))
@click.option("--name", "name_filter", help="Match filenames containing this fragment")
@click.option(
    "--content", "content_filter", help="Search for files containing this text"
)
@click.option("--ext", "ext_filter", help="Only include files with this extension")
@click.option(
    "--output", is_flag=True, help="Save results to logs/find_files_<timestamp>.log"
)
@click.option("--show-size", is_flag=True, help="Show file size next to each result")
def cli(search_path, name_filter, content_filter, ext_filter, output, show_size):
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
                if content_filter not in file.read_text(
                    encoding="utf-8", errors="ignore"
                ):
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
            size_mb = os.path.getsize(file) / (1024 * 1024)
            results.append(f"{file}  [{size_mb:.2f} MB]")
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
