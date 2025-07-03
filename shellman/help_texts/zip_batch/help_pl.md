📦 **zip_batch – Hurtowe tworzenie ZIP-ów**

Tworzy archiwa ZIP z wielu plików lub osobne archiwum dla każdego podkatalogu.

---

### 🔧 Opcje

| opcja | opis |
|-------|------|
| `--path DIR`     | Katalog źródłowy (domyślnie `.`) |
| `--ext EXT`      | Tylko pliki z rozszerzeniem `EXT` |
| `--per-folder`   | Jedno archiwum na każdy podkatalog |
| `--output DIR`   | Katalog docelowy (domyślnie `./zips`) |
| `--name PREFIKS` | Prefiks nazwy (`batch_` domyślnie) |
| `--password HASŁO` | Hasło do zip (`zip -P`; słabe szyfrowanie) |
| `--lang-help`    | Pokaż pomoc (`pl` / `eng`) |

---

### 📦 Przykłady

Osobny ZIP dla każdego podkatalogu:

shellman zip_batch --path ./projekty --per-folder

Jedno archiwum ze wszystkimi plikami .txt:
shellman zip_batch --ext txt --name teksty_ --output archiwa
