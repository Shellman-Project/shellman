🔌 **open_ports – Lista aktywnych portów TCP/UDP i portów szeregowych**

Wyświetla otwarte porty TCP/UDP (proces, PID, stan),  
**a dodatkowo (na żądanie) wszystkie fizyczne porty szeregowe i równoległe** (COM, LPT, tty, cu).

---

### 🔧 Opcje

| opcja           | opis |
|-----------------|------|
| `--proto tcp/udp` | Filtruj po protokole |
| `--port N`        | Filtruj po porcie lokalnym |
| `--json`          | Surowy JSON (tylko TCP/UDP) |
| `--serial`        | Wypisz porty szeregowe/równoległe (COMx, LPTx, ttyUSB, ttyACM, cu.* itp.) |
| `--lang-help`     | Pokaż pomoc (pl / eng) |

---

### 📦 Przykłady

Wszystkie otwarte porty sieciowe:
shellman open_ports

Wszystkie porty szeregowe i równoległe:
shellman open_ports --serial

Tylko UDP na porcie 53:
shellman open_ports --proto udp --port 53

Wymaga pyserial do najlepszej detekcji portów (Windows).
