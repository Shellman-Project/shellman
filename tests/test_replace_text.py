from click.testing import CliRunner

from shellman.commands.replace_text import cli


def test_basic_replace(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("hello world\nhello again")

    runner = CliRunner()
    result = runner.invoke(
        cli, [str(tmp_path), "--find", "hello", "--replace", "hi", "--ext", "txt"]
    )

    assert "==>" in result.output
    assert "hi again" not in result.output  # preview off
    assert file.read_text() == "hello world\nhello again"  # not in-place


def test_in_place_replace(tmp_path):
    file = tmp_path / "edit.md"
    file.write_text("replace me")

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            str(tmp_path),
            "--find",
            "replace",
            "--replace",
            "fixed",
            "--ext",
            "md",
            "--in-place",
        ],
    )

    assert result.exit_code == 0
    assert "Replaced in:" in result.output
    assert "fixed me" in file.read_text()


def test_confirm_skips_file(tmp_path):
    file = tmp_path / "ask.txt"
    file.write_text("maybe replace this")

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            str(tmp_path),
            "--find",
            "maybe",
            "--replace",
            "definitely",
            "--ext",
            "txt",
            "--in-place",
            "--confirm",
        ],
        input="n\n",
    )

    assert "Skipped" in result.output
    assert "maybe replace this" in file.read_text()


def test_preview_diff_shown(tmp_path):
    file = tmp_path / "diff.txt"
    file.write_text("start\nreplace this\nend")

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            str(tmp_path),
            "--find",
            "replace",
            "--replace",
            "fix",
            "--ext",
            "txt",
            "--preview",
        ],
    )

    assert "---" in result.output
    assert "+fix this" in result.output or "+replace this" not in result.output
