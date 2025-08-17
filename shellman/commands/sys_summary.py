import importlib.resources
import os
import platform
import shutil
import socket
import subprocess

import click


def _is_git_bash():
    # Sprawdza czy działa w Git Bash na Windows
    return (os.name == "nt" and (
        "MSYSTEM" in os.environ or
        "GIT_INSTALL_ROOT" in os.environ or
        "git" in (os.environ.get("SHELL") or "") or
        (shutil.which("bash") and "usr/bin/bash" in shutil.which("bash").replace("\\", "/"))
    ))

@click.command(
    help="Show system, shell and tool environment summary."
)
@click.option("--lang-help", "lang", help="Show localized help (pl, eng) instead of executing")
def cli(lang):
    if lang:
        _print_help_md(lang)
        return

    print("\U0001f4cb  System Summary")
    print("─" * 40)

    os_name = platform.system()
    os_ver = platform.release()
    arch = platform.machine()
    distro = ""
    wsl = "Yes" if "microsoft" in platform.version().lower() else "No"

    # --- GIT BASH info tip ---
    if _is_git_bash():
        print("💡 TIP: For full hardware info (Bluetooth, serial no., etc), run sys_summary in Windows PowerShell or CMD — not in Git Bash.")
        print()

    # ----------- System Info ----------- #
    print("\U0001f5a5️  OS & Host")
    print("─" * 40)
    print(f"System       : {os_name}")
    if os_name == "Linux" and os.path.exists("/etc/os-release"):
        try:
            with open("/etc/os-release") as f:
                lines = f.read().splitlines()
                name = next((l.split("=")[1].strip('"') for l in lines if l.startswith("NAME=")), "")
                version = next((l.split("=")[1].strip('"') for l in lines if l.startswith("VERSION_ID=")), "")
                distro = f"{name} {version}"
                print(f"Distro       : {distro}")
        except Exception:
            pass
    elif os_name == "Darwin":
        try:
            mac_ver = subprocess.run(["sw_vers", "-productVersion"], stdout=subprocess.PIPE, text=True).stdout.strip()
            print(f"macOS        : {mac_ver}")
        except Exception:
            pass
    elif os_name == "Windows":
        try:
            ver = platform.win32_ver()
            print(f"Windows      : {ver[0]} {ver[1]}")
        except Exception:
            pass

    print(f"Version      : {os_ver}")
    print(f"Architecture : {arch}")
    print(f"WSL          : {wsl}")
    print(f"Hostname     : {socket.gethostname()}")

    # ----------- Serial Number ----------- #
    print("🔑 Serial Number")
    print("─" * 40)
    serial_number = None
    try:
        if os_name == "Windows":
            try:
                if shutil.which("wmic"):
                    out = subprocess.run(["wmic", "bios", "get", "serialnumber"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                else:
                    out = subprocess.run(["cmd.exe", "/c", "wmic bios get serialnumber"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                lines = [l.strip() for l in out.stdout.splitlines() if l.strip() and "SerialNumber" not in l]
                serial_number = lines[0] if lines else None
            except Exception:
                serial_number = None
        elif os_name == "Linux":
            if os.path.exists("/sys/class/dmi/id/product_serial"):
                with open("/sys/class/dmi/id/product_serial") as f:
                    serial_number = f.read().strip()
            elif shutil.which("dmidecode"):
                out = subprocess.run(["sudo", "dmidecode", "-s", "system-serial-number"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                serial_number = out.stdout.strip().splitlines()[0]
        elif os_name == "Darwin":
            out = subprocess.run(["system_profiler", "SPHardwareDataType"], stdout=subprocess.PIPE, text=True)
            for line in out.stdout.splitlines():
                if "Serial Number" in line:
                    serial_number = line.split(":")[-1].strip()
                    break
    except Exception:
        serial_number = None
    print(f"Serial       : {serial_number or 'unavailable'}\n")

    # ----------- CPU ----------- #
    print("\U0001f9be  CPU")
    print("─" * 40)
    try:
        import psutil
        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else None
        print(f"Cores        : {cpu_count} (logical: {cpu_count_logical})")
        if cpu_freq:
            print(f"Frequency    : {cpu_freq:.1f} MHz")
    except Exception:
        print("psutil not available")
    try:
        # Model name
        if os_name == "Linux":
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        print(f"Model        : {line.split(':')[1].strip()}")
                        break
        elif os_name == "Windows":
            print(f"Model        : {platform.processor()}")
        elif os_name == "Darwin":
            out = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], stdout=subprocess.PIPE, text=True)
            print(f"Model        : {out.stdout.strip()}")
    except Exception:
        pass
    print()

    # ----------- Sensors / Temperatures ----------- #
    print("\U0001f321️  Sensors / Temperature")
    print("─" * 40)
    found_sensor = False
    try:
        import psutil
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                for chip, values in temps.items():
                    for entry in values:
                        print(f"{chip}: {entry.label or 'temp'} = {entry.current} °C")
                        found_sensor = True
        if not found_sensor:
            print("No temperature sensors found or supported.")
    except Exception:
        print("psutil not available or sensors not supported")
    print()

    # ----------- GPU ----------- #
    print("\U0001f5a5️  GPU")
    print("─" * 40)
    gpus = []
    try:
        if os_name == "Linux":
            out = subprocess.run(["lspci"], stdout=subprocess.PIPE, text=True)
            for line in out.stdout.splitlines():
                if "VGA compatible controller" in line or "3D controller" in line:
                    gpus.append(line.split(":")[-1].strip())
        elif os_name == "Windows":
            try:
                import wmi
                w = wmi.WMI()
                for gpu in w.Win32_VideoController():
                    gpus.append(gpu.Name)
            except ImportError:
                try:
                    out = subprocess.run(["wmic", "path", "win32_VideoController", "get", "name"], stdout=subprocess.PIPE, text=True)
                    gpus += [l.strip() for l in out.stdout.splitlines()[1:] if l.strip()]
                except Exception:
                    pass
        elif os_name == "Darwin":
            out = subprocess.run(["system_profiler", "SPDisplaysDataType"], stdout=subprocess.PIPE, text=True)
            for line in out.stdout.splitlines():
                if "Chipset Model" in line:
                    gpus.append(line.split(":")[-1].strip())
    except Exception:
        pass
    if gpus:
        for gpu in gpus:
            print(f"GPU          : {gpu}")
    else:
        print("GPU info     : unavailable")
    print()

    # ----------- Battery ----------- #
    print("\U0001faab️  Battery")
    print("─" * 40)
    try:
        import psutil
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()
            if battery is not None:
                print(f"Percent      : {battery.percent}%")
                print(f"Plugged in   : {'Yes' if battery.power_plugged else 'No'}")
                if hasattr(battery, "secsleft") and battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft != psutil.POWER_TIME_UNKNOWN:
                    import datetime
                    t = str(datetime.timedelta(seconds=battery.secsleft))
                    print(f"Time left    : {t}")
            else:
                print("No battery detected.")
        else:
            print("psutil (sensors_battery) not supported")
    except Exception:
        print("psutil not available or battery info not supported")
    print()

    # ----------- Bluetooth ----------- #
    print("\U0001f4e1  Bluetooth")
    print("─" * 40)
    found_bt = False
    try:
        if os_name == "Linux":
            out = subprocess.run(['bluetoothctl', 'show'], stdout=subprocess.PIPE, text=True)
            for line in out.stdout.splitlines():
                if "Powered" in line:
                    print(f"{line.strip()}")
                    found_bt = True
        elif os_name == "Windows":
            try:
                if shutil.which("powershell"):
                    out = subprocess.run(['powershell', '-Command', 'Get-PnpDevice -Class Bluetooth'], stdout=subprocess.PIPE, text=True)
                else:
                    out = subprocess.run(["cmd.exe", "/c", "powershell -Command \"Get-PnpDevice -Class Bluetooth\""], stdout=subprocess.PIPE, text=True)
                bt_devices = [l for l in out.stdout.splitlines() if l and not l.startswith("Status")]
                for line in bt_devices:
                    print(line)
                    found_bt = True
            except Exception:
                print("Bluetooth info unavailable")
        elif os_name == "Darwin":
            out = subprocess.run(['system_profiler', 'SPBluetoothDataType'], stdout=subprocess.PIPE, text=True)
            lines = [l for l in out.stdout.splitlines() if "Bluetooth" in l or "Connected" in l or "Manufacturer" in l]
            for line in lines:
                print(line)
                found_bt = True
        if not found_bt:
            print("No bluetooth devices/info detected.")
    except Exception:
        print("Bluetooth info unavailable")
    print()

    # ----------- Tools ----------- #
    print("\U0001f6e0  Tools")
    print("─" * 40)
    print(f"python3      : {shutil.which('python3') or 'not found'}")
    print(f"jq           : {shutil.which('jq') or 'not found'}")
    print(f"xlsx2csv     : {shutil.which('xlsx2csv') or 'not found'}\n")

    # ----------- Memory ----------- #
    print("\U0001f9e0  Memory")
    print("─" * 40)
    if os_name == "Linux":
        try:
            result = subprocess.run(["free", "-h"], stdout=subprocess.PIPE, text=True)
            print(result.stdout.strip())
        except FileNotFoundError:
            print("free command not available")
    elif os_name == "Darwin":
        try:
            mem = subprocess.run(["vm_stat"], stdout=subprocess.PIPE, text=True).stdout
            total = int(subprocess.run(["sysctl", "-n", "hw.memsize"], stdout=subprocess.PIPE, text=True).stdout) // (1024 * 1024)
            print(f"Total memory: {total} MB")
            print(mem.strip())
        except Exception:
            print("vm_stat/sysctl not available")
    elif os_name == "Windows":
        try:
            import psutil
            vm = psutil.virtual_memory()
            print(f"Total      : {vm.total // (1024*1024)} MB")
            print(f"Available  : {vm.available // (1024*1024)} MB")
            print(f"Used       : {vm.used // (1024*1024)} MB")
            print(f"Percent    : {vm.percent}%")
        except Exception:
            print("psutil not available")
    print()

    # ----------- Uptime & Load ----------- #
    print("\u23f1  Uptime & Load")
    print("─" * 40)
    if os_name in ["Linux", "Darwin"]:
        try:
            up1 = subprocess.run(["uptime", "-p"], stdout=subprocess.PIPE, text=True).stdout.strip()
            up2 = subprocess.run(["uptime"], stdout=subprocess.PIPE, text=True).stdout.strip()
            print(f"Uptime       : {up1}")
            if "load average" in up2:
                print("Load Avg.    :" + up2.split("load average:")[-1])
        except Exception:
            print("uptime command not available")
    elif os_name == "Windows":
        try:
            import psutil
            boot = psutil.boot_time()
            import datetime
            uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot)
            print(f"Uptime       : {str(uptime).split('.')[0]}")
            print("Load Avg.    : (not available on Windows)")
        except Exception:
            print("psutil not available")
    print()

    # ----------- Disks ----------- #
    print("\U0001f4bd  Disks")
    print("─" * 40)
    if os_name == "Linux":
        try:
            result = subprocess.run(["df", "-h", "-x", "tmpfs", "-x", "devtmpfs"], stdout=subprocess.PIPE, text=True)
            print(result.stdout.strip())
        except FileNotFoundError:
            print("df command not available")
    elif os_name == "Darwin":
        try:
            result = subprocess.run(["df", "-H"], stdout=subprocess.PIPE, text=True)
            print(result.stdout.strip())
        except Exception:
            print("df command not available")
    elif os_name == "Windows":
        try:
            import psutil
            for part in psutil.disk_partitions():
                usage = psutil.disk_usage(part.mountpoint)
                print(f"{part.device} - {usage.percent}% used ({usage.used // (1024*1024)} MB of {usage.total // (1024*1024)} MB)")
        except Exception:
            print("psutil not available")
    print()

    # ----------- Network ----------- #
    print("\U0001f310  Network")
    print("─" * 40)
    ip_local = ip_public = "unavailable"
    if os_name in ["Linux", "Darwin"]:
        try:
            ip_local = subprocess.run(["hostname", "-I"], stdout=subprocess.PIPE, text=True).stdout.strip().split()[0]
        except Exception:
            pass
    elif os_name == "Windows":
        try:
            ip_local = socket.gethostbyname(socket.gethostname())
        except Exception:
            pass
    try:
        import urllib.request
        ip_public = urllib.request.urlopen("https://ifconfig.me").read().decode().strip()
    except Exception:
        pass
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
    count = "unknown"
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
    except Exception:
        pass
    print(f"Pkg Manager  : {pkg_mgr}")
    print(f"Total pkgs   : {count}\n")

    # ----------- Printers ----------- #
    print("\U0001f5a8️  Printers")
    print("─" * 40)
    printers = []
    try:
        if os_name == "Windows":
            out = subprocess.run(['wmic', 'printer', 'get', 'name'], stdout=subprocess.PIPE, text=True)
            printers = [l.strip() for l in out.stdout.splitlines()[1:] if l.strip()]
        elif os_name == "Linux":
            out = subprocess.run(['lpstat', '-p'], stdout=subprocess.PIPE, text=True)
            printers = [line.split()[1] for line in out.stdout.splitlines() if line.startswith("printer ")]
        elif os_name == "Darwin":
            out = subprocess.run(['lpstat', '-p'], stdout=subprocess.PIPE, text=True)
            printers = [line.split()[1] for line in out.stdout.splitlines() if line.startswith("printer ")]
    except Exception:
        pass
    if printers:
        for p in printers:
            print(f"Printer      : {p}")
    else:
        print("No printers found.")
    print()

    # ----------- Wi-Fi Info ----------- #
    print("\U0001f4f6  Wi-Fi")
    print("─" * 40)
    try:
        ssid = None
        if os_name == "Windows":
            out = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE, text=True)
            for line in out.stdout.splitlines():
                if "SSID" in line and "BSSID" not in line:
                    ssid = line.split(":")[-1].strip()
                    break
        elif os_name == "Darwin":
            out = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], stdout=subprocess.PIPE, text=True)
            for line in out.stdout.splitlines():
                if " SSID" in line:
                    ssid = line.split(":")[-1].strip()
                    break
        elif os_name == "Linux":
            out = subprocess.run(['iwgetid', '-r'], stdout=subprocess.PIPE, text=True)
            ssid = out.stdout.strip() if out.returncode == 0 else None
        print(f"Connected SSID: {ssid or 'unavailable'}")
    except Exception:
        print("Wi-Fi info unavailable")
    print()

    # ----------- Display Info ----------- #
    print("\U0001f5b5️  Displays")
    print("─" * 40)
    try:
        if os_name == "Windows":
            import ctypes
            user32 = ctypes.windll.user32
            screens = user32.GetSystemMetrics(80)
            width = user32.GetSystemMetrics(0)
            height = user32.GetSystemMetrics(1)
            print(f"Main display: {width} x {height}")
            print(f"Number of screens: {screens or 1}")
        elif os_name == "Darwin":
            out = subprocess.run(['system_profiler', 'SPDisplaysDataType'], stdout=subprocess.PIPE, text=True)
            for line in out.stdout.splitlines():
                if "Resolution:" in line:
                    print(" ".join(line.split()))
        elif os_name == "Linux":
            try:
                out = subprocess.run(['xrandr'], stdout=subprocess.PIPE, text=True)
                for line in out.stdout.splitlines():
                    if " connected " in line:
                        print(line)
            except Exception:
                print("xrandr not available")
    except Exception:
        print("Display info unavailable")
    print()

def _print_help_md(lang: str = "eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/sys_summary/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
