"""Shellman: zip command (group)

Provides two subcommands:
  • zip pack   – create a .zip archive from a file or directory
  • zip unpack – extract a .zip archive into a target location

Design goals (per user spec):
- PACK:
  - NAME can be given either positionally or via -n/--name. It must point to an existing file/dir.
  - Optional --password/-pass to protect archive (AES-256 via pyzipper).
  - Optional --output/-o to choose output directory; default is ./zips in current working dir.
  - Archive name equals <basename(NAME)>.zip inside the chosen output directory.

- UNPACK:
  - NAME can be given positionally or via -n/--name; must be an existing .zip file.
  - Optional --password/-pass if the archive is password-protected.
    • If the archive is not protected, we inform the user.
    • If it requires a password and none is provided, we fail with a clear message.
  - Optional --output/-o:
    • Not provided → extract to ./output_<zip_stem>
    • Provided → extract to <output>/<zip_stem>

Notes:
- We use pyzipper for password-protected packing (AES-256) and for reading encrypted zips.
- For non-password packing we use stdlib zipfile.
- Safe extraction prevents path traversal.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import click
import zipfile

try:
    import pyzipper  # AES-capable zipfile fork
except Exception:  # pragma: no cover
    pyzipper = None  # type: ignore


# ================================ CLI GROUP ================================ #

@click.group(name="zip", help="ZIP utilities: pack files/folders or unpack archives.")
def zip_cli() -> None:
    """Top-level Click group for ZIP operations."""
    pass


# ================================= PACK =================================== #

@zip_cli.command(
    "pack",
    help=(
        "Create a .zip archive from a file or directory.\n\n"
        "Usage:\n"
        "  shellman zip pack NAME [--password PASS] [--output DIR]\n"
        "  shellman zip pack -n NAME [--password PASS] [--output DIR]\n\n"
        "Examples:\n"
        "  # Pack a folder into ./zips/project.zip\n"
        "  shellman zip pack ./project\n\n"
        "  # Pack a single file into a custom output directory\n"
        "  shellman zip pack report.csv -o ./artifacts\n\n"
        "  # Pack a folder with a password (AES-256 via pyzipper)\n"
        "  shellman zip pack -n ./secret -pass Pa55\n"
    ),
)
@click.argument("name_arg", required=False, type=click.Path(exists=True, path_type=Path))
@click.option(
    "-n", "--name",
    "name_opt",
    type=click.Path(exists=True, path_type=Path),
    help="File or directory to pack (alternative to positional NAME).",
)
@click.option("--password", "-pass", help="Password for the archive (AES-256 via pyzipper).")
@click.option(
    "--output",
    "-o",
    "out_dir",
    type=click.Path(path_type=Path),
    help="Target directory for the archive (default: ./zips in current working dir).",
)
def pack(name_arg: Optional[Path], name_opt: Optional[Path], password: Optional[str], out_dir: Optional[Path]) -> None:
    """Pack a file or directory into <output>/<basename(NAME)>.zip."""
    src_path = name_opt or name_arg
    if src_path is None:
        raise click.UsageError("Provide NAME positionally or via -n/--name.")
    src_path = src_path.resolve()

    out = (out_dir.resolve() if out_dir else (Path.cwd() / "zips"))
    out.mkdir(parents=True, exist_ok=True)

    # If source is a file, use stem; if directory, use its name
    archive_path = out / f"{(src_path.stem if src_path.is_file() else src_path.name)}.zip"

    if password:
        if pyzipper is None:
            raise click.ClickException(
                "Password-protected packing requires 'pyzipper'. Add it to your environment."
            )
        click.echo(f"📦  Packing (AES-256): {src_path} → {archive_path}")
        _pack_with_pyzipper(source=src_path, archive_path=archive_path, password=password)
        click.secho(f"Created: {archive_path}", fg="green")
        return

    # No password → stdlib zipfile
    click.echo(f"📦  Packing: {src_path} → {archive_path}")
    _pack_with_zipfile(source=src_path, archive_path=archive_path)
    click.secho(f"Created: {archive_path}", fg="green")


def _pack_with_zipfile(source: Path, archive_path: Path) -> None:
    """Pack using stdlib `zipfile` (no encryption)."""
    compression = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(archive_path, "w", compression=compression) as zf:
        if source.is_file():
            zf.write(source, arcname=source.name)
            return

        root = source
        for path in root.rglob("*"):
            if path.is_file():
                # Keep top-level directory name inside the archive
                rel = path.relative_to(root).as_posix()
                arcname = f"{root.name}/{rel}"
                zf.write(path, arcname=arcname)


def _pack_with_pyzipper(source: Path, archive_path: Path, password: str) -> None:
    """Pack using pyzipper with AES-256 encryption."""
    if pyzipper is None:  # safety
        raise click.ClickException("pyzipper not available.")

    with pyzipper.AESZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zf:
        # Set AES-256 (nbits=256) and password
        zf.setencryption(pyzipper.WZ_AES, nbits=256)
        zf.setpassword(password.encode("utf-8"))

        if source.is_file():
            zf.write(source, arcname=source.name)
            return

        root = source
        for path in root.rglob("*"):
            if path.is_file():
                rel = path.relative_to(root).as_posix()
                arcname = f"{root.name}/{rel}"
                zf.write(path, arcname=arcname)


# ================================= UNPACK ================================= #

@zip_cli.command(
    "unpack",
    help=(
        "Extract a .zip archive.\n\n"
        "Usage:\n"
        "  shellman zip unpack NAME [--password PASS] [--output DIR]\n"
        "  shellman zip unpack -n NAME [--password PASS] [--output DIR]\n\n"
        "Destination rules:\n"
        "  • No --output → ./output_<zip_stem>\n"
        "  • With --output DIR → DIR/<zip_stem>\n\n"
        "Examples:\n"
        "  # Unpack into ./output_report\n"
        "  shellman zip unpack ./report.zip\n\n"
        "  # Unpack into ./unzipped/report/\n"
        "  shellman zip unpack -n ./report.zip -o ./unzipped\n"
    ),
)
@click.argument("name_arg", required=False, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "-n", "--name",
    "name_opt",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to a .zip file (alternative to positional NAME).",
)
@click.option("--password", "-pass", help="Password if the archive is protected (AES/ZipCrypto).")
@click.option("--output", "-o", "out_dir", type=click.Path(path_type=Path), help="Extraction base directory.")
def unpack(name_arg: Optional[Path], name_opt: Optional[Path], password: Optional[str], out_dir: Optional[Path]) -> None:
    """Extract NAME into the appropriate directory, handling password if needed."""
    zip_path = (name_opt or name_arg)
    if zip_path is None:
        raise click.UsageError("Provide NAME positionally or via -n/--name.")
    zip_path = zip_path.resolve()

    stem = zip_path.stem
    base_out = (out_dir.resolve() if out_dir else Path.cwd())
    target = (base_out / stem) if out_dir else (base_out / f"output_{stem}")
    target.mkdir(parents=True, exist_ok=True)

    # Always try pyzipper first if available (handles AES + ZipCrypto). Fallback to stdlib.
    opened = None
    try:
        if pyzipper is not None:
            opened = pyzipper.AESZipFile(zip_path)
        else:
            opened = zipfile.ZipFile(zip_path)

        with opened as zf:
            encrypted = _is_encrypted(zf)
            if encrypted and not password:
                raise click.ClickException(
                    "This archive appears to be password-protected. Provide --password to proceed."
                )
            if not encrypted:
                click.echo("ℹ️  Archive is not password-protected.")

            pwd = password.encode("utf-8") if password else None
            _safe_extract(zf, target, pwd=pwd)

    except RuntimeError as e:
        # Wrong password or encryption unsupported by stdlib
        raise click.ClickException(
            "Failed to extract: wrong password or unsupported encryption. "
            "AES-encrypted ZIPs require 'pyzipper'."
        ) from e
    except zipfile.BadZipFile as e:
        raise click.ClickException("The file is not a valid ZIP archive.") from e

    click.secho(f"Extracted to: {target}", fg="green")


def _is_encrypted(zf) -> bool:
    """Return True if any member indicates encryption via general purpose bit flag."""
    for info in zf.infolist():
        # bit 0 of flag_bits denotes encryption (true for both ZipCrypto and AES)
        if getattr(info, "flag_bits", 0) & 0x1:
            return True
    return False


def _safe_extract(zf, dest_dir: Path, pwd: Optional[bytes] = None) -> None:
    """Safely extract all members into dest_dir, preventing path traversal."""
    dest_root = dest_dir.resolve()

    for member in zf.infolist():
        name = getattr(member, "filename", "")
        member_path = Path(name)

        # Skip absolute paths
        if member_path.is_absolute():
            continue

        final = (dest_root / member_path).resolve()
        if not str(final).startswith(str(dest_root)):
            continue  # path traversal attempt

        if getattr(member, "is_dir", lambda: name.endswith("/"))():
            final.mkdir(parents=True, exist_ok=True)
            continue

        final.parent.mkdir(parents=True, exist_ok=True)
        with zf.open(member, pwd=pwd) as src, open(final, "wb") as dst:
            dst.write(src.read())
