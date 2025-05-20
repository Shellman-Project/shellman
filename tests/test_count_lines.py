import pytest
from click.testing import CliRunner
from shellman.commands.count_lines import cli
import tempfile
import os
from pathlib import Path

def write_temp_file(content, suffix=".txt"):
    tf = tempfile.NamedTemporaryFile(delete=False, mode="w+", suffix=suffix)
    tf.write(content)
    tf.flush()
    tf.close()
    return tf.name

def test_simple_line_count():
    path = write_temp_file("line1\nline2\nline3\n")
    runner = CliRunner()
    result = runner.invoke(cli, [path])
    assert result.exit_code == 0
    assert "Matching lines: 3" in result.output

def test_contains_option():
    path = write_temp_file("error\ninfo\nerror\n")
    runner = CliRunner()
    result = runner.invoke(cli, [path, "--contains", "error"])
    assert "Matching lines: 2" in result.output

def test_regex_case_insensitive():
    path = write_temp_file("Error\nerror\nINFO\n")
    runner = CliRunner()
    result = runner.invoke(cli, [path, "--regex", "error", "--ignore-case"])
    assert "Matching lines: 2" in result.output

def test_summary_and_percent():
    path = write_temp_file("x\nx\nx\n", suffix=".log")
    runner = CliRunner()
    result = runner.invoke(cli, [path, "--contains", "x", "--summary", "--percent", "--ext", "log"])
    assert "Total lines: 3" in result.output
    assert "Match percentage: 100.00%" in result.output

def test_directory_filtering(tmp_path):
    file1 = tmp_path / "a.txt"
    file1.write_text("a\nb\nc\n")

    file2 = tmp_path / "b.log"
    file2.write_text("error\nerror\nok\n")

    runner = CliRunner()
    result = runner.invoke(cli, [str(tmp_path), "--ext", "log", "--contains", "error"])
    assert "Matching lines: 2" in result.output
    assert "a.txt" not in result.output

