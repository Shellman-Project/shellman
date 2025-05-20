import click
import hashlib
import os
from pathlib import Path

SUPPORTED_ALGOS = {
    "sha256": hashlib.sha256,
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
}

@click.command(help="""Creates or verifies checksums for files in a directory.

Examples:
  shellman checksum_files --path ./dist --ext zip --algo sha256 --out builds.sha256sum
  shellman checksum_files --verify --out builds.sha256sum
""")
@click.option("--path", "scan_path", type=click.Path(exists=True, file_okay=False), default=".", help="Directory to scan")
@click.option("--ext", "ext_filter", help="Only include files with this extension")
@click.option("--algo", type=click.Choice(["sha256", "md5", "sha1"]), default="sha256", help="Hash algorithm")
@click.option("--out", "out_file", type=click.Path(), help="Output list file name")
@click.option("--verify", is_flag=True, help="Verify instead of generate (reads --out list)")
def cli(scan_path, ext_filter, algo, out_file, verify):
    scan_path = Path(scan_path)
    if not out_file:
        out_file = f"checksums.{algo}sum"

    hash_func = SUPPORTED_ALGOS[algo]

    if verify:
        out_path = Path(out_file)
        if not out_path.is_file():
            click.echo(f"Checksum list {out_file} not found", err=True)
            raise click.Abort()

        click.echo(f"🔎 Verifying files via {algo} list {out_file} ...")
        success = True
        with out_path.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    expected, filename = line.strip().split(maxsplit=1)
                    filename = filename.strip()
                    file_path = Path(filename)
                    if not file_path.is_file():
                        click.echo(f"❌ {filename} not found")
                        success = False
                        continue
                    actual = hash_file(file_path, hash_func)
                    if actual != expected:
                        click.echo(f"❌ MISMATCH: {filename}")
                        success = False
                    else:
                        click.echo(f"✅ OK: {filename}")
                except Exception as e:
                    click.echo(f"Error verifying line: {line.strip()} → {e}")
                    success = False

        if not success:
            raise click.Abort()
        return

    # Generate checksums
    files = [f for f in scan_path.rglob("*") if f.is_file() and (not ext_filter or f.suffix == f".{ext_filter}")]

    if not files:
        click.echo("No files matched.")
        return

    click.echo(f"✍️  Writing {len(files)} checksums to {out_file} ...")
    with open(out_file, "w", encoding="utf-8") as f:
        for file in files:
            checksum = hash_file(file, hash_func)
            f.write(f"{checksum}  {file}\n")

    click.echo("✅ Done.")

def hash_file(file_path, hash_func):
    h = hash_func()
    with file_path.open("rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
