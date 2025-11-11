
# 🐚 Shellman

**Shellman** is your friendly CLI assistant – a curated toolbox for working with files, data and your system.

---

## 🔧 Installation

### 1 · Clone the repository

```bash
git clone https://github.com/Shellman-Project/shellman.git
cd shellman
```

### 2 · Installation

A virtual-env is recommended:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
pip install .
```

Using Poetry instead?

```bash
poetry install
```

### 2 · Install Shellman in editable / dev mode

```bash
pip install -e .
```
(Any code or help-file change is picked up instantly – re-install only if you rename/move modules.)

## Usage

List all commands:

```bash
shellman --help
```

Every command supports multi-language help via:

```bash
shellman <command> --lang-help eng       # English help
shellman <command> --lang-help pl        # Polish help
```

Example:

```bash
shellman lines README.md --count --show-size --contains shellman/com --extract --before 2 --after 2 --percent

==> README.md <==
88:
89:Pull-requests and feature ideas are welcome!
90:Each command lives in shellman/commands/ – feel free to add your own tool.
91:
92:########################################################################################
--------------------
182:
183:Masz pomysł lub poprawkę? Zgłoś pull-request lub otwórz issue.
184:Każde narzędzie znajduje się w shellman/commands/ – śmiało dodaj własne!
185:

==> README.md <==
Matching lines: 2
Match percentage: 1.08%
File size: 5.31 KB
```
## 📦 Available commands (short list)

command	short description:

| Command| Purpose| Quick example|
|-----------------|--------------------------------------|---------------------------------------------|
| excel | Excel utilities: info / preview / export | shellman excel info data.xlsx |
| find_files      | Locate files by name, content or extension  | `shellman find_files ./src --name util` |
| change_line_end | LF ↔ CRLF conversion / check                | `shellman change_line_end file.txt`     |
| checksum_files  | Create or verify checksums (sha256, md5, sha1)   | `shellman checksum_files ./downloads`   |
| clean_files     | Delete junk files by name, ext or age   | `shellman clean_files ./tmp --ext log`  |
| count_lines     | Count lines in files                                                    | `shellman count_lines ./src`            |
| extract_lines   | Extract or summarize lines with filters and context                     | `shellman extract_lines ./src --contains TODO` |
| csv_extract     | Extract columns/rows from CSV                                           | `shellman csv_extract data.csv --cols 1,3` |
| date_utils      | Add/subtract dates, diff, strftime                                      | `shellman date_utils --add 5d`          |
| encrypt_files   | AES-256 encrypt / decrypt with password                                 | `shellman encrypt_files secret.txt`     |
| file_convert    | Convert between JSON, YAML, TOML                                        | `shellman file_convert config.toml json`|
| file_stats      | Show path, size, line-count, extension                                  | `shellman file_stats ./src`             |
| json_extract    | JSON path, filter and field selection                                   | `shellman json_extract data.json --path user.name` |
| merge_files     | Merge multiple text files into one                                      | `shellman merge_files ./logs -o merged.txt` |
| replace_text    | Batch find-&-replace with diff preview                                  | `shellman replace_text ./docs --find old --replace new --preview` |
| sys_summary     | System / shell / resource report                                        | `shellman sys_summary`                  |
| zip       | Bulk ZIP creation (per-folder or flat)                          | `shellman zip pack example_folder -pass example_password`         |
| open_ports      | Show currently open TCP/UDP ports (process, pid, address, state)| `shellman open_ports`                   |
| speed_test      | Run a quick internet speed test (download, upload, ping)        | `shellman speed_test`                   |
| dir_tree        | Prints a visual tree of directories (like `tree`)               | `shellman dir_tree ./src -f -d 2`       |


