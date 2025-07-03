📏 **Count Lines in Files or Folders**

This command lets you count lines in one or more files or folders.  
You can filter by content, regular expressions, extensions, or display interactive summaries.

---

### 💡 Options Explained

- `--contains TEXT`: count only lines that contain this substring
- `--regex PATTERN`: count lines matching the regular expression
- `--ignore-case`: case-insensitive match (applies to `--contains` and `--regex`)
- `--ext EXT`: only process files with given extension
- `--summary`: show total lines per file and full summary
- `--percent`: show matching percentage
- `--show-size`: display file size in MB
- `--output`: save results to timestamped log in `logs/`
- `--interactive`: view output interactively using pager

---

### 📦 Examples

Count all lines in Python files:
shellman count_lines . --ext py

Count all lines containing `error` (case-insensitive):
shellman count_lines logs --contains error --ignore-case

Count lines matching "TODO" or "FIXME" via regex:
shellman count_lines . --regex "TODO|FIXME" --summary --percent

Export results to a file:
shellman count_lines . --contains error --output

Show results interactively:
shellman count_lines . --regex "import" --interactive
