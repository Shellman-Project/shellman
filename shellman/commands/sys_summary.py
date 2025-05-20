import click
import platform
import socket
import shutil
import subprocess
import os
import sys

@click.command(help="""Shows system, shell, and tool environment summary.

Examples:
  shellman sys_summary
""")
def cli():
    print("\U0001F4CB  System Summary")
    print("─" * 40)

    # System Info
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

    print("\U0001F5A5️  OS & Host")
    print("─" * 40)
    print(f"System       : {os_name}")
    if distro:
        print(f"Distro       : {distro}")
    print(f"Version      : {os_ver}")
    print(f"Architecture : {arch}")
    print(f"WSL          : {wsl}")
    print(f"Hostname     : {socket.gethostname()}")
    print()

    # Shell
    shell = os.environ.get("SHELL", "N/A")
    shell_name = os.path.basename(shell)
    shell_ver = ""
    try:
        shell_ver = subprocess.run([shell, "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout.strip()
    except Exception:
        shell_ver = "N/A"

    print("\U0001F41A  Shell")
    print("─" * 40)
    print(f"Shell        : {shell_name}")
    print(f"Shell Ver.   : {shell_ver}")
    if "bash" in shell_name:
        print(f"Bash Ver.    : {os.environ.get('BASH_VERSION', 'N/A')}")
    print()

    # Tools
    print("\U0001F6E0  Tools")
    print("─" * 40)
    print(f"python3      : {shutil.which('python3') or 'not found'}")
    print(f"jq           : {shutil.which('jq') or 'not found'}")
    print(f"xlsx2csv     : {shutil.which('xlsx2csv') or 'not found'}")
    print()

    # Memory
    print("\U0001F9E0  Memory")
    print("─" * 40)
    try:
        result = subprocess.run(["free", "-h"], stdout=subprocess.PIPE, text=True)
        print(result.stdout.strip())
    except FileNotFoundError:
        print("free command not available")
    print()

    # Uptime & Load
    print("\u23F1  Uptime & Load")
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

    # Disks
    print("\U0001F4BD  Disks")
    print("─" * 40)
    try:
        result = subprocess.run(["df", "-h", "-x", "tmpfs", "-x", "devtmpfs"], stdout=subprocess.PIPE, text=True)
        print(result.stdout.strip())
    except FileNotFoundError:
        print("df command not available")
    print()

    # Network
    print("\U0001F310  Network")
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
    print(f"Public IP    : {ip_public}")
    print()

    # Packages
    print("\U0001F4E6  Packages")
    print("─" * 40)
    def detect_pkg_mgr():
        for cmd in ["apt", "dnf", "pacman", "brew", "choco"]:
            if shutil.which(cmd):
                return cmd
        return "none"

    pkg_mgr = detect_pkg_mgr()
    try:
        if pkg_mgr == "apt":
            count = int(subprocess.run(["dpkg", "-l"], stdout=subprocess.PIPE).stdout.decode().count("\nii"))
        elif pkg_mgr == "pacman":
            count = int(subprocess.run(["pacman", "-Q"], stdout=subprocess.PIPE).stdout.decode().count("\n"))
        elif pkg_mgr == "dnf":
            count = int(subprocess.run(["dnf", "list", "installed"], stdout=subprocess.PIPE).stdout.decode().count("\n"))
        elif pkg_mgr == "brew":
            count = int(subprocess.run(["brew", "list"], stdout=subprocess.PIPE).stdout.decode().count("\n"))
        elif pkg_mgr == "choco":
            count = int(subprocess.run(["choco", "list", "-l"], stdout=subprocess.PIPE).stdout.decode().count("\n"))
        else:
            count = "unknown"
    except Exception:
        count = "unknown"

    print(f"Pkg Manager  : {pkg_mgr}")
    print(f"Total pkgs   : {count}")
    print()
