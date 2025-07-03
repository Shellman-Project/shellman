📄 **CSV Extract – Wybierz kolumny i wiersze z pliku CSV**

To narzędzie umożliwia wyodrębnienie konkretnych kolumn i/lub wierszy z pliku CSV.

---

### 💡 Jak to działa

- Kolumny wybierasz po numerze (od 1): np. `1,2,5` lub `2-4`
- Wiersze możesz filtrować na podstawie:
  - numerów (po pominięciu nagłówka)
  - obecności konkretnego tekstu
  - braku konkretnego tekstu
- Możesz pominąć nagłówek (`--skip-header`)
- Wynik można wypisać, zapisać lub wyświetlić interaktywnie

---

### 🔍 Opcje

- `--cols`: wymagane; które kolumny wyodrębnić (np. `1,3` lub `2-4`)
- `--rows`: które wiersze wyodrębnić (np. `2-10`)
- `--contains`: tylko wiersze zawierające tekst
- `--not-contains`: pomiń wiersze zawierające tekst
- `--delim`: separator CSV (domyślnie: `,`)
- `--skip-header`: pomiń pierwszy wiersz
- `--output`: zapisz wynik do pliku
- `--interactive`: pokaż wynik interaktywnie (np. przez `less`)

---

### 📦 Przykłady

Wyciągnij kolumny 1 i 4 z wierszy 2–100, pomiń nagłówek:
shellman csv_extract data.csv --cols 1,4 --rows 2-100 --skip-header

Wyciągnij tylko wiersze zawierające "ERROR" i zapisz do pliku:
shellman csv_extract logs.csv --cols 1,2 --contains ERROR --output errors.csv

Pomiń wiersze z "DEBUG":
shellman csv_extract logs.csv --cols 1,3 --not-contains DEBUG

Wyświetl wynik w trybie interaktywnym:
shellman csv_extract data.csv --cols 1,2 --interactive
