import difflib
import importlib.resources
from pathlib import Path

import click


@click.command(
    help="Replace occurrences of text in multiple files with optional preview and confirmation."
)
@click.argument("search_path", required=False)
@click.option("--find","-f", "find_text",
              required=False,
              help="Text to find (required unless using --lang-help)")
@click.option("--replace","-r", "replace_text",
              required=False,
              help="Replacement text (required unless using --lang-help)")
@click.option("--ext","-e", help="Only process files with this extension")
@click.option("--in-place","-ip", is_flag=True, help="Write changes back to files")
@click.option("--preview","-p", is_flag=True, help="Show unified diff preview")
@click.option("--confirm","-c", is_flag=True, help="Ask before replacing in each file")
@click.option("--lang-help","-lh", "lang", help="Show localized help (pl, eng) instead of executing")
def cli(search_path, find_text, replace_text, ext, in_place, preview, confirm, lang):
    # ---------- pomoc .md ---------- #
    if lang:
        _print_help_md(lang)
        return

    # ---------- walidacja ---------- #
    if not search_path:
        raise click.UsageError("Missing required argument 'search_path'")
    if find_text is None:
        raise click.UsageError("Missing required option '--find'")
    if replace_text is None:
        raise click.UsageError("Missing required option '--replace'")

    search_path = Path(search_path)
    if not search_path.exists() or search_path.is_file():
        raise click.ClickException("search_path must be an existing directory")

    # ---------- skan plików ---------- #
    candidates = []
    for file in search_path.rglob("*"):
        if not file.is_file():
            continue
        if ext and file.suffix != f".{ext}":
            continue
        try:
            if find_text in file.read_text(encoding="utf-8", errors="ignore"):
                candidates.append(file)
        except Exception:
            continue

    if not candidates:
        click.secho("⚠️  No files matched search criteria.", fg="yellow")
        return

    # ---------- przetwarzanie ---------- #
    for file in candidates:
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
            do_write = True
            if confirm:
                choice = input("Replace in this file? (Y/n): ").strip().lower()
                if choice == "n":
                    do_write = False

            if do_write:
                try:
                    file.write_text(modified, encoding="utf-8")
                    click.secho(f"Replaced in: {file}", fg="green")
                except Exception as e:
                    click.secho(f"Failed to write {file}: {e}", fg="red")
            else:
                click.secho(f"Skipped: {file}", fg="yellow")


# ---------- loader pomocy ---------- #
def _print_help_md(lang: str = "eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/replace_text/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
