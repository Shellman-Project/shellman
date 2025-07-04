📊 **file_stats – Statystyki i metadane plików**

Skanuje pliki i pokazuje:
- ścieżkę
- rozmiar
- liczbę linii
- rozszerzenie

Dodatkowo można uzyskać:
- datę utworzenia i modyfikacji
- czy plik jest tekstowy/binarny
- wykryte kodowanie

#### Opcje
| opcja         | opis |
|---------------|------|
| `--ext`       | filtruj po rozszerzeniu |
| `--output`    | zapisz wynik do loga |
| `--meta`      | pokaż metadane pliku |
| `--lang-help` | pokaż pomoc po polsku lub angielsku |

#### Przykłady
shellman file_stats . --ext py
shellman file_stats README.md --meta
shellman file_stats src/ --output
