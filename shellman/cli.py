import click
from .commands import (
    change_line_end,
    checksum_files,
    clean_files,
    count_lines,
    encrypt_files,
    extract_lines,
    file_convert,
    file_stats,
    find_files,
    replace_text,
    sys_summary,
    excel_info,
    excel_to_csv,
    excel_preview,
    csv_extract,
    json_extract,
    date_utils,
    merge_files,
    zip_batch,
)

import importlib.resources

try:
    VERSION = importlib.resources.files("shellman").joinpath("VERSION").read_text().strip()
except Exception:
    VERSION = "unknown"


@click.group()
@click.version_option(version=VERSION)
def cli():
    """Shellman – your friendly shell assistant 💬"""
    pass

cli.add_command(count_lines.cli, name="count_lines")
cli.add_command(file_stats.cli, name="file_stats")
cli.add_command(find_files.cli, name="find_files")
cli.add_command(checksum_files.cli, name="checksum_files")
cli.add_command(clean_files.cli, name="clean_files")
cli.add_command(file_convert.cli, name="file_convert")
cli.add_command(replace_text.cli, name="replace_text")
cli.add_command(encrypt_files.cli, name="encrypt_files")
cli.add_command(sys_summary.cli, name="sys_summary")
cli.add_command(change_line_end.cli, name="change_line_end")
cli.add_command(extract_lines.cli, name="extract_lines")
cli.add_command(excel_info.cli, name="excel_info")
cli.add_command(excel_to_csv.cli, name="excel_to_csv")
cli.add_command(excel_preview.cli, name="excel_preview")
cli.add_command(csv_extract.cli, name="csv_extract")
cli.add_command(json_extract.cli, name="json_extract")
cli.add_command(date_utils.cli, name="date_utils")
cli.add_command(merge_files.cli, name="merge_files")
cli.add_command(zip_batch.cli, name="zip_batch")
@cli.command(name="help")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def help_cmd(args):
    """Show this message and exit."""
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"] if not args else list(args) + ["--help"])
    click.echo(result.output)
@cli.command(name="version")
def version_cmd():
    """Show version and exit."""
    click.echo(VERSION)

