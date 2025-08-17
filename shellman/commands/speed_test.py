# shellman/commands/speed_test.py
"""
Cross-platform internet speed test (download / upload / ping).
Falls back through: Ookla binary → speedtest-cli binary → python speedtest-cli.
"""
import importlib.resources
import json as _json
import shutil
import subprocess
import sys
from pathlib import Path

import click


@click.command(
    help="Run a quick internet speed test (download, upload, ping)."
)
@click.option("--json", "json_out", is_flag=True, help="Output raw JSON result")
@click.option(
    "--only",
    type=click.Choice(["download", "upload", "ping"]),
    help="Show only a single metric",
)
@click.option("--lang-help", "lang", help="Show localized help (pl, eng)")
def cli(json_out, only, lang):
    if lang:
        _print_help_md(lang)
        return

    # ---- 1) Spróbuj oficjalnego binarnego klienta Ookla ------------------ #
    if shutil.which("speedtest"):
        if _is_ookla_binary("speedtest"):
            try:
                raw = subprocess.check_output(
                    ["speedtest", "--accept-license", "--accept-gdpr", "-f", "json"],
                    text=True,
                    stderr=subprocess.DEVNULL,
                )
                return _print_from_ookla_json(raw, json_out, only)
            except Exception:
                pass  # spadnij niżej

    # ---- 2) speedtest-cli binary (python) -------------------------------- #
    if shutil.which("speedtest-cli"):
        try:
            raw = subprocess.check_output(
                ["speedtest-cli", "--json"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            return _print_from_cli_json(raw, json_out, only)
        except Exception:
            pass

    # ---- 3) python speedtest-cli ---------------------------------------- #
    try:
        import speedtest  # noqa: E402
    except ModuleNotFoundError:
        click.echo("Installing python speedtest-cli...", err=True)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", "speedtest-cli"]
        )
        import speedtest  # noqa: E402

    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download()
    upload = st.upload()
    ping = st.results.ping
    data = {
        "download_mbps": round(download / 1_000_000, 2),
        "upload_mbps": round(upload / 1_000_000, 2),
        "ping_ms": round(ping, 1),
    }
    _print_result(data, json_out, only)


# ------------------------- helpers ---------------------------------------- #
def _is_ookla_binary(cmd: str) -> bool:
    """Return True if `cmd --help` shows Ookla flags."""
    try:
        help_txt = subprocess.check_output([cmd, "--help"], text=True, stderr=subprocess.DEVNULL)
        return "--accept-license" in help_txt and "--accept-gdpr" in help_txt
    except Exception:
        return False


def _print_from_ookla_json(raw: str, json_out: bool, only: str | None):
    data = _json.loads(raw)
    result = {
        "download_mbps": round(data["download"]["bandwidth"] * 8 / 1_000_000, 2),
        "upload_mbps": round(data["upload"]["bandwidth"] * 8 / 1_000_000, 2),
        "ping_ms": round(data["ping"]["latency"], 1),
    }
    _print_result(result, json_out, only)


def _print_from_cli_json(raw: str, json_out: bool, only: str | None):
    data = _json.loads(raw)
    result = {
        "download_mbps": round(data["download"] / 1_000_000, 2),
        "upload_mbps": round(data["upload"] / 1_000_000, 2),
        "ping_ms": round(data["ping"], 1),
    }
    _print_result(result, json_out, only)


def _print_result(res: dict, json_out: bool, only: str | None):
    if json_out:
        click.echo(_json.dumps(res, ensure_ascii=False))
        return

    if not only or only == "download":
        click.echo(f"⬇️  Download : {res['download_mbps']} Mbit/s")
    if not only or only == "upload":
        click.echo(f"⬆️  Upload   : {res['upload_mbps']} Mbit/s")
    if not only or only == "ping":
        click.echo(f"🏓 Ping      : {res['ping_ms']} ms")


def _print_help_md(lang="eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/speed_test/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
