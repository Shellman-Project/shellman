import click
from .commands import count_lines, file_stats, find_files

VERSION = open("VERSION").read().strip()

@click.group()
@click.version_option(version=VERSION)
def cli():
    """Shellman – your friendly shell assistant 💬"""
    pass

cli.add_command(count_lines.cli, name="count_lines")
cli.add_command(file_stats.cli, name="file_stats")
cli.add_command(find_files.cli, name="find_files")

