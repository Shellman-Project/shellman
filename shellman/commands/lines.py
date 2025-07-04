from pathlib import Path
import re
import os
from datetime import datetime
import importlib.resources

import click

@click.command(
    help="Extract, count or summarize lines in files or folders with powerful filters and context options."
)
@click.argument("inputs", nargs=-1, type=click.Path(exists=True))
@click.option("--extract", is_flag=True, help="Print out matching lines (default mode)")
@click.option("--count", is_flag=True, help="Show only count of matching lines")
@click.option("--summary", is_flag=True, help="Print summary (files, total lines, matches)")
@click.option("--contains", help="Keep lines containing this text")
@click.option("--not-contains", help="Keep lines NOT containing this text")
@click.option("--regex", help="Count or extract lines matching regex")
@click.option("--ignore-case", is_flag=True, help="Case-insensitive matching")
@click.option("--before", type=int, default=0, help="Show N lines before each match")
@click.option("--after", type=int, default=0, help="Show N lines after each match")
@click.option("--ext", help="Only include files with this extension")
@click.option("--percent", is_flag=True, help="Show percentage of matches")
@click.option("--output", type=click.Path(), help="Save result to file")
@click.option("--interactive", is_flag=True, help="View results in pager")
@click.option("--show-size", is_flag=True, help="Show file size in output")
@click.option("--lang-help", "lang", help="Show localized help (pl, eng) instead of executing")
def cli(
    inputs,
    extract,
    count,
    summary,
    contains,
    not_contains,
    regex,
    ignore_case,
    before,
    after,
    ext,
    percent,
    output,
    interactive,
    show_size,
    lang
):
    if lang:
        _print_help_md(lang)
        return

    # Default: extract if nothing else
    if not extract and not count and not summary:
        extract = True

    # Validation
    if contains and regex:
        click.echo("Use either --contains OR --regex, not both.", err=True)
        return

    if not inputs:
        click.echo("No files or directories provided.", err=True)
        return

    files = []
    for input_path in inputs:
        path = Path(input_path)
        if path.is_file():
            if ext and not path.name.endswith(f".{ext}"):
                continue
            files.append(path)
        elif path.is_dir():
            for file in path.rglob("*"):
                if file.is_file() and (not ext or file.name.endswith(f".{ext}")):
                    files.append(file)
        else:
            click.echo(f"Invalid path: {input_path}", err=True)

    if not files:
        click.echo("No valid files found after filtering.", err=True)
        return

    total_all_lines = 0
    total_all_matched = 0
    output_lines = []

    flags = re.IGNORECASE if ignore_case else 0
    pattern = re.compile(regex, flags) if regex else None

    for file in files:
        with file.open("r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        total_lines = len(lines)
        total_all_lines += total_lines

        # Find matched line indices
        matched_indices = []
        for idx, line in enumerate(lines):
            match = False
            if contains:
                match = (contains.lower() in line.lower()) if ignore_case else (contains in line)
            elif not_contains:
                match = (not_contains.lower() not in line.lower()) if ignore_case else (not_contains not in line)
            elif pattern:
                match = bool(pattern.search(line))
            else:
                match = True  # if no filter, everything matches

            if match:
                matched_indices.append(idx)
        num_matched = len(matched_indices)
        total_all_matched += num_matched

        # --extract mode: print matching lines ± context
        if extract:
            if num_matched == 0:
                continue
            output_lines.append(f"\n==> {file} <==")
            ranges = []
            for idx in matched_indices:
                start = max(idx - before, 0)
                end = min(idx + after, len(lines) - 1)
                if ranges and start <= ranges[-1][1] + 1:
                    ranges[-1] = (ranges[-1][0], max(ranges[-1][1], end))
                else:
                    ranges.append((start, end))
            for r_start, r_end in ranges:
                for i in range(r_start, r_end + 1):
                    output_lines.append(f"{i + 1}:{lines[i].rstrip()}")
                output_lines.append("-" * 20)
            if output_lines and output_lines[-1] == "-" * 20:
                output_lines.pop()

        # --count mode: print only the count
        if count:
            output_lines.append(f"\n==> {file} <==")
            output_lines.append(f"Matching lines: {num_matched}")
            if percent and total_lines > 0:
                perc = (num_matched / total_lines) * 100
                output_lines.append(f"Match percentage: {perc:.2f}%")
            if show_size:
                size_bytes = os.path.getsize(file)
                size_display = (
                    f"{size_bytes / 1024:.2f} KB" if size_bytes < 1024 * 1024
                    else f"{size_bytes / (1024 * 1024):.2f} MB"
                )
                output_lines.append(f"File size: {size_display}")

    # --summary mode
    if summary and len(files) > 1:
        output_lines.append("\n==> Summary <==")
        output_lines.append(f"Total files: {len(files)}")
        output_lines.append(f"Total lines: {total_all_lines}")
        output_lines.append(f"Total matching lines: {total_all_matched}")

    final_output = "\n".join(output_lines)

    # Output
    if output:
        Path("logs").mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/lines_{timestamp}.log"
        Path(log_file).write_text(final_output, encoding="utf-8")
        click.echo(f"Results saved to {log_file}")
    elif interactive:
        click.echo_via_pager(final_output)
    else:
        click.echo(final_output)


def _print_help_md(lang="eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/lines/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
