from click.testing import CliRunner

from shellman.commands.change_line_end import cli


def test_check_line_endings_lf(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("one\nline\ntwo\n")
    runner = CliRunner()
    result = runner.invoke(cli, ["--file", str(f), "--check"])
    assert "→ LF" in result.output


def test_check_line_endings_crlf(tmp_path):
    f = tmp_path / "file.txt"
    f.write_bytes(b"one\r\nline\r\ntwo\r\n")
    runner = CliRunner()
    result = runner.invoke(cli, ["--file", str(f), "--check"])
    assert "→ CRLF" in result.output


def test_check_line_endings_lf(tmp_path):
    f = tmp_path / "file.txt"
    f.write_bytes(b"one\nline\ntwo\n")
    runner = CliRunner()
    result = runner.invoke(cli, ["--file", str(f), "--check"])
    assert "→ LF" in result.output


def test_convert_to_crlf(tmp_path):
    f = tmp_path / "lf.txt"
    f.write_text("line1\nline2\n")
    runner = CliRunner()
    result = runner.invoke(cli, ["--file", str(f), "--to", "crlf"])
    assert f.read_bytes() == b"line1\r\nline2\r\n"
    assert "converted to CRLF" in result.output


def test_check_mixed_endings(tmp_path):
    f = tmp_path / "mixed.txt"
    f.write_bytes(b"one\r\ntwo\nthree\r\n")
    runner = CliRunner()
    result = runner.invoke(cli, ["--file", str(f), "--check"])
    assert "→ MIXED" in result.output


def test_ext_filter_on_dir(tmp_path):
    (tmp_path / "keep.md").write_text("hi\n")
    (tmp_path / "skip.txt").write_text("bye\n")
    runner = CliRunner()
    result = runner.invoke(cli, ["--dir", str(tmp_path), "--ext", "md", "--check"])
    assert "keep.md" in result.output
    assert "skip.txt" not in result.output
