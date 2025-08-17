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
    required=False,  # sprawdzane ręcznie
    type=click.Choice(["encrypt", "decrypt"]),
    help="Operation mode (required unless using --lang-help)",
)
@click.option(
    "--password",
    required=False,  # sprawdzane ręcznie
    help="Password to encrypt/decrypt (required unless using --lang-help)",
)
@click.option("--ext", help="Only process files with this extension")
@click.option(
    "--path",
    "scan_path",
    type=click.Path(exists=True, file_okay=False),
    default=".",
    help="Directory to scan",
)
@click.option("--out", "out_dir", type=click.Path(), help="Output directory")
@click.option(
    "--lang-help",
    "lang",
    help="Show localized help (pl, eng) instead of executing the command",
)
def cli(mode, password, ext, scan_path, out_dir, lang):
    # --lang-help: pokaż markdown i wyjdź
    if lang:
        print_help_md(lang)
        return

    # Ręczna walidacja wymaganych opcji
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
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())


def encrypt_file(data: bytes, password: str) -> bytes:
    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)
    iv = secrets.token_bytes(16)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return salt + iv + ciphertext  # zapis: salt|iv|ciphertext


def decrypt_file(data: bytes, password: str) -> bytes:
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
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/encrypt_files/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
