Język polski dostępny poniżej

# 🐚 Shellman

**Shellman** is your friendly CLI assistant – a curated toolbox for working with files, data and your system.

---

## 🔧 Installation

### 1 · Clone the repository

```bash
git clone https://github.com/JakubMarciniak93/shellman
cd shellman
```

### 2 · Install dependencies

A virtual-env is recommended:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
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

## 🚀 Usage

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
```bash
excel info | preview | export	sheet list • quick preview • export ranges to CSV
find_files	locate files by name, content or extension
change_line_end	LF ↔ CRLF conversion / check
checksum_files	create or verify checksums (sha256, md5, sha1)
clean_files	delete junk files by name, ext or age
lines	Extract, count or summarize lines in files or folders with powerful filters and context options.
csv_extract	extract columns/rows from CSV
date_utils	add/subtract dates, diff, strftime
encrypt_files	AES-256 encrypt / decrypt with password
file_convert	JSON ←→ YAML ←→ TOML
file_stats	full path • size • line-count • extension
json_extract	JSON path, filter and field selection
merge_files	merge multiple text files into one
replace_text	batch find-&-replace with diff preview
sys_summary	system / shell / resource report
zip_batch	bulk ZIP creation (per-folder or flat)
open_ports  Show currently open TCP/UDP ports (process, pid, address, state).
speed_test	Run a quick internet speed test (download, upload, ping).
dir_tree  Prints a visual tree of directories (like 'tree').
```
Plus a few helpers: checksum_files, date_utils, etc. Run --help on any sub-command for full docs.

---
# 🔄 change_line_end
Convert or check LF/CRLF line endings in files or folders.

---

## 📝 Description
This command allows you to:
- **Convert** line endings in files or entire directories between LF (Unix, `\n`) and CRLF (Windows, `\r\n`) formats.
- **Check** the line ending type of files and quickly detect if files contain mixed line endings.

This is especially useful when working on projects across different operating systems or collaborating with others, to ensure consistency and avoid hidden issues.

---

## 🚦 Usage
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

⚡ Examples
1. Check line endings of a file
```sh
shellman change_line_end --file script.py --check
```
Output:
```
🔍 script.py → CRLF
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
🔍 scripts/install.sh → LF
🔍 scripts/legacy_convert.sh → MIXED
```
⚠️ Notes
You must specify either --file or --dir.

Either --to or --check is required.

Mixed line endings (MIXED) indicate a file contains both LF and CRLF. It's best to normalize these.
The extension filter (--ext) should be used with --dir.
The command works on all text files, but binary files may yield incorrect results.

# 🔐 checksum_files

Generate or verify file checksums (SHA256, MD5, SHA1) in directories and projects.

---

## 📝 Description

This command allows you to:
- **Generate** checksums for all files in a directory (with optional extension filter), saving the list to a file.
- **Verify** the integrity of files based on a previously generated checksum list (detects tampering or corruption).
- Choose popular algorithms: **SHA256** (default), **MD5**, or **SHA1**.

Checksums are essential for verifying data integrity after transfers, backups, or before deployment.

---

## 🚦 Usage

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

⚡ Examples
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
⚠️ Notes
The extension filter (--ext) works only with the --path directory option.

The default output file is checksums.<algo>sum, e.g., checksums.sha256sum.

When verifying, all files and their hashes are checked against the list; any mismatch or missing file is reported.

The command works on all file types, but binary and large files may take longer to process.

Only supported algorithms: SHA256, MD5, SHA1.
---
# 🧹 clean_files

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

## 🚦 Usage

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

⚡ Examples
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

⚠️ Notes
At least one of --ext or --name is required.

--older-than is optional; applies additional filtering by modification time.

Use --dry-run first to preview which files would be deleted.

Use --confirm to prompt for each file before deletion (safer).

Matching is case-sensitive.

Deletion is permanent – files are not moved to trash/recycle bin!

---
# 📑 csv_extract

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

## 🚦 Usage

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

⚡ Examples
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
⚠️ Notes
Both --cols and file argument are required.

Columns and rows are 1-based (first column = 1).

You can combine column and row selection, with or without filtering.

Use either --contains or --not-contains (not both at once).

For custom delimiters (e.g., ;), use --delim ";".

--skip-header only skips the first line (useful if your CSV has a header).

Output is printed to the terminal unless --output is given.

---
# 📅 date_utils

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

## 🚦 Usage

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

⚡ Examples
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
⚠️ Notes
Date input must be YYYY-MM-DD or YYYY-MM-DD HH:MM:SS

Only one --add or --sub operation at a time

Units are case-insensitive, e.g. 10MIN is valid

Use strftime for custom output (see docs for all codes)

Negative differences (--diff) are shown with minus in days/hours
---
# 🌳 dir_tree

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

## 🚦 Usage

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
Show this help in Polish or English.

⚡ Examples
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
⚠️ Notes
By default, only folders are shown – add --files for full content.

Maximum depth is unlimited unless set by --depth.

Some systems may have permission errors on protected folders – these will be marked.

ASCII mode is useful for displaying trees in plain text files or Markdown.
---

# 🔒 encrypt_files

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

## 🚦 Usage

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

⚡ Examples
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
⚠️ Notes
Password is never stored – losing it means files are unrecoverable.

Decrypted files are restored without the .enc extension.

You must specify --mode and --password for all operations.

Key derivation uses 100,000 PBKDF2 iterations for good security.

Each file is encrypted separately, with a unique salt and IV.

This is not a replacement for full-disk encryption or secure file storage!
---
# 📋 excel info

Show all sheets in an Excel file with row and column count.

---

## 📝 Description

Lists every sheet in a given `.xlsx` file, showing:
- Sheet name
- Number of rows
- Number of columns

Useful for quick inspection of Excel structure.

---

## 🚦 Usage

```sh
shellman excel info FILE.xlsx
```
⚡ Example
```sh
shellman excel info data.xlsx
```
Output:

```sh
Sheet                 Rows   Cols
----------------------------------
Sheet1                 125      8
Summary                12      4
```
⚠️ Notes
FILE must be a valid Excel file (.xlsx).

Works in read-only mode (safe for large files).
---
# 👁️ excel preview

Preview the first N rows or selected columns of a chosen Excel sheet.

---

## 📝 Description

Displays a preview of data from an Excel sheet:
- Choose sheet by index or name (default: first)
- Select columns (e.g., `A,C-E`)
- Limit number of rows shown
- Show row numbers, headers, and custom separators
- Output as table or raw CSV

Optionally, save the preview to a file or view interactively (paged).

---

## 🚦 Usage

```sh
shellman excel preview FILE.xlsx [--sheet NAME/NUM] [--rows N] [--columns SPEC] [OPTIONS]
```
Options
```sh
--sheet
```
Sheet name or number (default: 1st sheet)
```sh
--rows
```
Number of rows to preview (default: 20)
```sh
--columns
```
Columns, e.g. A,C-E
```sh
--output
```
Save preview to file
```sh
--interactive
```
Pipe result to pager (e.g., less)
```sh
--info, -i
```
Show column headers, row numbers, | separator

⚡ Examples
Preview columns A and C-E from the 2nd sheet, show first 10 rows:

```sh
shellman excel preview data.xlsx --sheet 2 --rows 10 --columns A,C-E -i
```
Save first 50 rows of sheet "Report" to out.csv:

```sh
shellman excel preview data.xlsx --sheet Report --rows 50 --output out.csv
```
⚠️ Notes
File must be .xlsx

Columns: A, B, C-E, etc.

If using --info, data is shown as a table with row numbers.

---
# ⬇️ excel export

Export one or more Excel sheets (or selected rows/columns) to CSV files.

---

## 📝 Description

Exports data from Excel sheets to CSV:
- Choose sheets by name or index
- Select rows (range: e.g., `2-100`)
- Select columns (e.g., `A,B-D`)
- Output each sheet as a separate CSV file
- Overwrite or create new CSVs (with timestamp)

Output files go to a chosen directory (default: `csv/`).

---

## 🚦 Usage

```sh
shellman excel export FILE.xlsx [--sheets NAME/NUM ...] [--rows START-END] [--columns SPEC] [OPTIONS]
```
Options
```sh
--sheets
```
Names or indexes of sheets to export (multiple allowed)
```sh
--rows
```
Row range, e.g. 2-100
```sh
--columns
```
Columns, e.g. A,B-D
```sh
--out
```
Output directory (default: csv/)
```sh
--overwrite
```
Overwrite files (no timestamp in names)
```sh
--lang-help {pl,eng}
```
Show this help in Polish or English

⚡ Examples
Export all sheets to CSVs in csv/:

```sh
shellman excel export data.xlsx
```
Export sheet "Data" rows 2-50, columns A-E, overwrite file:

```sh
shellman excel export data.xlsx --sheets Data --rows 2-50 --columns A-E --overwrite
```
Export sheets 1 and 3, save CSVs to out/:

```sh
shellman excel export data.xlsx --sheets 1 --sheets 3 --out out
```
⚠️ Notes
Only .xlsx files supported

Each exported sheet is a separate CSV file

Without --overwrite, filenames include timestamp to avoid overwriting

---
# 🔄 file_convert

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

## 🚦 Usage

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

⚡ Examples
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
⚠️ Notes
You must provide both --from and --to formats.

Only valid UTF-8 text files are supported.

Pretty printing is available for JSON and YAML only.

The tool will try to preserve structure and comments (where format allows).

Errors in parsing (e.g. invalid JSON) will stop the command.
---
# 📊 file_stats

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

## 🚦 Usage

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

⚡ Examples
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
⚠️ Notes
Accepts multiple files or directories at once.

Directory arguments are searched recursively.

For binary files, line-count may not be meaningful.

File type and encoding detection uses heuristics (via chardet).
---
# 🔍 find_files

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

## 🚦 Usage

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

⚡ Examples
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
⚠️ Notes
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

## 🚦 Usage

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

⚡ Examples
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
⚠️ Notes
If the path does not resolve to a list, the result is wrapped in a list for uniform handling.

Filter uses simple string equality.

If you use --fields, only those fields are kept in each result object.

Output is always one JSON object per line (JSONL format).

Works only with valid UTF-8 JSON files.

---
# 📏 lines

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

## 🚦 Usage

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

⚡ Examples
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

⚠️ Notes
By default, --extract is used if no mode is given.

You cannot use --contains and --regex together.

Inputs can be a mix of files and folders (folders searched recursively).

If a filter is not set, all lines are included.

The --before and --after options add context lines to each match.

Non-UTF-8 files may be read with errors ignored.

---
# 🛡️ open_ports

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

## 🚦 Usage

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

⚡ Examples
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

⚠️ Notes
TCP/UDP info is gathered using the psutil library.

Serial port listing requires pyserial; falls back to device globbing on POSIX.

On first run, psutil may auto-install if missing (internet required).

If running without permissions, you may not see all ports/processes.

Output as JSON includes all fields: protocol, pid, process, local/remote addresses, state.

---

# ✏️ replace_text

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

## 🚦 Usage

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

⚡ Examples
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
⚠️ Notes
Changes are only made if --in-place is given; otherwise, nothing is written.

You can combine --preview and --in-place to see diffs before changes.

If --confirm is used, you will be prompted (Y/n) for each file.

Only files containing the search text are processed.

Recursively searches all subfolders.

Only processes text files (UTF-8, errors ignored).

Extension filtering matches the file suffix (e.g., .md).

---

# 🚀 speed_test

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

## 🚦 Usage

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

⚡ Examples
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

⚠️ Notes
For best accuracy, the official speedtest binary from Ookla will be used if available.

Falls back to Python speedtest-cli if necessary (may auto-install).

Actual speeds depend on your current connection, time of day, and server location.

The test may take a few seconds to complete.

On first use, an internet connection is needed to install missing backends.

---
# 🖥️ sys_summary

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

## 🚦 Usage

```sh
shellman sys_summary [--lang-help pl|eng]
```
⚡ Example output (Linux)
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

⚠️ Notes
Some fields require extra permissions (e.g., serial number, sensors, dmidecode).

Some info may be unavailable or limited depending on platform/hardware.

Battery, sensors, Bluetooth, printers, Wi-Fi may not be present on servers or VMs.

For full hardware info on Windows, run from PowerShell/CMD (not Git Bash).

---

# 📦 zip_batch

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

## 🚦 Usage

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

⚡ Examples
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
⚠️ Notes
Requires the zip utility (Linux/macOS/WSL/Windows with zip.exe).

Password protection (-P) in zip is weak – do not use for strong security!

--per-folder makes one archive per each direct subdirectory (ignores files at root level).

Filenames have the given prefix (default: batch_) and a timestamp for batch mode.

---

## ❤️ Contributing

Pull-requests and feature ideas are welcome!
Each command lives in shellman/commands/ – feel free to add your own tool.

########################################################################################

# 🐚 Shellman (Polski)

**Shellman** to przyjazny asystent CLI – zestaw narzędzi do pracy z plikami, danymi i systemem.

---

## 🔧 Instalacja

### 1 · Klonowanie repozytorium

```bash
git clone https://github.com/JakubMarciniak93/shellman
cd shellman
```
### 2 · Instalacja zależności

Zalecana wirtualna środowisko:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```
Lub z Poetry:

```bash
poetry install
```

### 3 · Instalacja w trybie developerskim

```bash
pip install -e .
```

(Zmiany w kodzie / plikach .md są widoczne od razu – reinstaluj tylko przy zmianie struktury pakietu).

## 🚀 Użycie

Lista komend:

```bash
shellman --help
```
Każda komenda obsługuje wielojęzyczną pomoc:

```bash
shellman <komenda> --lang-help eng     # pomoc po angielsku
shellman <komenda> --lang-help pl      # pomoc po polsku
```
Przykład:

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
## 📦 Dostępne komendy (wybrane)

komenda	opis skrócony:
```bash
excel info | preview | export	lista arkuszy • szybki podgląd • eksport do CSV
find_files	wyszukiwanie plików po nazwie, treści lub rozszerzeniu
change_line_end	konwersja lub sprawdzenie końców linii LF/CRLF
checksum_files	generowanie / weryfikacja sum kontrolnych
clean_files	usuwanie zbędnych plików wg wzorca lub wieku
lines	Wyodrębniaj, licz lub podsumowuj wiersze w plikach lub folderach przy użyciu zaawansowanych filtrów i opcji kontekstowych.
csv_extract	wyciąganie kolumn / wierszy z CSV
date_utils	operacje na datach: +/- czas, różnice, formatowanie
encrypt_files	szyfrowanie / deszyfrowanie AES-256
file_convert	konwersja JSON ↔ YAML ↔ TOML
file_stats	ścieżka • rozmiar • liczba linii • rozszerzenie
json_extract	filtrowanie / wybór pól w JSON
merge_files	łączenie plików tekstowych
replace_text	zbiorcza podmiana tekstu z podglądem diff
sys_summary	raport o systemie, powłoce, zasobach
zip_batch	hurtowe tworzenie plików ZIP
open_ports  Pokaż aktualnie otwarte porty TCP/UDP (proces, pid, adres, stan).
speed_test	Wykonaj szybki test szybkości łącza internetowego (pobieranie, wysyłanie, pingowanie).
dir_tree  Drukuje wizualne drzewo katalogów (jak „drzewo”).
```
Do odkrywania szczegółów użyj --help, np.:

```bash
shellman excel export --help
```
---
# 🔄 change_line_end

Konwersja lub sprawdzanie zakończeń linii LF/CRLF w plikach lub folderach.
---

## 📝 Opis
To polecenie pozwala:
- **Konwertować** zakończenia linii w plikach lub całych katalogach między LF (Unix, `\n`) a CRLF (Windows, `\r\n`).
- **Sprawdzać** typ zakończenia linii w plikach oraz wykrywać pliki z mieszanymi zakończeniami (MIXED).

Przydatne podczas pracy w zespołach lub na różnych systemach operacyjnych, by uniknąć problemów z kodowaniem plików czy konfliktów przy scalaniu.

---

## 🚦 Użycie

```sh
shellman change_line_end [OPCJE]
```
Opcje
```sh
--file ŚCIEŻKA
```
Ścieżka do pojedynczego pliku do przetworzenia.

```sh
--dir ŚCIEŻKA
```
Ścieżka do katalogu – przetwarzane są wszystkie pliki rekurencyjnie.
```sh
--ext ROZSZERZENIE
```
Przetwarzaj tylko pliki z tym rozszerzeniem (np. --ext py). Wymaga --dir.
```sh
--to {lf,crlf}
```
Konwertuj wszystkie znalezione pliki do wybranego typu zakończenia linii.
```sh
--check
```
Tylko sprawdź i pokaż typ zakończenia linii, nie dokonuj zmian.
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku zamiast uruchamiać polecenie.

⚡ Przykłady
1. Sprawdzenie zakończeń linii w pliku
```sh
shellman change_line_end --file skrypt.py --check
```
Wyjście:
```sh
🔍 skrypt.py → CRLF
```
2. Konwersja pojedynczego pliku do LF (Unix)
```sh
shellman change_line_end --file README.md --to lf
```
Wyjście:
```sh
→ converted to LF: README.md
```
3. Rekurencyjna konwersja wszystkich plików .txt w folderze do CRLF (Windows)
```sh
shellman change_line_end --dir dokumenty --ext txt --to crlf
```
4. Sprawdzenie wszystkich skryptów .sh w katalogu pod kątem typu zakończenia linii
```sh
shellman change_line_end --dir scripts --ext sh --check
```
Możliwe wyniki:
```sh
🔍 scripts/install.sh → LF
🔍 scripts/legacy_convert.sh → MIXED
```
⚠️ Uwagi
Musisz podać --file lub --dir.

Opcja 
--to lub --check jest wymagana.

Mieszane zakończenia linii (MIXED) oznaczają obecność zarówno LF, jak i CRLF w pliku. Zaleca się normalizację.
Filtr rozszerzeń (--ext) stosuj z --dir.
Działa na plikach tekstowych – dla binarnych wynik może być nieprawidłowy.

---
# 🔐 checksum_files

Generowanie i weryfikacja sum kontrolnych plików (SHA256, MD5, SHA1) w katalogach i projektach.

---

## 📝 Opis

To polecenie pozwala:
- **Generować** sumy kontrolne wszystkich plików w katalogu (z opcjonalnym filtrem rozszerzenia) i zapisywać je do pliku.
- **Weryfikować** integralność plików na podstawie wcześniej wygenerowanej listy sum (wykrywa modyfikacje lub uszkodzenia).
- Wybrać popularne algorytmy: **SHA256** (domyślnie), **MD5** lub **SHA1**.

Sumy kontrolne pomagają upewnić się, że pliki nie zostały zmienione np. podczas przesyłania, backupów czy wdrażania projektów.

---

## 🚦 Użycie

```sh
shellman checksum_files [OPCJE]
```
Opcje
```sh
--path ŚCIEŻKA
```
Katalog do skanowania (domyślnie: bieżący katalog .).
```sh
--ext ROZSZERZENIE
```
Uwzględnij tylko pliki z tym rozszerzeniem (np. --ext py).
```sh
--algo {sha256,md5,sha1}
```
Wybierz algorytm sumy (domyślnie: sha256).
```sh
--out PLIK
```
Nazwa pliku z listą sum (domyślnie: checksums.<algo>sum).
```sh
--verify
```
Weryfikuj pliki na podstawie istniejącej listy sum (czyta z pliku podanego w --out).
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku.

⚡ Przykłady
1. Generowanie sum SHA256 dla wszystkich plików w bieżącym katalogu
```sh
shellman checksum_files --algo sha256
```
Tworzy plik checksums.sha256sum z zawartością np.:

```sh
d2f0b8...  ./skrypt.py
342ab9...  ./dane/config.json
```
2. Generowanie sum MD5 dla wszystkich plików .txt w folderze docs
```sh
shellman checksum_files --path docs --ext txt --algo md5 --out docs.md5list
```
3. Weryfikacja plików na podstawie wcześniej wygenerowanej listy sum
```sh
shellman checksum_files --verify --out docs.md5list
```
Wyjście:

```sh
🔎 Verifying files via md5 list docs.md5list ...
✅ OK: docs/notes.txt
❌ MISMATCH: docs/draft.txt
❌ docs/old.txt not found
```
⚠️ Uwagi
Filtrowanie po rozszerzeniu (--ext) działa tylko z opcją katalogu (--path).

Domyślny plik wyjściowy to checksums.<algo>sum, np. checksums.sha256sum.

Podczas weryfikacji sprawdzane są wszystkie pliki i ich sumy – wszelkie niezgodności lub brakujące pliki zostaną zgłoszone.

Komenda działa na wszystkich typach plików, ale duże lub binarne pliki mogą wydłużyć czas działania.

Obsługiwane algorytmy: SHA256, MD5, SHA1.

---
# 🧹 clean_files

Usuwanie plików po nazwie, rozszerzeniu lub wieku – z podglądem i potwierdzeniem.

---

## 📝 Opis

To polecenie pozwala **oczyszczać projekt lub katalog** przez usuwanie plików:
- Z określonym **wzorem w nazwie** (podciąg w nazwie pliku)
- Z danym **rozszerzeniem** (np. `log`, `tmp`)
- **Starszych niż** wybrana liczba dni
- Lub dowolną **kombinacją** powyższych kryteriów

Możesz bezpiecznie **przeglądać** i **potwierdzać** usuwanie przed faktyczną operacją.

Świetnie sprawdza się do porządkowania logów, backupów, plików tymczasowych czy śmieci po budowie projektu!

---

## 🚦 Użycie

```sh
shellman clean_files [OPCJE]
```
Opcje
```sh
--path ŚCIEŻKA
```
Katalog do skanowania (domyślnie: bieżący katalog .)
```sh
--ext ROZSZERZENIE
```
Usuń pliki z tym rozszerzeniem (np. --ext log)
```sh
--name FRAGMENT
```
Usuń pliki, których nazwa zawiera podany fragment
```sh
--older-than DNI
```
Usuń tylko pliki starsze niż N dni
```sh
--dry-run
```
Podgląd: wyświetl, które pliki zostałyby usunięte, ale ich nie usuwaj
```sh
--confirm
```
Pytaj o potwierdzenie przed usunięciem każdego pliku (Y/n)
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku

⚡ Przykłady
1. Podgląd wszystkich plików .log do usunięcia w bieżącym katalogu
```sh
shellman clean_files --ext log --dry-run
```
2. Usuń pliki .tmp starsze niż 30 dni (z pytaniem o potwierdzenie)
```sh
shellman clean_files --ext tmp --older-than 30 --confirm
```
3. Usuń wszystkie pliki zawierające backup w nazwie (bez potwierdzenia)
```sh
shellman clean_files --name backup
```
4. Usuń pliki .bak w /var/data z podglądem
```sh
shellman clean_files --path /var/data --ext bak --dry-run
```
5. Usuń pliki .old zawierające report w nazwie i starsze niż 60 dni
```sh
shellman clean_files --ext old --name report --older-than 60 --dry-run
```

⚠️ Uwagi
Przynajmniej jedno z: --ext lub --name jest wymagane.

--older-than jest opcjonalne i pozwala ograniczyć wiekowo pliki.

Najpierw użyj --dry-run, aby upewnić się, które pliki zostaną usunięte.

Opcja --confirm zapewnia bezpieczeństwo – możesz zrezygnować z usuwania wybranych plików.

Wyszukiwanie jest wrażliwe na wielkość liter.

Usuwanie jest nieodwracalne – pliki nie trafiają do kosza!

---
# 📑 csv_extract

Ekstrakcja wybranych kolumn lub wierszy z pliku CSV, z filtrami i opcją eksportu.

---

## 📝 Opis

To polecenie pozwala szybko **wyciągać i filtrować dane z plików CSV**, np.:
- Wybierać konkretne kolumny (po numerach)
- Pobierać zakres wierszy
- Zostawiać lub wykluczać wiersze na podstawie tekstu
- Pomijać nagłówek, jeśli potrzeba
- Zapis do pliku lub podgląd interaktywny

Działa z każdym plikiem w formacie CSV – możesz ustawić dowolny separator.

---

## 🚦 Użycie

```sh
shellman csv_extract PLIK --cols KOLUMNY [OPCJE]
```
Argumenty:

PLIK – ścieżka do pliku CSV (wymagane)

Opcje:
```sh
--cols KOLUMNY
```
Wymagane. Kolumny do wybrania (liczone od 1), np. 1,3 lub 2-4.
```sh
--rows WIERSZE
```
Wiersze do wybrania (po nagłówku). Format: 2-10 lub 1,3,5.
```sh
--contains TEKST
```
Zostaw tylko wiersze zawierające ten tekst (niewrażliwe na wielkość liter).
```sh
--not-contains TEKST
```
Zostaw tylko wiersze nie zawierające tego tekstu.
```sh
--delim ZNAK
```
Separator w pliku CSV (domyślnie: ,).
```sh
--skip-header
```
Pomija pierwszą linię (nagłówek).
```sh
--output PLIK
```
Zapisz wynik do pliku zamiast wypisywać na ekran.
```sh
--interactive
```
Przekaż wynik do przeglądarki stron (np. less).
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku.

⚡ Przykłady
1. Ekstrakcja kolumn 2 i 4 z CSV
```sh
shellman csv_extract dane.csv --cols 2,4
```
2. Ekstrakcja kolumn 1–3 i tylko wierszy 2–10 (bez nagłówka)
```sh
shellman csv_extract dane.csv --cols 1-3 --rows 2-10 --skip-header
```
3. Eksport wierszy zawierających „error” w dowolnej kolumnie
```sh
shellman csv_extract dane.csv --cols 1,2 --contains error
```
4. Eksport wierszy nie zawierających „backup”, zapis do pliku
```sh
shellman csv_extract dane.csv --cols 1,3 --not-contains backup --output wynik.csv
```
5. Interaktywny podgląd dużego wyniku
```sh
shellman csv_extract dane.csv --cols 1,2,3 --interactive
```
⚠️ Uwagi
Zarówno --cols, jak i argument plik są wymagane.

Kolumny i wiersze liczone są od 1 (pierwsza kolumna = 1).

Możesz łączyć wybór kolumn, wierszy i filtrów.

Użyj tylko jednej z opcji: --contains lub --not-contains.

Dla niestandardowych separatorów (np. ;), użyj --delim ";".

--skip-header pomija tylko pierwszą linię (przydatne przy nagłówkach CSV).

Wynik drukowany jest na ekran, chyba że użyjesz --output.
---
# 📅 date_utils

Praca z datami: dodawanie/odejmowanie czasu, porównania, formatowanie – elastyczne narzędzie CLI.

---

## 📝 Opis

To polecenie pozwala:
- **Dodawać** lub **odejmować** czas od wybranej daty (lub bieżącej)
- **Porównywać** dwie daty (pokazuje różnicę w dniach, godzinach, minutach, sekundach)
- **Formatować** daty wg dowolnego wzoru [strftime](https://strftime.org/)
- Obsługuje popularne formaty: `YYYY-MM-DD` oraz `YYYY-MM-DD HH:MM:SS`

Świetne do automatyzacji, raportów lub szybkiej arytmetyki dat w terminalu.

---

## 🚦 Użycie

```sh
shellman date_utils [OPCJE]
```
Opcje
```sh
--date DATA
```
Data bazowa (domyślnie: teraz). Format: 2024-07-08 lub 2024-07-08 15:30:00.
```sh
--add OKRES
```
Dodaj czas do daty bazowej. Przykłady: 5d, 3w, 2h, 10min, 1m, 1y, 2q, 45s.
Wspierane jednostki:
```sh
d = dni
w = tygodnie
m = miesiące
y = lata
q = kwartały (3 miesiące)
h = godziny
min = minuty
s = sekundy
```
```sh
--sub OKRES
```
Odejmij czas od daty bazowej (te same formaty/jednostki co wyżej).
```sh
--diff DATA
```
Pokaż różnicę między datą bazową a tą datą (dni, godziny, minuty, sekundy).
```sh
--format WZÓR
```
Sformatuj datę/wynik wg strftime, np. %Y-%m-%d, %d/%m/%Y, %A, %H:%M.
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku.

⚡ Przykłady
1. Dodaj 3 dni do teraz
```sh
shellman date_utils --add 3d
```
2. Odejmij 2 miesiące od konkretnej daty
```sh
shellman date_utils --date 2023-10-01 --sub 2m
```
3. Różnica między dwoma datami
```sh
shellman date_utils --date 2024-01-01 --diff 2024-07-08
```
4. Formatowanie aktualnej daty
```sh
shellman date_utils --format "%A, %d-%m-%Y %H:%M"
```
5. Połącz obliczenia i formatowanie
```sh
shellman date_utils --date 2024-01-01 --add 1y --format "%Y/%m/%d"
```
⚠️ Uwagi
Wprowadź daty w formacie YYYY-MM-DD lub YYYY-MM-DD HH:MM:SS

Można wykonać tylko jedną operację --add lub --sub jednocześnie

Jednostki są niewrażliwe na wielkość liter (np. 10MIN działa)

Formatowanie według strftime – zobacz dokumentację po więcej kodów

Różnica (--diff) pokazuje także wartości ujemne (jeśli pierwsza data jest później niż druga)
---
# 🌳 dir_tree

Wizualne drzewo katalogów (jak polecenie `tree` w Uniksie) – z opcjami plików, głębokości, ASCII i nie tylko.

---

## 📝 Opis

To polecenie wyświetla uporządkowaną **strukturę drzewa** wskazanego katalogu:
- Zobacz hierarchię folderów i podfolderów na raz
- Możesz dodać pliki, nie tylko katalogi
- Ogranicz głębokość (przy dużych projektach)
- Zapisz wynik do pliku tekstowego
- Uwzględnij pliki/folery ukryte lub tylko jawne
- Wybierz między znakami Unicode i czystym ASCII

Przydatne do przeglądania kodu, dokumentowania repozytorium czy prezentacji struktury projektu.

---

## 🚦 Użycie

```sh
shellman dir_tree [ŚCIEŻKA] [OPCJE]
```
Argumenty:

ŚCIEŻKA – katalog do przejrzenia (domyślnie: bieżący katalog .)

Opcje:
```sh
--files
```
Uwzględnij pliki (nie tylko katalogi).
```sh
--depth N
```
Ogranicz zaglądanie do N poziomów w głąb.
```sh
--output PLIK
```
Zapisz drzewo do wskazanego pliku tekstowego.
```sh
--hidden
```
Pokaż ukryte pliki i foldery (nazwy zaczynające się od .).
```sh
--ascii
```
Użyj wyłącznie znaków ASCII do rysowania drzewa (przydatne np. do dokumentacji).
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku.

⚡ Przykłady
1. Drzewo katalogów (tylko foldery)
```sh
shellman dir_tree
```
2. Drzewo katalogów i plików do 2 poziomów w głąb
```sh
shellman dir_tree --files --depth 2
```
3. Z ukrytymi plikami i ASCII
```sh
shellman dir_tree --files --hidden --ascii
```
4. Zapisz strukturę projektu do pliku tree.txt
```sh
shellman dir_tree /home/user/projekt --output tree.txt
```
⚠️ Uwagi
Domyślnie wyświetlane są tylko katalogi – dodaj --files, by widzieć także pliki.

Maksymalna głębokość nieograniczona, chyba że ustawisz --depth.

Niektóre katalogi mogą być chronione (błąd dostępu zostanie oznaczony).

Tryb ASCII sprawdza się przy umieszczaniu drzewa w zwykłych plikach tekstowych lub markdown.
---
# 🔒 encrypt_files

Szyfruj lub odszyfruj pliki w folderze silnym algorytmem AES-256 z hasłem.

---

## 📝 Opis

To polecenie pozwala:
- **Zaszyfrować** wszystkie pasujące pliki w katalogu (można filtrować po rozszerzeniu) za pomocą **AES-256** i hasła.
- **Odszyfrować** pliki `.enc` przy pomocy poprawnego hasła.
- Pliki wynikowe trafiają domyślnie do folderów `encrypted/` lub `decrypted/` (możesz wskazać własny folder przez `--out`).

Szyfrowanie odbywa się w trybie AES-256-CBC, z losowym salt i IV dla każdego pliku. Klucz wyliczany jest przez PBKDF2-HMAC-SHA256 (100 000 iteracji).

**Idealne do backupów, wysyłania poufnych plików lub ochrony tajemnic w projektach.**

---

## 🚦 Użycie

```sh
shellman encrypt_files --mode {encrypt|decrypt} --password HASŁO [OPCJE]
```
Opcje
```sh
--mode {encrypt, decrypt}
```
Wymagane. Wybierz szyfrowanie lub deszyfrowanie.
```sh
--password HASŁO
```
Wymagane. Hasło do szyfrowania/odszyfrowania plików (nie zgub go!).
```sh
--ext ROZSZERZENIE
```
Przetwarzaj tylko pliki o danym rozszerzeniu (np. --ext pdf).
```sh
--path KATALOG
```
Katalog do skanowania (domyślnie: bieżący katalog).
```sh
--out KATALOG
```
Folder wyjściowy (domyślnie: encrypted/ lub decrypted/).
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku.

⚡ Przykłady
1. Zaszyfruj wszystkie pliki w bieżącym katalogu
```sh
shellman encrypt_files --mode encrypt --password MojeHaslo
```
2. Szyfruj tylko pliki .pdf z folderu docs/ do moje_szyfrowane/
```sh
shellman encrypt_files --mode encrypt --password Tajne123 --path docs --ext pdf --out moje_szyfrowane
```
3. Odszyfruj wszystkie pliki .enc z katalogu backup/ przy użyciu hasła
```sh
shellman encrypt_files --mode decrypt --password MojeHaslo --path backup
```
⚠️ Uwagi
Hasło nie jest nigdzie zapisywane – zgubienie go oznacza trwałą utratę danych!

Odszyfrowane pliki przywracają oryginalną nazwę (bez .enc).

Wymagane są opcje --mode i --password.

Klucz wyliczany przez PBKDF2 z 100 000 iteracjami dla bezpieczeństwa.

Każdy plik ma własny salt i IV.

To nie jest substytut szyfrowania całych dysków ani bezpiecznych sejfów na pliki!

---
# 📋 excel info

Wyświetl wszystkie arkusze Excela z liczbą wierszy i kolumn.

---

## 📝 Opis

Wypisuje każdy arkusz podanej tabeli `.xlsx`, pokazując:
- Nazwę arkusza
- Liczbę wierszy
- Liczbę kolumn

Idealne do szybkiego sprawdzenia struktury pliku Excel.

---

## 🚦 Użycie

```sh
shellman excel info PLIK.xlsx
```
⚡ Przykład
```sh
shellman excel info dane.xlsx
```
Wyjście:

```sh
Sheet                 Rows   Cols
----------------------------------
Arkusz1                125      8
Podsumowanie            12      4
```
⚠️ Uwagi
PLIK musi być prawidłowym plikiem Excela (.xlsx).

Odczyt tylko do podglądu – bezpieczne dla dużych plików.
---

# 👁️ excel preview

Podgląd pierwszych N wierszy lub wybranych kolumn wskazanego arkusza Excela.

---

## 📝 Opis

Wyświetla podgląd danych z arkusza Excela:
- Wybór arkusza po numerze lub nazwie (domyślnie: pierwszy)
- Wybór kolumn (np. `A,C-E`)
- Ograniczenie liczby wierszy
- Numery wierszy, nagłówki, separator `|`
- Wyjście jako tabela lub surowy CSV

Możesz zapisać podgląd do pliku lub przeglądać interaktywnie (stronicowanie).

---

## 🚦 Użycie

```sh
shellman excel preview PLIK.xlsx [--sheet NAZWA/NR] [--rows N] [--columns SPEC] [OPCJE]
```
Opcje
```sh
--sheet
```
Nazwa lub numer arkusza (domyślnie: 1)
```sh
--rows
```
Liczba wierszy do podglądu (domyślnie: 20)
```sh
--columns
```
Kolumny, np. A,C-E
```sh
--output
```
Zapisz podgląd do pliku
```sh
--interactive
```
Podgląd w pagerze (np. less)
```sh
--info, -i
```
Pokaż nagłówki, numery wierszy i separator |

⚡ Przykłady
Podgląd kolumn A oraz C-E z 2. arkusza, pierwsze 10 wierszy:

```sh
shellman excel preview dane.xlsx --sheet 2 --rows 10 --columns A,C-E -i
```
Zapisz 50 pierwszych wierszy z arkusza "Raport" do pliku:

```sh
shellman excel preview dane.xlsx --sheet Raport --rows 50 --output out.csv
```
⚠️ Uwagi
PLIK musi być .xlsx

Kolumny: A, B, C-E itd.

Opcja --info wyświetla tabelę z numerami wierszy.

---
# ⬇️ excel export

Eksportuj jeden lub więcej arkuszy Excela (lub wybrane wiersze/kolumny) do plików CSV.

---

## 📝 Opis

Eksportuje dane z Excela do CSV:
- Wybór arkuszy po nazwie lub numerze
- Wybór wierszy (zakres, np. `2-100`)
- Wybór kolumn (np. `A,B-D`)
- Każdy arkusz jako osobny plik CSV
- Nadpisywanie lub nowe pliki (z timestampem)

Pliki trafiają do wybranego katalogu (domyślnie: `csv/`).

---

## 🚦 Użycie

```sh
shellman excel export PLIK.xlsx [--sheets NAZWA/NR ...] [--rows START-KONIEC] [--columns SPEC] [OPCJE]
```
Opcje
```sh
--sheets
```
Nazwy lub numery arkuszy do eksportu (wiele dozwolonych)
```sh
--rows
```
Zakres wierszy, np. 2-100
```sh
--columns
```
Kolumny, np. A,B-D
```sh
--out
```
Katalog wyjściowy (domyślnie: csv/)
```sh
--overwrite
```
Nadpisuj pliki (bez timestampu w nazwie)
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku

⚡ Przykłady
Eksport wszystkich arkuszy do csv/:

```sh
shellman excel export dane.xlsx
```
Eksport arkusza "Dane", wiersze 2-50, kolumny A-E, nadpisz plik:
```sh
shellman excel export dane.xlsx --sheets Dane --rows 2-50 --columns A-E --overwrite
```
Eksport arkuszy 1 i 3 do folderu out/:

```sh
shellman excel export dane.xlsx --sheets 1 --sheets 3 --out out
```
⚠️ Uwagi
Obsługiwane są tylko pliki .xlsx

Każdy arkusz to osobny plik CSV

Bez --overwrite pliki mają w nazwie timestamp
---
# 🔄 file_convert

Konwersja między formatami JSON, YAML i TOML jednym poleceniem.

---

## 📝 Opis

Przekształcaj pliki danych pomiędzy popularnymi formatami:
- **JSON ↔ YAML**
- **JSON ↔ TOML**
- **YAML ↔ TOML**

Możesz wydrukować wynik jako sformatowany (czytelny), zapisać do pliku lub podejrzeć interaktywnie.

Przydatne przy migracji konfiguracji, konwersji danych do różnych narzędzi czy porządkowaniu formatów.

---

## 🚦 Użycie

```sh
shellman file_convert PLIK --from FORMAT --to FORMAT [OPCJE]
```
Argumenty i opcje
PLIK
Ścieżka do pliku wejściowego (wymagane)
```sh
--from FORMAT
```
Wymagane. Format wejściowy: json, yaml lub toml
```sh
--to FORMAT
```
Wymagane. Format wyjściowy: json, yaml lub toml
```sh
--output PLIK
```
Zapisz wynik do pliku
```sh
--pretty
```
Sformatuj wynik dla czytelności (tylko JSON/YAML)
```sh
--interactive
```
Podejrzyj wynik w pagerze (np. less)
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku

⚡ Przykłady
1. Konwersja YAML do JSON i wydruk na ekran
```sh
shellman file_convert config.yaml --from yaml --to json --pretty
```
2. Konwersja TOML do YAML i zapis do pliku
```sh
shellman file_convert pyproject.toml --from toml --to yaml --output config.yaml
```
3. Konwersja JSON do TOML i podgląd w trybie interaktywnym
```sh
shellman file_convert settings.json --from json --to toml --interactive
```

⚠️ Uwagi
Musisz podać oba formaty: --from oraz --to.

Obsługiwane są tylko tekstowe pliki UTF-8.

Formatowanie czytelne (--pretty) dostępne tylko dla JSON i YAML.

Narzędzie stara się zachować strukturę oraz komentarze (o ile pozwala na to format).

Błędy parsowania (np. niepoprawny JSON) zatrzymują polecenie.
---
# 📊 file_stats

Wyświetl pełną ścieżkę, rozmiar, liczbę linii i rozszerzenie każdego pliku – opcjonalnie z metadanymi.

---

## 📝 Opis

To polecenie zbiera i pokazuje statystyki plików:
- Wyświetla ścieżkę, liczbę linii, rozmiar, rozszerzenie
- Wspiera rekurencyjne przeszukiwanie katalogów
- Opcjonalnie pokazuje metadane (daty utworzenia/modyfikacji, typ, kodowanie)
- Filtruje po rozszerzeniu, umożliwia zapis wyników do loga

Idealne do audytów kodu, sprawdzania repozytoriów, czy szybkiego raportowania plików.

---

## 🚦 Użycie

```sh
shellman file_stats [ŚCIEŻKI...] [OPCJE]
```
Argumenty:

ŚCIEŻKI...
Lista plików lub katalogów (dowolna liczba; wymagane)

Opcje:
```sh
--ext ROZSZERZENIE
```
Uwzględnij tylko pliki o tym rozszerzeniu (np. py)
```sh
--meta
```
Pokaż metadane: utworzony, zmodyfikowany, typ, kodowanie
```sh
--output
```
Zapisz wynik do logs/file_stats_<timestamp>.log
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku

⚡ Przykłady
1. Statystyki pojedynczego pliku
```sh
shellman file_stats main.py
```
2. Rekurencyjne raportowanie plików .txt w katalogu docs/
```sh
shellman file_stats docs --ext txt
```
3. Statystyki wszystkich plików w katalogach src i test + metadane
```sh
shellman file_stats src test --meta
```
4. Zapisz raport do pliku logu
```sh
shellman file_stats mydir --output
```
⚠️ Uwagi
Możesz podać wiele plików lub katalogów naraz.

Katalogi są przeszukiwane rekurencyjnie.

Dla plików binarnych liczba linii może być bez sensu.

Typ i kodowanie pliku wykrywane są heurystycznie (biblioteka chardet).
---
# 🔍 find_files

Wyszukiwanie plików po nazwie, rozszerzeniu lub treści – z elastycznym filtrowaniem i opcjami zapisu.

---

## 📝 Opis

To polecenie pozwala przeszukiwać katalog i podkatalogi po:
- Nazwie (dowolny fragment w nazwie pliku)
- Rozszerzeniu pliku (np. tylko `.py` lub `.txt`)
- Zawartości pliku (znajdź pliki zawierające określony tekst)
- Możesz łączyć filtry!

Dodatkowo możesz wyświetlić rozmiary plików i zapisać wyniki do pliku logu.

---

## 🚦 Użycie

```sh
shellman find_files ŚCIEŻKA [OPCJE]
```
Argumenty i opcje
ŚCIEŻKA
Katalog do przeszukania (wymagany, rekurencyjnie)
```sh
--name FRAGMENT
```
Dopasuj pliki, których nazwa zawiera podany fragment
```sh
--content TEKST
```
Wyszukaj pliki zawierające podany tekst (UTF-8)
```sh
--ext ROZSZERZENIE
```
Uwzględnij tylko pliki o tym rozszerzeniu (np. --ext py)
```sh
--output
```
Zapisz wyniki do logs/find_files_<timestamp>.log
```sh
--show-size
```
Pokaż rozmiar każdego pliku (w KB lub MB)
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku

⚡ Przykłady
1. Znajdź wszystkie pliki z „log” w nazwie w ./data
```sh
shellman find_files ./data --name log
```
2. Znajdź pliki .md zawierające słowo „draft”
```sh
shellman find_files docs --ext md --content draft
```
3. Znajdź wszystkie pliki .py i pokaż ich rozmiary
```sh
shellman find_files src --ext py --show-size
```
4. Zapisz wszystkie znalezione pliki .csv do pliku logu
```sh
shellman find_files exports --ext csv --output
```
⚠️ Uwagi
ŚCIEŻKA musi być istniejącym katalogiem.

Możesz łączyć dowolne filtry (nazwa, rozszerzenie, treść).

Szukanie po treści jest wrażliwe na wielkość liter i działa tylko dla plików UTF-8.

Pliki binarne lub z błędami odczytu są pomijane.

Przeszukiwanie zawsze obejmuje podkatalogi (rekurencja).
---
# 🗂️ json_extract

Ekstrakcja i filtrowanie danych JSON z opcjonalnym wyborem pól.

---

## 📝 Opis

To polecenie pozwala:
- **Ekstrahować** dane z pliku JSON, nawigując po zagnieżdżeniach ścieżką z kropkami (`--path`)
- **Filtrować** elementy listy po wartości wybranego pola (np. tylko `status=active`)
- **Wybrać pola** do wyświetlenia w wyniku (np. tylko `id,nazwa`)
- Wyniki są wypisywane jako osobne obiekty JSON w każdej linii, na ekran lub do pliku, opcjonalnie z podglądem stronicowanym

Idealne do szybkiego wydobywania, przetwarzania czy analizy dużych JSON-ów, logów lub eksportów API.

---

## 🚦 Użycie

```sh
shellman json_extract PLIK [OPCJE]
```
Opcje
PLIK
Plik wejściowy JSON (wymagany)
```sh
--path KLUCZ.ŚCIEŻKA
```
Ścieżka do listy lub obiektu, np. items, dane.wyniki, root.items
```sh
--filter KLUCZ=WARTOŚĆ
```
Uwzględnij tylko elementy, gdzie KLUCZ == WARTOŚĆ (porównanie tekstowe)
```sh
--fields POLE1,POLE2,...
```
Wyświetl tylko te pola
```sh
--output PLIK
```
Zapisz wynik do pliku zamiast na ekran
```sh
--interactive
```
Przekaż wynik do pagera (np. less)
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku

⚡ Przykłady
1. Wyodrębnij listę główną z dane.json
```sh
shellman json_extract dane.json
```
2. Wyodrębnij elementy zagnieżdżone i przefiltruj po polu
```sh
shellman json_extract dane.json --path dane.items --filter status=active
```
3. Wyświetl tylko wybrane pola jako JSONL
```sh
shellman json_extract dane.json --path users --fields id,nazwa
```
4. Zapisz przefiltrowane wyniki do pliku i przeglądaj interaktywnie
```sh
shellman json_extract logs.json --path logs --filter level=ERROR --fields time,message --output errors.jsonl --interactive
```
⚠️ Uwagi
Jeśli ścieżka nie prowadzi do listy, wynik zostanie opakowany w listę.

Filtrowanie porównuje wartości tekstowo.

Przy --fields pokazane będą tylko wybrane pola w każdym obiekcie.

Wynik to zawsze jeden obiekt JSON na linię (format JSONL).

Działa tylko z poprawnymi plikami JSON UTF-8.
---
# 📏 lines

Ekstrakcja, liczenie i podsumowanie linii w plikach oraz folderach – z zaawansowanymi filtrami i kontekstem.

---

## 📝 Opis

To polecenie pozwala:
- **Wydobywać** pasujące linie z plików (z kontekstem przed/po)
- **Liczyć** linie spełniające filtry lub wyrażenia regularne
- **Podsumowywać**: liczba plików, linii, trafień
- Filtrować po treści, regexie, rozszerzeniu
- Pokazywać procent trafień, rozmiar pliku, zapisywać wyniki do logów
- Łączyć opcje dla zaawansowanej analizy tekstu i plików

---

## 🚦 Użycie

```sh
shellman lines [PLIKI LUB FOLDERY...] [OPCJE]
```
Opcje
```sh
--extract
```
Wypisz pasujące linie (domyślnie, jeśli nie wybrano innego trybu)
```sh
--count
```
Pokaż tylko liczbę pasujących linii
```sh
--summary
```
Pokaż podsumowanie: liczba plików, linii, trafień
```sh
--contains TEKST
```
Uwzględnij linie zawierające ten tekst
```sh
--not-contains TEKST
```
Uwzględnij linie, które NIE zawierają tego tekstu
```sh
--regex WZORZEC
```
Dopasuj linie wyrażeniem regularnym
```sh
--ignore-case
```
Ignoruj wielkość liter
```sh
--before N
```
Pokaż N linii przed trafieniem (kontekst)
```sh
--after N
```
Pokaż N linii po trafieniu (kontekst)
```sh
--ext ROZSZERZENIE
```
Uwzględnij tylko pliki o tym rozszerzeniu
```sh
--percent
```
Pokaż procent trafień względem wszystkich linii
```sh
--output PLIK
```
Zapisz wynik do pliku
```sh
--interactive
```
Podgląd wyniku w pagerze (np. less)
```sh
--show-size
```
Pokaż rozmiar pliku przy wyniku
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku

⚡ Przykłady
1. Wypisz linie z „TODO” w plikach .py
```sh
shellman lines src --ext py --contains TODO
```
2. Policz liczbę i procent linii dopasowanych przez regex
```sh
shellman lines logs.txt --regex "ERROR.*" --count --percent
```
3. Wydobądź linie (z 2 liniami przed i 1 po) z folderu
```sh
shellman lines logs/ --contains WARNING --before 2 --after 1
```
4. Podsumowanie wszystkich plików .txt w katalogu
```sh
shellman lines data --ext txt --summary
```
5. Zapisz pasujące linie do pliku i podglądaj interaktywnie
```sh
shellman lines myfile.txt --contains "secret" --output results.log --interactive
```
⚠️ Uwagi
Domyślnie aktywne jest --extract, jeśli nie wybrano innego trybu.

Nie można łączyć --contains i --regex.

Argumenty mogą być plikami i/lub katalogami (katalogi rekurencyjnie).

Bez filtra wyświetlane są wszystkie linie.

Opcje --before i --after dodają kontekst do każdego trafienia.

Pliki nie-UTF-8 mogą być czytane z pomijaniem błędów.
---
# 🛡️ open_ports

Wyświetl otwarte porty TCP/UDP i porty szeregowe (COM/LPT/tty) z procesem, PID, stanem i opisem urządzenia.

---

## 📝 Opis

To polecenie pozwala:
- Wypisać wszystkie otwarte porty TCP i UDP z nazwą procesu oraz PID
- Filtrować wyniki po protokole (`tcp` lub `udp`) lub po lokalnym numerze portu
- Wyświetlać wyniki w tabeli lub jako surowy JSON (do automatyzacji/skryptów)
- Pokazywać fizyczne porty szeregowe i równoległe (COM, LPT, tty, cu) wraz z opisem urządzenia (działa na Linux, macOS i Windows)

Obsługa wielu platform. Do pełnych możliwości wymagane są pakiety `psutil` i `pyserial`.

---

## 🚦 Użycie

```sh
shellman open_ports [OPCJE]
```
Opcje
```sh
--proto {tcp, udp}
```
Filtrowanie tylko po TCP lub tylko po UDP
```sh
--port N
```
Filtrowanie po lokalnym porcie (np. --port 8080)
```sh
--json
```
Wyjście jako surowy JSON (nie tabela)
```sh
--serial
```
Lista portów szeregowych/równoległych (COM, LPT, tty, cu) z opisem urządzenia
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku

⚡ Przykłady
1. Wypisz wszystkie otwarte porty TCP i UDP z info o procesach
```sh
shellman open_ports
```
2. Pokaż tylko otwarte porty TCP
```sh
shellman open_ports --proto tcp
```
3. Znajdź procesy nasłuchujące na porcie 5432
```sh
shellman open_ports --port 5432
```
4. Wyjście jako JSON (do skryptów, logów, audytu)
```sh
shellman open_ports --json
```
5. Lista portów szeregowych/równoległych z opisem urządzenia
```sh
shellman open_ports --serial
```
⚠️ Uwagi
Dane TCP/UDP zbierane są z pomocą biblioteki psutil.

Lista portów szeregowych wymaga pyserial; na POSIX fallback do wyszukiwania po nazwach urządzeń.

Przy pierwszym uruchomieniu psutil może być doinstalowany automatycznie (wymagany internet).

Bez uprawnień możesz nie widzieć wszystkich portów/procesów.

Wyjście JSON zawiera wszystkie pola: protokół, pid, proces, adresy lokalny/zdalny, stan.
---
# ✏️ replace_text

Zamieniaj wystąpienia tekstu w wielu plikach – z podglądem, diffem i interaktywnym potwierdzeniem.

---

## 📝 Opis

To polecenie pozwala:
- **Znajdować i zamieniać** tekst w wielu plikach jednocześnie (rekurencyjnie w katalogu)
- Filtrować pliki po rozszerzeniu
- Podglądać zmiany jako unified diff przed zapisaniem
- Potwierdzać każdą zamianę interaktywnie
- Bezpiecznie masowo edytować configi, kod, dokumentację i notatki

---

## 🚦 Użycie

```sh
shellman replace_text ŚCIEŻKA --find TEKST --replace TEKST [OPCJE]
```
Opcje
ŚCIEŻKA
Katalog do przeszukania (wymagany)
```sh
--find TEKST
```
Wymagane. Szukany tekst
```sh
--replace TEKST
```
Wymagane. Tekst zamienny
```sh
--ext ROZSZERZENIE
```
Przetwarzaj tylko pliki o danym rozszerzeniu
```sh
--in-place
```
Zapisz zmiany do plików (domyślnie tylko podgląd)
```sh
--preview
```
Pokaż unified diff proponowanych zmian
```sh
--confirm
```
Pytaj o potwierdzenie każdej zamiany
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku

⚡ Przykłady
1. Zamień "foo" na "bar" w plikach .md w katalogu docs/ (tylko podgląd)
```sh
shellman replace_text docs --find foo --replace bar --ext md --preview
```
2. Zamień "localhost" na "127.0.0.1" w plikach konfiguracyjnych z pytaniem o potwierdzenie
```sh
shellman replace_text config --find localhost --replace 127.0.0.1 --ext conf --in-place --confirm
```
3. Masowa aktualizacja roku copyright w projekcie
```sh
shellman replace_text . --find "Copyright 2023" --replace "Copyright 2024" --ext py --in-place --preview
```
⚠️ Uwagi
Zmiany są zapisywane tylko jeśli podasz --in-place; inaczej to tylko podgląd.

Połączenie --preview i --in-place daje podgląd diffów przed zapisem.

Z opcją --confirm pojawia się pytanie (Y/n) dla każdego pliku.

Przetwarzane są tylko pliki zawierające wyszukiwany tekst.

Przeszukuje podkatalogi rekurencyjnie.

Działa na plikach tekstowych (UTF-8, błędy odczytu ignorowane).

Filtrowanie po rozszerzeniu dotyczy sufiksu pliku (np. .md).
---
# 🚀 speed_test

Szybki test prędkości internetu (pobieranie, wysyłanie, ping) – z automatycznym wyborem najszybszej metody.

---

## 📝 Opis

Polecenie wykonuje test prędkości łącza i pokazuje:
- Prędkość pobierania (Mbps)
- Prędkość wysyłania (Mbps)
- Ping (ms)

Automatycznie wybiera najlepsze dostępne narzędzie:
1. **Ookla CLI** (`speedtest` – oficjalny binarny klient)
2. **speedtest-cli** (wersja binarna Pythona)
3. **speedtest-cli** (moduł Python, automatyczna instalacja jeśli brak)

Wynik wyświetlany jest jako tekst lub surowy JSON – idealne do raportów, monitoringu lub diagnostyki.

---

## 🚦 Użycie

```sh
shellman speed_test [OPCJE]
```
Opcje
```sh
--json
```
Zwróć wynik jako surowy JSON z download/upload/ping
```sh
--only {download, upload, ping}
```
Pokaż tylko jeden parametr (np. --only download)
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku

⚡ Przykłady
1. Pełny test prędkości
```sh
shellman speed_test
```
2. Pokaż tylko prędkość pobierania
```sh
shellman speed_test --only download
```
3. Wynik jako JSON
```sh
shellman speed_test --json
```
⚠️ Uwagi
Jeśli dostępny, używany będzie oficjalny speedtest od Ookla.

W razie braku, polecenie użyje speedtest-cli (może automatycznie doinstalować).

Wyniki zależą od rzeczywistego łącza, pory dnia i wybranego serwera.

Test może potrwać kilka sekund.

Przy pierwszym użyciu wymagane jest aktywne połączenie internetowe (by doinstalować backendy).
---
# 🖥️ sys_summary

Podsumowanie systemu, powłoki i środowiska narzędziowego – cross-platformowy raport sprzętu i OS (Linux, macOS, Windows).

---

## 📝 Opis

To polecenie daje pełne podsumowanie Twojego systemu, w tym:
- **System operacyjny, wersja, architektura, host, info o WSL**
- **Numer seryjny** (jeśli dostępny)
- **CPU**: model, liczba rdzeni, częstotliwość
- **Czujniki/temperatura** (jeśli wspierane)
- **GPU**: wykryte karty graficzne
- **Bateria**: poziom, ładowanie, czas pozostały
- **Bluetooth**: wykryte urządzenia / adaptery
- **Narzędzia**: `python3`, `jq`, `xlsx2csv` itd.
- **Pamięć**: całkowita, używana, wolna
- **Uptime & Load**: od ostatniego uruchomienia, obciążenie
- **Dyski**: zużycie, wolne miejsce na partycjach
- **Sieć**: lokalny/publiczny IP, interfejsy
- **Pakiety**: rodzaj menedżera, liczba zainstalowanych pakietów
- **Drukarki**: wykryte drukarki
- **Wi-Fi**: połączony SSID (jeśli dostępny)
- **Monitory**: rozdzielczości ekranów, liczba wyświetlaczy

Działa na Linuxie, macOS i Windows, automatycznie dostosowuje się do systemu.

---

## 🚦 Użycie

```sh
shellman sys_summary [--lang-help pl|eng]
```
⚡ Przykładowy output (Linux)
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

🌡️  Czujniki / Temperatura
────────────────────────────────────────────
coretemp: temp = 48.0 °C

🖥️  GPU
────────────────────────────────────────────
GPU          : Intel Iris Xe Graphics

🔋  Bateria
────────────────────────────────────────────
Percent      : 85%
Plugged in   : Yes
Time left    : 2:34:00

📡  Bluetooth
────────────────────────────────────────────
Powered: yes

🛠️  Narzędzia
────────────────────────────────────────────
python3      : /usr/bin/python3
jq           : /usr/bin/jq
xlsx2csv     : /usr/local/bin/xlsx2csv

🧠  Pamięć
────────────────────────────────────────────
              total        used        free      shared  buff/cache   available
Mem:           15Gi       3.7Gi       8.1Gi       400Mi       3.3Gi        11Gi
Swap:         2.0Gi       0.0Ki       2.0Gi

⏱️  Uptime & Load
────────────────────────────────────────────
Uptime       : up 4 days, 5 hours, 12 minutes
Load Avg.    : 0.65, 0.45, 0.35

💾  Dyski
────────────────────────────────────────────
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  470G   60G  387G  14% /

🌐  Sieć
────────────────────────────────────────────
Local IP     : 192.168.0.13
Public IP    : 83.12.45.67

📦  Pakiety
────────────────────────────────────────────
Pkg Manager  : apt
Total pkgs   : 2024

🖨️  Drukarki
────────────────────────────────────────────
Printer      : HP_LaserJet

📶  Wi-Fi
────────────────────────────────────────────
Connected SSID: Domowy_5G

🖥️  Monitory
────────────────────────────────────────────
eDP-1 connected primary 1920x1080+0+0
HDMI-1 disconnected
```
⚠️ Uwagi
Niektóre pola wymagają uprawnień administratora/roota (np. numer seryjny, czujniki, dmidecode).

Część informacji może być niedostępna lub ograniczona zależnie od platformy/sprzętu.

Bateria, czujniki, Bluetooth, drukarki, Wi-Fi mogą nie być obecne w serwerach lub VM.

Pełne info sprzętowe w Windows uzyskasz tylko z PowerShell/CMD (nie Git Bash).
---

# 📦 zip_batch

Twórz archiwa ZIP z folderów lub plików hurtowo, z filtrem rozszerzeń i opcjonalnym hasłem.

---

## 📝 Opis

Szybko kompresuj i archiwizuj wiele plików lub katalogów:
- **Archiwizacja wszystkich plików** (opcjonalnie tylko z wybranym rozszerzeniem) z katalogu źródłowego
- **Tryb per-folder:** Jeden ZIP dla każdego podfolderu (z pominięciem plików z głównego poziomu)
- **Własny prefix** nazw archiwów
- **Ochrona hasłem** (uwaga: ZIP `-P` to słabe szyfrowanie!)
- Wyniki trafiają do wybranego katalogu (domyślnie: `./zips`)

Wymaga narzędzia `zip` w systemie.

---

## 🚦 Użycie

```sh
shellman zip_batch [OPCJE]
```
Opcje
```sh
--path KATALOG
```
Katalog źródłowy do skanowania (domyślnie: bieżący katalog)
```sh
--ext ROZSZERZENIE
```
Uwzględnij tylko pliki o tym rozszerzeniu (np. --ext txt)
```sh
--per-folder
```
Jeden ZIP dla każdego bezpośredniego podfolderu
```sh
--output KATALOG
```
Folder wyjściowy na ZIPy (domyślnie: ./zips)
```sh
--name PREFIX
```
Prefix do nazw archiwów (domyślnie: batch_)
```sh
--password HASŁO
```
Ustaw hasło do ZIPa (zip -P; słabe szyfrowanie)
```sh
--lang-help {pl,eng}
```
Wyświetl tę pomoc po polsku lub angielsku

⚡ Przykłady
1. Zarchiwizuj wszystkie pliki z reports/ do jednego ZIPa
```sh
shellman zip_batch --path reports
```
2. Osobne archiwa dla każdego folderu w datasets/ (per-folder)
```sh
shellman zip_batch --path datasets --per-folder --name data_
```
3. Spakuj tylko pliki .csv do folderu myzips/
```sh
shellman zip_batch --ext csv --output myzips
```
4. ZIP z hasłem dla wszystkich plików .pdf
```sh
shellman zip_batch --ext pdf --password MojeHaslo123
```

⚠️ Uwagi
Wymaga narzędzia zip (Linux/macOS/WSL/Windows z zip.exe).

Szyfrowanie hasłem (-P) jest słabe – nie używaj do ochrony wrażliwych danych!

Opcja --per-folder tworzy archiwum dla każdego podfolderu bezpośredniego (pomija pliki z głównego poziomu).

Nazwy archiwów mają prefix (domyślnie: batch_) i znacznik czasu w trybie batch.
---
## ❤️ Współpraca

Masz pomysł lub poprawkę? Zgłoś pull-request lub otwórz issue.
Każde narzędzie znajduje się w shellman/commands/ – śmiało dodaj własne!

