🔐 **Tworzenie lub weryfikacja sum kontrolnych plików**

Ta komenda pozwala tworzyć lub weryfikować sumy kontrolne (hashy) dla plików w katalogu, używając popularnych algorytmów.

---

### 💡 Jak to działa

- Domyślnie generowana jest **lista hashy** dla pasujących plików
- Z przełącznikiem `--verify` możesz **zweryfikować pliki** względem listy
- Obsługiwane algorytmy: `sha256`, `sha1`, `md5`
- Możesz ograniczyć wyniki tylko do wybranego rozszerzenia (`--ext`)
- Przetwarzane są wszystkie pasujące pliki rekurencyjnie

---

### 🧠 Tryby działania

- Bez `--verify`: generowanie listy hashy (`*.sha256sum`, `*.md5sum`, itd.)
- Z `--verify`: sprawdzanie, czy pliki mają zgodne sumy z listy

---

### 🧪 Format listy

Każdy wiersz zawiera:
<hash> <ścieżka_do_pliku>

Listy te można archiwizować lub śledzić w kontroli wersji.

---

### 💡 Opcje

- `--path`: katalog główny (domyślnie bieżący)
- `--ext`: filtruj tylko po rozszerzeniu (np. `zip`, `exe`)
- `--algo`: algorytm (domyślnie: sha256)
- `--out`: plik wyjściowy z hashami lub lista do weryfikacji
- `--verify`: przełączenie w tryb weryfikacji

---

### 📦 Przykłady

Generowanie sum SHA-256 dla plików `.zip`:
shellman checksum_files --path ./dist --ext zip --algo sha256 --out builds.sha256sum

Weryfikacja plików z listy:
shellman checksum_files --verify --out builds.sha256sum

Tworzenie sum MD5 dla plików `.mp4`:
shellman checksum_files --ext mp4 --algo md5 --out videos.md5sum

Domyślne generowanie hashy dla wszystkich plików:
shellman checksum_files --out checksums.txt
