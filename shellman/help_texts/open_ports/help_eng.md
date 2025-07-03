🔌 **open_ports – List Active TCP/UDP Ports**

Show which local ports are currently open and which process owns them.  
Works cross-platform via the pure-python `psutil` library (auto-installed on first run).

---

### 🔧 Options

| option | description |
|--------|-------------|
| `--proto tcp/udp` | Filter by protocol |
| `--port N`        | Filter by local port number |
| `--json`          | Output raw JSON |
| `--lang-help`     | Show help (`pl` / `eng`) |

---

### 📦 Examples

All sockets:
shellman open_ports

Only UDP sockets on port 53:
shellman open_ports --proto udp --port 53

Machine-readable JSON:
shellman open_ports --json

