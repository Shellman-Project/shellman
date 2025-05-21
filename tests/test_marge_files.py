import os
from click.testing import CliRunner
from shellman.commands.merge_files import cli
from pathlib import Path


def create_file(path: Path, content: str):
    path.write_text(content, encoding="utf-8")


def test_basic_merge(tmp_path):
    prev = os.getcwd()
    os.chdir(tmp_path)
    try:
        file1 = tmp_path / "a.txt"
        file2 = tmp_path / "b.txt"
        create_file(file1, "Hello from A\n")
        create_file(file2, "Hello from B\n")

        runner = CliRunner()
        result = runner.invoke(cli, ["--path", ".", "--ext", "txt"])
        assert result.exit_code == 0
        assert "Merging 2 file(s)" in result.output

        merged_file = list((tmp_path / "logs").glob("merged_*.txt"))[0]
        content = merged_file.read_text()
        assert "Hello from A" in content
        assert "Hello from B" in content
    finally:
        os.chdir(prev)


def test_with_header(tmp_path):
    prev = os.getcwd()
    os.chdir(tmp_path)
    try:
        file1 = tmp_path / "x.txt"
        create_file(file1, "some content")

        runner = CliRunner()
        result = runner.invoke(cli, ["--path", ".", "--ext", "txt", "--header"])
        assert result.exit_code == 0

        merged_file = list((tmp_path / "logs").glob("merged_*.txt"))[0]
        content = merged_file.read_text()
        assert f"=== {file1.resolve()}" in content
    finally:
        os.chdir(prev)


def test_sorted_merge(tmp_path):
    prev = os.getcwd()
    os.chdir(tmp_path)
    try:
        file1 = tmp_path / "b.txt"
        file2 = tmp_path / "a.txt"
        create_file(file1, "from B")
        create_file(file2, "from A")

        runner = CliRunner()
        result = runner.invoke(cli, ["--path", ".", "--ext", "txt", "--sort", "--header"])
        assert result.exit_code == 0

        merged_file = list((tmp_path / "logs").glob("merged_*.txt"))[0]
        content = merged_file.read_text()
        assert content.index("=== " + str(file2.resolve())) < content.index("=== " + str(file1.resolve()))
    finally:
        os.chdir(prev)


def test_output_file(tmp_path):
    prev = os.getcwd()
    os.chdir(tmp_path)
    try:
        file1 = tmp_path / "only.txt"
        create_file(file1, "alpha")

        out = tmp_path / "final.txt"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "--path", ".", "--ext", "txt", "--out", str(out)
        ])
        assert result.exit_code == 0
        assert out.exists()
        assert "alpha" in out.read_text()
    finally:
        os.chdir(prev)


def test_filter_by_extension(tmp_path):
    prev = os.getcwd()
    os.chdir(tmp_path)
    try:
        file1 = tmp_path / "file.log"
        file2 = tmp_path / "file.txt"
        create_file(file1, "log content")
        create_file(file2, "txt content")

        runner = CliRunner()
        result = runner.invoke(cli, ["--path", ".", "--ext", "log"])
        assert result.exit_code == 0

        merged_file = list((tmp_path / "logs").glob("merged_*.txt"))[0]
        content = merged_file.read_text()
        assert "log content" in content
        assert "txt content" not in content
    finally:
        os.chdir(prev)
