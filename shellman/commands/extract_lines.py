from pathlib import Path

import click


@click.command(
    help="""Extracts lines from a file that contain or do NOT contain specific text, with optional context.

Examples:
  shellman extract_lines sys.log --contains ERROR --before 2 --after 3
  shellman extract_lines notes.txt --not-contains TODO --output clean.txt
"""
)
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--contains", help="Keep lines that contain this text")
@click.option(
    "--not-contains", "not_contains", help="Keep lines that do NOT contain this text"
)
@click.option("--before", type=int, default=0, help="Show N lines before each match")
@click.option("--after", type=int, default=0, help="Show N lines after each match")
@click.option("--output", type=click.Path(), help="Save result instead of printing")
def cli(file, contains, not_contains, before, after, output):
    if contains and not_contains:
        raise click.UsageError("Use either --contains OR --not-contains")
    if not contains and not not_contains:
        raise click.UsageError("Need --contains or --not-contains")

    path = Path(file)
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

    result = []
    matched_indices = []

    for idx, line in enumerate(lines):
        if contains and contains in line:
            matched_indices.append(idx)
        elif not_contains and not_contains not in line:
            matched_indices.append(idx)

    seen = set()
    for idx in matched_indices:
        start = max(idx - before, 0)
        end = min(idx + after + 1, len(lines))
        for i in range(start, end):
            if i not in seen:
                result.append(f"{i + 1}:{lines[i]}")
                seen.add(i)

    final_output = "\n".join(result)

    if output:
        Path(output).write_text(final_output, encoding="utf-8")
        click.echo(f"Saved to {output}  (lines: {len(result)})")
    else:
        click.echo(final_output)
        click.echo(f"Lines printed: {len(result)}")
