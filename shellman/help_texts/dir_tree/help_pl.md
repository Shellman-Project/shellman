🌲 **dir_tree – Wyświetlanie struktury katalogów**

Rysuje strukturę folderów w formacie podobnym do `tree`.

#### Opcje
| opcja        | opis |
|--------------|------|
| `--files`    | pokaż także pliki |
| `--depth N`  | maksymalna głębokość zaglądania |
| `--output`   | zapisz wynik do pliku |
| `--hidden`   | uwzględnij ukryte pliki i foldery |
| `--ascii`    | użyj znaków ASCII zamiast linii Unicode |

#### Przykłady
shellman dir_tree .
shellman dir_tree . --files --depth 2
shellman dir_tree . --output struktura.txt