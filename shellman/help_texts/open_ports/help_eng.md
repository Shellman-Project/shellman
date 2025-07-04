🔌 **open_ports – List Active TCP/UDP and Serial Ports**

Show which local TCP/UDP ports are currently open (with process/PID/state),  
**plus (optionally) all physical serial/parallel ports** (COM, LPT, tty, cu).

---

### 🔧 Options

| option         | description |
|----------------|-------------|
| `--proto tcp/udp` | Filter by protocol |
| `--port N`        | Filter by local port number |
| `--json`          | Output raw JSON (TCP/UDP only) |
| `--serial`        | List serial/parallel ports (COMx, LPTx, ttyUSB, ttyACM, cu.* etc.) |
| `--lang-help`     | Show help (`pl` / `eng`) |

---

### 📦 Examples

All open network ports:
shellman open_ports

All serial and parallel ports:
shellman open_ports --serial

Only UDP on port 53:
shellman open_ports --proto udp --port 53

Requires pyserial for best serial port detection (on Windows).
