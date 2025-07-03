🔎 **json_extract – Filtrowanie i wybór danych JSON**

Wyciąga fragment dokumentu JSON, z opcjonalnym filtrem `klucz=wartość` i listą pól do wyświetlenia.

---

### 🔧 Opcje

| opcja | opis |
|-------|------|
| `--path klucz.sciezka` | Przejdź do zagnieżdżonej listy/obiektu |
| `--filter k=v` | Zostaw obiekty, w których `k` = `v` (porównanie tekstowe) |
| `--fields a,b,c` | Lista pól do wypisania |
| `--output PLIK`  | Zapisz wynik do pliku |
| `--interactive`  | Wyświetl w `less -S` (pomijane przy `--output`) |
| `--lang-help`    | Pokaż pomoc (`pl` / `eng`) |

---

### 📦 Przykłady

Lista `items`, filtr `status=ERROR`, tylko pola `id,msg`, zapis do pliku:

shellman json_extract dane.json --path items --filter status=ERROR --fields id,msg --output bledy.json

Wyświetl obiekty z root.users interaktywnie:
shellman json_extract users.json --path root.users --interactive