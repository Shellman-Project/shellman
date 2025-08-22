import hashlib
import importlib.resources
from pathlib import Path

import click

SUPPORTED_ALGOS = {
    "sha256": hashlib.sha256,
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
}


def print_help_md(lang="eng"):
    """Print localized help text for the `checksum_files` command."""
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(f"help_texts/checksum_files/{lang_file}")
        content = help_path.read_text(encoding="utf-8")
        click.echo(content)
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)


@click.command(
    help="Generate or verify checksums (SHA256, MD5, etc.) for files."
)
@click.option("--path", "-p", "scan_path", type=click.Path(exists=True, file_okay=False), default=".", help="Directory to scan")
@click.option("--ext", "-e", "ext_filter", help="Only include files with this extension")
@click.option("--algo", "-a", type=click.Choice(["sha256", "md5", "sha1"]), default="sha256", help="Hash algorithm")
@click.option("--out", "-o", "out_file", type=click.Path(), help="Output list file name")
@click.option("--verify", "-v", is_flag=True, help="Verify instead of generate (reads --out list)")
@click.option("--lang-help", "-lh", "lang", help="Show localized help (pl, eng) instead of executing the command")
def cli(scan_path, ext_filter, algo, out_file, verify, lang):
    """
    Command-line interface for generating or verifying file checksums.

    Scans a directory recursively and computes checksums for all matching files.
    Can either generate a checksum list file, or verify an existing list
    against current file contents.

    Args:
        scan_path (str): Path to the directory to scan (default: ".").
        ext_filter (str | None): Restrict to files with this extension (without dot).
        algo (str): Hashing algorithm to use ("sha256", "md5", "sha1").
        out_file (str | None): Path to the checksum output list file.
            Defaults to `checksums.{algo}sum` if not specified.
        verify (bool): If True, verify files against the list instead of generating it.
        lang (str | None): Show localized help ("pl" or "eng") instead of running.

    Raises:
        click.Abort: If verification fails or no files are found.

    Examples:
        Generate SHA256 checksums for all files in `downloads/`:
            $ shellman checksum_files -p downloads -a sha256 -o myhashes.sha256

        Verify files against an existing checksum list:
            $ shellman checksum_files --verify -o myhashes.sha256
    """
    if lang:
        print_help_md(lang)
        return

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
    files = [
        f
        for f in scan_path.rglob("*")
        if f.is_file() and (not ext_filter or f.suffix == f".{ext_filter}")
    ]

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
    """
    Compute the checksum of a single file.

    Reads the file in chunks to avoid memory issues with large files and
    applies the given hashing function (e.g., SHA256, MD5, SHA1).

    Args:
        file_path (Path): Path to the file to hash.
        hash_func (Callable[[], hashlib._Hash]): Hash constructor from hashlib
            (e.g., `hashlib.sha256`).

    Returns:
        str: Hexadecimal digest of the computed checksum.

    Examples:
        >>> from pathlib import Path
        >>> import hashlib
        >>> hash_file(Path("data.txt"), hashlib.sha256)
        '5d41402abc4b2a76b9719d911017c592'
    """
    h = hash_func()
    with file_path.open("rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
