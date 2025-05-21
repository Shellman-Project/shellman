import os
import re
import sys
from datetime import datetime
from pathlib import Path

import click


@click.command(
    help="""Counts lines in files or folders with filtering options.

Examples:
  shellman count_lines logs --contains error --ext log --output
  shellman count_lines . --regex "TODO|FIXME" --ignore-case --summary --percent
"""
)
@click.argument("inputs", nargs=-1, type=click.Path(exists=True))
@click.option("--contains", help="Count lines containing this text")
@click.option("--regex", help="Count lines matching regex pattern")
@click.option("--ignore-case", is_flag=True, help="Case-insensitive matching")
@click.option("--ext", help="Only include files with this extension")
@click.option("--summary", is_flag=True, help="Show summary per file and overall")
@click.option("--percent", is_flag=True, help="Show percentage of matching lines")
@click.option("--output", is_flag=True, help="Save results to logs/ folder")
@click.option("--interactive", is_flag=True, help="View results interactively")
@click.option("--show-size", is_flag=True, help="Show file size")
def cli(
    inputs,
    contains,
    regex,
    ignore_case,
    ext,
    summary,
    percent,
    output,
    interactive,
    show_size,
):
    if contains and regex:
        click.echo("Use either --contains or --regex, not both.", err=True)
        sys.exit(1)

    all_files = []
    for input_path in inputs:
        path = Path(input_path)
        if path.is_file():
            if ext and not path.name.endswith(f".{ext}"):
                continue
            all_files.append(path)
        elif path.is_dir():
            for file in path.rglob("*"):
                if file.is_file() and (not ext or file.name.endswith(f".{ext}")):
                    all_files.append(file)
        else:
            click.echo(f"Invalid path: {input_path}", err=True)

    if not all_files:
        click.echo("No valid files found after filtering.", err=True)
        sys.exit(1)

    flags = re.IGNORECASE if ignore_case else 0
    pattern = re.compile(regex, flags) if regex else None

    results = []
    total_all_lines = 0
    total_all_matched = 0

    for file in all_files:
        with file.open("r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        total_lines = len(lines)
        matched_lines = 0

        for line in lines:
            if contains:
                if (
                    (contains.lower() in line.lower())
                    if ignore_case
                    else (contains in line)
                ):
                    matched_lines += 1
            elif pattern:
                if pattern.search(line):
                    matched_lines += 1
            else:
                matched_lines = total_lines
                break

        total_all_lines += total_lines
        total_all_matched += matched_lines

        results.append(f"\n==> {file} <==")
        if summary:
            results.append(f"Total lines: {total_lines}")
        results.append(f"Matching lines: {matched_lines}")

        if percent and total_lines > 0:
            perc = (matched_lines / total_lines) * 100
            results.append(f"Match percentage: {perc:.2f}%")

        if show_size:
            size_mb = os.path.getsize(file) / (1024 * 1024)
            results.append(f"File size: {size_mb:.2f} MB")

    if len(all_files) > 1:
        results.append("\n==> Summary <==")
        results.append(f"Total files: {len(all_files)}")
        results.append(f"Total lines: {total_all_lines}")
        results.append(f"Total matching lines: {total_all_matched}")

    final_output = "\n".join(results)
    click.echo(final_output)

    if output:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/count_lines_{timestamp}.log"
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(final_output)
        click.echo(f"Results saved to {log_file}")

    if interactive:
        pager = os.environ.get("PAGER", "less")
        click.echo("\n(Showing result interactively...)\n")
        click.echo_via_pager(final_output)
