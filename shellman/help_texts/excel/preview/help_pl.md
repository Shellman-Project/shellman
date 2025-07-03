🔍 **excel preview – Szybki podgląd arkusza**

Pokazuje pierwsze *N* wierszy i wybrane kolumny z arkusza.

### 🔧 Opcje

| opcja | domyślnie | opis |
|-------|-----------|------|
| `--sheet`    | `1`   | Nazwa lub numer arkusza (licząc od 1) |
| `--rows N`   | `20`  | Ile wierszy pokazać |
| `--columns`  | ―    | Litery kolumn, np. `A,C-E` |
| `--output`   | ―    | Zapisz podgląd do pliku CSV |
| `--interactive` | ✗ | Wyświetl w pagerze (`less -S`) |

### 📦 Przykłady
shellman excel preview plik.xlsx --rows 10 --columns A,B
shellman excel preview plik.xlsx --sheet Sheet2 --interactive
shellman excel preview plik.xlsx --output podglad.csv
