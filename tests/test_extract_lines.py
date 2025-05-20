from click.testing import CliRunner
from shellman.commands.extract_lines import cli
from pathlib import Path

def create_log(path: Path):
    content = "\n".join([
        "Info: system starting",
        "Info: init done",
        "Warning: low memory",
        "ERROR: failed to load",
        "Debug: retrying...",
        "ERROR: timeout",
        "Info: done"
    ])
    path.write_text(content)

def test_contains_basic(tmp_path):
    f = tmp_path / "log.txt"
    create_log(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--contains", "ERROR"])
    assert result.exit_code == 0
    assert "ERROR: failed to load" in result.output
    assert "ERROR: timeout" in result.output
    assert "Lines printed:" in result.output

def test_not_contains_and_output(tmp_path):
    f = tmp_path / "log.txt"
    out = tmp_path / "filtered.txt"
    create_log(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--not-contains", "ERROR", "--output", str(out)])
    assert result.exit_code == 0
    assert "Saved to" in result.output
    assert "ERROR" not in out.read_text()

def test_context_before_after(tmp_path):
    f = tmp_path / "log.txt"
    create_log(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--contains", "timeout", "--before", "1", "--after", "1"])
    assert result.exit_code == 0
    assert "Debug: retrying..." in result.output
    assert "Info: done" in result.output

def test_invalid_usage(tmp_path):
    f = tmp_path / "log.txt"
    create_log(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--contains", "X", "--not-contains", "Y"])
    assert result.exit_code != 0
    assert "either" in result.output.lower()
