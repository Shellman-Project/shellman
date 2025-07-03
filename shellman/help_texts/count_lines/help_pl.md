📏 **Liczenie linii w plikach lub folderach**

Ta komenda umożliwia zliczanie linii w jednym lub wielu plikach.  
Możesz filtrować wyniki według treści, wyrażeń regularnych, rozszerzeń oraz wyświetlać podsumowania.

---

### 💡 Opis opcji

- `--contains TEKST`: zlicza tylko linie zawierające podany ciąg znaków
- `--regex WZORZEC`: zlicza linie pasujące do wyrażenia regularnego
- `--ignore-case`: ignoruje wielkość liter przy dopasowaniu
- `--ext EXT`: filtruj pliki po rozszerzeniu (np. `py`, `log`)
- `--summary`: pokaż podsumowanie dla każdego pliku i ogólne
- `--percent`: pokaż procent dopasowanych linii
- `--show-size`: wyświetl rozmiar pliku w MB
- `--output`: zapisz wyniki do pliku w folderze `logs/`
- `--interactive`: pokaż wyniki interaktywnie (np. przez `less`)

---

### 📦 Przykłady

Zlicz wszystkie linie w plikach `.py`:
shellman count_lines . --ext py

Zlicz linie zawierające `error` (niewrażliwie na wielkość liter):
shellman count_lines logs --contains error --ignore-case

Zlicz linie pasujące do "TODO" lub "FIXME":
shellman count_lines . --regex "TODO|FIXME" --summary --percent

Zapisz wynik do pliku:
shellman count_lines . --contains error --output

Wyświetl wynik interaktywnie:
shellman count_lines . --regex "import" --interactive
