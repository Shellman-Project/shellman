🔍 **excel preview – Quick Sheet Preview**

Show the first *N* rows and selected columns of a worksheet.

### 🔧 Options

| option | default | description |
|--------|---------|-------------|
| `--sheet`    | `1`   | Sheet name or index (1-based) |
| `--rows N`   | `20`  | How many rows to show |
| `--columns`  | ―    | Column letters, e.g. `A,C-E` |
| `--output`   | ―    | Save preview to CSV file |
| `--interactive` | ✗ | Pipe output to `less -S` |

### 📦 Examples
first 10 rows, columns A & B
shellman excel preview file.xlsx --rows 10 --columns A,B

preview Sheet2 interactively
shellman excel preview file.xlsx --sheet Sheet2 --interactive

save preview to preview.csv
shellman excel preview file.xlsx --rows 50 --output preview.csv