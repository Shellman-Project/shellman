📊 **file_stats – File Statistics and Metadata**

Scans one or more files/folders and shows:
- file path
- size
- number of lines
- extension

Optional metadata:
- creation and modification time
- text/binary classification
- encoding

#### Options
| option        | description |
|---------------|-------------|
| `--ext`       | filter by extension |
| `--output`    | save result to log |
| `--meta`      | show file metadata |
| `--lang-help` | show help in pl / eng |

#### Examples
shellman file_stats . --ext py
shellman file_stats README.md --meta
shellman file_stats src/ --output
