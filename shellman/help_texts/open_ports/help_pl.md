🔌 **open_ports – Lista aktywnych portów TCP/UDP**

Wyświetla aktualnie otwarte porty wraz z nazwą procesu i PID.  
Działa na każdym systemie dzięki bibliotece `psutil` (instaluje się automatycznie przy pierwszym uruchomieniu).

---

### 🔧 Opcje

| opcja | opis |
|-------|------|
| `--proto tcp/udp` | Filtruj po protokole |
| `--port N`        | Filtruj po numerze portu |
| `--json`          | Zwróć surowy JSON |
| `--lang-help`     | Pokaż pomoc (`pl` / `eng`) |

---

### 📦 Przykłady

Wszystkie otwarte porty:
shellman open_ports

Tylko UDP na porcie 53:
shellman open_ports --proto udp --port 53

JSON do dalszego przetwarzania:
shellman open_ports --json

---

Po dodaniu plików i reinstalacji w trybie editable:
shellman open_ports
shellman open_ports --lang-help pl
