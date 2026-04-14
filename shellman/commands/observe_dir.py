from __future__ import annotations

import time
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Deque

import click


def _timestamp_now() -> str:
    """Return the current local timestamp for file markers."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _echo_text(text: str, *, is_green: bool, nl: bool = True) -> None:
    """Print text using alternating color blocks for observed files."""
    if is_green:
        click.secho(text, fg="green", nl=nl)
    else:
        click.echo(text, nl=nl)


def _print_marker(kind: str, file_path: Path, *, is_green: bool) -> None:
    """Print a visible marker for the start or end of a file stream."""
    click.echo()
    _echo_text(f"[{kind} {_timestamp_now()}] {file_path}", is_green=is_green)


def _iter_files(directory: Path):
    """Yield regular files from the observed directory."""
    for file_path in directory.iterdir():
        if file_path.is_file():
            yield file_path.resolve()


def _discover_new_files(
    *,
    directory: Path,
    known_files: set[Path],
    queued_files: set[Path],
    pending_files: Deque[Path],
) -> bool:
    """Scan the directory and queue files that have not been seen yet."""
    discovered_now: list[Path] = []

    for file_path in _iter_files(directory):
        if file_path in known_files or file_path in queued_files:
            continue
        discovered_now.append(file_path)

    discovered_now.sort(key=lambda item: (item.stat().st_mtime_ns, str(item)))

    for file_path in discovered_now:
        pending_files.append(file_path)
        queued_files.add(file_path)

    return bool(discovered_now)


@click.command(
    help="""Observe a directory and print full contents of files as they appear.

The command reads a file from the beginning. When a new file appears,
Shellman stops reading the current file and switches to the new one.
Every second file block is displayed in green.

Examples:
  shellman observe_dir ./logs
  shellman observe_dir ./logs -s 1
"""
)
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option(
    "-s",
    "seconds",
    default=1.0,
    show_default=True,
    type=click.FloatRange(min=0.1),
    help="Refresh interval in seconds.",
)
def cli(directory, seconds):
    """Observe files in a directory and stream their contents to stdout."""
    base_path = Path(directory).resolve()
    if not base_path.is_dir():
        raise click.ClickException(f"Path is not a directory: {base_path}")

    known_files: set[Path] = set()
    queued_files: set[Path] = set()
    pending_files: Deque[Path] = deque()

    current_file: Path | None = None
    current_stream = None
    current_is_green = False
    file_counter = 0

    try:
        while True:
            _discover_new_files(
                directory=base_path,
                known_files=known_files,
                queued_files=queued_files,
                pending_files=pending_files,
            )

            if pending_files and current_stream is not None and current_file is not None:
                _print_marker("END", current_file, is_green=current_is_green)
                current_stream.close()
                current_stream = None
                current_file = None

            if current_stream is None and pending_files:
                current_file = pending_files.popleft()
                queued_files.discard(current_file)
                known_files.add(current_file)

                file_counter += 1
                current_is_green = (file_counter % 2 == 0)

                _print_marker("BEGIN", current_file, is_green=current_is_green)
                try:
                    current_stream = current_file.open(
                        "r",
                        encoding="utf-8",
                        errors="replace",
                    )
                except Exception as exc:
                    click.echo(f"Failed to open {current_file}: {exc}", err=True)
                    current_stream = None
                    current_file = None
                    time.sleep(seconds)
                    continue

            if current_stream is not None and current_file is not None:
                try:
                    chunk = current_stream.read()
                except Exception as exc:
                    click.echo(f"Failed to read {current_file}: {exc}", err=True)
                    _print_marker("END", current_file, is_green=current_is_green)
                    current_stream.close()
                    current_stream = None
                    current_file = None
                    time.sleep(seconds)
                    continue

                if chunk:
                    _echo_text(chunk, is_green=current_is_green, nl=False)

            time.sleep(seconds)
    except KeyboardInterrupt:
        if current_stream is not None and current_file is not None:
            _print_marker("END", current_file, is_green=current_is_green)
