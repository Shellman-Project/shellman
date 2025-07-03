✏️ **replace_text – Batch Find & Replace**

Search through a directory tree and replace text in matching files, with optional preview and confirmation.

---

### 🔧 Options

| option | required | description |
|--------|----------|-------------|
| `--find TEXT`    | ✔ | Text to search for |
| `--replace TEXT` | ✔ | Replacement text |
| `--ext EXT`      | ✗ | Only files with extension `EXT` |
| `--in-place`     | ✗ | Write changes back to disk (otherwise read-only) |
| `--preview`      | ✗ | Show unified diff preview |
| `--confirm`      | ✗ | Ask before modifying each file (only with `--in-place`) |
| `--lang-help`    | ✗ | Show this help (`pl` / `eng`) |

---

### 📦 Example

Preview replacements in all `.md` files under `docs/`:

shellman replace_text ./docs --find old --replace new --ext md --preview

Perform replacements with confirmation:
shellman replace_text src --find TODO --replace DONE --ext py --in-place --confirm
