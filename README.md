# 🐚 Shellman

**Shellman** is your friendly CLI assistant – a collection of tools for working with files, data, the system and more.

---

## 🔧 Installation

### 1. Cloning a repository

```bash
git clone https://github.com/JakubMarciniak93/shellman
cd shellman
```

### 2. Installing dependencies

Recommend creating a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

Or using Poetry:

```bash
poetry install
```

### 3. Installing in developer mode

```bash
pip install -e .
```

## 🚀 Usage

Check available commands:
```bash
shellman --help
```
Example:
```bash
shellman sys_summary
```

## 📦 Available commands

sys_summary – summary of system, shell, tools, memory, etc.
count_lines – count lines in files
replace_text – replace text in files
file_convert – file conversion (e.g. JSON ↔ TOML)
encrypt_files – file encryption and decryption
excel_to_csv, excel_preview, csv_extract, json_extract – data tools
date_utils, merge_files, zip_batch, clean_files, checksum_files, etc.
