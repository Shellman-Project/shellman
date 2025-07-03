🧹 **Czyszczenie plików – Usuń po nazwie, rozszerzeniu lub wieku**

Ta komenda pozwala usunąć pliki z drzewa katalogów na podstawie:

- Rozszerzenia pliku (np. `.log`, `.tmp`)
- Fragmentu nazwy (np. `~`, `backup`)
- Daty modyfikacji (np. starsze niż 7 dni)
- Z opcjonalnym potwierdzeniem i trybem podglądu (dry-run)

---

### 💡 Opis opcji

- `--path`: katalog bazowy (domyślnie `.`)
- `--ext`: usuwa pliki z podanym rozszerzeniem
- `--name`: usuwa pliki zawierające fragment w nazwie
- `--older-than`: tylko pliki starsze niż N dni
- `--dry-run`: tylko wyświetl pliki do usunięcia, bez kasowania
- `--confirm`: zapytaj przed usunięciem każdego pliku

---

### ⚠️ Wskazówki bezpieczeństwa

- Zawsze użyj `--dry-run` przed faktycznym usunięciem
- Łącz `--ext`, `--name` i `--older-than`, aby zawęzić wyniki
- `--confirm` zapewnia interaktywne potwierdzenie (Y/n)

---

### 📦 Przykłady

Symulacja usunięcia plików `.tmp` starszych niż 7 dni:
shellman clean_files --ext tmp --older-than 7 --dry-run

Usuń pliki z `~` w nazwie w katalogu `./build`:
shellman clean_files --path ./build --name '~' --confirm

Usuń pliki `.log` starsze niż 30 dni:
shellman clean_files --ext log --older-than 30

Usuń tylko pliki z `backup` w nazwie:
shellman clean_files --name backup

Usuń pliki `.bak` z potwierdzeniem:
shellman clean_files --ext bak --confirm
