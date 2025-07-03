📊 **file_stats – Szybkie statystyki plików**

Wyświetla pełną ścieżkę, liczbę linii, rozmiar i rozszerzenie każdego pliku.

---

### 🔧 Opcje

| opcja | opis |
|-------|------|
| `--ext EXT` | Uwzględnij tylko pliki z rozszerzeniem `EXT` |
| `--output`  | Zapisz wynik do `logs/file_stats_<timestamp>.log` |
| `--lang-help pl/eng` | Pokaż tę pomoc po PL / ENG |

---

### 📦 Przykłady

Statystyki pojedynczego pliku:
shellman file_stats plik.txt

Statystyki wszystkich plików .py w src/ z logiem:
shellman file_stats ./src --ext py --output
