🔐 **Szyfrowanie lub deszyfrowanie plików za pomocą AES-256**

Ta komenda pozwala na bezpieczne szyfrowanie lub odszyfrowywanie wielu plików w katalogu, z wykorzystaniem hasła i algorytmu AES-256.

---

### 🧠 Jak to działa

- Używa AES-256 w trybie CBC z hasłem (PBKDF2)
- Każdy plik jest szyfrowany osobno
- Plik wynikowy zawiera salt + IV + szyfrogram w jednym `.enc` pliku
- Wyniki są zapisywane do wskazanego katalogu

---

### 🔧 Opcje

- `--mode encrypt|decrypt`: tryb działania (szyfrowanie lub deszyfrowanie)
- `--password`: hasło do wygenerowania klucza szyfrującego
- `--ext`: przetwarzaj tylko pliki z podanym rozszerzeniem
- `--path`: katalog z plikami (domyślnie bieżący)
- `--out`: katalog docelowy (domyślnie `encrypted` lub `decrypted`)

---

### ⚠️ Uwagi

- Bezpieczeństwo zależy od siły hasła
- Te same pliki odszyfrujesz tylko tym samym hasłem
- Nazwy plików są zachowane – w trybie `encrypt` dodawane jest `.enc`

---

### 📦 Przykłady

Zaszyfruj pliki `.log` z katalogu `logs/` do `secure/`:
shellman encrypt_files --mode encrypt --password mypass --ext log --path ./logs --out ./secure

Odszyfruj pliki `.enc` i zapisz je do `plain/`:
shellman encrypt_files --mode decrypt --password mypass --ext enc --path ./secure --out ./plain
