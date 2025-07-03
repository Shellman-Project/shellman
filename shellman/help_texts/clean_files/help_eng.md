🧹 **Clean Files – Delete by Name, Extension or Age**

Use this command to delete files in a directory tree based on:

- File **extension** (e.g. `.log`, `.tmp`)
- File **name fragment** (e.g. `~`, `backup`)
- File **modification age** (e.g. older than 7 days)
- With optional confirmation and dry-run preview

---

### 💡 Options Explained

- `--path`: base directory to scan (default: `.`)
- `--ext`: delete files with a specific extension
- `--name`: delete files containing this text in their name
- `--older-than`: only delete files older than N days
- `--dry-run`: show files that would be deleted, but don't delete them
- `--confirm`: ask for confirmation before deleting each file

---

### ⚠️ Safety Notes

- Use `--dry-run` first to preview what would be deleted
- Combine `--ext`, `--name`, and `--older-than` for precise control
- `--confirm` adds an interactive Y/n prompt for each file

---

### 📦 Examples

Dry-run all `.tmp` files older than 7 days:
shellman clean_files --ext tmp --older-than 7 --dry-run

Delete all backup files containing `~` in `./build` directory:
shellman clean_files --path ./build --name '~' --confirm

Clean up `.log` files older than 30 days:
shellman clean_files --ext log --older-than 30

Only delete files containing `backup` in name:
shellman clean_files --name backup

Delete `.bak` files with confirmation prompt:
shellman clean_files --ext bak --confirm
