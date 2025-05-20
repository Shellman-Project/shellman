import os
from pathlib import Path
from click.testing import CliRunner
from shellman.commands.clean_files import cli

def create_file(path: Path, days_old=0):
    path.write_text("temp")
    if days_old > 0:
        old_time = (path.stat().st_mtime - days_old * 86400)
        os.utime(path, (old_time, old_time))

def test_dry_run_does_not_delete(tmp_path):
    file = tmp_path / "test.tmp"
    create_file(file)
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", str(tmp_path), "--ext", "tmp", "--dry-run"])
    assert result.exit_code == 0
    assert "test.tmp" in result.output
    assert file.exists()

def test_file_deletion(tmp_path):
    file = tmp_path / "delete.me"
    create_file(file)
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", str(tmp_path), "--name", "delete"])
    assert result.exit_code == 0
    assert "Deleted" in result.output
    assert not file.exists()

def test_confirm_prevents_deletion(tmp_path):
    file = tmp_path / "confirm.log"
    create_file(file)
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", str(tmp_path), "--ext", "log", "--confirm"], input="n\n")
    assert result.exit_code == 0
    assert "Delete" in result.output
    assert file.exists()

def test_older_than_filter(tmp_path):
    old_file = tmp_path / "old.tmp"
    new_file = tmp_path / "new.tmp"
    create_file(old_file, days_old=10)
    create_file(new_file, days_old=1)
    runner = CliRunner()
    result = runner.invoke(cli, ["--path", str(tmp_path), "--ext", "tmp", "--older-than", "5", "--dry-run"])
    assert "old.tmp" in result.output
    assert "new.tmp" not in result.output
