# 🔍 Wyszukiwanie plików

Komenda `find_files` umożliwia rekurencyjne wyszukiwanie plików w katalogu na podstawie:

* fragmentu nazwy pliku,
* rozszerzenia pliku,
* zawartości tekstowej wewnątrz pliku,
* opcjonalnego zapisu wyników do pliku logu,
* opcjonalnego wyświetlania rozmiarów plików.

---

## 🧠 Jak to działa

* Komenda przeszukuje wszystkie podfoldery, zaczynając od `SEARCH_PATH`.
* Pliki są filtrowane według podanych opcji: `--name`, `--ext`, `--content`.
* Pasujące pliki są wyświetlane w terminalu.
* Jeśli podano `--output`, wyniki są zapisywane do pliku `logs/find_files_<timestamp>.log`.
* Jeśli podano `--show-size`, obok ścieżki pojawi się rozmiar pliku w formacie `B`, `KB` albo `MB`.

---

## 💡 Opcje

* `--name`, `-n` — wyszukuje pliki, których nazwa zawiera podany fragment. Wielkość liter ma znaczenie.
* `--ext`, `-e` — ogranicza wyniki do plików z podanym rozszerzeniem, np. `py`, `.py`, `md`, `.md`.
* `--content`, `-c` — pokazuje tylko pliki, które zawierają podany tekst.
* `--output`, `-o` — zapisuje wyniki do pliku logu z datą i godziną.
* `--show-size`, `-s` — pokazuje rozmiar pliku obok każdej ścieżki.
* `--lang-help`, `-lh` — wyświetla rozszerzoną pomoc językową, np. `pl` albo `eng`.

---

## 📦 Przykłady

Szukaj wszystkich plików zawierających `log` w nazwie:
shellman find_files . --name log

Szukaj plików Markdown w katalogu `./docs`, które zawierają tekst `error 404`:
shellman find_files ./docs --content "error 404" --ext md

Szukaj plików Pythona zawierających `util` w nazwie i pokaż ich rozmiary:
shellman find_files ./src --name util --ext py --show-size

Zapisz wyniki do pliku logu:
shellman find_files ./src --name helper --output

Połącz wszystkie filtry dla dokładniejszego wyszukiwania:
shellman find_files ./data --name report --content "Suma" --ext txt --show-size --output

Wyświetl pomoc po polsku:
shellman find_files --lang-help pl

Wyświetl pomoc po angielsku:
shellman find_files --lang-help eng
