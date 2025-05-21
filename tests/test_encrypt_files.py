from pathlib import Path

from click.testing import CliRunner

from shellman.commands.encrypt_files import cli


def test_encrypt_and_decrypt(tmp_path):
    original = tmp_path / "note.txt"
    original.write_text("super secret")

    enc_dir = tmp_path / "enc"
    dec_dir = tmp_path / "dec"

    # Encrypt
    runner = CliRunner()
    result_enc = runner.invoke(
        cli,
        [
            "--mode",
            "encrypt",
            "--password",
            "mypassword",
            "--path",
            str(tmp_path),
            "--ext",
            "txt",
            "--out",
            str(enc_dir),
        ],
    )
    assert result_enc.exit_code == 0
    enc_file = next(enc_dir.glob("note.txt.enc"))
    assert enc_file.exists()
    assert enc_file.read_bytes() != original.read_bytes()

    # Decrypt
    result_dec = runner.invoke(
        cli,
        [
            "--mode",
            "decrypt",
            "--password",
            "mypassword",
            "--path",
            str(enc_dir),
            "--ext",
            "enc",
            "--out",
            str(dec_dir),
        ],
    )
    assert result_dec.exit_code == 0
    dec_file = dec_dir / "note.txt"
    assert dec_file.exists()
    assert dec_file.read_text() == "super secret"


def test_no_matching_files(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--mode",
            "encrypt",
            "--password",
            "abc",
            "--path",
            str(tmp_path),
            "--ext",
            "log",
        ],
    )
    assert result.exit_code == 0
    assert "No matching files" in result.output
