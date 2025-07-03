🔎 **json_extract – Filter & Select JSON Data**

Extract part of a JSON document, optionally filter by a key/value pair and choose specific fields.

---

### 🔧 Options

| option | description |
|--------|-------------|
| `--path key.path` | Navigate to nested list/object before processing |
| `--filter k=v`    | Keep objects where `k` equals `v` (string comparison) |
| `--fields a,b,c`  | Comma-separated list of fields to include |
| `--output FILE`   | Write result to file |
| `--interactive`   | Pipe result to `less -S` (ignored if `--output`) |
| `--lang-help`     | Show this help (`pl` / `eng`) |

---

### 📦 Examples

Take list `items`, filter `status=ERROR`, return only `id,msg`, save to file:

shellman json_extract data.json --path items --filter status=ERROR --fields id,msg --output errors.json

Print every object in root.users with pretty pager:
shellman json_extract users.json --path root.users --interactive
