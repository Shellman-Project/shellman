from shellman.commands.find_files import cli
from click.testing import CliRunner
import tempfile
import os
from pathlib import Path

def test_find_by_name(tmp_path):
    (tmp_path / "file_log.txt").write_text("some content")
    (tmp_path / "data.txt").write_text("other content")
    runner = CliRunner()
    result = runner.invoke(cli, [str(tmp_path), "--name", "log"])
    assert "file_log.txt" in result.output
    assert "data.txt" not in result.output

def test_find_by_content(tmp_path):
    (tmp_path / "a.txt").write_text("hello world")
    (tmp_path / "b.txt").write_text("no match here")
    runner = CliRunner()
    result = runner.invoke(cli, [str(tmp_path), "--content", "world"])
    assert "a.txt" in result.output
    assert "b.txt" not in result.output

def test_find_by_ext_and_size(tmp_path):
    file = tmp_path / "script.sh"
    file.write_text("echo test\n")
    runner = CliRunner()
    result = runner.invoke(cli, [str(tmp_path), "--ext", "sh", "--show-size"])
    assert "script.sh" in result.output
    assert "[" in result.output  # file size indicator

def test_find_nothing(tmp_path):
    (tmp_path / "a.txt").write_text("irrelevant")
    runner = CliRunner()
    result = runner.invoke(cli, [str(tmp_path), "--name", "notfound"])
    assert result.exit_code != 0
    assert "No files found" in result.output
