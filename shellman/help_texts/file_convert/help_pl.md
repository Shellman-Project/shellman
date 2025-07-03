🔄 **file_convert – Konwersja między JSON, YAML a TOML**

Konwertuj pliki konfiguracyjne pomiędzy wspieranymi formatami tekstowymi.

---

### 🔧 Opcje

| opcja | wymagane | opis |
|-------|----------|------|
| `--from json|yaml|toml` | ✔ | Format wejściowy |
| `--to   json|yaml|toml` | ✔ | Format wyjściowy |
| `--output PLIK` | ✗ | Zapisz wynik do pliku zamiast na ekran |
| `--pretty` | ✗ | Czytelny zapis (wcięcia / Unicode) tam, gdzie obsługiwane |
| `--interactive` | ✗ | Wyświetl wynik w `less -S` (pomijane przy `--output`) |
| `--lang-help pl/eng` | ✗ | Pokaż tę pomoc po PL / ENG |

---

### 📦 Przykłady

Konwersja JSON → YAML na wyjście standardowe:

shellman file_convert config.json --from json --to yaml
TOML → JSON z zapisem do pliku:
shellman file_convert settings.toml --from toml --to json --pretty --output settings.json
