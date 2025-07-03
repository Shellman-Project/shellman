🔍 **Wyszukiwanie plików**

Ta komenda umożliwia rekurencyjne przeszukiwanie katalogów na podstawie:

- Fragmentu **nazwy pliku**
- Rozszerzenia **pliku**
- Zawartości tekstowej **wewnątrz pliku**
- Z opcjonalnym zapisem do pliku logu i wyświetlaniem rozmiarów plików

---

### 🧠 Jak to działa

- Komenda przeszukuje wszystkie podfoldery począwszy od `SEARCH_PATH`
- Pliki są filtrowane według podanych opcji (`--name`, `--ext`, `--content`)
- Pasujące pliki są wyświetlane w terminalu
- Jeśli podano `--output`, wyniki zapisywane są do `logs/find_files_<timestamp>.log`
- Jeśli podano `--show-size`, obok ścieżki pojawi się rozmiar pliku (MB)

---

### 💡 Wyjaśnienie opcji

- `--name`: pasuje do każdego pliku, którego nazwa zawiera ten fragment (z uwzględnieniem wielkości liter)
- `--ext`: ogranicza do plików z podanym rozszerzeniem (np. `md`, `py`)
- `--content`: filtruje tylko te pliki, które zawierają dany tekst
- `--output`: zapisuje wyniki do pliku logu z datą i godziną
- `--show-size`: pokazuje rozmiar pliku obok każdej ścieżki

---

### 📦 Przykłady

Szukaj wszystkich plików zawierających `"log"` w nazwie:
shellman find_files . --name log

Szukaj plików Markdown w katalogu `./docs` zawierających "error 404":
shellman find_files ./docs --content "error 404" --ext md

Szukaj plików `util*.py` i pokazuj ich rozmiary:
shellman find_files ./src --name util --ext py --show-size

Zapisz wyniki do pliku logu:
shellman find_files ./src --name helper --output

Połącz wszystkie filtry dla dokładnego wyszukiwania:
shellman find_files ./data --name report --content "Suma" --ext txt --show-size --output
