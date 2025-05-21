import click
from pathlib import Path
from datetime import datetime


@click.command()
@click.option("--ext", help="Only include files with this extension (e.g. txt)")
@click.option("--out", "out_file", type=click.Path(), help="Output file name")
@click.option("--path", "scan_path", type=click.Path(exists=True, file_okay=False), default=".", help="Directory to scan")
@click.option("--header", is_flag=True, help="Add filename headers before each file's content")
@click.option("--sort", is_flag=True, help="Sort files alphabetically before merging")
def cli(ext, out_file, scan_path, header, sort):
    """Merges multiple text files into a single file."""
    scan_dir = Path(scan_path)

    files = [f for f in scan_dir.rglob("*") if f.is_file() and (not ext or f.suffix == f".{ext}")]
    if not files:
        click.echo("⚠️  No files found to merge.", err=True)
        return

    if sort:
        files.sort()

    Path("logs").mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = Path(out_file) if out_file else Path(f"logs/merged_{timestamp}.txt")

    click.echo(f"🔀 Merging {len(files)} file(s) into: {out_path}")
    with out_path.open("w", encoding="utf-8") as out_f:
        for f in files:
            if header:
                out_f.write(f"\n=== {f.resolve()} ===\n")
            out_f.write(f.read_text(encoding="utf-8", errors="ignore"))

    click.echo(f"✅ Merge complete: {out_path}")
