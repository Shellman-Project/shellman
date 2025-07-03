📊 **file_stats – Quick File Statistics**

List each file’s absolute path, number of lines, file-size and extension.

---

### 🔧 Options

| option | description |
|--------|-------------|
| `--ext EXT` | Only include files with extension `EXT` |
| `--output`  | Save results to `logs/file_stats_<timestamp>.log` |
| `--lang-help pl/eng` | Show this help in Polish / English |

---

### 📦 Examples

Inspect a single file:
shellman file_stats myfile.txt

Show stats of all .py files inside src/ and save to log:
shellman file_stats ./src --ext py --output
