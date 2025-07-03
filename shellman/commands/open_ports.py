# shellman/commands/open_ports.py
"""
List currently open TCP / UDP ports with process name, PID and state.
Works on Linux, macOS and Windows.  Requires `psutil`.
"""
from pathlib import Path
import subprocess
import sys
import shutil
import socket
import importlib.resources
import json as _json

import click


@click.command(
    help="Show currently open TCP/UDP ports (process, pid, address, state)."
)
@click.option("--proto", type=click.Choice(["tcp", "udp"]), help="Filter by protocol")
@click.option("--port", type=int, help="Filter by local port number")
@click.option("--json", "json_out", is_flag=True, help="Output raw JSON")
@click.option("--lang-help", "lang", help="Show localized help (pl, eng)")
def cli(proto, port, json_out, lang):
    if lang:
        _print_help_md(lang)
        return

    # ensure psutil
    try:
        import psutil
    except ModuleNotFoundError:
        click.echo("Installing psutil...", err=True)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "psutil"])
        import psutil

    conns = psutil.net_connections(kind="inet")
    result = []
    for c in conns:
        proto_name = "tcp" if c.type == socket.SOCK_STREAM else "udp"
        if proto and proto_name != proto:
            continue
        if port and (c.laddr and c.laddr.port != port):
            continue

        laddr = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else ""
        raddr = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else ""
        entry = {
            "proto": proto_name,
            "pid": c.pid or "-",
            "process": _proc_name(c.pid),
            "local": laddr,
            "remote": raddr,
            "state": getattr(c, "status", ""),
        }
        result.append(entry)

    if json_out:
        click.echo(_json.dumps(result, ensure_ascii=False, indent=2))
        return

    if not result:
        click.echo("No matching open ports.")
        return

    hdr = f"{'Proto':<4} {'PID':>6} {'Process':<18} {'Local':<22} {'Remote':<22} State"
    click.echo(hdr)
    click.echo("-" * len(hdr))
    for e in result:
        click.echo(
            f"{e['proto']:<4} {str(e['pid']):>6} {e['process'][:17]:<18} "
            f"{e['local']:<22} {e['remote']:<22} {e['state']}"
        )


def _proc_name(pid):
    if pid is None:
        return "-"
    try:
        import psutil
        return psutil.Process(pid).name()
    except Exception:
        return "?"


def _print_help_md(lang="eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/open_ports/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
