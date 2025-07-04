# 🐚 Shellman

**Shellman** is your friendly CLI assistant – a curated toolbox for working with files, data and your system.

---

## 🔧 Installation

### 1 · Clone the repository

```bash
git clone https://github.com/JakubMarciniak93/shellman
cd shellman
```

### 2 · Install dependencies

A virtual-env is recommended:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

Using Poetry instead?

```bash
poetry install
```

### 2 · Install Shellman in editable / dev mode

```bash
pip install -e .
```
(Any code or help-file change is picked up instantly – re-install only if you rename/move modules.)

## 🚀 Usage

List all commands:

```bash
shellman --help
```

Every command supports multi-language help via:

```bash
shellman <command> --lang-help eng       # English help
shellman <command> --lang-help pl        # Polish help
```

Example:

```bash
shellman lines README.md --count --show-size --contains shellman/com --extract --before 2 --after 2 --percent

==> README.md <==
88:
89:Pull-requests and feature ideas are welcome!
90:Each command lives in shellman/commands/ – feel free to add your own tool.
91:
92:########################################################################################
--------------------
182:
183:Masz pomysł lub poprawkę? Zgłoś pull-request lub otwórz issue.
184:Każde narzędzie znajduje się w shellman/commands/ – śmiało dodaj własne!
185:

==> README.md <==
Matching lines: 2
Match percentage: 1.08%
File size: 5.31 KB
```
## 📦 Available commands (short list)

command	short description:
```bash
excel info | preview | export	sheet list • quick preview • export ranges to CSV
find_files	locate files by name, content or extension
change_line_end	LF ↔ CRLF conversion / check
checksum_files	create or verify checksums (sha256, md5, sha1)
clean_files	delete junk files by name, ext or age
lines	Extract, count or summarize lines in files or folders with powerful filters and context options.
csv_extract	extract columns/rows from CSV
date_utils	add/subtract dates, diff, strftime
encrypt_files	AES-256 encrypt / decrypt with password
file_convert	JSON ←→ YAML ←→ TOML
file_stats	full path • size • line-count • extension
json_extract	JSON path, filter and field selection
merge_files	merge multiple text files into one
replace_text	batch find-&-replace with diff preview
sys_summary	system / shell / resource report
zip_batch	bulk ZIP creation (per-folder or flat)
open_ports  Show currently open TCP/UDP ports (process, pid, address, state).
speed_test	Run a quick internet speed test (download, upload, ping).
dir_tree  Prints a visual tree of directories (like 'tree').
```
Plus a few helpers: checksum_files, date_utils, etc. Run --help on any sub-command for full docs.

## ❤️ Contributing

Pull-requests and feature ideas are welcome!
Each command lives in shellman/commands/ – feel free to add your own tool.

########################################################################################

# 🐚 Shellman (Polski)

**Shellman** to przyjazny asystent CLI – zestaw narzędzi do pracy z plikami, danymi i systemem.

---

## 🔧 Instalacja

### 1 · Klonowanie repozytorium

```bash
git clone https://github.com/JakubMarciniak93/shellman
cd shellman
```
### 2 · Instalacja zależności

Zalecana wirtualna środowisko:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```
Lub z Poetry:

```bash
poetry install
```

### 3 · Instalacja w trybie developerskim

```bash
pip install -e .
```

(Zmiany w kodzie / plikach .md są widoczne od razu – reinstaluj tylko przy zmianie struktury pakietu).

## 🚀 Użycie

Lista komend:

```bash
shellman --help
```
Każda komenda obsługuje wielojęzyczną pomoc:

```bash
shellman <komenda> --lang-help eng     # pomoc po angielsku
shellman <komenda> --lang-help pl      # pomoc po polsku
```
Przykład:

```bash
shellman lines README.md --count --show-size --contains shellman/com --extract --before 2 --after 2 --percent

==> README.md <==
88:
89:Pull-requests and feature ideas are welcome!
90:Each command lives in shellman/commands/ – feel free to add your own tool.
91:
92:########################################################################################
--------------------
182:
183:Masz pomysł lub poprawkę? Zgłoś pull-request lub otwórz issue.
184:Każde narzędzie znajduje się w shellman/commands/ – śmiało dodaj własne!
185:

==> README.md <==
Matching lines: 2
Match percentage: 1.08%
File size: 5.31 KB
```
## 📦 Dostępne komendy (wybrane)

komenda	opis skrócony:
```bash
excel info | preview | export	lista arkuszy • szybki podgląd • eksport do CSV
find_files	wyszukiwanie plików po nazwie, treści lub rozszerzeniu
change_line_end	konwersja lub sprawdzenie końców linii LF/CRLF
checksum_files	generowanie / weryfikacja sum kontrolnych
clean_files	usuwanie zbędnych plików wg wzorca lub wieku
lines	Wyodrębniaj, licz lub podsumowuj wiersze w plikach lub folderach przy użyciu zaawansowanych filtrów i opcji kontekstowych.
csv_extract	wyciąganie kolumn / wierszy z CSV
date_utils	operacje na datach: +/- czas, różnice, formatowanie
encrypt_files	szyfrowanie / deszyfrowanie AES-256
file_convert	konwersja JSON ↔ YAML ↔ TOML
file_stats	ścieżka • rozmiar • liczba linii • rozszerzenie
json_extract	filtrowanie / wybór pól w JSON
merge_files	łączenie plików tekstowych
replace_text	zbiorcza podmiana tekstu z podglądem diff
sys_summary	raport o systemie, powłoce, zasobach
zip_batch	hurtowe tworzenie plików ZIP
open_ports  Pokaż aktualnie otwarte porty TCP/UDP (proces, pid, adres, stan).
speed_test	Wykonaj szybki test szybkości łącza internetowego (pobieranie, wysyłanie, pingowanie).
dir_tree  Drukuje wizualne drzewo katalogów (jak „drzewo”).
```
Do odkrywania szczegółów użyj --help, np.:

```bash
shellman excel export --help
```

## ❤️ Współpraca

Masz pomysł lub poprawkę? Zgłoś pull-request lub otwórz issue.
Każde narzędzie znajduje się w shellman/commands/ – śmiało dodaj własne!

