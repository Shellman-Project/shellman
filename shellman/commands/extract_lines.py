from pathlib import Path
import importlib.resources
from typing import List, Tuple

import click


@click.command(
    help="Extract lines from a file that contain—or do NOT contain—given text, with optional context."
)
@click.argument("file", required=False)
@click.option("--contains", help="Keep lines that contain this text")
@click.option("--not-contains", "not_contains", help="Keep lines that do NOT contain this text")
@click.option("--before", type=int, default=0, help="Show N lines before each match")
@click.option("--after", type=int, default=0, help="Show N lines after each match")
@click.option("--output", type=click.Path(), help="Save result instead of printing")
@click.option("--lang-help", "lang", help="Show localized help (pl, eng) instead of executing the command")
def cli(file, contains, not_contains, before, after, output, lang):
    # ---------- lokalizowana pomoc ---------- #
    if lang:
        _print_help_md(lang)
        return

    # ---------- walidacja argumentów ---------- #
    if not file:
        raise click.UsageError("Missing required argument 'file'")
    if contains and not_contains:
        raise click.UsageError("Use either --contains OR --not-contains")
    if not contains and not not_contains:
        raise click.UsageError("Need --contains or --not-contains")

    # ---------- wczytaj plik ---------- #
    path = Path(file)
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

    # ---------- wyszukaj indexy pasujących wierszy ---------- #
    matched_indices = [
        idx
        for idx, line in enumerate(lines)
        if (contains and contains in line) or (not_contains and not_contains not in line)
    ]
    if not matched_indices:
        click.echo("No matching lines found.")
        return

    # ---------- zbuduj listę bloków z kontekstem ---------- #
    ranges: List[Tuple[int, int]] = []
    for idx in matched_indices:
        start = max(idx - before, 0)
        end = min(idx + after, len(lines) - 1)
        if ranges and start <= ranges[-1][1] + 1:            # zlewaj zachodzące/ciągłe bloki
            ranges[-1] = (ranges[-1][0], max(ranges[-1][1], end))
        else:
            ranges.append((start, end))

    # ---------- wypisz bloki + separator ---------- #
    out_lines = []
    for r_start, r_end in ranges:
        for i in range(r_start, r_end + 1):
            out_lines.append(f"{i + 1}:{lines[i]}")
        out_lines.append("-" * 20)        # separator po każdym bloku

    # usuń ostatni separator, jeśli występuje
    if out_lines and out_lines[-1] == "-" * 20:
        out_lines.pop()

    final_output = "\n".join(out_lines)

    # ---------- wyjście ---------- #
    if output:
        Path(output).write_text(final_output, encoding="utf-8")
        click.echo(f"Saved to {output}  (lines: {len(out_lines)})")
    else:
        click.echo(final_output)
        click.echo(f"Lines printed: {len(out_lines)}")


# ---------- loader markdown help ---------- #
def _print_help_md(lang: str = "eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/extract_lines/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
