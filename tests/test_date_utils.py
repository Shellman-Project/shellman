from click.testing import CliRunner

from shellman.commands.date_utils import cli


def test_add_days():
    runner = CliRunner()
    result = runner.invoke(cli, ["--date", "2024-01-01 00:00:00", "--add", "10d"])
    assert result.exit_code == 0
    assert "2024-01-11" in result.output


def test_subtract_hours():
    runner = CliRunner()
    result = runner.invoke(cli, ["--date", "2024-01-01 12:00:00", "--sub", "2h"])
    assert result.exit_code == 0
    assert "2024-01-01 10:00:00" in result.output


def test_add_months():
    runner = CliRunner()
    result = runner.invoke(cli, ["--date", "2024-01-15", "--add", "2m"])
    assert result.exit_code == 0
    assert "2024-03-15" in result.output


def test_format_only():
    runner = CliRunner()
    result = runner.invoke(cli, ["--date", "2024-12-24", "--format", "%A %d %B %Y"])
    assert result.exit_code == 0
    assert "Tuesday" in result.output or "Tuesday" in result.output  # depending on locale


def test_diff_dates():
    runner = CliRunner()
    result = runner.invoke(cli, [
        "--date", "2024-12-24 00:00:00",
        "--diff", "2024-12-26 12:30:45"
    ])
    assert result.exit_code == 0
    assert "2 days" in result.output
    assert "12 hours" in result.output
    assert "30 minutes" in result.output


def test_invalid_base_date():
    runner = CliRunner()
    result = runner.invoke(cli, ["--date", "2024-99-99", "--add", "1d"])
    assert result.exit_code != 0
    assert "Invalid base date" in result.output


def test_invalid_unit():
    runner = CliRunner()
    result = runner.invoke(cli, ["--add", "5blabla"])
    assert result.exit_code != 0
    assert "Unsupported unit" in result.output

