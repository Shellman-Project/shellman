🔁 **Konwersja lub sprawdzanie zakończeń linii (LF ↔ CRLF)**

To narzędzie umożliwia wykrywanie lub konwersję zakończeń linii w plikach pomiędzy formatami Unix (LF) i Windows (CRLF).

---

### 🧠 Jak to działa

- Możesz przetwarzać **pojedynczy plik** lub **rekurencyjnie cały katalog**
- Do wyboru: **konwersja** (`--to`) albo **sprawdzenie** zakończeń (`--check`)
- Możliwe jest filtrowanie po rozszerzeniu plików (`--ext`)

---

### 💡 Opis opcji

- `--file`: ścieżka do pojedynczego pliku
- `--dir`: katalog, w którym szukamy plików (rekurencyjnie)
- `--ext`: opcjonalne rozszerzenie plików (używane z `--dir`)
- `--to`: konwersja zakończeń linii (`lf` lub `crlf`)
- `--check`: tylko sprawdzanie rodzaju zakończeń (bez modyfikacji)

---

### 🧪 Typy zakończeń

- `LF`: styl Unix (Linux/macOS)
- `CRLF`: styl Windows
- `MIXED`: plik zawiera oba typy zakończeń
- `NONE`: brak zakończeń linii
- `ERROR`: nie udało się odczytać pliku

---

### 📦 Przykłady

Konwersja pliku `.sh` na zakończenia LF:
shellman line_endings --file script.sh --to lf

Konwersja wszystkich `.txt` w katalogu na CRLF:
shellman line_endings --dir src --ext txt --to crlf

Sprawdzenie zakończeń w plikach `.py`:
shellman line_endings --dir src --ext py --check

Sprawdzenie pojedynczego pliku:
shellman line_endings --file README.md --check
