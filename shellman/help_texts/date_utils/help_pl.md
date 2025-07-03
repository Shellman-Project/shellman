🗓️ **Narzędzia dat – dodawanie, odejmowanie, porównywanie i formatowanie dat**

To narzędzie pozwala w prosty sposób operować na datach i godzinach w terminalu.

---

### 💡 Co potrafi

- Dodawaj lub odejmuj czas od daty (lub teraz)
- Porównuj dwie daty i zobacz różnicę
- Formatuj datę zgodnie ze wzorcem `strftime`

---

### 🧠 Format czasu trwania

Możesz używać:

- `d` → dni
- `w` → tygodnie
- `m` → miesiące
- `y` → lata
- `q` → kwartały (czyli 3 miesiące)
- `h` → godziny
- `min` → minuty
- `s` → sekundy

---

### ⌚ Akceptowane formaty dat

- `YYYY-MM-DD`
- `YYYY-MM-DD HH:MM[:SS]`

---

### 🔧 Opcje

- `--date`: data bazowa (domyślnie: teraz)
- `--add`: dodaj czas (np. `5d`, `3h`, `2m`)
- `--sub`: odejmij czas
- `--diff`: porównaj dwie daty
- `--format`: sformatuj wynik według wzorca `strftime`

---

### 📦 Przykłady

Dodaj 5 dni do aktualnej daty:
shellman date_utils --add 5d

Odejmij 2 godziny od konkretnej daty:
shellman date_utils --date "2024-12-01 13:00" --sub 2h

Porównaj dwie daty:
shellman date_utils --date "2024-01-01" --diff "2025-04-18 09:15:00"

Sformatuj datę:
shellman date_utils --date "2025-01-01" --format "%A, %d %B %Y, %H:%M"
