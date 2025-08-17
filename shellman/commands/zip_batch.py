import importlib.resources
import os
import subprocess
from datetime import datetime
from pathlib import Path

import click


@click.command(
    help="Create zip archives from folders or files in batch."
)
@click.option("--path", "src_path",
              type=click.Path(exists=True, file_okay=False),
              default=".",
              help="Source directory to scan (default: current dir)")

@click.option("--ext", help="Only include files with this extension")
@click.option("--per-folder", is_flag=True, help="Create one archive per immediate sub-folder")
@click.option("--output", "out_dir",
              type=click.Path(),
              default="./zips",
              help="Output directory (default: ./zips)")

@click.option("--name", "name_prefix", default="batch_", help="Prefix for archive name")
@click.option("--password", help="Password for zip (uses `zip -P` – weak encryption!)")
@click.option("--lang-help", "lang", help="Show localized help (pl, eng) instead of executing")
def cli(src_path, ext, per_folder, out_dir, name_prefix, password, lang):
    # ---------- lokalizowana pomoc ---------- #
    if lang:
        _print_help_md(lang)
        return

    # ---------- przygotowanie ---------- #
    src_path = Path(src_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if per_folder:
        # jedno archiwum na każdy katalog bezpośredni
        for sub in src_path.iterdir():
            if not sub.is_dir():
                continue
            zipfile = out_dir / f"{name_prefix}{sub.name}.zip"
            click.echo(f"📦  {sub} → {zipfile}")
            cmd = ["zip", "-r", str(zipfile), str(sub)]
            if password:
                cmd.extend(["-P", password])
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            click.secho(f"Created: {zipfile}", fg="green")
    else:
        # jedno archiwum ze wszystkich plików (ew. filtrowane po rozszerzeniu)
        files = [
            f for f in src_path.rglob("*")
            if f.is_file() and (not ext or f.suffix == f".{ext}")
        ]
        if not files:
            click.secho("No matching files found to zip.", fg="yellow")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zipfile = out_dir / f"{name_prefix}files_{timestamp}.zip"
        click.echo(f"📦  Creating archive: {zipfile}")
        cmd = ["zip", str(zipfile)]
        if password:
            cmd.extend(["-P", password])
        cmd.extend(str(f) for f in files)
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        click.secho(f"Created: {zipfile}", fg="green")


# ---------- Markdown help loader ---------- #
def _print_help_md(lang: str = "eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/zip_batch/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
