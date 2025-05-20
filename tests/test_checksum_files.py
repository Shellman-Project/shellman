import pytest
from click.testing import CliRunner
from shellman.commands.checksum_files import cli
import tempfile
from pathlib import Path

def test_generate_and_verify_checksum(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello world\n")

    out_file = tmp_path / "output.sha256sum"

    # Generate checksums
    runner = CliRunner()
    result_gen = runner.invoke(cli, ["--path", str(tmp_path), "--algo", "sha256", "--out", str(out_file)])
    assert result_gen.exit_code == 0
    assert out_file.exists()

    # Verify checksums
    result_ver = runner.invoke(cli, ["--verify", "--out", str(out_file)])
    assert result_ver.exit_code == 0
    assert "✅ OK:" in result_ver.output

def test_checksum_filter_by_extension(tmp_path):
    (tmp_path / "a.log").write_text("aaa")
    (tmp_path / "b.txt").write_text("bbb")

    out_file = tmp_path / "log_only.sha1sum"
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", str(tmp_path), "--ext", "log", "--algo", "sha1", "--out", str(out_file)])
    assert result.exit_code == 0
    with open(out_file) as f:
        lines = f.readlines()
        assert any("a.log" in line for line in lines)
        assert all("b.txt" not in line for line in lines)
