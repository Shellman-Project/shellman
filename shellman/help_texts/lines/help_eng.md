📏 **lines – Extract, Count, or Summarize Lines**

Extract lines with context, count matches, or summarize line stats in files or folders.
Filters: by substring, regex, negative match, extension.  
Context: print lines ±N around each match.  
Everything in one command!

---

### 🔧 Options

| option           | description |
|------------------|-------------|
| `--extract`      | Print out matching lines (default if no mode given) |
| `--count`        | Only print count of matches per file |
| `--summary`      | Print summary for all files (totals) |
| `--contains TEXT`| Lines must include this text |
| `--not-contains TEXT` | Lines must **not** include this text |
| `--regex PATTERN`| Match lines using regex (mutually exclusive with `--contains`) |
| `--ignore-case`  | Ignore case in match |
| `--before N`     | N lines of context before match |
| `--after N`      | N lines of context after match |
| `--ext EXT`      | Only files with this extension |
| `--percent`      | Show percentage of matches |
| `--show-size`    | Show file size in output |
| `--output FILE`  | Save result to file |
| `--interactive`  | View results in pager (`less`) |
| `--lang-help pl/eng` | Show help in Polish / English |

---

### 📦 Examples

Extract lines with ±2 lines context:
shellman lines log.txt --contains error --before 2 --after 2

Count lines matching TODO/FIXME in Python files:
shellman lines . --ext py --regex "TODO|FIXME" --count

Show percent matches for each file, plus summary:
shellman lines src/ --contains "def " --count --percent --summary
