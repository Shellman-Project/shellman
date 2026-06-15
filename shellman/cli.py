import difflib
from importlib.metadata import PackageNotFoundError, version

import click

from .commands import (
    checksum_files,
    dir_tree,
    excel,
    file_stats,
    find_files,
    observe_dir,
    open_ports,
    speed_test,
)
from .commands import sys as sys_cmd
from .commands import zip as zip_cmd


try:
    VERSION = version("shellman")
except PackageNotFoundError:
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


CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}


class ShellmanGroup(click.Group):
    """
    Custom Click command group for Shellman.

    Extends click.Group to:
      - Add author/contact info to the global help output.
      - Suggest similar commands when the user types an unknown command.
    """

    def format_help(self, ctx, formatter):
        """
        Extend the default help output with author information.
        """
        super().format_help(ctx, formatter)
        formatter.write(AUTHOR_INFO)

    def resolve_command(self, ctx, args):
        """
        Resolve a command name and show suggestions for unknown commands.
        """
        try:
            return super().resolve_command(ctx, args)
        except click.UsageError as exc:
            if args:
                cmd_name = args[0]
                suggestions = difflib.get_close_matches(
                    cmd_name,
                    self.commands.keys(),
                    n=4,
                    cutoff=0.5,
                )

                if suggestions:
                    suggestion_text = "\n\nDid you mean:\n" + "\n".join(
                        f"  {item}" for item in suggestions
                    )
                    exc.message = f"{exc.message}{suggestion_text}"

            raise exc


@click.group(
    cls=ShellmanGroup,
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
)
@click.version_option(version=VERSION)
def cli():
    """
    Shellman – your friendly shell assistant.

    For command help in your language:
      shellman find_files --lang-help pl

    Available languages: eng, pl
    """
    pass


cli.add_command(file_stats.cli, name="file_stats")
cli.add_command(find_files.cli, name="find_files")
cli.add_command(checksum_files.cli, name="checksum_files")
cli.add_command(sys_cmd.cli, name="sys")
cli.add_command(excel.cli, name="excel")
cli.add_command(zip_cmd.zip_cli, name="zip")
cli.add_command(speed_test.cli, name="speed_test")
cli.add_command(open_ports.cli, name="open_ports")
cli.add_command(dir_tree.cli, name="dir_tree")
cli.add_command(observe_dir.cli, name="observe_dir")


@cli.command(name="help")
@click.argument("command_path", nargs=-1)
@click.pass_context
def help_cmd(ctx, command_path):
    """
    Show global help or help for a selected command.
    """
    root_ctx = ctx.parent

    if not command_path:
        click.echo(root_ctx.get_help())
        return

    current_command = root_ctx.command
    current_ctx = root_ctx

    for command_name in command_path:
        if not isinstance(current_command, click.Group):
            raise click.ClickException(
                f"Command '{current_command.name}' has no subcommands."
            )

        next_command = click.Group.get_command(
            current_command,
            current_ctx,
            command_name,
        )

        if next_command is None:
            available = ", ".join(current_command.commands.keys())
            raise click.ClickException(
                f"Unknown command: {command_name}\nAvailable commands: {available}"
            )

        current_ctx = click.Context(
            next_command,
            info_name=command_name,
            parent=current_ctx,
        )
        current_command = next_command

    click.echo(current_command.get_help(current_ctx))


@cli.command(name="version")
def version_cmd():
    """
    Show version and exit.
    """
    click.echo(VERSION)
    