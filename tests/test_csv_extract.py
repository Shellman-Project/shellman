from click.testing import CliRunner
from shellman.commands.csv_extract import cli
from pathlib import Path


def create_csv(path: Path):
    lines = [
        "id,name,status,message",
        "1,alpha,ok,initialized",
        "2,beta,fail,ERROR: missing field",
        "3,gamma,ok,complete",
        "4,delta,fail,ERROR: timeout"
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def test_basic_column_extraction(tmp_path):
    f = tmp_path / "data.csv"
    create_csv(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--cols", "2,4"])
    assert result.exit_code == 0
    assert "alpha,initialized" in result.output
    assert "delta,ERROR: timeout" in result.output


def test_row_range_and_skip_header(tmp_path):
    f = tmp_path / "data.csv"
    create_csv(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--cols", "1", "--rows", "2-3", "--skip-header"])
    assert result.exit_code == 0
    lines = result.output.strip().splitlines()
    assert lines[0] == "1"
    assert lines[1] == "2"


def test_contains_filter(tmp_path):
    f = tmp_path / "data.csv"
    create_csv(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--cols", "4", "--contains", "ERROR"])
    assert result.exit_code == 0
    assert "ERROR" in result.output
    assert "complete" not in result.output


def test_not_contains_filter(tmp_path):
    f = tmp_path / "data.csv"
    create_csv(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--cols", "3", "--not-contains", "fail"])
    assert result.exit_code == 0
    assert "ok" in result.output
    assert "fail" not in result.output


def test_output_to_file(tmp_path):
    f = tmp_path / "data.csv"
    out = tmp_path / "extracted.csv"
    create_csv(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--cols", "1,2", "--output", str(out)])
    assert result.exit_code == 0
    content = out.read_text()
    assert "1,alpha" in content
    assert out.exists()
