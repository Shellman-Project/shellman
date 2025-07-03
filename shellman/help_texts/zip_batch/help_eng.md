📦 **zip_batch – Batch ZIP Creation**

Create ZIP archives from many files or one archive per sub-folder.

---

### 🔧 Options

| option | description |
|--------|-------------|
| `--path DIR`     | Source directory (default: `.`) |
| `--ext EXT`      | Include only files with extension `EXT` |
| `--per-folder`   | Make one archive per immediate sub-folder |
| `--output DIR`   | Output directory (default: `./zips`) |
| `--name PREFIX`  | Prefix for archive name (`batch_` by default) |
| `--password PWD` | Zip password (`zip -P`; weak encryption) |
| `--lang-help`    | Show help (`pl` / `eng`) |

---

### 📦 Examples

One archive per sub-folder:

shellman zip_batch --path ./projects --per-folder

Single archive of all .log files:
shellman zip_batch --ext log --name logs_ --output out
