🔁 **Convert or Check Line Endings (LF ↔ CRLF)**

This tool helps you detect or convert line endings in files between Unix (LF) and Windows (CRLF) formats.

---

### 🧠 How It Works

- You can process a **single file** or **recursively scan a directory**
- Either **convert** line endings (`--to`) or **check** their type (`--check`)
- Supports filtering by file extension with `--ext`

---

### 💡 Options Explained

- `--file`: process one specific file
- `--dir`: scan all files in a directory (and subdirectories)
- `--ext`: optional extension filter, used with `--dir`
- `--to`: convert to either `lf` or `crlf`
- `--check`: check current line ending type (no conversion)

---

### 🧪 Line Ending Types

- `LF`: Unix-style (Linux/macOS)
- `CRLF`: Windows-style
- `MIXED`: file contains both LF and CRLF
- `NONE`: no line endings found
- `ERROR`: file could not be read

---

### 📦 Examples

Convert a `.sh` file to LF endings:
shellman line_endings --file script.sh --to lf

Convert all `.txt` files in a directory to CRLF:
shellman line_endings --dir src --ext txt --to crlf

Just check line endings in `.py` files:
shellman line_endings --dir src --ext py --check

Check a single file:
shellman line_endings --file README.md --check
