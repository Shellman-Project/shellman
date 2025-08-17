import csv
from pathlib import Path

from click.testing import CliRunner
from openpyxl import Workbook

from shellman.commands.excel_preview import cli


def create_test_workbook(path: Path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Main"
    ws.append(["A", "B", "C", "D"])
    ws.append([1, 2, 3, 4])
    ws.append([5, 6, 7, 8])
    wb.create_sheet("Extra").append(["X", "Y"])
    wb.save(path)


def read_csv(path: Path):
    return list(csv.reader(path.open(encoding="utf-8")))


def test_preview_default(tmp_path):
    f = tmp_path / "sheet.xlsx"
    create_test_workbook(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--rows", "2"])
    assert result.exit_code == 0
    assert "A,B,C,D" in result.output
    assert "1,2,3,4" in result.output


def test_preview_columns(tmp_path):
    f = tmp_path / "sheet.xlsx"
    create_test_workbook(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--rows", "2", "--columns", "A,C"])
    assert result.exit_code == 0
    assert "A,C" in result.output
    assert "1,3" in result.output


def test_preview_output_file(tmp_path):
    f = tmp_path / "sheet.xlsx"
    out = tmp_path / "preview.csv"
    create_test_workbook(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--output", str(out), "--rows", "1"])
    assert result.exit_code == 0
    assert "Saved to" in result.output
    rows = read_csv(out)
    assert rows[0] == ["A", "B", "C", "D"]


def test_sheet_by_name(tmp_path):
    f = tmp_path / "sheet.xlsx"
    create_test_workbook(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--sheet", "Extra"])
    assert result.exit_code == 0
    assert "X,Y" in result.output


def test_invalid_sheet(tmp_path):
    f = tmp_path / "sheet.xlsx"
    create_test_workbook(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--sheet", "Nonexistent"])
    assert result.exit_code != 0
    assert "Invalid sheet" in result.output
