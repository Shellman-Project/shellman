🗓️ **Date Utilities – Add, Subtract, Compare, and Format Dates**

This tool allows you to manipulate dates and times easily from the command line.

---

### 💡 Features

- Add or subtract time from a given date or current time
- Compare two dates to see the difference
- Format a date/time using a custom pattern

---

### 🧠 Duration Format

You can use:

- `d` → days
- `w` → weeks
- `m` → months
- `y` → years
- `q` → quarters (3 months)
- `h` → hours
- `min` → minutes
- `s` → seconds

---

### ⌚ Accepted Date Formats

- `YYYY-MM-DD`
- `YYYY-MM-DD HH:MM[:SS]`

---

### 🔧 Options

- `--date`: base date (default: now)
- `--add`: add duration (e.g. `5d`, `2h`, `3w`)
- `--sub`: subtract duration
- `--diff`: compare two dates and show time difference
- `--format`: format result using a custom `strftime` pattern

---

### 📦 Examples

Add 5 days to current date:
shellman date_utils --add 5d

Subtract 2 hours from specific datetime:
shellman date_utils --date "2024-12-01 13:00" --sub 2h

Compare two dates:
shellman date_utils --date "2024-01-01" --diff "2025-04-18 09:15:00"

Format a date:
shellman date_utils --date "2025-01-01" --format "%A, %d %B %Y, %H:%M"
