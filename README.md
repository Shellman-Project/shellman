## ☕ Sponsor me

If my projects are helpful and worth developing, you can buy me a coffee:

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-☕️-yellow?style=flat&logo=buymeacoffee)](https://buycoffee.to/jakubmarciniak)


# 🐚 Shellman – your friendly terminal assistant

Shellman is a modular CLI toolkit for everyday file‑, log‑ and project‑chores.  
Every feature lives in its own **`commands/<name>.sh`** script, so the toolbox grows with you.

---

## 🚀 One‑liner system‑wide install

```bash
curl -sSL https://raw.githubusercontent.com/JakubMarciniak93/shellman/main/install_shellman_system_wide.sh \
  | sudo bash
```

Installs code to /usr/local/lib/shellman and links
/usr/local/bin/shellman so every user on the machine can simply type shellman.

---

🏁 Quick start (local clone)
```bash
git clone https://github.com/JakubMarciniak93/shellman.git
cd shellman
```

# one‑shot install for the current user
```bash
./install.sh
```

---

✅ First step after installing
```bash
shellman doctor        # overview
shellman doctor --fix  # auto‑repair (installs zip, fixes perms, etc.)

./install.sh
```

---

📚 Command overview


|Command | What it does|
|------|---------|
|count_lines | Count lines in files — text / regex filters, summaries, export|
|file_stats | Full path, readable size, line count, extension (--ext, --output)|
|find_files | Search files by name fragment, extension or content (--show-size, --output)|
|replace_text | Safe find‑&‑replace across files with preview / confirm|
|merge_files | Concatenate many text files into one (headers, sorting)|
|encrypt_files | AES‑256 encrypt / decrypt files with password → .enc|
|clean_files | Delete temp / backup files (--dry-run, age filter, confirm)|
|extract_lines | Grab lines that (don’t) match text, with N lines of context|
|csv_extract | Pull selected columns / rows from a CSV, save or print|
|checksum_files | Generate / verify SHA‑256 / MD5 checksum lists|
|zip_batch | Batch‑zip files or folders, per‑folder mode, optional password|
|tail_follow | Live tail -f on a single file with filter & highlight|
|excel_info | Quick overview of Excel (.xlsx, .xlsm, .xlsb - .xls not supported) – sheet names, rows, columns |
|excel_preview | Preview first N rows / chosen columns, optional CSV export |
|excel_to_csv | Batch‑export one or more sheets to individual CSV files |
|json_extract | Extract and filter JSON using jq expressions |
|sys_summary | Sustem Summary |
|file_convert |Convert between JSON, YAML, TOML (auto-detect, pretty, save/view)|
|update | Pull newest source, reinstall and relink|
|install_bats | Install the BATS Bash test framework (for Shellman tests)|
|doctor | Diagnose installation; --fix auto‑installs missing deps|


---

🧪 Running the test‑suite
```bash
shellman install_bats   # installs BATS once
bats tests/             # run all *.bats tests
```

---

## 📏 Command • `count_lines`

> Quickly count lines in one or many files & folders, with text / regex filtering, summary mode and optional log export.

| Flag | Purpose |
|------|---------|
| `--contains <text>` | Count only lines that contain **literal** `<text>` |
| `--regex <pattern>` | Count lines matching a **regular expression** |
| `--ignore-case` | Case‑insensitive search (works with both flags above) |
| `--ext <ext>` | Process only files with given extension, e.g. `txt` |
| `--summary` | Show totals per file **and** grand total |
| `--percent` | Print match percentage relative to each file |
| `--output` | Save result to `logs/count_lines_<timestamp>.log` |
| `--interactive` | Pipe result to `less` for comfy browsing |
| `--show-size` | Append human‑readable file size (B / KB / MB) |
| `--help` | Show built‑in help |

### Usage

```bash
shellman count_lines <file(s) | folder(s)> [options]
```
---

## 🗂️ Command • `file_stats`

> Display quick, per‑file facts — full path, human‑readable size, line count and extension.

| Flag | Purpose |
|------|---------|
| `--ext <ext>` | Process only files whose extension equals `<ext>` |
| `--output` | Save the full report to `logs/file_stats_<timestamp>.log` |
| `--help` | Show built‑in help |

### Usage

```bash
shellman file_stats <file(s) | folder(s)> [options]
```

|Example | What happens|
|------|---------|
|shellman file_stats readme.md | prints path,  size (XX KB), line count, extension .md|
|shellman file_stats src include --ext sh | scans both folders, shows stats for every *.sh file|
|shellman file_stats ./scripts --ext py --output | writes the table to logs/file_stats_YYYYMMDD_HHMMSS.log|

Result sample:
```bash
==> /home/user/project/scripts/build.sh <==
Lines: 120
Size: 4.12 KB
Extension: .sh
```

🔍 Combine file_stats with find_files to locate interesting files first, then inspect their size/lines.

---

## 🔍 Command • `find_files`

> Locate files by (partial) **name**, **extension** or **content**, print full paths, optionally file size, and export the list.

| Flag | Purpose |
|------|---------|
| `--name <fragment>` | Match filenames that contain `<fragment>` |
| `--content <text>` | Return only files whose content contains `<text>` |
| `--ext <ext>` | Restrict search to files with extension `<ext>` |
| `--show-size` | Append human‑readable size (B / KB / MB) to every hit |
| `--output` | Write results to `logs/find_files_<timestamp>.log` |
| `--help` | Show built‑in help |

### Usage

```bash
shellman find_files <path> [options]
```

Typical examples
|Example | What happens|
|------|---------|
|shellman find_files . --name log | lists every file whose name contains “log” under current dir|
|shellman find_files ./docs --content "error 404" --ext md --show-size | searches *.md in docs/ that include text error 404, prints size|
|shellman find_files src --name util --output | finds any “util” file in src/, saves list to logs/|

Output sample with --show-size:
```bash
/home/user/proj/src/util.cpp  [7.33 KB]
/home/user/proj/src/string_utils.h  [2.51 KB]

```
📝 Tip: Pipe the list into other commands, e.g.
shellman find_files . --ext sh | xargs shellcheck

---

## ✏️ Command • `replace_text`

> Safe, scriptable **find‑&‑replace** across many files – with preview, per‑file confirmation and in‑place editing.

| Flag | Purpose |
|------|---------|
| `--find <text>` | **Required.** Literal text to search for |
| `--replace <text>` | **Required.** Replacement text |
| `--ext <ext>` | Touch only files whose extension is `<ext>` |
| `--in-place` | Write the substitution back to disk (otherwise dry‑run) |
| `--preview` | Show a unified `diff` of the changes before saving |
| `--confirm` | Ask *Y/n* per file when `--in-place` is active |
| `--help` | Built‑in help |

### Usage

```bash
shellman replace_text <path> [options]
```

Typical workflow
Example| What happens
|------|---------|
|shellman replace_text ./docs --find APIv1 --replace APIv2 --ext md --preview | shows a coloured diff for every *.md that would change|
|shellman replace_text ./src --find foo --replace bar --ext c --in-place --confirm | walks through each .c file, asks “Replace in this file? (Y/n)”|
|shellman replace_text . --find TODO --replace '' | lists all files containing TODO (dry‑run)|
|shellman replace_text configs --find 8080 --replace 9090 --in-place | silent in‑place rewrite (no preview, no questions)|

⚠️ Without --in-place Shellman never touches the files – you get a preview‑only run.
Combine --preview --in-place --confirm for maximum safety.

---

## 📦 Command • `zip_batch`

> Batch‑create ZIP archives from a folder hierarchy – single archive or one‑per‑subfolder, optional password.

| Flag | Purpose |
|------|---------|
| `--path <dir>` | Source directory (default: current `.`) |
| `--ext <ext>` | Include only files whose extension is `<ext>` |
| `--per-folder` | Instead of one big zip, create a separate archive for every first‑level subfolder |
| `--name <prefix>` | Prefix for generated archives (default `batch_`) |
| `--output <dir>` | Destination directory for zips (default `./zips`) |
| `--password <pwd>` | Protect the archive with `<pwd>` (uses `zip -P`) |
| `--help` | Built‑in help |

### Usage

```bash
shellman zip_batch [options]
```
Typical examples

|Example | What happens|
|------|---------|
|shellman zip_batch --path ./src --ext log --output ./archives | One archive archives/batch_files_<timestamp>.zip containing all *.log files in src/|
|shellman zip_batch --path ./projects --per-folder --name backup_ | Creates backup_<subdir>.zip for every subfolder of projects/|
|shellman zip_batch --path . --ext txt --password s3cr3t | Packs all .txt files in current tree into ./zips/batch_files_<timestamp>.zip encrypted with password s3cr3t|

Result messages:
```bash
📦 Creating archive: ./archives/batch_files_20250417_153201.zip
✔︎ Created: ./archives/batch_files_20250417_153201.zip
```
💡 Tip: Pair with find_files --name log --output to inspect which files will be archived first.

---

## 🔎 Command • `tail_follow`

> A convenience wrapper around **`tail -f`** with live filtering and colour‑highlighting.

| Flag | Purpose |
|------|---------|
| `--contains <text>` | Stream only lines that contain `<text>` |
| `--ignore-case` | Case‑insensitive search for `--contains` |
| `--highlight <text>` | Paint `<text>` red in the output (ANSI colour) |
| `--help` | Built‑in help |

### Usage

```bash
shellman tail_follow <file> [options]
```
Typical examples

|Example | What happens|
|------|---------|
|shellman tail_follow /var/log/syslog | Plain live view of syslog|
|shellman tail_follow app.log --contains ERROR --highlight ERROR | Shows only lines with ERROR, highlights them|
|shellman tail_follow access.log --contains 404 --ignore-case | Streams any 404 (upper / lower‑case) hits|

Output sample with highlight:
```bash
2025‑04‑17 15:42:03  GET /index.html  **\x1b[31m404\x1b[0m**  12 ms
```
✋ Press Ctrl + C to stop following the file.

---

## 📑 Command • `merge_files`

> Concatenate many text files into a **single output file** – add headers, sort the list, restrict by extension.

| Flag | Purpose |
|------|---------|
| `--path <dir>` | Directory to scan (default `.`) |
| `--ext <ext>` | Include only files whose extension is `<ext>` |
| `--out <file>` | Output filename (default `logs/merged_<timestamp>.txt`) |
| `--header` | Prepend `=== /full/path/to/file ===` before each file’s content |
| `--sort` | Alphabetically sort the file list before merging |
| `--help` | Built‑in help |

### Usage

```bash
shellman merge_files [options]
```
Typical examples

|Example | What happens|
|------|---------|
|shellman merge_files --ext log --out all_logs.txt | Writes every *.log under current dir into all_logs.txt|
|shellman merge_files --path ./reports --header --sort | Sorts all files in reports/, adds header banner before each, saves to logs/merged_<ts>.txt|
|shellman merge_files --path notes --ext md --out notes.md | Stitches all Markdown files in notes/ into one big notes.md|

Header sample:
```bash
=== /home/user/reports/2025‑04‑Q1.log ===
...file content...
```
📜 Tip: pair with find_files → pipe to xargs cat for more advanced selection, but merge_files is the quick all‑in‑one solution.

---

## 🔐 Command • `encrypt_files`

> Simple AES‑256 **file encryption / decryption** via OpenSSL – restrict by extension, choose in/out folders.

| Flag | Purpose |
|------|---------|
| `--mode encrypt \| decrypt` | **Required.** Select operation |
| `--password <pwd>` | **Required.** Password used as key |
| `--path <dir>` | Directory to scan (default `.`) |
| `--ext <ext>` | Process only files with extension `<ext>` |
| `--out <dir>` | Where to drop results (default `./encrypted` or `./decrypted`) |
| `--help` | Built‑in help |

### Usage

```bash
shellman encrypt_files --mode <encrypt|decrypt> --password <pwd> [options]
```
Typical examples

|Example | What happens|
|------|---------|
|shellman encrypt_files --mode encrypt --password mypass --ext log --path ./logs --out ./secure | Encrypts every *.log under logs/ → secure/<file>.log.enc|
|shellman encrypt_files --mode decrypt --password mypass --ext enc --path ./secure --out ./plain | Decrypts .enc files back to clear text in plain/|
|shellman encrypt_files --mode encrypt --password secret | Encrypts all files in current dir tree, saves to ./encrypted/|

Result line sample:

```bash
Encrypted: ./logs/error.log → ./secure/error.log.enc
```

🔐 Reminder: Lose the password = lose the data.
OpenSSL’s -P flag (“show key/iv”) is intentionally not used to keep things simple & safe.

---

## 🩺 Command • `doctor`

> Diagnose (and optionally auto‑repair) your Shellman installation – checks directory structure, permissions, external tools, symlink, and core commands.

| Flag | Purpose |
|------|---------|
| `--fix` | Attempt to auto‑solve detected issues:<br>• creates missing folders<br>• sets execute permission on `bin/shellman`<br>• re‑creates symlink in `/usr/local/bin`<br>• installs needed tools (`zip`, BATS) via `apt` |

### What does it check?

* Presence of **`bin/ commands/ lib/ logs/`** directories  
* Existence of `VERSION`, `lib/utils.sh`, launcher script  
* Executable bit on `bin/shellman`  
* Correct symlink `/usr/local/bin/shellman`  
* Availability of built‑in command scripts (`count_lines`, `file_stats`, …)  
* External dependencies: **`bats`**, **`zip`** (and auto‑installs when `--fix` + `apt` present)

### Usage

```bash
# read‑only health report
shellman doctor

# fix everything it can (needs sudo for apt)
shellman doctor --fix
```

Output excerpt:
```bash
✔︎ bin/ directory
✔︎ zip command found
⚠️  BATS is not installed
Trying to install bats ...
✔︎ BATS successfully installed
🛠️  Fix mode enabled – issues corrected where possible.
📁 Log zapisany do: logs/doctor_20250417_162122.log
```
📜 Doctor writes a full timestamped log in logs/ so you can review every action later.

---

## 🔄 Command • `update`

> Copy the latest local source over the system install, refresh permissions and symlink – keeps Shellman up to date between `git pull`s.

| Prompt | Meaning |
|--------|---------|
| `Proceed with update? (Y/n)` | Hit **Enter / y** to continue, or **n** to abort |
| **update**        | Copy current clone into system install. Add **`--remote`** to `git pull` the latest code from GitHub first |


### What it does

1. Reads the version in your checkout (`./VERSION`)  
2. Prints the currently installed version from `/usr/local/lib/shellman/VERSION`  
3. On confirmation it:  
   * `cp -r bin commands lib VERSION` ⇒ `/usr/local/lib/shellman/`  
   * re‑applies execute bit to `bin/shellman`  
   * recreates symlink `/usr/local/bin/shellman` → new launcher  
4. Prints the fresh version via `shellman --version`

### Usage

```bash
# pull newest code first
git pull origin main

# update the system copy
shellman update
```
Typical output:
```bash
🔁 Updating Shellman...
Current version: 0.2.1
New version:     0.2.2
Proceed with update? (Y/n): y
📁 Updating files in /usr/local/lib/shellman...
🔓 Setting permissions...
🔗 Recreating symlink in /usr/local/bin...
✅ Shellman updated!
Shellman version 0.2.2
```
📝 If you installed Shellman only locally (without the system‑wide installer),
you can simply run git pull – no need for update.

---

## 🧹 Command • `clean_files`

Delete temporary or stale files in bulk – supports dry‑run, age filter and per‑file confirmation.

| Flag | Purpose |
|------|---------|
| `--path <dir>` | Folder to scan (default `.`) |
| `--ext <ext>` | Remove files with extension `<ext>` (`tmp`, `log` …) |
| `--name <pattern>` | Remove files whose name contains `<pattern>` (`~`, `.bak`) |
| `--older-than <days>` | Only delete files older than N days |
| `--dry-run` | Preview list – don’t delete |
| `--confirm` | Ask **Y/n** for every file |
| `--help` | Built‑in help |

Examples:

```bash
# Just show what would be deleted
shellman clean_files --ext tmp --older-than 10 --dry-run

# Interactively remove backup files in project/
shellman clean_files --path ./project --name '~' --confirm
```
---

## ✅ Command • `checksum_files`

Generate or verify SHA‑256 / MD5 / SHA‑1 sums for a batch of files.

| Flag | Purpose |
|------|---------|
| `--path <dir>` | Where to look (default `.`) |
| `--ext <ext>` | Limit to files with extension `<ext>` |
| `--algo <sha256|md5|sha1>` | Choose hash algo (default sha256) |
| `--out <file>` | Name of checksum list (default `checksums.<algo>sum`) |
| `--verify` | Verify existing list instead of creating one |
| `--help` | Built‑in help |

Examples:

```bash
# create SHA‑256 list of all .zip files in dist/
shellman checksum_files --path dist --ext zip --algo sha256 --out dist.sha256sum

# later, verify integrity
shellman checksum_files --verify --out dist.sha256sum
```

---

## 🔎 Command • `extract_lines`

Extract only the lines you need – keep / drop by text and include N lines of context.

| Flag | Purpose |
|------|---------|
| `--contains <text>` | Show lines that **contain** `<text>` |
| `--not-contains <text>` | Show lines that **do NOT contain** `<text>` |
| `--before <N>` | Also print N lines **before** each hit |
| `--after <N>` | Also print N lines **after** each hit |
| `--output <file>` | Write result instead of printing |
| `--help` | Built‑in help |

Examples:

```bash
# 2 lines before + 3 after every ERROR
shellman extract_lines sys.log --contains ERROR --before 2 --after 3

# Remove all TODO lines and save clean version
shellman extract_lines notes.md --not-contains TODO --output notes.clean.md

# View only warnings and errors (case‑insensitive) in the Apache log
shellman extract_lines access.log --contains "[Ee][Rr][Rr][Oo][Rr]"
```
---

## 📊 Command • `csv_extract`

Pull out chosen **columns & rows** from a CSV, with simple text filters and optional output‑to‑file.

| Flag | Purpose |
|------|---------|
| `--cols 1,3` / `--cols 2-4` | Select columns (1‑based) – ranges or comma list |
| `--rows 10-100` / `--rows 1,5,9` | Select rows |
| `--contains <text>` / `--not-contains <text>` | Keep (or drop) rows by substring |
| `--delim ';'` | Set delimiter (default `,`) |
| `--skip-header`	|Ignore the first CSV line when counting rows|
| `--interactive`|	Pipe the result to less for live browsing (can be combined with --output)|
| `--output <file>` | Save extracted slice |
| `--help` | Built‑in help |

Examples:

```bash
# id, name columns for rows 2‑20
shellman csv_extract data.csv --cols 1,3 --rows 2-20

# only lines with ERROR, save to new file
shellman csv_extract logs.csv --cols 1-5 --contains ERROR --output errors.csv

# Quick ad‑hoc view in less (no file created)
shellman csv_extract data.csv --cols 1-4 --contains ERROR --interactive

# Save slice to file and open it interactively
shellman csv_extract users.csv --rows 2-100 --output slice.csv --interactive

```
---

### 📄 Command • `excel_info`

```bash
shellman excel_info workbook.xlsx
shellman excel_info Users/Downloads/TP_20250401-0745151545.xlsx
```
Output:
```bash
Sheet        Rows  Cols
-----------  ----  ----
Test Plan                 58     15
Test Case Category R      11      7
```
❗ Note: the tool relies on openpyxl, which supports .xlsx, .xlsm, .xltx, .xltm, .xlsb.
Old binary Excel files *.xls are not supported.

---

### 📊 Command • excel_preview`

Quick workbook overview:

```bash
# first 20 rows of sheet 1
shellman excel_preview report.xlsx          
# by name
shellman excel_preview data.xlsm --sheet name_sheet
# columns A,D,E and 100 rows
shellman excel_preview book.xlsb --rows 100 --columns A,D-E
# save CSV
shellman excel_preview data.xlsx --output slice.csv
```
| Flag | Purpose | Default |
|------|---------|---------|
| `--sheet <name>` | Choose worksheet by number ( 1‑based ) or by exact name | 1 |
| `--rows <N>` / `--rows 1,5,9` | Show only the first N data rows | 20 |
| `--columns <A,C‑E>` | Limit output to selected columns (comma‑list or Excel‑style range) | all |
| `--output file.csv`| Save result to CSV instead of a live preview | disable |
| `--interactive	`| Pipe preview to less -S for horizontal scroll; automatically on unless --output is used | auto |

---

### 📑 excel_to_csv

Convert any sheet – or all sheets – to separate CSV files.

```bash
# export everything to ./csv
shellman excel_to_csv report.xlsx

# only sheet 2 and sheet "Summary" to out/
shellman excel_to_csv book.xlsm --sheets 2,Summary --out out/ --overwrite
```

|Flags |	Meaning |
|------|---------|
|--sheets 1,Summary |	comma list of numbers / names (default: all)|
|--rows <a-b>|      Keep only rows a‑b|
|--columns A,C‑E  | Keep only chosen columns  |
|--out ./dir |	destination folder (created if missing)|
|--overwrite |	overwrite existing CSVs|
|--help      |      This help screen|


---

### 📑 excel_diff — Cell‑level comparison for Excel workbooks

## 1 · What does it do?

`excel_diff` compares **two spreadsheets (or two sheets)** and reports
**every cell whose value changed**, in either **Markdown** (default) or
plain **CSV**.

Typical use‑cases ⬇︎

| Scenario | Example |
|----------|---------|
| QA report v1 vs v2 | `excel_diff qa_v1.xlsx qa_v2.xlsx --sheet Summary` |
| Daily KPI sheet | `excel_diff 17‑Apr.xlsx 18‑Apr.xlsx` |
| Same workbook, two sheets | `excel_diff file.xlsx file.xlsx --sheet NewCopy` |

Markdown sample:

| Sheet | Cell | Old value | New value |
|-------|------|-----------|-----------|
| Plan | A5 | *cancelled* | **done** |
| Plan | B8 | 12 | 14 |

---

## 2 · Installation

The command needs **Python 3** with:

* `openpyxl`
* `pandas`

Run once:

```bash
shellman doctor --fix    # installs everything
```

```bash
shellman excel_diff <old.xlsx> <new.xlsx> [options]
```

|Flag |	Meaning	| Default |
|-------|------|-----------|
|--sheet <n/name>	 |sheet number (1‑based) or sheet name |	first sheet |
|--format csv/md	| output as CSV or GitHub‑flavoured Markdown |	md
|--out <file> |	save result to a file instead of stdout	 |– |
|--ignore-case |	ignore case differences (ABC vs abc)	 |off |
|--help |	show help	 |– |
```bash
Exit codes

Code	Meaning
0	sheets identical or diff saved
1	invalid input / sheet not found
2	missing dependencies
```
---

### 📜 json_extract 
Extract and filter JSON using jq expressions, selecting fields and saving or viewing the result.

|Flag |	Meaning	|
|-------|------|
|--path <jq_expr>	 | Apply a jq path or expression (e.g. .[]) |
|--filter <jq_expr>	| Filter JSON array items (requires array input) |
|--fields <list> |	Comma-separated list of fields to select (e.g. id,name) |
|--interactive |	Pipe the result through less -S (default when no --output) |
|--output <file>| Save output to file (disables interactive) |
|--help |	show help	 |

Examples:
```bash
# Extract each element of the top-level array
shellman json_extract data.json --path '.[]'

# Filter where status == "ERROR" and select id and msg
shellman json_extract data.json --filter '.[] | select(.status=="ERROR")' --fields id,msg --output errors.json

# Interactive view of selected fields
shellman json_extract data.json --path '.users[]' --fields id,email
```

---
### 🖥️ sys_summary

Display a concise overview of your system: OS, shell, tools, memory, uptime, disk usage, network IPs, and more.
Useful for quick diagnostics or remote session introspection.

|Section |	What it includes|
|-------|------|
|OS & Host |	OS type, distro version, architecture, WSL, hostname|
|Shell |	Shell type and version, bash version if applicable|
|Tools |	Versions of Python 3, jq, and xlsx2csv|
|Memory |	RAM and swap usage summary (human-readable)|
|Uptime & Load |	System uptime and load average|
|Disks |	Mounted disk partitions, total/used/avail space|
||Network |	Local IP, public IP (via ifconfig.me)|
|Packages |	Detected package manager and installed count|

Supported environments: Linux, WSL, macOS

Example:
```bash
shellman sys_summary
```
You’ll see a colorful summary like this:

```bash
📋  System Summary
────────────────────────────────────────
🖥️  OS & Host
System       : Linux
Distro       : Ubuntu 22.04
Version      : 5.15.0-91-generic
Architecture : x86_64
WSL          : No
Hostname     : my-laptop

🐚  Shell
Shell        : bash
Shell Ver.   : GNU bash, version 5.1.16(1)-release
Bash Ver.    : 5.1.16(1)-release

🛠  Tools
python3      : Python 3.10.12
jq           : jq-1.6
xlsx2csv     : 0.8.2

🧠  Memory
              total      used       free
Mem:          15Gi       4Gi        10Gi
Swap:         2Gi        512Mi      1.5Gi

⏱  Uptime & Load
Uptime       : up 3 hours, 42 minutes
Load Avg.    : 0.31, 0.24, 0.17

💽  Disks
Filesystem           Size     Used     Avail    Use%
/dev/nvme0n1p2       100G     30G      65G      30%

🌐  Network
Local IP     : 192.168.1.22
Public IP    : 89.74.192.XXX

📦  Packages
Pkg Manager  : apt
Total pkgs   : 1792

```
---

### 🔄 file_convert
Convert structured data between JSON, YAML, and TOML formats. Automatically detects input format. You can pipe to less, or save to a file.

|Flag | Description|
|-------|------|
|--from <format> | Force input format (json, yaml, toml)|
|--to <format> | Required. Output format (json, yaml, toml)|
|--pretty | Beautify output (indentation)|
|--output file | Save result to file instead of stdout|
|--interactive | View result in less (default unless --output)|
|--help | Show help|

Examples:
```bash
# Convert JSON to YAML and view in pager
shellman file_convert data.json --to yaml

# Convert YAML to JSON and save to file
shellman file_convert config.yml --to json --output out.json

# Convert TOML to pretty YAML
shellman file_convert config.toml --to yaml --pretty

# Force format detection (if needed)
shellman file_convert rawdata.txt --from toml --to json
```

---
### 📅 date_utils

Manipulate and compare dates: add/subtract time units, format, and compute differences.

|Flag | Purpose|
|-------|------|
|--now | Use current date (default if no --date)|
|--date <YYYY-MM-DD> | Provide base date to operate on|
|--add 5d / --sub 2w | Add/subtract 5d, 2w, 3m, 1y, 4h, 30min, 20s|
|--diff <YYYY-MM-DD> | Calculate difference in days between two dates|
|--format '%d/%m/%Y' | Format output date|
|--sub <n><unit> |  ( 10d, 1m, 2h, 15s)|
|--help | Show built‑in help|

Examples:
```bash
# Add 10 days to today
shellman date_utils --add 10d

# Subtract 2 months from given date
shellman date_utils --date 2024-12-01 --sub 2m

# Show how many days between two dates
shellman date_utils --date 2024-01-01 --diff 2025-04-18

# Show today’s date in custom format 
shellman date_utils --format '%A, %d %B %Y'

shellman date_utils --add 200h
shellman date_utils --date "2024-05-01 12:00:00" --sub 45min
```

---

### 🔁 `line_endings` – Convert line endings (CRLF ↔ LF)

Convert line endings of a single file or all files in a directory.

#### Usage

```bash
shellman line_endings --file path/to/file.txt --to lf
shellman line_endings --file script.ps1 --to crlf
shellman line_endings --dir ./project --ext .sh --to lf
```

|Flag | Purpose|
|-------|------|
|--file <path>| Convert single file |
|--dir <path> | Convert all files in director y|
|--ext <.ext> | (Optional) Only files with given extension |
|--to lf / crlf |  Target line ending |
|--help | Show help |
If dos2unix or unix2dos are not available, a fallback using sed is used.

---
🤝 Contributing
Add or copy a script into commands/.

Keep code & comments in English (conversation can stay Polish 😉).

Add a small test in tests/.

shellman doctor must be green before opening a PR.

