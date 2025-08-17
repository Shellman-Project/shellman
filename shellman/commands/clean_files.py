import importlib.resources
import os
from datetime import datetime, timedelta
from pathlib import Path

import click


def print_help_md(lang="eng"):
    """Print localized help text for the `clean_files` command."""
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(f"help_texts/clean_files/{lang_file}")
        content = help_path.read_text(encoding="utf-8")
        click.echo(content)
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)


@click.command(
    help="Delete files by name, extension, or age – with preview and confirmation."
)
@click.option("--path","-p", "scan_path", type=click.Path(exists=True, file_okay=False), default=".", help="Directory to scan")
@click.option("--ext","-e", "ext_filter", help="Delete files with this extension")
@click.option("--name","-n", "name_filter", help="Delete files whose name contains this pattern")
@click.option("--older-than", "-ot", "age_days", type=int, help="Delete only files older than N days")
@click.option("--dry-run","-dr", is_flag=True, help="Preview: list files but do NOT delete")
@click.option("--confirm","-c", is_flag=True, help="Ask Y/n before deleting each file")
@click.option("--lang-help","-lh", "lang", help="Show localized help (pl, eng) instead of executing the command")
def cli(scan_path, ext_filter, name_filter, age_days, dry_run, confirm, lang):
    """
    Command-line interface for cleaning up files by extension, name, or age.

    Recursively scans a directory and selects files matching filters.
    Depending on options, either previews them (dry-run) or deletes them
    with optional confirmation.

    Args:
        scan_path (str): Path to the directory to scan. Defaults to current dir.
        ext_filter (str | None): Only include files with this extension.
        name_filter (str | None): Only include files containing this substring in the name.
        age_days (int | None): Only include files older than this number of days.
        dry_run (bool): If True, only preview matching files, do not delete.
        confirm (bool): If True, ask for Y/n confirmation before deleting each file.
        lang (str | None): Show localized help ("pl" or "eng") instead of executing.

    Raises:
        click.Abort: If neither `--ext` nor `--name` is provided.

    Effects:
        - Deletes matching files (unless `--dry-run` is enabled).
        - Prints summary of matched and deleted files.

    Examples:
        Delete all `.log` files in current dir:
            $ shellman clean_files -e log

        Delete files containing "backup" in name, older than 7 days:
            $ shellman clean_files -n backup -ot 7

        Preview what would be deleted:
            $ shellman clean_files -e tmp --dry-run
    """
    if lang:
        print_help_md(lang)
        return

    scan_path = Path(scan_path)

    if not ext_filter and not name_filter:
        click.echo("Need --ext or --name (or both) to know what to delete!", err=True)
        raise click.Abort()

    candidates = []
    cutoff_time = None
    if age_days:
        cutoff_time = datetime.now() - timedelta(days=age_days)

    for file in scan_path.rglob("*"):
        if not file.is_file():
            continue
        if ext_filter and file.suffix != f".{ext_filter}":
            continue
        if name_filter and name_filter not in file.name:
            continue
        if cutoff_time and datetime.fromtimestamp(file.stat().st_mtime) > cutoff_time:
            continue
        candidates.append(file.resolve())

    if not candidates:
        click.echo("No files matched the criteria – nothing to do.")
        return

    click.echo(f"🧹  {len(candidates)} file(s) match the criteria:")
    for f in candidates:
        click.echo(f"  {f}")
    click.echo()

    if dry_run:
        click.echo("Dry‑run mode – nothing deleted.")
        return

    for file in candidates:
        delete = True
        if confirm:
            response = input(f"Delete {file}? (Y/n): ").strip().lower()
            if response == "n":
                delete = False
        if delete:
            try:
                file.unlink()
                click.echo(f"Deleted: {file}")
            except Exception as e:
                click.echo(f"Failed to delete {file}: {e}")

    click.echo("✅ Clean-up complete.")
