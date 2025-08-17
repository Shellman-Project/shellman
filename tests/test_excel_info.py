from pathlib import Path

from click.testing import CliRunner
from openpyxl import Workbook

from shellman.commands.excel_info import cli


def create_workbook(path: Path, sheets: dict):
    wb = Workbook()
    # Replace default sheet
    default_sheet = wb.active
    default_sheet.title = list(sheets.keys())[0]
    for name, data in sheets.items():
        ws = wb[default_sheet.title if name == default_sheet.title else wb.create_sheet(title=name).title]
        for row in data:
            ws.append(row)
    wb.save(path)


def test_excel_info_basic(tmp_path):
    f = tmp_path / "test.xlsx"
    create_workbook(f, {"Sheet1": [["A", "B"], [1, 2], [3, 4]]})

    runner = CliRunner()
    result = runner.invoke(cli, [str(f)])

    assert result.exit_code == 0
    assert "Sheet" in result.output
    assert "Sheet1" in result.output
    assert "3" in result.output  # Rows
    assert "2" in result.output  # Columns


def test_excel_info_multiple_sheets(tmp_path):
    f = tmp_path / "multi.xlsx"
    create_workbook(f, {
        "Summary": [["A"]],
        "Data": [[1, 2, 3], [4, 5, 6]]
    })

    runner = CliRunner()
    result = runner.invoke(cli, [str(f)])

    assert result.exit_code == 0
    assert "Summary" in result.output
    assert "Data" in result.output
    assert "2" in result.output  # Rows for Data
    assert "3" in result.output  # Columns for Data


def test_excel_info_invalid_file(tmp_path):
    f = tmp_path / "not_excel.txt"
    f.write_text("This is not an Excel file")

    runner = CliRunner()
    result = runner.invoke(cli, [str(f)])

    assert result.exit_code != 0
    assert "Failed to read workbook" in result.output
