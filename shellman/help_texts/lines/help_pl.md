📏 **lines – Wyciąganie, liczenie, podsumowania linii**

Wyciągaj linie z kontekstem, licz dopasowania lub podsumuj statystyki linii w plikach i folderach.
Filtruj po tekście, regexie, negacji, rozszerzeniu.
Wszystko w jednej komendzie!

---

### 🔧 Opcje

| opcja            | opis |
|------------------|------|
| `--extract`      | Wypisz pasujące linie (domyślnie) |
| `--count`        | Tylko liczba dopasowań na plik |
| `--summary`      | Podsumowanie dla wszystkich plików |
| `--contains TEKST` | Linia musi zawierać ten tekst |
| `--not-contains TEKST` | Linia NIE może zawierać tekstu |
| `--regex WZORZEC`| Dopasuj linie wyrażeniem regularnym (nie łączyć z `--contains`) |
| `--ignore-case`  | Wielkość liter bez znaczenia |
| `--before N`     | N linii kontekstu przed |
| `--after N`      | N linii kontekstu po |
| `--ext EXT`      | Tylko pliki o podanym rozszerzeniu |
| `--percent`      | Pokaż procent dopasowań |
| `--show-size`    | Pokaż rozmiar pliku |
| `--output PLIK`  | Zapisz wynik do pliku |
| `--interactive`  | Wyświetl wynik w pagerze (`less`) |
| `--lang-help pl/eng` | Pokaż pomoc po polsku / angielsku |

---

### 📦 Przykłady

Wypisz linie z błędem i ±2 linie kontekstu:
shellman lines log.txt --contains error --before 2 --after 2

Policz linie z TODO/FIXME w plikach .py:
shellman lines . --ext py --regex "TODO|FIXME" --count

Pokaż procent dopasowań i podsumowanie:
shellman lines src/ --contains "def " --count --percent --summary
