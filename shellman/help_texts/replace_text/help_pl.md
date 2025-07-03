✏️ **replace_text – Hurtowa zamiana tekstu w plikach**

Przeszukuje drzewo katalogów i podmienia tekst w pasujących plikach. Można użyć podglądu i potwierdzania.

---

### 🔧 Opcje

| opcja | wymagane | opis |
|-------|----------|------|
| `--find TEKST`    | ✔ | Tekst do znalezienia |
| `--replace TEKST` | ✔ | Tekst zamienny |
| `--ext EXT`       | ✗ | Tylko pliki z rozszerzeniem `EXT` |
| `--in-place`      | ✗ | Zapisz zmiany na dysk |
| `--preview`       | ✗ | Pokaż diff przed zmianą |
| `--confirm`       | ✗ | Pytaj przed zmianą każdego pliku (`--in-place`) |
| `--lang-help`     | ✗ | Pokaż pomoc (`pl` / `eng`) |

---

### 📦 Przykład

Podgląd zmian we wszystkich `.md` w `docs/`:

shellman replace_text ./docs --find old --replace new --ext md --preview

Zamiana „TODO” na „DONE” w .py z potwierdzeniem:
shellman replace_text src --find TODO --replace DONE --ext py --in-place --confirm
