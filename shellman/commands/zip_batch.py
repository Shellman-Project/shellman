import click
import os
from pathlib import Path
from datetime import datetime
import subprocess

@click.command()
@click.option("--path", "src_path", type=click.Path(exists=True, file_okay=False), default=".", help="Source directory")
@click.option("--ext", help="Only include files with this extension")
@click.option("--per-folder", is_flag=True, help="Create one archive per subfolder")
@click.option("--output", "out_dir", type=click.Path(), default="./zips", help="Output directory")
@click.option("--name", "name_prefix", default="batch_", help="Prefix for archive name")
@click.option("--password", help="Optional password for zip")
def cli(src_path, ext, per_folder, out_dir, name_prefix, password):
    """Creates zip archives from folders or files in batch."""
    src_path = Path(src_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if per_folder:
        for sub in src_path.iterdir():
            if not sub.is_dir():
                continue
            zipname = f"{name_prefix}{sub.name}.zip"
            zipfile = out_dir / zipname
            click.echo(f"📦 Archiving folder: {sub} → {zipfile}")
            cmd = ["zip", "-r", str(zipfile), str(sub)]
            if password:
                cmd.extend(["-P", password])
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            click.secho(f"Created: {zipfile}", fg="green")
    else:
        all_files = [f for f in src_path.rglob("*") if f.is_file() and (not ext or f.suffix == f".{ext}")]
        if not all_files:
            click.secho("No matching files found to zip.", fg="yellow")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zipfile = out_dir / f"{name_prefix}files_{timestamp}.zip"
        click.echo(f"📦 Creating archive: {zipfile}")
        cmd = ["zip", str(zipfile)]
        if password:
            cmd.extend(["-P", password])
        cmd.extend(str(f) for f in all_files)
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        click.secho(f"Created: {zipfile}", fg="green")
