✂️ **extract_lines – Wybieranie linii z pliku tekstowego**

Wypisz linie, które **zawierają** lub **NIE zawierają** danego tekstu, z opcjonalnym kontekstem wierszy przed i po.

---

### 🔧 Opcje

| opcja | domyślnie | opis |
|-------|-----------|------|
| `--contains TEKST` | — | Zachowaj linie zawierające `TEKST` |
| `--not-contains TEKST` | — | Zachowaj linie, które **NIE** zawierają `TEKST` |
| `--before N` | `0` | Pokaż *N* wierszy **przed** każdym dopasowaniem |
| `--after N`  | `0` | Pokaż *N* wierszy **po** każdym dopasowaniu |
| `--output PLIK` | — | Zapisz wynik do pliku zamiast drukować |
| `--lang-help pl/eng` | — | Pokaż tę pomoc po polsku / angielsku |

> Trzeba podać **tylko jedną** z opcji `--contains` lub `--not-contains`.

Każda linia w wyniku ma numer (1-indeksowany), np. `42:Tekst linii`.

---

### 📦 Przykłady

Wypisz linie z „ERROR” i 2 wiersze przed oraz 3 po:
shellman extract_lines sys.log --contains ERROR --before 2 --after 3

Usuń linie z „TODO” i zapisz wynik:
shellman extract_lines notatki.txt --not-contains TODO --output czyste.txt
