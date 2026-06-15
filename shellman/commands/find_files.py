import importlib.resources
from datetime import datetime
from pathlib import Path

import click


def print_help_md(lang: str = "eng") -> None:
    """Load and print help from markdown file."""
    lang_file = f"help_{lang.lower()}.md"

    try:
        help_path = (
            importlib.resources.files("shellman")
            .joinpath("help_texts")
            .joinpath("find_files")
            .joinpath(lang_file)
        )
        content = help_path.read_text(encoding="utf-8")
        click.echo(content)
    except Exception:
        click.echo(f"Help not available for language: {lang}", err=True)


def normalize_extension(ext: str | None) -> str | None:
    """Normalize extension to '.ext' format."""
    if not ext:
        return None

    ext = ext.strip()
    if not ext:
        return None

    return ext if ext.startswith(".") else f".{ext}"


def format_file_size(size_bytes: int) -> str:
    """Format file size as KB or MB."""
    if size_bytes < 1024:
        return f"{size_bytes} B"

    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"

    return f"{size_bytes / (1024 * 1024):.2f} MB"


@click.command(help="Find files by name, extension or content with filtering options.")
@click.argument(
    "search_path",
    required=False,
    type=click.Path(exists=True, file_okay=False),
)
@click.option(
    "--name",
    "-n",
    "name_filter",
    help="Match filenames containing this fragment",
)
@click.option(
    "--content",
    "-c",
    "content_filter",
    help="Search for files containing this text",
)
@click.option(
    "--ext",
    "-e",
    "ext_filter",
    help="Only include files with this extension",
)
@click.option(
    "--output",
    "-o",
    is_flag=True,
    help="Save results to logs/find_files_<timestamp>.log",
)
@click.option(
    "--show-size",
    "-s",
    is_flag=True,
    help="Show file size next to each result",
)
@click.option(
    "--lang-help",
    "-lh",
    "lang",
    help="Show localized help (pl, eng) instead of executing the command",
)
def cli(
    search_path: str | None,
    name_filter: str | None,
    content_filter: str | None,
    ext_filter: str | None,
    output: bool,
    show_size: bool,
    lang: str | None,
) -> None:
    if lang:
        print_help_md(lang)
        return

    if not search_path:
        raise click.UsageError("Missing required argument: SEARCH_PATH")

    path = Path(search_path)
    if not path.is_dir():
        raise click.ClickException(f"Path is not a directory: {search_path}")

    normalized_ext = normalize_extension(ext_filter)
    found_files: list[Path] = []

    for file in path.rglob("*"):
        if not file.is_file():
            continue

        if name_filter and name_filter not in file.name:
            continue

        if normalized_ext and file.suffix != normalized_ext:
            continue

        if content_filter:
            try:
                file_content = file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            if content_filter not in file_content:
                continue

        found_files.append(file.resolve())

    if not found_files:
        raise click.ClickException("No files found matching criteria.")

    results = []
    for file in found_files:
        if show_size:
            size_display = format_file_size(file.stat().st_size)
            results.append(f"{file}  [{size_display}]")
        else:
            results.append(str(file))

    final_output = "\n".join(results)
    click.echo(final_output)

    if output:
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = logs_dir / f"find_files_{timestamp}.log"

        log_file.write_text(final_output, encoding="utf-8")
        click.echo(f"Results saved to {log_file}")
        