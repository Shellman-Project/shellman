📤 **excel export – Convert Sheets (or Ranges) to CSV**

Export one or many worksheets – or just specific rows/columns – to standalone CSV files.

### 🔧 Options

| option | default | description |
|--------|---------|-------------|
| `--sheets`   | all | Sheet names or indices (space-separated) |
| `--rows`     | ―   | Row range `start-end`, e.g. `2-100` |
| `--columns`  | ―   | Column letters `A,B-D` |
| `--out DIR`  | `csv` | Output directory |
| `--overwrite`| ✗   | Overwrite existing CSVs (no timestamp) |

### 📦 Example
shellman excel export book.xlsx --sheets Sheet1 Sheet3 --rows 2-50 --columns A,C-E --out ./csv

Creates `csv/Sheet1_<timestamp>.csv` and `csv/Sheet3_<timestamp>.csv`
