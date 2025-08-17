import importlib.resources
import secrets
from pathlib import Path

import click
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


@click.command(
    help="Encrypts or decrypts files using AES-256 with a password."
)
@click.option(
    "--mode",
    "-m",
    required=False,
    type=click.Choice(["encrypt", "decrypt"]),
    help="Operation mode (required unless using --lang-help)",
)
@click.option(
    "--password",
    "-pas",
    required=False,
    help="Password to encrypt/decrypt (required unless using --lang-help)",
)
@click.option("--ext", help="Only process files with this extension")
@click.option(
    "--path",
    "-p",
    "scan_path",
    type=click.Path(exists=True, file_okay=False),
    default=".",
    help="Directory to scan",
)
@click.option("--out", "out_dir", type=click.Path(), help="Output directory")
@click.option(
    "--lang-help",
    "-lh",
    "lang",
    help="Show localized help (pl, eng) instead of executing the command",
)
def cli(mode, password, ext, scan_path, out_dir, lang):
    """
    Encrypt or decrypt files using AES-256 with a password.

    Recursively scans a directory for matching files (by extension),
    then encrypts or decrypts them. Encrypted files are saved with
    `.enc` extension, decrypted files restore the original name.

    Args:
        mode (str): Operation mode: "encrypt" or "decrypt".
        password (str): Password used to derive the AES key.
        ext (str | None): Only include files with this extension.
        scan_path (str): Directory to scan. Defaults to current dir.
        out_dir (str | None): Directory to write results.
            Defaults to "encrypted/" or "decrypted/" depending on mode.
        lang (str | None): Show localized help ("pl", "eng") instead of executing.

    Raises:
        click.UsageError: If `--mode` or `--password` is missing.

    Effects:
        - Creates an output directory if not existing.
        - Processes matching files and writes encrypted/decrypted versions.

    Examples:
        Encrypt all `.txt` files:
            $ shellman encrypt_files --mode encrypt --password secret --ext txt

        Decrypt previously encrypted files:
            $ shellman encrypt_files --mode decrypt --password secret --ext txt --path encrypted
    """
    if lang:
        print_help_md(lang)
        return

    if not mode:
        raise click.UsageError("Missing required option '--mode'")
    if not password:
        raise click.UsageError("Missing required option '--password'")

    scan_path = Path(scan_path)
    out_dir = (
        Path(out_dir)
        if out_dir
        else Path("encrypted" if mode == "encrypt" else "decrypted")
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    files = [
        f
        for f in scan_path.rglob("*")
        if f.is_file() and (not ext or f.suffix == f".{ext}")
    ]

    if not files:
        click.echo("No matching files found.", err=True)
        return

    for file in files:
        basename = file.name
        if mode == "encrypt":
            out_file = out_dir / f"{basename}.enc"
            encrypted = encrypt_file(file.read_bytes(), password)
            out_file.write_bytes(encrypted)
            click.echo(f"Encrypted: {file} → {out_file}")
        else:  # decrypt
            rawname = basename[:-4] if basename.endswith(".enc") else basename
            out_file = out_dir / rawname
            decrypted = decrypt_file(file.read_bytes(), password)
            out_file.write_bytes(decrypted)
            click.echo(f"Decrypted: {file} → {out_file}")


# ---------- AES-256-CBC helpers ---------- #
def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit AES key from a password and salt using PBKDF2-HMAC-SHA256.

    Args:
        password (str): Input password string.
        salt (bytes): Random salt (16 bytes recommended).

    Returns:
        bytes: 32-byte derived key.

    Notes:
        - Uses 100,000 PBKDF2 iterations for stronger resistance
          against brute-force attacks."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())


def encrypt_file(data: bytes, password: str) -> bytes:
    """
    Encrypt a byte string using AES-256-CBC with PKCS7 padding.

    Args:
        data (bytes): Plaintext data to encrypt.
        password (str): Password for key derivation.

    Returns:
        bytes: Encrypted data in format: salt|iv|ciphertext

    Process:
        - Generate random 16-byte salt and IV.
        - Derive a 256-bit key from password+salt.
        - Apply PKCS7 padding to data.
        - Encrypt with AES-256-CBC.
        - Concatenate salt, IV, and ciphertext.
    """
    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)
    iv = secrets.token_bytes(16)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return salt + iv + ciphertext  # salt|iv|ciphertext


def decrypt_file(data: bytes, password: str) -> bytes:
    """
    Decrypt AES-256-CBC encrypted data produced by `encrypt_file`.

    Args:
        data (bytes): Encrypted data (salt|iv|ciphertext).
        password (str): Password for key derivation.

    Returns:
        bytes: Decrypted plaintext data.

    Process:
        - Extract salt (first 16 bytes) and IV (next 16 bytes).
        - Derive AES key using PBKDF2-HMAC-SHA256.
        - Decrypt ciphertext with AES-256-CBC.
        - Remove PKCS7 padding.
    """
    salt = data[:16]
    iv = data[16:32]
    ciphertext = data[32:]
    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()


# ---------- Localized help loader ---------- #
def print_help_md(lang: str = "eng"):
    """Print localized help text for the `encrypt_files` command."""
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/encrypt_files/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
