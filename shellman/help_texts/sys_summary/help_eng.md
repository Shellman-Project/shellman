🖥️ **sys_summary – System & Environment Summary**

Print a concise overview of your operating-system, shell, key CLI tools and resource usage.

---

### 🔧 Options

| option | description |
|--------|-------------|
| `--lang-help pl/eng` | Show this help in Polish / English |

*(all other information is auto-detected; no further flags needed).*

---

### 🗂️ What’s Included

* OS name, version, architecture, distribution  
* Detects WSL / hostname  
* Current shell and version (Bash version if applicable)  
* Presence of common CLI tools (`python3`, `jq`, `xlsx2csv`)  
* Memory overview (`free -h`)  
* Uptime and load average  
* Disk usage (`df -h`) minus tmpfs/devtmpfs  
* Local & public IP addresses  
* Package-manager type and total installed packages

---

### 📦 Example

shellman sys_summary
Sample output (truncated):

📋  System Summary
────────────────────────────────
🖥️  OS & Host
────────────────────────────────
System       : Linux
Distro       : Ubuntu 22.04
Version      : 6.5.0-28-generic
Architecture : x86_64
WSL          : No
Hostname     : devbox
