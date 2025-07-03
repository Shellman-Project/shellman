✂️ **extract_lines – Select Lines from a Text File**

Extract lines that **do** or **do NOT** contain a given substring, with optional surrounding context.

---

### 🔧 Options

| option | default | description |
|--------|---------|-------------|
| `--contains TEXT` | — | Keep only lines that include `TEXT` |
| `--not-contains TEXT` | — | Keep only lines that **do NOT** include `TEXT` |
| `--before N` | `0` | Show *N* lines **before** every match |
| `--after N`  | `0` | Show *N* lines **after** every match |
| `--output FILE` | — | Save result to a file instead of printing |
| `--lang-help pl/eng` | — | Show this help in Polish / English |

> Use **either** `--contains` **or** `--not-contains` (mandatory).

Lines are prefixed with their 1-based line-number, e.g. `42:Some text`.

---

### 📦 Examples

Keep lines containing “ERROR” plus 2 lines before and 3 after:
shellman extract_lines sys.log --contains ERROR --before 2 --after 3

Remove lines that contain “TODO” and save result:
shellman extract_lines notes.txt --not-contains TODO --output clean.txt
