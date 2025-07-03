📤 **excel export – Zapis arkuszy lub zakresów do CSV**

Eksportuje wybrane arkusze (lub tylko określone wiersze / kolumny) do osobnych plików CSV.

### 🔧 Opcje

| opcja | domyślnie | opis |
|-------|-----------|------|
| `--sheets`   | wszystkie | Nazwy lub numery arkuszy (oddzielone spacją) |
| `--rows`     | ―        | Zakres wierszy `start-koniec`, np. `2-100` |
| `--columns`  | ―        | Litery kolumn `A,B-D` |
| `--out DIR`  | `csv`    | Katalog wyjściowy |
| `--overwrite`| ✗        | Nadpisuj pliki CSV (bez znacznika czasu) |

### 📦 Przykład
shellman excel export plik.xlsx --sheets 1 2 --rows 5-30 --out ./wyniki --overwrite

Utworzy `wyniki/Sheet1.csv` i `wyniki/Sheet2.csv`
