import csv
import importlib.resources
from pathlib import Path

import click


@click.command(
    help="Extracts specific columns or rows from a CSV file with filtering options."
)
@click.argument("file", required=False)
@click.option("--cols","-c", required=False, help="Columns to keep (1-based), e.g. 1,3 or 2-4")
@click.option("--rows","-r", help="Rows to keep (after header), e.g. 2-10")
@click.option("--contains","-con", help="Only keep rows containing this text")
@click.option("--not-contains","-ncon", "not_contains", help="Only keep rows NOT containing this text")
@click.option("--delim","-d", default=",", help="CSV delimiter (default: ,)")
@click.option("--skip-header","-sh", is_flag=True, default=False, help="Skip first line (header)")
@click.option("--output","-o", type=click.Path(), help="Save result instead of printing")
@click.option("--interactive","-i", is_flag=True, default=False, help="Pipe result to less")
@click.option("--lang-help","-lh", "lang", help="Show localized help (pl, eng) instead of executing the command")
def cli(file, cols, rows, contains, not_contains, delim, skip_header, output, interactive, lang):
    """
    Extract specific columns or rows from a CSV file with optional filtering.

    Supports selecting columns by index (1-based), row ranges, and
    filtering by text presence or absence. Results can be printed,
    paged interactively, or saved to a file.

    Args:
        file (str): Path to the CSV file.
        cols (str): Comma-separated list of columns to keep (1-based).
            Supports ranges, e.g. "1,3" or "2-4".
        rows (str | None): Comma-separated list of rows (after header) to keep.
            Supports ranges.
        contains (str | None): Only include rows containing this text.
        not_contains (str | None): Only include rows NOT containing this text.
        delim (str): CSV delimiter (default: ",").
        skip_header (bool): If True, skip the first line (header).
        output (str | None): Path to save the extracted data instead of printing.
        interactive (bool): If True, pipe output to pager (`less`).
        lang (str | None): Show localized help ("pl" or "eng") instead of running.

    Raises:
        click.UsageError:
            - If `file` or `--cols` are missing.
            - If both `--contains` and `--not-contains` are provided.

    Effects:
        - Prints selected CSV content to stdout.
        - Optionally saves to a file or displays interactively.

    Examples:
        Extract only first and third column:
            $ shellman csv_extract data.csv --cols 1,3

        Extract rows 2–10, skipping header:
            $ shellman csv_extract data.csv --cols 1,2 --rows 2-10 --skip-header

        Save filtered output to file:
            $ shellman csv_extract data.csv --cols 1-3 --contains error --output out.csv
    """
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
    """Print localized help text for the `csv_extract` command."""
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(f"help_texts/csv_extract/{lang_file}")
        content = help_path.read_text(encoding="utf-8")
        click.echo(content)
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
