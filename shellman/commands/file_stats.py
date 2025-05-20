import click
import os
from pathlib import Path
from datetime import datetime

@click.command()
@click.argument("inputs", nargs=-1, type=click.Path(exists=True))
@click.option("--ext", help="Only include files with this extension")
@click.option("--output", is_flag=True, help="Save results to logs/file_stats_<timestamp>.log")
def cli(inputs, ext, output):
    """Shows full path, file size, number of lines, and extension for each file."""
    if not inputs:
        click.echo("No files or directories provided.", err=True)
        raise click.Abort()

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
        if size_bytes < 1024 * 1024:
            size_display = f"{size_bytes / 1024:.2f} KB"
        else:
            size_display = f"{size_bytes / (1024 * 1024):.2f} MB"

        ext = file.suffix or ""

        results.append(f"\n==> {file} <==")
        results.append(f"Lines: {line_count}")
        results.append(f"Size: {size_display}")
        results.append(f"Extension: {ext}")

    final_output = "\n".join(results)
    click.echo(final_output)

    if output:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/file_stats_{timestamp}.log"
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(final_output)
        click.echo(f"Results saved to {log_file}")
        