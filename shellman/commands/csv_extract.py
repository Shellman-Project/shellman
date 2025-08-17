import csv
import importlib.resources
from pathlib import Path

import click


@click.command(
    help="Extracts specific columns or rows from a CSV file with filtering options."
)
@click.argument("file", required=False)
@click.option("--cols", required=False, help="Columns to keep (1-based), e.g. 1,3 or 2-4")
@click.option("--rows", help="Rows to keep (after header), e.g. 2-10")
@click.option("--contains", help="Only keep rows containing this text")
@click.option("--not-contains", "not_contains", help="Only keep rows NOT containing this text")
@click.option("--delim", default=",", help="CSV delimiter (default: ,)")
@click.option("--skip-header", is_flag=True, default=False, help="Skip first line (header)")
@click.option("--output", type=click.Path(), help="Save result instead of printing")
@click.option("--interactive", is_flag=True, default=False, help="Pipe result to less")
@click.option("--lang-help", "lang", help="Show localized help (pl, eng) instead of executing the command")
def cli(file, cols, rows, contains, not_contains, delim, skip_header, output, interactive, lang):
    if lang:
        print_help_md(lang)
        return

    if not file:
        raise click.UsageError("Missing required argument 'file'")
    if not cols:
        raise click.UsageError("Missing required option '--cols'")
    if contains and not_contains:
        raise click.UsageError("Use --contains XOR --not-contains")

    def parse_ranges(expr):
        result = set()
        if not expr:
            return result
        for part in expr.split(","):
            if "-" in part:
                a, b = map(int, part.split("-"))
                result.update(range(a, b + 1))
            else:
                result.add(int(part))
        return result

    col_idxs = parse_ranges(cols)
    row_idxs = parse_ranges(rows)

    path = Path(file)
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter=delim)
        result_lines = []

        for idx, row in enumerate(reader):
            if skip_header and idx == 0:
                continue
            if row_idxs and (idx + 1) not in row_idxs:
                continue

            joined = delim.join(row).lower()
            if contains and contains.lower() not in joined:
                continue
            if not_contains and not_contains.lower() in joined:
                continue

            selected = [row[i - 1] for i in sorted(col_idxs) if i - 1 < len(row)]
            result_lines.append(delim.join(selected))

    output_text = "\n".join(result_lines)

    if output:
        Path(output).write_text(output_text, encoding="utf-8")
        click.echo(f"Saved to {output}")
        if interactive:
            click.echo_via_pager(output_text)
    else:
        click.echo(output_text)
        click.echo(f"Lines printed: {len(result_lines)}")
        if interactive:
            click.echo_via_pager(output_text)


def print_help_md(lang="eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(f"help_texts/csv_extract/{lang_file}")
        content = help_path.read_text(encoding="utf-8")
        click.echo(content)
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
