import click
import csv
from pathlib import Path

@click.command(help="""Extracts selected columns or rows from a CSV file.

Examples:
  shellman csv_extract data.csv --cols 1,4 --rows 2-100 --skip-header
  shellman csv_extract logs.csv --contains ERROR --output errors.csv --interactive
""")
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--cols", required=True, help="Columns to keep (1-based), e.g. 1,3 or 2-4")
@click.option("--rows", help="Rows to keep (after header), e.g. 2-10")
@click.option("--contains", help="Only keep rows containing this text")
@click.option("--not-contains", "not_contains", help="Only keep rows NOT containing this text")
@click.option("--delim", default=",", help="CSV delimiter (default: ,)")
@click.option("--skip-header", is_flag=True, default=False, help="Skip first line (header)")
@click.option("--output", type=click.Path(), help="Save result instead of printing")
@click.option("--interactive", is_flag=True, default=False, help="Pipe result to less")
def cli(file, cols, rows, contains, not_contains, delim, skip_header, output, interactive):
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
            row_number = idx if not skip_header else idx  # Adjusted already by skipping
            if row_idxs and (row_number + 1) not in row_idxs:
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
