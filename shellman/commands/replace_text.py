import difflib
import os
from pathlib import Path

import click


@click.command(
    help="""Replaces text in multiple files with optional preview and confirmation.

Examples:
  shellman replace_text ./docs --find old --replace new --ext md --in-place --preview
"""
)
@click.argument("search_path", type=click.Path(exists=True, file_okay=False))
@click.option("--find", "find_text", required=True, help="Text to find")
@click.option("--replace", "replace_text", required=True, help="Text to replace with")
@click.option("--ext", "ext", help="Only process files with this extension")
@click.option("--in-place", is_flag=True, help="Write changes back to files")
@click.option("--preview", is_flag=True, help="Show changes using 'diff'")
@click.option("--confirm", is_flag=True, help="Ask before replacing in each file")
def cli(search_path, find_text, replace_text, ext, in_place, preview, confirm):
    search_path = Path(search_path)
    files = []

    for file in search_path.rglob("*"):
        if not file.is_file():
            continue
        if ext and file.suffix != f".{ext}":
            continue
        try:
            text = file.read_text(encoding="utf-8")
        except Exception:
            continue
        if find_text in text:
            files.append(file)

    if not files:
        click.secho("⚠️  No files matched search criteria.", fg="yellow")
        return

    for file in files:
        click.echo(f"\n==> {file}")
        try:
            original = file.read_text(encoding="utf-8")
            modified = original.replace(find_text, replace_text)
        except Exception as e:
            click.secho(f"Error reading {file}: {e}", fg="red")
            continue

        if preview:
            diff = difflib.unified_diff(
                original.splitlines(),
                modified.splitlines(),
                fromfile=str(file),
                tofile=f"{file} (modified)",
                lineterm="",
            )
            for line in diff:
                click.echo(line)

        if in_place:
            do_replace = True
            if confirm:
                choice = input("Replace in this file? (Y/n): ").strip().lower()
                if choice == "n":
                    do_replace = False

            if do_replace:
                try:
                    file.write_text(modified, encoding="utf-8")
                    click.secho(f"Replaced in: {file}", fg="green")
                except Exception as e:
                    click.secho(f"Failed to write {file}: {e}", fg="red")
            else:
                click.secho(f"Skipped: {file}", fg="yellow")
