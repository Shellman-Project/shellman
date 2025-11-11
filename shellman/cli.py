import difflib
import importlib.resources
import click

from .commands import (
    change_line_end,
    checksum_files,
    clean_files,
    encrypt_files,
    lines,
    file_convert,
    file_stats,
    find_files,
    replace_text,
    sys_summary,
    excel,
    csv_extract,
    json_extract,
    date_utils,
    zip,
    speed_test,
    open_ports,
    dir_tree,
)

try:
    VERSION = importlib.resources.files("shellman").joinpath("VERSION").read_text().strip()
except Exception:
    VERSION = "unknown"

AUTHOR_INFO = """
──────────────────────────────────────────────
Author:
  Jakub Marciniak
Contact:
  jakub.marciniak.app@gmail.com | marciniakjakub93@gmail.com
LinkedIn:
  https://www.linkedin.com/in/jakub-marciniak-33586b150/
GitHub:
  https://github.com/JakubMarciniak93
──────────────────────────────────────────────
"""

# alias -h -> --help
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class ShellmanGroup(click.Group):
    """
    Custom Click command group for Shellman.

    Extends `click.Group` to:
      - Append project author/contact info to the help output.
      - Override `get_command` so that unknown commands trigger
        the general help display with suggestions, instead of raising
        a fatal "No such command" error.
    """
    def format_help(self, ctx, formatter):
        """
        Extend the default help formatter with author information.

        Args:
          ctx (click.Context): Current Click context.
          formatter (click.HelpFormatter): Formatter used to render help text.
        """
        super().format_help(ctx, formatter)
        formatter.write(AUTHOR_INFO)

    def get_command(self, ctx, cmd_name):
        """
        Resolve a subcommand by name, with fallback for unknown commands.

          - If the command exists, returns it as usual.
          - If not, prints a message with closest matches and shows the global help.
            Exits with code 0 (no error).

        Args:
          ctx (click.Context): Current Click context.
          cmd_name (str): The command name provided by the user.

        Returns:
          click.Command | None: Resolved command object, or None if handled as fallback.
        """
        cmd = super().get_command(ctx, cmd_name)
        if cmd is not None:
            return cmd

        suggestions = difflib.get_close_matches(cmd_name, self.commands.keys(), n=4, cutoff=0.5)
        if cmd_name:
            click.echo(f"Unknown command: {cmd_name}")
            if suggestions:
                click.echo("Did you mean:")
                for s in suggestions:
                    click.echo(f"  {s}")
            click.echo()  

        click.echo(self.get_help(ctx))
        ctx.exit(0)  

@click.group(
    cls=ShellmanGroup,
    context_settings=CONTEXT_SETTINGS,
    invoke_without_command=True,
)
@click.version_option(version=VERSION)
@click.pass_context
def cli(ctx):
    """
    Shellman – your friendly shell assistant 💬

    For command help in your lang:
      shellman count_lines --lang-help pl

    [Available languages: eng, pl]
    ──────────────────────────────────────────────
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


cli.add_command(file_stats.cli,   name="file_stats")
cli.add_command(find_files.cli,   name="find_files")
cli.add_command(checksum_files.cli, name="checksum_files")
cli.add_command(clean_files.cli,  name="clean_files")
cli.add_command(file_convert.cli, name="file_convert")
cli.add_command(replace_text.cli, name="replace_text")
cli.add_command(encrypt_files.cli, name="encrypt_files")
cli.add_command(sys_summary.cli,  name="sys_summary")
cli.add_command(change_line_end.cli, name="change_line_end")
cli.add_command(excel.cli,        name="excel")
cli.add_command(csv_extract.cli,  name="csv_extract")
cli.add_command(json_extract.cli, name="json_extract")
cli.add_command(date_utils.cli,   name="date_utils")
cli.add_command(zip.zip_cli, name="zip")
cli.add_command(speed_test.cli,   name="speed_test")
cli.add_command(open_ports.cli,   name="open_ports")
cli.add_command(dir_tree.cli,     name="dir_tree")
cli.add_command(lines.cli,        name="lines")


@cli.command(name="help")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def help_cmd(args):
    """Show this message and exit."""
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(cli, (list(args) if args else []) + ["--help"])
    click.echo(result.output)


@cli.command(name="version")
def version_cmd():
    """Show version and exit."""
    click.echo(VERSION)
