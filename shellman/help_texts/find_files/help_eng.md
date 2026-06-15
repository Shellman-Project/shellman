# 🔍 Find Files

The `find_files` command searches for files recursively in a directory based on:

* partial filename,
* file extension,
* text content inside files,
* optional output to a log file,
* optional file size display.

---

## 🧠 How It Works

* The command scans all subdirectories starting from `SEARCH_PATH`.
* Files are filtered using the provided options: `--name`, `--ext`, `--content`.
* Matching files are printed in the terminal.
* If `--output` is used, results are saved to `logs/find_files_<timestamp>.log`.
* If `--show-size` is used, file sizes are shown next to paths in `B`, `KB`, or `MB`.

---

## 💡 Options

* `--name`, `-n` — match files whose names contain the given fragment. Matching is case-sensitive.
* `--ext`, `-e` — only include files with the given extension, for example `py`, `.py`, `md`, `.md`.
* `--content`, `-c` — only include files that contain the given text.
* `--output`, `-o` — save matched results to a timestamped log file.
* `--show-size`, `-s` — display file size next to each result.
* `--lang-help`, `-lh` — show localized extended help, for example `pl` or `eng`.

---

## 📦 Examples

Search for all files that contain `log` in their filename:
shellman find_files . --name log

Search only Markdown files in `./docs` that contain `error 404`:
shellman find_files ./docs --content "error 404" --ext md

Search for Python files containing `util` in their name and show their sizes:
shellman find_files ./src --name util --ext py --show-size

Save search results to a log file:
shellman find_files ./src --name helper --output

Combine all filters for precise targeting:
shellman find_files ./data --name report --content "Total" --ext txt --show-size --output

Show help in Polish:
shellman find_files --lang-help pl

Show help in English:
shellman find_files --lang-help eng
