"""
shellman/commands/open_ports.py

Show open TCP/UDP ports and physical serial/parallel ports with process info and device descriptions.
Works on Linux, macOS, and Windows. Requires `psutil` and `pyserial` for full serial port info.
"""

import importlib.resources
import json as _json
import socket
import subprocess
import sys

import click


@click.command(
    help="Show currently open TCP/UDP ports and serial ports (COM/LPT/tty) with process, PID, state, and device name."
)
@click.option("--proto", "-pro", type=click.Choice(["tcp", "udp"]), help="Filter by protocol")
@click.option("--port", "-p", type=int, help="Filter by local port number")
@click.option("--json", "-j", "json_out", is_flag=True, help="Output raw JSON (TCP/UDP only)")
@click.option("--serial", "-s", is_flag=True, help="List physical serial/parallel ports (COM/LPT/tty) with device description")
@click.option("--lang-help", "-lh", "lang", help="Show localized help (pl, eng)")
def cli(proto, port, json_out, serial, lang):
    if lang:
        _print_help_md(lang)
        return

    out_blocks = []

    # --- TCP/UDP ports ---
    if not serial:
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
            out_blocks.append("No matching open TCP/UDP ports.")
        else:
            hdr = f"{'Proto':<4} {'PID':>6} {'Process':<18} {'Local':<22} {'Remote':<22} State"
            out_blocks.append(hdr)
            out_blocks.append("-" * len(hdr))
            out_blocks.extend(
                f"{e['proto']:<4} {str(e['pid']):>6} {e['process'][:17]:<18} "
                f"{e['local']:<22} {e['remote']:<22} {e['state']}"
                for e in result)

    # --- SERIAL ports (COM, LPT, tty, cu), with descriptions ---
    if serial:
        serial_ports = find_serial_ports_with_desc()
        if not serial_ports:
            out_blocks.append("No serial (COM/LPT/tty) ports found.")
        else:
            out_blocks.append("Available serial/parallel ports:")
            out_blocks.extend(f"  {port}" for port in serial_ports)

    click.echo("\n".join(out_blocks))


def find_serial_ports_with_desc():
    try:
        from serial.tools import list_ports
        ports = list_ports.comports()
        out = []
        for p in ports:
            desc = p.description
            name = p.device
            if desc and desc != name:
                out.append(f"{desc} ({name})")
            else:
                out.append(name)
        return out
    except Exception:
        # Fallback for POSIX: glob possible device names
        import glob
        patterns = [
            "/dev/ttyUSB*",
            "/dev/ttyACM*",
            "/dev/ttyS*",
            "/dev/cu.*",
            "/dev/tty.*",
            "/dev/lp*",
        ]
        found = []
        for pat in patterns:
            found.extend(glob.glob(pat))
        return sorted(set(found))


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
