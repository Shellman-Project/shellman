import os
import platform
import shutil
import socket
import subprocess
import importlib.resources

import click


@click.command(
    help="Show system, shell and tool environment summary."
)
@click.option("--lang-help", "lang", help="Show localized help (pl, eng) instead of executing")
def cli(lang):
    # ---------- lokalizowana pomoc ---------- #
    if lang:
        _print_help_md(lang)
        return

    print("\U0001f4cb  System Summary")
    print("─" * 40)

    # ----------- System Info ----------- #
    os_name = platform.system()
    os_ver = platform.release()
    arch = platform.machine()
    distro = ""
    wsl = "Yes" if "microsoft" in platform.version().lower() else "No"
    try:
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release") as f:
                lines = f.read().splitlines()
                name = next((l.split("=")[1].strip('"') for l in lines if l.startswith("NAME=")), "")
                version = next((l.split("=")[1].strip('"') for l in lines if l.startswith("VERSION_ID=")), "")
                distro = f"{name} {version}"
    except Exception:
        pass

    print("\U0001f5a5️  OS & Host")
    print("─" * 40)
    print(f"System       : {os_name}")
    if distro:
        print(f"Distro       : {distro}")
    print(f"Version      : {os_ver}")
    print(f"Architecture : {arch}")
    print(f"WSL          : {wsl}")
    print(f"Hostname     : {socket.gethostname()}\n")

    # ----------- Shell ----------- #
    shell = os.environ.get("SHELL", "N/A")
    shell_name = os.path.basename(shell)
    try:
        shell_ver = subprocess.run([shell, "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout.strip()
    except Exception:
        shell_ver = "N/A"

    print("\U0001f41a  Shell")
    print("─" * 40)
    print(f"Shell        : {shell_name}")
    print(f"Shell Ver.   : {shell_ver}")
    if "bash" in shell_name:
        print(f"Bash Ver.    : {os.environ.get('BASH_VERSION', 'N/A')}\n")

    # ----------- Tools ----------- #
    print("\U0001f6e0  Tools")
    print("─" * 40)
    print(f"python3      : {shutil.which('python3') or 'not found'}")
    print(f"jq           : {shutil.which('jq') or 'not found'}")
    print(f"xlsx2csv     : {shutil.which('xlsx2csv') or 'not found'}\n")

    # ----------- Memory ----------- #
    print("\U0001f9e0  Memory")
    print("─" * 40)
    try:
        result = subprocess.run(["free", "-h"], stdout=subprocess.PIPE, text=True)
        print(result.stdout.strip())
    except FileNotFoundError:
        print("free command not available")
    print()

    # ----------- Uptime & Load ----------- #
    print("\u23f1  Uptime & Load")
    print("─" * 40)
    try:
        up1 = subprocess.run(["uptime", "-p"], stdout=subprocess.PIPE, text=True).stdout.strip()
        up2 = subprocess.run(["uptime"], stdout=subprocess.PIPE, text=True).stdout.strip()
        print(f"Uptime       : {up1}")
        if "load average" in up2:
            print("Load Avg.    :" + up2.split("load average:")[-1])
    except FileNotFoundError:
        print("uptime command not available")
    print()

    # ----------- Disks ----------- #
    print("\U0001f4bd  Disks")
    print("─" * 40)
    try:
        result = subprocess.run(["df", "-h", "-x", "tmpfs", "-x", "devtmpfs"], stdout=subprocess.PIPE, text=True)
        print(result.stdout.strip())
    except FileNotFoundError:
        print("df command not available")
    print()

    # ----------- Network ----------- #
    print("\U0001f310  Network")
    print("─" * 40)
    try:
        ip_local = subprocess.run(["hostname", "-I"], stdout=subprocess.PIPE, text=True).stdout.strip().split()[0]
    except Exception:
        ip_local = "unavailable"
    try:
        import urllib.request
        ip_public = urllib.request.urlopen("https://ifconfig.me").read().decode().strip()
    except Exception:
        ip_public = "unavailable"
    print(f"Local IP     : {ip_local}")
    print(f"Public IP    : {ip_public}\n")

    # ----------- Packages ----------- #
    print("\U0001f4e6  Packages")
    print("─" * 40)

    def detect_pkg_mgr():
        for cmd in ["apt", "dnf", "pacman", "brew", "choco"]:
            if shutil.which(cmd):
                return cmd
        return "none"

    pkg_mgr = detect_pkg_mgr()
    try:
        if pkg_mgr == "apt":
            count = subprocess.run(["dpkg", "-l"], stdout=subprocess.PIPE).stdout.decode().count("\nii")
        elif pkg_mgr == "pacman":
            count = subprocess.run(["pacman", "-Q"], stdout=subprocess.PIPE).stdout.decode().count("\n")
        elif pkg_mgr == "dnf":
            count = subprocess.run(["dnf", "list", "installed"], stdout=subprocess.PIPE).stdout.decode().count("\n")
        elif pkg_mgr == "brew":
            count = subprocess.run(["brew", "list"], stdout=subprocess.PIPE).stdout.decode().count("\n")
        elif pkg_mgr == "choco":
            count = subprocess.run(["choco", "list", "-l"], stdout=subprocess.PIPE).stdout.decode().count("\n")
        else:
            count = "unknown"
    except Exception:
        count = "unknown"

    print(f"Pkg Manager  : {pkg_mgr}")
    print(f"Total pkgs   : {count}\n")


# ---------- Markdown help loader ---------- #
def _print_help_md(lang: str = "eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/sys_summary/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
