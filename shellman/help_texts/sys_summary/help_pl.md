🖥️ **sys_summary – Podsumowanie systemu i środowiska**

Wyświetla zwięzły raport o systemie operacyjnym, powłoce, kluczowych narzędziach i zasobach.

---

### 🔧 Opcje

| opcja | opis |
|-------|------|
| `--lang-help pl/eng` | Pokaż tę pomoc po polsku / angielsku |

*(pozostałe dane zbierane są automatycznie – brak dodatkowych flag).*

---

### 🗂️ Zawartość raportu

* Nazwa systemu, wersja, architektura, dystrybucja  
* Wykrywanie WSL / nazwa hosta  
* Aktualna powłoka i jej wersja (wersja Bash, jeśli dotyczy)  
* Obecność popularnych narzędzi CLI (`python3`, `jq`, `xlsx2csv`)  
* Pamięć (`free -h`)  
* Czas działania i średnie obciążenie  
* Użycie dysków (`df -h`) bez tmpfs/devtmpfs  
* Lokalny i publiczny adres IP  
* Rodzaj menedżera pakietów oraz liczba zainstalowanych paczek

---

### 📦 Przykład

shellman sys_summary
Przykładowy fragment wyniku:

📋  System Summary
────────────────────────────────
🖥️  OS & Host
────────────────────────────────
System       : Linux
Distro       : Ubuntu 22.04
Wersja       : 6.5.0-28-generic
Architektura : x86_64
WSL          : Nie
Hostname     : devbox
