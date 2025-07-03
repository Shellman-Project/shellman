📄 **CSV Extract – Select Columns and Rows with Filters**

This tool allows you to extract specific columns and/or rows from a CSV file.

---

### 💡 How It Works

- Columns are selected by position (1-based): e.g. `1,2,5`, or `2-4`
- Rows are filtered by:
  - row number (after header)
  - containing specific text
  - not containing specific text
- You can skip the header row
- The output can be printed, saved to a file, or viewed interactively

---

### 🔍 Options

- `--cols`: required; which columns to keep (e.g. `1,3` or `2-4`)
- `--rows`: which rows to keep, after header (e.g. `2-10`)
- `--contains`: keep only rows that contain this text
- `--not-contains`: exclude rows that contain this text
- `--delim`: CSV delimiter (default: `,`)
- `--skip-header`: skip the first line
- `--output`: save result to a file
- `--interactive`: view result with pager (e.g. `less`)

---

### 📦 Examples

Extract columns 1 and 4, from rows 2 to 100, skip header:
shellman csv_extract data.csv --cols 1,4 --rows 2-100 --skip-header

Extract all rows with "ERROR" in them and save to a file:
shellman csv_extract logs.csv --cols 1,2 --contains ERROR --output errors.csv

Exclude rows that contain "DEBUG":
shellman csv_extract logs.csv --cols 1,3 --not-contains DEBUG

Preview the result interactively:
shellman csv_extract data.csv --cols 1,2 --interactive
