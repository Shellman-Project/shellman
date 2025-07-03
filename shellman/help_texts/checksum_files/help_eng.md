🔐 **Generate or Verify Checksums for Files**

This command lets you create or verify checksums for files in a directory, using popular hash algorithms.

---

### 💡 How It Works

- You can **generate a list of hashes** for selected files (default mode)
- Or **verify files** using an existing list (`--verify`)
- Supported algorithms: `sha256`, `sha1`, `md5`
- Optionally filter by file extension (`--ext`)
- All matched files in the directory tree will be processed

---

### 🧠 Mode Selection

- Without `--verify`: generates a `.sha256sum`, `.md5sum`, etc.
- With `--verify`: checks all files listed in the given file and compares their hash

---

### 🧪 Hash Formats

Hash output follows the standard format:
<hash> <filename>

Generated lists can be reused or version-controlled.

---

### 💡 Options

- `--path`: root directory to scan (default: current folder)
- `--ext`: limit to specific file extension (e.g. `zip`, `exe`)
- `--algo`: hash algorithm (default: sha256)
- `--out`: file to save/read checksums
- `--verify`: enable verification mode (use with `--out`)

---

### 📦 Examples

Generate SHA-256 checksums for `.zip` files:
shellman checksum_files --path ./dist --ext zip --algo sha256 --out builds.sha256sum

Verify files listed in a checksum list:
shellman checksum_files --verify --out builds.sha256sum

Create MD5 checksums for all `.mp4` files:
shellman checksum_files --ext mp4 --algo md5 --out videos.md5sum

Use default settings to checksum all files:
shellman checksum_files --out checksums.txt
