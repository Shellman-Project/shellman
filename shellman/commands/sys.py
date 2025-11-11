"""Shellman: sys command

Rich system summary with OS/host, CPU, GPU, sensors, battery, BT, tools,
memory, uptime, disks, network, packages, printers, Wi-Fi and displays.

Design goals:
- Cross-platform (Windows / Linux / macOS) with best-effort fallbacks.
- Keep output human-friendly (icons, separators) and fast:
  * external commands use short timeouts;
  * network calls use strict timeouts;
  * failures never crash the command (soft fallbacks).

User notes:
- For the most complete hardware info on Windows, run in PowerShell/CMD (not Git Bash).
- Public IP and some queries may be skipped if offline or blocked by firewall.
"""

from __future__ import annotations

import importlib.resources
import os
import platform
import shutil
import socket
import subprocess
import sys
from pathlib import Path
from typing import Optional

import click


# ───────────────────────────── Helpers ───────────────────────────── #

def _is_git_bash() -> bool:
    """Heuristically detect Git Bash on Windows to show a friendly tip."""
    return (
        os.name == "nt"
        and (
            "MSYSTEM" in os.environ
            or "GIT_INSTALL_ROOT" in os.environ
            or "git" in (os.environ.get("SHELL") or "")
            or (shutil.which("bash") and "usr/bin/bash" in (shutil.which("bash") or "").replace("\\", "/"))
        )
    )


def _run_cmd(cmd: list[str], timeout: float = 2.0, text: bool = True) -> tuple[int, str, str]:
    """Run a command with a short timeout, return (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=text,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except Exception:
        return 1, "", ""


def _bytes_to_mb(n: int) -> int:
    """Convert bytes to whole megabytes."""
    return n // (1024 * 1024)


def _print_sep(title: str) -> None:
    """Print a titled section separator (emoji + title + horizontal rule)."""
    click.echo(title)
    click.echo("─" * 40)


# ───────────────────────────── CLI ───────────────────────────── #

@click.command(help="Show system, shell and tool environment summary.")
@click.option("--lang-help", "-lh", "lang", help="Show localized help (pl, eng) instead of executing.")
def cli(lang: Optional[str]) -> None:
    """Entry point for the `sys` command."""
    if lang:
        _print_help_md(lang)
        return

    click.echo("📋  System Summary")
    click.echo("────────────────────────────────────────")
    if _is_git_bash():
        click.echo("💡 TIP: For full hardware info (Bluetooth, serial no., etc), run sys in Windows PowerShell or CMD — not in Git Bash.\n")

    # -------- OS & Host -------- #
    _print_sep("🖥️  OS & Host")
    os_name = platform.system()
    os_ver = platform.release()
    arch = platform.machine() or platform.architecture()[0]
    wsl = "Yes" if "microsoft" in platform.version().lower() else "No"
    click.echo(f"System       : {os_name}")
    try:
        if os_name == "Linux" and Path("/etc/os-release").exists():
            try:
                name = version = ""
                with open("/etc/os-release", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                name = next((l.split("=", 1)[1].strip('"') for l in lines if l.startswith("NAME=")), "")
                version = next((l.split("=", 1)[1].strip('"') for l in lines if l.startswith("VERSION_ID=")), "")
                if name:
                    click.echo(f"Distro       : {name} {version}".rstrip())
            except Exception:
                pass
        elif os_name == "Darwin":
            rc, out, _ = _run_cmd(["sw_vers", "-productVersion"])
            if rc == 0 and out.strip():
                click.echo(f"macOS        : {out.strip()}")
        elif os_name == "Windows":
            try:
                ver = platform.win32_ver()
                click.echo(f"Windows      : {ver[0]} {ver[1]}")
            except Exception:
                pass
    except Exception:
        pass
    click.echo(f"Version      : {os_ver}")
    click.echo(f"Architecture : {arch}")
    click.echo(f"WSL          : {wsl}")
    click.echo(f"Hostname     : {socket.gethostname()}")

    # -------- Serial Number -------- #
    _print_sep("🔑 Serial Number")
    serial_number = "unavailable"
    try:
        if os_name == "Windows":
            # Try WMIC first (still available on many systems)
            rc, out, _ = _run_cmd(["wmic", "bios", "get", "serialnumber"], timeout=3.0)
            if rc == 0 and out:
                lines = [ln.strip() for ln in out.splitlines() if ln.strip() and "SerialNumber" not in ln]
                if lines:
                    serial_number = lines[0]
        elif os_name == "Linux":
            dmi = Path("/sys/class/dmi/id/product_serial")
            if dmi.exists():
                serial_number = dmi.read_text(encoding="utf-8", errors="ignore").strip()
            else:
                rc, out, _ = _run_cmd(["dmidecode", "-s", "system-serial-number"], timeout=3.0)
                if rc == 0 and out.strip():
                    serial_number = out.strip().splitlines()[0]
        elif os_name == "Darwin":
            rc, out, _ = _run_cmd(["system_profiler", "SPHardwareDataType"], timeout=3.0)
            if rc == 0:
                for line in out.splitlines():
                    if "Serial Number" in line:
                        serial_number = line.split(":")[-1].strip()
                        break
    except Exception:
        pass
    click.echo(f"Serial       : {serial_number}\n")

    # -------- CPU -------- #
    _print_sep("🦾  CPU")
    try:
        import psutil  # type: ignore

        cores = psutil.cpu_count(logical=False)
        cores_log = psutil.cpu_count(logical=True)
        freq = psutil.cpu_freq().current if psutil.cpu_freq() else None
        click.echo(f"Cores        : {cores} (logical: {cores_log})")
        if freq:
            click.echo(f"Frequency    : {freq:.1f} MHz")
    except Exception:
        click.echo("psutil not available")
    try:
        if os_name == "Linux":
            with open("/proc/cpuinfo", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "model name" in line:
                        click.echo(f"Model        : {line.split(':', 1)[1].strip()}")
                        break
        elif os_name == "Windows":
            click.echo(f"Model        : {platform.processor()}")
        elif os_name == "Darwin":
            rc, out, _ = _run_cmd(["sysctl", "-n", "machdep.cpu.brand_string"])
            if rc == 0 and out.strip():
                click.echo(f"Model        : {out.strip()}")
    except Exception:
        pass
    click.echo()

    # -------- Sensors / Temperature -------- #
    _print_sep("🌡️  Sensors / Temperature")
    found_sensor = False
    try:
        import psutil  # type: ignore
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures() or {}
            for chip, vals in temps.items():
                for entry in vals:
                    click.echo(f"{chip}: {entry.label or 'temp'} = {entry.current} °C")
                    found_sensor = True
        if not found_sensor:
            click.echo("No temperature sensors found or supported.")
    except Exception:
        click.echo("psutil not available or sensors not supported")
    click.echo()

    # -------- GPU -------- #
    _print_sep("🖥️  GPU")
    gpus: list[str] = []
    try:
        if os_name == "Linux":
            rc, out, _ = _run_cmd(["lspci"])
            if rc == 0:
                gpus.extend(
                    line.split(":", 2)[-1].strip()
                    for line in out.splitlines()
                    if "VGA compatible controller" in line or "3D controller" in line
                )
        elif os_name == "Windows":
            try:
                import wmi  # type: ignore

                w = wmi.WMI()
                gpus.extend(g.Name for g in w.Win32_VideoController())
            except Exception:
                rc, out, _ = _run_cmd(["wmic", "path", "win32_VideoController", "get", "name"])
                if rc == 0:
                    gpus += [ln.strip() for ln in out.splitlines()[1:] if ln.strip()]
        elif os_name == "Darwin":
            rc, out, _ = _run_cmd(["system_profiler", "SPDisplaysDataType"], timeout=3.0)
            if rc == 0:
                for line in out.splitlines():
                    if "Chipset Model" in line:
                        gpus.append(line.split(":")[-1].strip())
    except Exception:
        pass
    if gpus:
        for gpu in gpus:
            click.echo(f"GPU          : {gpu}")
    else:
        click.echo("GPU info     : unavailable")
    click.echo()

    # -------- Battery -------- #
    _print_sep("🪫️  Battery")
    try:
        import psutil  # type: ignore
        if hasattr(psutil, "sensors_battery"):
            b = psutil.sensors_battery()
            if b is not None:
                click.echo(f"Percent      : {b.percent}%")
                click.echo(f"Plugged in   : {'Yes' if b.power_plugged else 'No'}")
                if getattr(b, "secsleft", None) not in (psutil.POWER_TIME_UNLIMITED, psutil.POWER_TIME_UNKNOWN, None):
                    import datetime

                    t = str(datetime.timedelta(seconds=b.secsleft))
                    click.echo(f"Time left    : {t}")
            else:
                click.echo("No battery detected.")
        else:
            click.echo("psutil (sensors_battery) not supported")
    except Exception:
        click.echo("psutil not available or battery info not supported")
    click.echo()

    # -------- Bluetooth -------- #
    _print_sep("📡  Bluetooth")
    found_bt = False
    try:
        if os_name == "Linux":
            rc, out, _ = _run_cmd(["bluetoothctl", "show"])
            if rc == 0 and out.strip():
                for line in out.splitlines():
                    if "Powered" in line or "Controller" in line:
                        click.echo(line.strip())
                        found_bt = True
        elif os_name == "Windows":
            # Use PowerShell if available (short timeout)
            if shutil.which("powershell"):
                rc, out, _ = _run_cmd(["powershell", "-Command", "Get-PnpDevice -Class Bluetooth"], timeout=3.5)
                if rc == 0 and out.strip():
                    for line in out.splitlines():
                        if line.strip() and not line.startswith("Status"):
                            click.echo(line)
                            found_bt = True
        elif os_name == "Darwin":
            rc, out, _ = _run_cmd(["system_profiler", "SPBluetoothDataType"], timeout=3.5)
            if rc == 0 and out.strip():
                for line in out.splitlines():
                    if any(k in line for k in ("Bluetooth", "Connected", "Manufacturer")):
                        click.echo(line.strip())
                        found_bt = True
        if not found_bt:
            click.echo("No bluetooth devices/info detected.")
    except Exception:
        click.echo("Bluetooth info unavailable")
    click.echo()

    # -------- Tools -------- #
    _print_sep("🛠  Tools")
    def _w(cmd: str) -> str:
        return shutil.which(cmd) or "not found"
    click.echo(f"python3      : {_w('python3')}")
    click.echo(f"git          : {_w('git')}")
    click.echo(f"zip          : {_w('zip')}")
    click.echo(f"unzip        : {_w('unzip')}")
    click.echo(f"jq           : {_w('jq')}")
    click.echo(f"xlsx2csv     : {_w('xlsx2csv')}\n")

    # -------- Memory -------- #
    _print_sep("🧠  Memory")
    if os_name == "Linux":
        rc, out, _ = _run_cmd(["free", "-h"])
        click.echo(out.strip() or "free command not available")
    elif os_name == "Darwin":
        try:
            rc1, memsize, _ = _run_cmd(["sysctl", "-n", "hw.memsize"])
            total_mb = int(memsize.strip()) // (1024 * 1024) if rc1 == 0 and memsize.strip().isdigit() else None
            if total_mb:
                click.echo(f"Total memory: {total_mb} MB")
            rc2, out, _ = _run_cmd(["vm_stat"])
            click.echo(out.strip() or "vm_stat not available")
        except Exception:
            click.echo("vm_stat/sysctl not available")
    elif os_name == "Windows":
        try:
            import psutil  # type: ignore

            vm = psutil.virtual_memory()
            click.echo(f"Total      : {_bytes_to_mb(vm.total)} MB")
            click.echo(f"Available  : {_bytes_to_mb(vm.available)} MB")
            click.echo(f"Used       : {_bytes_to_mb(vm.used)} MB")
            click.echo(f"Percent    : {vm.percent}%")
        except Exception:
            click.echo("psutil not available")
    click.echo()

    # -------- Uptime & Load -------- #
    _print_sep("⏱  Uptime & Load")
    if os_name in ("Linux", "Darwin"):
        rc1, up1, _ = _run_cmd(["uptime", "-p"])
        rc2, up2, _ = _run_cmd(["uptime"])
        if rc1 == 0 and up1.strip():
            click.echo(f"Uptime       : {up1.strip()}")
        if rc2 == 0 and "load average" in up2:
            click.echo("Load Avg.    :" + up2.split("load average:")[-1].strip())
    else:
        try:
            import datetime
            import psutil  # type: ignore

            boot = psutil.boot_time()
            uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot)
            click.echo(f"Uptime       : {str(uptime).split('.')[0]}")
            click.echo("Load Avg.    : (not available on Windows)")
        except Exception:
            click.echo("psutil not available")
    click.echo()

    # -------- Disks -------- #
    _print_sep("💽  Disks")
    if os_name == "Linux":
        rc, out, _ = _run_cmd(["df", "-h", "-x", "tmpfs", "-x", "devtmpfs"])
        click.echo(out.strip() or "df command not available")
    elif os_name == "Darwin":
        rc, out, _ = _run_cmd(["df", "-H"])
        click.echo(out.strip() or "df command not available")
    elif os_name == "Windows":
        try:
            import psutil  # type: ignore

            for part in psutil.disk_partitions():
                # Some mountpoints (e.g. subst or inaccessible) may raise
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    click.echo(
                        f"{part.device} - {usage.percent:.1f}% used "
                        f"({_bytes_to_mb(usage.used)} MB of {_bytes_to_mb(usage.total)} MB)"
                    )
                except Exception:
                    continue
        except Exception:
            click.echo("psutil not available")
    click.echo()

    # -------- Network -------- #
    _print_sep("🌐  Network")
    ip_local = "unavailable"
    if os_name in ("Linux", "Darwin"):
        rc, out, _ = _run_cmd(["hostname", "-I"])
        if rc == 0 and out.strip():
            ip_local = out.strip().split()[0]
    elif os_name == "Windows":
        try:
            ip_local = socket.gethostbyname(socket.gethostname())
        except Exception:
            pass
    ip_public = "unavailable"
    try:
        import urllib.request

        with urllib.request.urlopen("https://ifconfig.me", timeout=2.0) as resp:
            ip_public = (resp.read().decode().strip() or "unavailable")
    except Exception:
        pass
    click.echo(f"Local IP     : {ip_local}")
    click.echo(f"Public IP    : {ip_public}\n")

    # -------- Packages -------- #
    _print_sep("📦  Packages")
    def detect_pkg_mgr() -> str:
        for cmd in ("apt", "dnf", "pacman", "brew", "choco", "winget", "scoop"):
            if shutil.which(cmd):
                return cmd
        return "none"
    pkg_mgr = detect_pkg_mgr()
    count = "unknown"
    try:
        if pkg_mgr == "apt":
            rc, out, _ = _run_cmd(["dpkg", "-l"], timeout=3.5)
            if rc == 0:
                count = str(out.count("\nii"))
        elif pkg_mgr == "pacman":
            rc, out, _ = _run_cmd(["pacman", "-Q"], timeout=3.5)
            if rc == 0:
                count = str(out.count("\n"))
        elif pkg_mgr == "dnf":
            rc, out, _ = _run_cmd(["dnf", "list", "installed"], timeout=3.5)
            if rc == 0:
                count = str(out.count("\n"))
        elif pkg_mgr == "brew":
            rc, out, _ = _run_cmd(["brew", "list"], timeout=3.5)
            if rc == 0:
                count = str(out.count("\n"))
        elif pkg_mgr == "choco":
            rc, out, _ = _run_cmd(["choco", "list", "-l"], timeout=5.0)
            if rc == 0:
                count = str(out.count("\n"))
        elif pkg_mgr == "winget":
            # winget may be slower; cap timeout
            rc, out, _ = _run_cmd(["winget", "list"], timeout=5.0)
            if rc == 0:
                count = str(out.count("\n"))
        elif pkg_mgr == "scoop":
            rc, out, _ = _run_cmd(["scoop", "list"], timeout=3.5)
            if rc == 0:
                count = str(out.count("\n"))
    except Exception:
        pass
    click.echo(f"Pkg Manager  : {pkg_mgr}")
    click.echo(f"Total pkgs   : {count}\n")

    # -------- Printers -------- #
    _print_sep("🖨️  Printers")
    printers: list[str] = []
    try:
        if os_name == "Windows":
            rc, out, _ = _run_cmd(["wmic", "printer", "get", "name"], timeout=3.0)
            if rc == 0:
                printers = [ln.strip() for ln in out.splitlines()[1:] if ln.strip()]
        elif os_name in ("Linux", "Darwin"):
            rc, out, _ = _run_cmd(["lpstat", "-p"], timeout=3.0)
            if rc == 0:
                printers = [ln.split()[1] for ln in out.splitlines() if ln.startswith("printer ")]
    except Exception:
        pass
    if printers:
        for p in printers:
            click.echo(f"Printer      : {p}")
    else:
        click.echo("No printers found.")
    click.echo()

    # -------- Wi-Fi -------- #
    _print_sep("📶  Wi-Fi")
    try:
        ssid = None
        if os_name == "Windows":
            rc, out, _ = _run_cmd(["netsh", "wlan", "show", "interfaces"], timeout=3.0)
            if rc == 0:
                for line in out.splitlines():
                    if "SSID" in line and "BSSID" not in line:
                        ssid = line.split(":", 1)[-1].strip()
                        break
        elif os_name == "Darwin":
            rc, out, _ = _run_cmd(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                timeout=3.0,
            )
            if rc == 0:
                for line in out.splitlines():
                    if " SSID" in line:
                        ssid = line.split(":", 1)[-1].strip()
                        break
        elif os_name == "Linux":
            rc, out, _ = _run_cmd(["iwgetid", "-r"], timeout=2.0)
            if rc == 0:
                ssid = out.strip() or None
        click.echo(f"Connected SSID: {ssid or 'unavailable'}")
    except Exception:
        click.echo("Wi-Fi info unavailable")
    click.echo()

    # -------- Displays -------- #
    _print_sep("🖵️  Displays")
    try:
        if os_name == "Windows":
            import ctypes  # type: ignore

            user32 = ctypes.windll.user32
            width = user32.GetSystemMetrics(0)
            height = user32.GetSystemMetrics(1)
            screens = user32.GetSystemMetrics(80)  # SM_CMONITORS (may be 0 on old systems)
            click.echo(f"Main display: {width} x {height}")
            click.echo(f"Number of screens: {screens or 1}")
        elif os_name == "Darwin":
            rc, out, _ = _run_cmd(["system_profiler", "SPDisplaysDataType"], timeout=3.0)
            if rc == 0:
                for line in out.splitlines():
                    if "Resolution:" in line:
                        click.echo(" ".join(line.split()))
        elif os_name == "Linux":
            rc, out, _ = _run_cmd(["xrandr"], timeout=2.0)
            if rc == 0:
                for line in out.splitlines():
                    if " connected " in line:
                        click.echo(line)
    except Exception:
        click.echo("Display info unavailable")
    click.echo()


# ───────────────────────────── Help MD ───────────────────────────── #

def _print_help_md(lang: str = "eng") -> None:
    """Print localized markdown help for the `sys` command.

    Looks for: shellman/help_texts/sys/help_<lang>.md
    """
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/sys/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
