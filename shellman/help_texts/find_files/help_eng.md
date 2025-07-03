🔍 **Find Files**

This command allows you to search for files recursively in a directory based on:

- Partial **filename**
- File **extension**
- Specific **text content**
- With optional output to a log file and file size display

---

### 🧠 How It Works

- The command scans all subdirectories starting from the given `SEARCH_PATH`
- Files are filtered based on the provided options (`--name`, `--ext`, `--content`)
- Matching files are listed in the terminal
- If `--output` is set, results are saved to `logs/find_files_<timestamp>.log`
- If `--show-size` is set, file sizes (in MB) are shown next to paths

---

### 💡 Options Explained

- `--name`: match any file whose name includes this fragment (case-sensitive)
- `--ext`: filter files with a given extension (e.g. `md`, `py`)
- `--content`: only include files that contain this text
- `--output`: save matched results to a timestamped log file
- `--show-size`: display file size next to each result

---

### 📦 Examples

Search for all files that contain `"log"` in their filename:
shellman find_files . --name log

Search only Markdown files in `./docs` that contain "error 404":
shellman find_files ./docs --content "error 404" --ext md

Search for utility-related Python files and show their sizes:
shellman find_files ./src --name util --ext py --show-size

Save search results to a log file for later use:
shellman find_files ./src --name helper --output

Combine all filters for precise targeting:
shellman find_files ./data --name report --content "Total" --ext txt --show-size --output
