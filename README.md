
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
| zip_batch       | Bulk ZIP creation (per-folder or flat)                          | `shellman zip_batch ./projects`         |
| open_ports      | Show currently open TCP/UDP ports (process, pid, address, state)| `shellman open_ports`                   |
| speed_test      | Run a quick internet speed test (download, upload, ping)        | `shellman speed_test`                   |
| dir_tree        | Prints a visual tree of directories (like `tree`)               | `shellman dir_tree ./src -f -d 2`       |



Plus a few helpers: checksum_files, date_utils, etc. Run --help on any sub-command for full docs.

---
# Command - change_line_end
Convert or check LF/CRLF line endings in files or folders.

---

## 📝 Description
This command allows you to:
- **Convert** line endings in files or entire directories between LF (Unix, `\n`) and CRLF (Windows, `\r\n`) formats.
- **Check** the line ending type of files and quickly detect if files contain mixed line endings.

This is especially useful when working on projects across different operating systems or collaborating with others, to ensure consistency and avoid hidden issues.

---

## Usage
```sh
shellman change_line_end [OPTIONS]
```
Options
```sh
--file PATH
```
Path to a single file to process.

```sh
--dir PATH
```
Path to a directory to process all files inside recursively.

```sh
--ext EXT
```
Only process files with this extension (e.g., --ext py). Requires --dir.
```sh
--to {lf,crlf}
```
Convert all matching files to the chosen line ending type.
```sh
--check
```
Only check and report the line ending type per file, do not modify.
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English instead of executing the command.

## Examples
1. Check line endings of a file
```sh
shellman change_line_end --file script.py --check
```
Output:
```
 script.py → CRLF
```

2. Convert a single file to LF (Unix)
```sh
shellman change_line_end --file README.md --to lf
```
Output:
```sh
→ converted to LF: README.md
```
3. Recursively convert all .txt files in a directory to CRLF (Windows)
```sh
shellman change_line_end --dir docs --ext txt --to crlf
```
4. Check all .sh scripts in a folder for line ending types
```sh
shellman change_line_end --dir scripts --ext sh --check
```

Possible outputs:
```sh
 scripts/install.sh → LF
 scripts/legacy_convert.sh → MIXED
```
## Notes
You must specify either --file or --dir.

Either --to or --check is required.

Mixed line endings (MIXED) indicate a file contains both LF and CRLF. It's best to normalize these.
The extension filter (--ext) should be used with --dir.
The command works on all text files, but binary files may yield incorrect results.

# Command - checksum_files

Generate or verify file checksums (SHA256, MD5, SHA1) in directories and projects.

---

## 📝 Description

This command allows you to:
- **Generate** checksums for all files in a directory (with optional extension filter), saving the list to a file.
- **Verify** the integrity of files based on a previously generated checksum list (detects tampering or corruption).
- Choose popular algorithms: **SHA256** (default), **MD5**, or **SHA1**.

Checksums are essential for verifying data integrity after transfers, backups, or before deployment.

---

## Usage

```sh
shellman checksum_files [OPTIONS]
```
Options
```sh
--path PATH
```
Directory to scan (default: current directory .).
```sh
--ext EXT 
```
Only include files with this extension (e.g., --ext py).
```sh
--algo {sha256,md5,sha1}
```
Select hash algorithm (default: sha256).
```sh
--out FILE
```
Name of the output file for checksum list (default: checksums.<algo>sum).
```sh
--verify
```
Verify files using an existing checksum list file (reads from --out).
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English.
## Examples
1. Generate SHA256 checksums for all files in the current directory
```sh
shellman checksum_files --algo sha256
```
Creates checksums.sha256sum with contents like:

```sh
d2f0b8...  ./script.py
342ab9...  ./data/config.json
```
2. Generate checksums for all .txt files in docs directory using MD5
```sh
shellman checksum_files --path docs --ext txt --algo md5 --out docs.md5list
```
3. Verify files using a previously generated checksum list
```sh
shellman checksum_files --verify --out docs.md5list
```
Output:

```sh
🔎 Verifying files via md5 list docs.md5list ...
✅ OK: docs/notes.txt
❌ MISMATCH: docs/draft.txt
❌ docs/old.txt not found
```
## Notes
The extension filter (--ext) works only with the --path directory option.

The default output file is checksums.<algo>sum, e.g., checksums.sha256sum.

When verifying, all files and their hashes are checked against the list; any mismatch or missing file is reported.

The command works on all file types, but binary and large files may take longer to process.

Only supported algorithms: SHA256, MD5, SHA1.
---
# Command -  clean_files

Delete files by name, extension, or age – with preview and confirmation.

---

## 📝 Description

This command lets you **clean up your project or directory** by deleting files:
- Matching a **name pattern** (substring in filename)
- With a specific **extension** (e.g., `log`, `tmp`)
- **Older than** a chosen number of days
- Or any **combination** of the above

**Preview** and **confirmation** options make clean-up safe and transparent.

Use it to remove logs, backups, temporary files, build artifacts, or any clutter!

---

## Usage

```sh
shellman clean_files [OPTIONS]
```
Options
```sh
--path PATH
```
Directory to scan (default: current directory .)
```sh
--ext EXT
```
Delete files with this extension (e.g., --ext log)
```sh
--name PATTERN
```
Delete files whose name contains this pattern (substring)
```sh
--older-than DAYS
```
Delete only files older than N days
```sh
--dry-run
```
Preview: list files that would be deleted, but do not delete them
```sh
--confirm
```
Ask before deleting each file (Y/n prompt for each)
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English

## Examples
1. Preview all .log files to be deleted in current directory
```sh
shellman clean_files --ext log --dry-run
```
2. Delete .tmp files older than 30 days (with confirmation prompt)
```sh
shellman clean_files --ext tmp --older-than 30 --confirm
```
3. Remove all files containing backup in their name (no confirmation)
```sh
shellman clean_files --name backup
```
4. Delete .bak files in /var/data and preview before deleting
```sh
shellman clean_files --path /var/data --ext bak --dry-run
```
5. Remove .old files containing report in the name, older than 60 days
```sh
shellman clean_files --ext old --name report --older-than 60 --dry-run
```

## Notes
At least one of --ext or --name is required.

--older-than is optional; applies additional filtering by modification time.

Use --dry-run first to preview which files would be deleted.

Use --confirm to prompt for each file before deletion (safer).

Matching is case-sensitive.

Deletion is permanent – files are not moved to trash/recycle bin!

---
# Command -  csv_extract

Extract specific columns or rows from a CSV file, with powerful filtering and export options.

---

## 📝 Description

This command helps you quickly **extract and filter data from CSV files**, such as:
- Selecting specific columns (by number)
- Extracting a range of rows
- Keeping or excluding rows based on text filters
- Skipping the header row if needed
- Saving output to a file or viewing interactively

Works with all CSV-like files (you can set the delimiter).

---

## Usage

```sh
shellman csv_extract FILE --cols COLUMNS [OPTIONS]
```
Arguments:

FILE – path to the CSV file to process (required)

Options:
```sh
--cols COLS
```
Required. Columns to keep (1-based), e.g. 1,3 or 2-4.
```sh
--rows ROWS
```
Only keep selected rows (after header). Format: 2-10 or 1,3,5.
```sh
--contains TEXT
```
Only keep rows containing this text (case-insensitive).
```sh
--not-contains TEXT
```
Only keep rows NOT containing this text.
```sh
--delim CHAR
```
CSV delimiter (default: ,).
```sh
--skip-header
```
Skip the first line (header row).
```sh
--output FILE
```
Save the result to a file instead of printing.
```sh
--interactive
```
Pipe the output to a pager (e.g., less).
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English.
## Examples
1. Extract columns 2 and 4 from a CSV
```sh
shellman csv_extract data.csv --cols 2,4
```
2. Extract columns 1–3 and only rows 2 to 10 (excluding the header)
```sh
shellman csv_extract data.csv --cols 1-3 --rows 2-10 --skip-header
```
3. Export rows containing "error" in any column
```sh
shellman csv_extract data.csv --cols 1,2 --contains error
```
4. Export rows not containing "backup", save to file
```sh
shellman csv_extract data.csv --cols 1,3 --not-contains backup --output filtered.csv
```
5. Preview large output interactively
```sh
shellman csv_extract data.csv --cols 1,2,3 --interactive
```
## Notes
Both --cols and file argument are required.

Columns and rows are 1-based (first column = 1).

You can combine column and row selection, with or without filtering.

Use either --contains or --not-contains (not both at once).

For custom delimiters (e.g., ;), use --delim ";".

--skip-header only skips the first line (useful if your CSV has a header).

Output is printed to the terminal unless --output is given.

---
# Command - date_utils

Work with dates: add/subtract time, compare or format – flexible CLI date/time helper.

---

## 📝 Description

This command allows you to:
- **Add** or **subtract** time from a given date (or now)
- **Compare** two dates (shows difference in days, hours, minutes, seconds)
- **Format** dates using any [strftime pattern](https://strftime.org/)
- Parse dates in common formats: `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS`

Great for scripting, reporting, or quick date math in the shell.

---

## Usage

```sh
shellman date_utils [OPTIONS]
```
Options
```sh
--date DATE
```
Base date (default: now). Accepted formats: 2024-07-08 or 2024-07-08 15:30:00.
```sh
--add DURATION
```
Add time to base date. Format: e.g. 5d, 3w, 2h, 10min, 1m, 1y, 2q, 45s.
Supported units:
```sh
d = days
w = weeks
m = months
y = years
q = quarters (3 months)
h = hours
min = minutes
s = seconds
```
```sh
--sub DURATION
```
Subtract time from base date (same formats/units as above).
```sh
--diff DATE
```
Show difference between base date and this date (in days, hours, minutes, seconds).
```sh
--format PATTERN
```
Format the date/result using any strftime pattern, e.g. %Y-%m-%d, %d/%m/%Y, %A, %H:%M.
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English.

## Examples
1. Add 3 days to now
```sh
shellman date_utils --add 3d
```
2. Subtract 2 months from specific date
```sh
shellman date_utils --date 2023-10-01 --sub 2m
```
3. Show difference between two dates
```sh
shellman date_utils --date 2024-01-01 --diff 2024-07-08
```
4. Format current date in custom format
```sh
shellman date_utils --format "%A, %d-%m-%Y %H:%M"
```
5. Chain calculations and formatting
```sh
shellman date_utils --date 2024-01-01 --add 1y --format "%Y/%m/%d"
```
## Notes
Date input must be YYYY-MM-DD or YYYY-MM-DD HH:MM:SS

Only one --add or --sub operation at a time

Units are case-insensitive, e.g. 10MIN is valid

Use strftime for custom output (see docs for all codes)

Negative differences (--diff) are shown with minus in days/hours
---
# Command - dir_tree

Prints a visual tree of directories (like the Unix `tree` command) – with options for files, depth, ASCII, and more.

---

## 📝 Description

This command displays a structured **tree view** of your directory and subdirectories:
- See the full hierarchy at a glance
- Optionally include files, not just folders
- Limit the depth of recursion for huge folders
- Save the tree as text to a file
- Show hidden files/folders or stick to visible ones
- Choose between Unicode and pure ASCII line graphics

Ideal for exploring codebases, reporting directory structure, or documenting projects.

---

## Usage

```sh
shellman dir_tree [PATH] [OPTIONS]
```
Arguments:

PATH – directory to scan (default: current directory .)

Options:
```sh
--files
```
Include files (not just directories) in the tree.
```sh
--depth N
```
Limit recursion to N levels deep.
```sh
--output FILE
```
Save the tree output to a text file.
```sh
--hidden
```
Include hidden files and folders (names starting with .).
```sh
--ascii
```
Use ASCII-only box drawing (for old terminals or code comments).
```sh
--lang-help {pl,eng}
```
Exclude patterns (folder names, file names, or extensions, e.g. __pycache__, *.txt, *.pyc)
```sh
--exclude
```    
Show this help in Polish or English.
## Examples
1. Print the full directory tree (folders only)
```sh
shellman dir_tree
```
2. Show directories and files up to 2 levels deep
```sh
shellman dir_tree --files --depth 2
```
3. Include hidden files and folders, ASCII lines
```sh
shellman dir_tree --files --hidden --ascii
```
4. Save tree view of /home/user/project to tree.txt
```sh
shellman dir_tree /home/user/project --output tree.txt
```
## Notes
By default, only folders are shown – add --files for full content.

Maximum depth is unlimited unless set by --depth.

Some systems may have permission errors on protected folders – these will be marked.

ASCII mode is useful for displaying trees in plain text files or Markdown.
---

# Command - encrypt_files

Encrypt or decrypt files in a folder using strong AES-256 encryption with a password.

---

## 📝 Description

This command allows you to:
- **Encrypt** all matching files in a directory (optionally filter by extension) using **AES-256** and a password.
- **Decrypt** `.enc` files with the correct password.
- Output files are saved in separate directories (`encrypted/` or `decrypted/` by default, or custom with `--out`).

The encryption uses AES-256 in CBC mode, with a randomly generated salt and IV per file. Key is derived using PBKDF2-HMAC-SHA256 with 100,000 iterations.

**Ideal for backups, archiving, sending files securely, or protecting secrets in projects.**

---

## Usage

```sh
shellman encrypt_files --mode {encrypt|decrypt} --password PASS [OPTIONS]
```
Options
```sh
--mode {encrypt, decrypt}
```
Required. Choose encryption or decryption mode.
```sh
--password PASSWORD
```
Required. Password to encrypt/decrypt files (do not lose this!).
```sh
--ext EXT
```
Only process files with this extension (e.g. --ext txt).
```sh
--path DIR
```
Directory to scan (default: current directory).
```sh
--out DIR
```
Output directory (default: encrypted/ or decrypted/).
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English.
## Examples
1. Encrypt all files in current directory
```sh
shellman encrypt_files --mode encrypt --password mySecret
```
2. Encrypt only .pdf files in docs/, save to my_encrypted/
```sh
shellman encrypt_files --mode encrypt --password MyPass123 --path docs --ext pdf --out my_encrypted
```
3. Decrypt all .enc files in backup/ using a password
```sh
shellman encrypt_files --mode decrypt --password mySecret --path backup
```
## Notes
Password is never stored – losing it means files are unrecoverable.

Decrypted files are restored without the .enc extension.

You must specify --mode and --password for all operations.

Key derivation uses 100,000 PBKDF2 iterations for good security.

Each file is encrypted separately, with a unique salt and IV.

This is not a replacement for full-disk encryption or secure file storage!
---

# Command – excel (group)

Utilities for working with Excel files: quick structure checks, table previews, and CSV export.

## Subcommands:

- excel info – list sheets with row/column counts 
- excel preview – preview the first N rows / selected columns
- excel export – export sheets or ranges to CSV

Quick examples:
```sh
shellman excel info report.xlsx
shellman excel preview data.xlsx --sheet 2 --rows 10 --columns A,C-E -i
shellman excel export workbook.xlsx -s 1 -s 3 -o out --overwrite
```

## excel info

List all sheets in an .xlsx file with the number of rows and columns.
### Usage
```sh
shellman excel info FILE.xlsx [--lang-help pl|eng]
```

Example output:

```sh
Sheet                 Rows   Cols
----------------------------------
Sheet1                 125      8
Summary                 12      4
```

Options:
```sh
--lang-help pl|eng — show localized help text instead of executing
```

## excel preview

Preview the first N rows of a sheet (by index or name) with optional column selection.
Can render as a neatly aligned table (row numbers, | separators) or raw CSV.
Supports saving to a file or paging interactively.

### Usage
```sh
shellman excel preview FILE.xlsx \
  [--sheet NAME_OR_NUM] [--rows N] [--columns SPEC] \
  [--output FILE] [--interactive] [--info|-i] [--lang-help pl|eng]
```

Options
```sh
--sheet TEXT — sheet name or 1-based index (default: 1)

--rows INT — number of rows to preview (default: 20)

--columns TEXT — column spec like A,C-E

--output PATH — save result to a file (text)

--interactive — pipe to pager (less -S)

--info, -i — show column headers, row numbers, and | separator

--lang-help pl|eng — localized help
```
Examples:
```sh
# 10 rows from sheet #2, columns A and C–E, pretty table:
shellman excel preview data.xlsx --sheet 2 --rows 10 --columns A,C-E -i
```
```sh
# Save first 50 rows of sheet "Report" to out.csv:
shellman excel preview data.xlsx --sheet Report --rows 50 --output out.csv
```

### Notes

Column spec supports single letters and ranges, e.g., A,B-D.

With -i, output is width-aligned and row-numbered.

## excel export

Export one or more sheets (optionally narrowed by row/column ranges) to CSV files.
Each sheet becomes a separate CSV. Without --overwrite, a timestamp is appended to filenames.

### Usage
```sh
shellman excel export FILE.xlsx \
  [--sheets|-s NAME_OR_INDEX ...] [--rows|-r START-END] [--columns|-c SPEC] \
  [--out|-o DIR] [--overwrite|-ow] [--lang-help|-lh pl|eng]
```

Options
```sh
--sheets, -s TEXT (repeatable) — sheet names or indexes to export; omit to export all

--rows, -r TEXT — row range start-end (e.g., 2-100)

--columns, -c TEXT — columns like A,B-D

--out, -o PATH — output directory (default: csv)

--overwrite, -ow — overwrite (no timestamp in filenames)

--lang-help, -lh pl|eng — localized help
```

Examples:
```sh
# Export all sheets to csv/:
shellman excel export data.xlsx
```
```sh
# Export sheet "Data", rows 2–50, columns A–E, without timestamp:
shellman excel export data.xlsx -s Data -r 2-50 -c A-E -o csv --overwrite
```
```sh
# Export sheets 1 and 3 to out/:
shellman excel export workbook.xlsx -s 1 -s 3 -o out
```

Notes

Supported input: .xlsx
One CSV per sheet
Without --overwrite, a timestamp is appended to avoid collisions

---
# Command - file_convert

Convert between JSON, YAML, and TOML formats in a single step.

---

## 📝 Description

Convert data files between popular formats:
- **JSON ↔ YAML**
- **JSON ↔ TOML**
- **YAML ↔ TOML**

You can pretty-print results, output to a file, or page interactively.

Useful for config migrations, converting data for different tools, or normalizing format style.

---

## Usage

```sh
shellman file_convert FILE --from FORMAT --to FORMAT [OPTIONS]
```
Arguments & Options
FILE
Input file path (required)
```sh
--from FORMAT
```
Required. Input format: json, yaml, or toml
```sh
--to FORMAT
```
Required. Output format: json, yaml, or toml
```sh
--output FILE
```
Save converted data to a file
```sh
--pretty
```
Pretty-print output (only for JSON/YAML)
```sh
--interactive
```
Pipe output to a pager (e.g., less)
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English

## Examples
1. Convert YAML to JSON, print result
```sh
shellman file_convert config.yaml --from yaml --to json --pretty
```
2. Convert TOML to YAML and save to file
```sh
shellman file_convert pyproject.toml --from toml --to yaml --output config.yaml
```
3. Convert JSON to TOML, view output interactively
```sh
shellman file_convert settings.json --from json --to toml --interactive
```
## Notes
You must provide both --from and --to formats.

Only valid UTF-8 text files are supported.

Pretty printing is available for JSON and YAML only.

The tool will try to preserve structure and comments (where format allows).

Errors in parsing (e.g. invalid JSON) will stop the command.
---
# Command - file_stats

Show full path, file size, line-count, and extension for each file – with optional metadata.

---

## 📝 Description

This command collects and displays statistics for files:
- Shows path, number of lines, file size, and extension
- Supports recursive scan of directories
- Optionally, prints file metadata (creation & modification dates, type, encoding)
- Supports extension filtering, result saving to logs

Ideal for code audits, data checks, repo hygiene, or quick file reporting.

---

## Usage

```sh
shellman file_stats [PATHS...] [OPTIONS]
```
Arguments:

PATHS...
List of files or directories (can be mixed; required)

Options:
```sh
--ext EXT
```
Only include files with this extension (e.g. py)
```sh
--meta
```
Include metadata: created, modified, type, encoding
```sh
--output
```
Save results to logs/file_stats_<timestamp>.log
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English

## Examples
1. Show stats for a single file
```sh
shellman file_stats main.py
```
2. Recursively report on all .txt files in docs/
```sh
shellman file_stats docs --ext txt
```
3. Show stats for all files in several folders and print metadata
```sh
shellman file_stats src test --meta
```
4. Save a full report to a log file
```sh
shellman file_stats mydir --output
```
## Notes
Accepts multiple files or directories at once.

Directory arguments are searched recursively.

For binary files, line-count may not be meaningful.

File type and encoding detection uses heuristics (via chardet).
---
# Command - find_files

Find files by name, extension, or content – with flexible filtering and output options.

---

## 📝 Description

This command lets you search for files in a directory tree using:
- Partial name matches (substring in filename)
- File extension (e.g. only `.py` or `.txt`)
- File content (find all files containing specific text)
- Any combination of the above

You can also show file sizes and export results to a log file.

---

## Usage

```sh
shellman find_files SEARCH_PATH [OPTIONS]
```
Arguments & Options
SEARCH_PATH
Directory to search (required; recursion is automatic)
```sh
--name FRAGMENT
```
Match filenames containing this substring
```sh
--content TEXT
```
Search for files containing this text (UTF-8)
```sh
--ext EXT
```
Only include files with this extension (e.g. --ext py)
```sh
--output
```
Save results to logs/find_files_<timestamp>.log
```sh
--show-size
```
Show file size (in KB or MB) next to each result
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English

## Examples
1. Find all files with "log" in the name under ./data
```sh
shellman find_files ./data --name log
```
2. Find .md files containing the word "draft"
```sh
shellman find_files docs --ext md --content draft
```
3. Find all Python files in a folder and show their size
```sh
shellman find_files src --ext py --show-size
```
4. Save all .csv files found in exports to a log file
```sh
shellman find_files exports --ext csv --output
```
## Notes

SEARCH_PATH must be an existing directory.

Multiple filters can be combined for precise results.

Content search is case-sensitive and only supports UTF-8 text files.

Binary files or those with read errors are skipped.

Recursion is always enabled (scans all subfolders).

---
# 🗂️ json_extract

Extract and filter JSON data with optional field selection.

---

## 📝 Description

This command lets you:
- **Extract** data from JSON files, navigating nested objects/lists with a dot-separated path
- **Filter** list entries by field value (e.g., only objects with `status=active`)
- **Select fields** to include in the output (e.g., only show `id,name`)
- Output results as JSON lines (one object per line), to screen or a file, optionally with paging

Perfect for quickly slicing, dicing, and filtering big JSONs, logs, or API exports.

---

## Usage

```sh
shellman json_extract FILE [OPTIONS]
```
Options
FILE
Input JSON file (required)
```sh
--path KEY.PATH
```
Dot-separated path to a list or object, e.g. items, data.results, root.items
```sh
--filter KEY=VALUE
```
Only keep items where KEY == VALUE (string comparison)
```sh
--fields FIELD1,FIELD2,...
```
Output only these fields
```sh
--output FILE
```
Save output to file instead of printing
```sh
--interactive
```
Pipe output to a pager (e.g. less)
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English

## Examples

1. Extract top-level list from data.json
```sh
shellman json_extract data.json
```
2. Extract items from a nested path and filter by key
```sh
shellman json_extract data.json --path data.items --filter status=active
```
3. Output only certain fields as JSON lines
```sh
shellman json_extract data.json --path users --fields id,name
```
4. Save filtered results to a file and preview interactively
```sh
shellman json_extract logs.json --path logs --filter level=ERROR --fields time,message --output errors.jsonl --interactive
```
## Notes
If the path does not resolve to a list, the result is wrapped in a list for uniform handling.

Filter uses simple string equality.

If you use --fields, only those fields are kept in each result object.

Output is always one JSON object per line (JSONL format).

Works only with valid UTF-8 JSON files.

---
# Command - lines

Extract, count or summarize lines in files and folders – with powerful filters and context options.

---

## 📝 Description

This command lets you:
- **Extract** matching lines from files (with before/after context)
- **Count** lines matching filters or regular expressions
- **Summarize** files: total files, total lines, total matches
- Filter by content, regex, or extension
- Show percentages, file sizes, and save to logs
- Combine multiple options for advanced text/file analytics

---

## Usage

```sh
shellman lines [FILES OR FOLDERS...] [OPTIONS]
```
Options
```sh
--extract
```
Print matching lines (default if no mode is chosen)
```sh
--count
```
Show only the number of matching lines
```sh
--summary
```
Print a summary: total files, total lines, matches
```sh
--contains TEXT
```
Only include lines containing this text
```sh
--not-contains TEXT
```
Only include lines NOT containing this text
```sh
--regex PATTERN
```
Use a regular expression to match lines
```sh
--ignore-case
```
Case-insensitive matching
```sh
--before N
```
Show N lines before each match (context)
```sh
--after N
```
Show N lines after each match (context)
```sh
--ext EXT
```
Only include files with this extension
```sh
--percent
```
Show percentage of matches vs total lines
```sh
--output FILE
```
Save results to a file
```sh
--interactive
```
Pipe results to pager (e.g. less)
```sh
--show-size
```
Show file size next to results
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English

## Examples
1. Print all lines containing "TODO" from .py files
```sh
shellman lines src --ext py --contains TODO
```
2. Count the number and percent of lines matching a regex
```sh
shellman lines logs.txt --regex "ERROR.*" --count --percent
```
3. Extract lines (with 2 lines before and 1 after each match) from a folder
```sh
shellman lines logs/ --contains WARNING --before 2 --after 1
```
4. Show summary of all .txt files in a directory
```sh
shellman lines data --ext txt --summary
```
5. Save matching lines to a log and preview interactively
```sh
shellman lines myfile.txt --contains "secret" --output results.log --interactive
```

## Notes
By default, --extract is used if no mode is given.

You cannot use --contains and --regex together.

Inputs can be a mix of files and folders (folders searched recursively).

If a filter is not set, all lines are included.

The --before and --after options add context lines to each match.

Non-UTF-8 files may be read with errors ignored.

---
# Command - open_ports

Show currently open TCP/UDP ports and serial ports (COM/LPT/tty) with process, PID, state, and device description.

---

## 📝 Description

This command allows you to:
- List all open TCP and UDP ports with associated process name and PID
- Filter by protocol (`tcp` or `udp`) or by local port number
- Display in a readable table or as raw JSON (for scripting/automation)
- List physical serial/parallel ports (COM, LPT, tty, cu) with human-readable device descriptions (cross-platform)

Supports Linux, macOS, and Windows. Requires `psutil` and `pyserial` for full features.

---

## Usage

```sh
shellman open_ports [OPTIONS]
```
Options
```sh
--proto {tcp, udp}
```
Filter only TCP or only UDP ports
```sh
--port N
```
Filter by local port number (e.g. --port 8080)
```sh
--json
```
Output raw JSON for open TCP/UDP sockets (no table)
```sh
--serial
```
Show available serial/parallel ports (COM, LPT, tty, cu) with device descriptions
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English

## Examples
1. List all open TCP and UDP ports with process info
```sh
shellman open_ports
```
2. Show only open TCP ports
```sh
shellman open_ports --proto tcp
```
3. Show all processes listening on port 5432
```sh
shellman open_ports --port 5432
```
4. Output open ports as JSON (for scripts, logs, or audits)
```sh
shellman open_ports --json
```
5. List all physical serial/parallel ports with device description
```sh
shellman open_ports --serial
```

## Notes
TCP/UDP info is gathered using the psutil library.

Serial port listing requires pyserial; falls back to device globbing on POSIX.

On first run, psutil may auto-install if missing (internet required).

If running without permissions, you may not see all ports/processes.

Output as JSON includes all fields: protocol, pid, process, local/remote addresses, state.

---

# Command - replace_text

Replace occurrences of text in multiple files – with preview, diff, and interactive confirmation.

---

## 📝 Description

This command allows you to:
- **Search and replace** specific text in many files at once (recursively in a folder)
- Filter files by extension
- Preview changes as unified diffs before saving
- Confirm each replacement interactively
- Safely batch-edit configs, code, docs, notes, and more

---

## Usage

```sh
shellman replace_text SEARCH_PATH --find TEXT --replace TEXT [OPTIONS]
```
Options
SEARCH_PATH
Directory to search (required)
```sh
--find TEXT
```
Required. Text to find
```sh
--replace TEXT
```
Required. Replacement text
```sh
--ext EXT
```
Only process files with this extension
```sh
--in-place
```
Write changes back to files (otherwise preview only)
```sh
--preview
```
Show unified diff preview of proposed changes
```sh
--confirm
```
Ask interactively before replacing in each file
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English

## Examples
1. Replace all "foo" with "bar" in .md files under docs/ (preview only)
```sh
shellman replace_text docs --find foo --replace bar --ext md --preview
```
2. Replace "localhost" with "127.0.0.1" in config files, with interactive confirmation
```sh
shellman replace_text config --find localhost --replace 127.0.0.1 --ext conf --in-place --confirm
```
3. Bulk update copyright year in project
```sh
shellman replace_text . --find "Copyright 2023" --replace "Copyright 2024" --ext py --in-place --preview
```
## Notes
Changes are only made if --in-place is given; otherwise, nothing is written.

You can combine --preview and --in-place to see diffs before changes.

If --confirm is used, you will be prompted (Y/n) for each file.

Only files containing the search text are processed.

Recursively searches all subfolders.

Only processes text files (UTF-8, errors ignored).

Extension filtering matches the file suffix (e.g., .md).

---

# Command - speed_test

Run a quick internet speed test (download, upload, ping) – using the fastest available method on your platform.

---

## 📝 Description

This command performs an internet speed test and displays:
- Download speed (Mbps)
- Upload speed (Mbps)
- Ping (ms)

It automatically selects the best available backend:
1. **Ookla CLI** (`speedtest` binary, official)
2. **speedtest-cli** (Python binary)
3. **speedtest-cli** (Python module, auto-installs if missing)

Results are printed as text or raw JSON – great for reports, monitoring, or troubleshooting.

---

## Usage

```sh
shellman speed_test [OPTIONS]
```
Options
```sh
--json
```
Output raw JSON with download, upload, and ping
```sh
--only {download, upload, ping}
```
Show only one metric (e.g. --only download)
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English

## Examples
1. Run a full speed test (download/upload/ping)
```sh
shellman speed_test
```
2. Show only download speed
```sh
shellman speed_test --only download
```
3. Output results as raw JSON
```sh
shellman speed_test --json
```

## Notes
For best accuracy, the official speedtest binary from Ookla will be used if available.

Falls back to Python speedtest-cli if necessary (may auto-install).

Actual speeds depend on your current connection, time of day, and server location.

The test may take a few seconds to complete.

On first use, an internet connection is needed to install missing backends.

---
# Command - sys_summary

Show system, shell, and tool environment summary – cross-platform hardware & OS info for Linux, macOS, Windows.

---

## 📝 Description

This command gives you a complete summary of your system, including:
- **OS, version, architecture, host and WSL info**
- **Serial number** (where supported)
- **CPU**: model, core count, frequency
- **Sensors/temperature**: (when supported)
- **GPU**: detected graphics cards
- **Battery**: charge status, percent, time remaining
- **Bluetooth**: detected devices/adapters
- **Tools**: `python3`, `jq`, `xlsx2csv`, etc.
- **Memory**: total/used/available
- **Uptime & Load**: since last boot, load averages
- **Disks**: usage, free space per partition
- **Network**: local/public IP, interfaces
- **Packages**: package manager type, package count
- **Printers**: detected printers
- **Wi-Fi**: connected SSID (if available)
- **Displays**: screen resolutions, number of displays

Works on Linux, macOS, and Windows, with automatic adaptation to platform capabilities.

---

## Usage

```sh
shellman sys_summary [--lang-help pl|eng]
```
## Example output (Linux)
```sh
📋  System Summary
────────────────────────────────────────────
🖥️  OS & Host
────────────────────────────────────────────
System       : Linux
Distro       : Ubuntu 22.04
Version      : 5.15.0-89-generic
Architecture : x86_64
WSL          : No
Hostname     : my-laptop

🔑 Serial Number
────────────────────────────────────────────
Serial       : ABCD1234EFGH

🦾  CPU
────────────────────────────────────────────
Cores        : 8 (logical: 16)
Frequency    : 3200.0 MHz
Model        : Intel(R) Core(TM) i7-1165G7 CPU @ 2.80GHz

🌡️  Sensors / Temperature
────────────────────────────────────────────
coretemp: temp = 48.0 °C

🖥️  GPU
────────────────────────────────────────────
GPU          : Intel Iris Xe Graphics

🔋  Battery
────────────────────────────────────────────
Percent      : 85%
Plugged in   : Yes
Time left    : 2:34:00

📡  Bluetooth
────────────────────────────────────────────
Powered: yes

🛠️  Tools
────────────────────────────────────────────
python3      : /usr/bin/python3
jq           : /usr/bin/jq
xlsx2csv     : /usr/local/bin/xlsx2csv

🧠  Memory
────────────────────────────────────────────
              total        used        free      shared  buff/cache   available
Mem:           15Gi       3.7Gi       8.1Gi       400Mi       3.3Gi        11Gi
Swap:         2.0Gi       0.0Ki       2.0Gi

⏱️  Uptime & Load
────────────────────────────────────────────
Uptime       : up 4 days, 5 hours, 12 minutes
Load Avg.    : 0.65, 0.45, 0.35

💾  Disks
────────────────────────────────────────────
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  470G   60G  387G  14% /

🌐  Network
────────────────────────────────────────────
Local IP     : 192.168.0.13
Public IP    : 83.12.45.67

📦  Packages
────────────────────────────────────────────
Pkg Manager  : apt
Total pkgs   : 2024

🖨️  Printers
────────────────────────────────────────────
Printer      : HP_LaserJet

📶  Wi-Fi
────────────────────────────────────────────
Connected SSID: Domowy_5G

🖥️  Displays
────────────────────────────────────────────
eDP-1 connected primary 1920x1080+0+0
HDMI-1 disconnected
```

## Notes
Some fields require extra permissions (e.g., serial number, sensors, dmidecode).

Some info may be unavailable or limited depending on platform/hardware.

Battery, sensors, Bluetooth, printers, Wi-Fi may not be present on servers or VMs.

For full hardware info on Windows, run from PowerShell/CMD (not Git Bash).

---

# Command - zip_batch

Create zip archives from folders or files in batch, with extension filtering and optional password.

---

## 📝 Description

Quickly compress and archive many files or folders at once:
- **Archive all files** (optionally filtered by extension) in a source directory
- **Per-folder mode:** Create one ZIP per immediate subfolder
- **Custom name prefix** for archives
- **Password protection** (warning: ZIP’s `-P` is weak!)
- Output goes to the selected directory (default: `./zips`)

Requires the `zip` command-line tool in your system.

---

## Usage

```sh
shellman zip_batch [OPTIONS]
```
Options
```sh
--path DIR
```
Source directory to scan (default: current directory)
```sh
--ext EXT
```
Only include files with this extension (e.g. --ext txt)
```sh
--per-folder
```
Create one archive per immediate sub-folder (instead of one big archive)
```sh
--output DIR
```
Output directory for ZIPs (default: ./zips)
```sh
--name PREFIX
```
Prefix for archive filenames (default: batch_)
```sh
--password PASS
```
Set ZIP password (uses zip -P; weak encryption)
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English

## Examples
1. Archive all files in reports/ as one ZIP
```sh
shellman zip_batch --path reports
```
2. Create separate ZIPs for each folder in datasets/ (per-folder mode)
```sh
shellman zip_batch --path datasets --per-folder --name data_
```
3. Archive only .csv files and save to myzips/
```sh
shellman zip_batch --ext csv --output myzips
```
4. Create a password-protected ZIP of all .pdf files
```sh
shellman zip_batch --ext pdf --password MySecret123
```
## Notes
Requires the zip utility (Linux/macOS/WSL/Windows with zip.exe).

Password protection (-P) in zip is weak – do not use for strong security!

--per-folder makes one archive per each direct subdirectory (ignores files at root level).

Filenames have the given prefix (default: batch_) and a timestamp for batch mode.

---

## ❤️ Contributing

Pull-requests and feature ideas are welcome!
Each command lives in shellman/commands/ – feel free to add your own tool.
