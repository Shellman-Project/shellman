import pytest
from click.testing import CliRunner
from shellman.commands.file_stats import cli
import tempfile
import os
from pathlib import Path

def write_temp_file(content, suffix=".txt"):
    tf = tempfile.NamedTemporaryFile(delete=False, mode="w+", suffix=suffix)
    tf.write(content)
    tf.flush()
    tf.close()
    return tf.name

def test_file_stats_basic():
    path = write_temp_file("a\nb\nc\n")
    runner = CliRunner()
    result = runner.invoke(cli, [path])
    assert result.exit_code == 0
    assert "Lines: 3" in result.output
    assert "Size:" in result.output
    assert "Extension:" in result.output

def test_file_stats_with_ext_filter(tmp_path):
    (tmp_path / "a.txt").write_text("line\n")
    (tmp_path / "b.log").write_text("log\nline\n")
    runner = CliRunner()
    result = runner.invoke(cli, [str(tmp_path), "--ext", "log"], catch_exceptions=False)
    assert "b.log" in result.output
    assert "a.txt" not in result.output


def test_file_stats_output_to_file(tmp_path):
    file = tmp_path / "example.txt"
    file.write_text("1\n2\n3\n")
    runner = CliRunner()
    os.chdir(tmp_path)  # so that logs/ is created here
    result = runner.invoke(cli, [str(file), "--output"])
    assert "Results saved to logs/file_stats_" in result.output
    logs_dir = tmp_path / "logs"
    assert any(f.name.startswith("file_stats_") for f in logs_dir.iterdir())
