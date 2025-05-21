from click.testing import CliRunner
from shellman.commands.excel_to_csv import cli
from openpyxl import Workbook
from pathlib import Path
import csv


def create_xlsx(path: Path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    ws.append(["A", "B", "C", "D"])
    for i in range(1, 6):
        ws.append([i, i+1, i+2, i+3])
    ws2 = wb.create_sheet("Other")
    ws2.append(["X", "Y"])
    ws2.append(["1", "2"])
    wb.save(path)


def read_csv(path: Path):
    return list(csv.reader(path.open(encoding="utf-8")))


def test_basic_export(tmp_path):
    xlsx = tmp_path / "test.xlsx"
    create_xlsx(xlsx)

    out_dir = tmp_path / "csv"
    runner = CliRunner()
    result = runner.invoke(cli, [str(xlsx), "--out", str(out_dir)])
    assert result.exit_code == 0

    exported = list(out_dir.glob("Data_*.csv"))
    assert len(exported) == 1
    rows = read_csv(exported[0])
    assert rows[0] == ["A", "B", "C", "D"]
    assert len(rows) == 6


def test_export_with_rows(tmp_path):
    xlsx = tmp_path / "test.xlsx"
    create_xlsx(xlsx)

    out_dir = tmp_path / "out"
    runner = CliRunner()
    result = runner.invoke(cli, [str(xlsx), "--out", str(out_dir), "--rows", "2-4"])
    assert result.exit_code == 0

    csv_file = next(out_dir.glob("Data_*.csv"))
    rows = read_csv(csv_file)
    assert len(rows) == 3  # rows 2 to 4 only


def test_export_with_columns(tmp_path):
    xlsx = tmp_path / "test.xlsx"
    create_xlsx(xlsx)

    out_dir = tmp_path / "filtered"
    runner = CliRunner()
    result = runner.invoke(cli, [str(xlsx), "--out", str(out_dir), "--columns", "A,C"])
    assert result.exit_code == 0

    csv_file = next(out_dir.glob("Data_*.csv"))
    rows = read_csv(csv_file)
    assert rows[0] == ["A", "C"]


def test_export_with_overwrite(tmp_path):
    xlsx = tmp_path / "test.xlsx"
    create_xlsx(xlsx)

    out_dir = tmp_path / "plain"
    runner = CliRunner()
    result = runner.invoke(cli, [str(xlsx), "--out", str(out_dir), "--overwrite"])
    assert result.exit_code == 0

    csv_file = out_dir / "Data.csv"
    assert csv_file.exists()


def test_ignore_unknown_sheet(tmp_path):
    xlsx = tmp_path / "test.xlsx"
    create_xlsx(xlsx)

    runner = CliRunner()
    result = runner.invoke(cli, [str(xlsx), "--sheets", "UnknownSheet"])
    assert "Skipping unknown sheet" in result.output
