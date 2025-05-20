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
)

VERSION = open("VERSION").read().strip()

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
