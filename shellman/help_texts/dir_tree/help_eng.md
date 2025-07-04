🌲 **dir_tree – Directory Structure Viewer**

Draws folder structure in a tree-like format.

#### Options
| option       | description |
|--------------|-------------|
| `--files`    | include files, not just folders |
| `--depth N`  | max depth to scan |
| `--output`   | save to text file |
| `--hidden`   | include hidden files/folders |
| `--ascii`    | use ASCII instead of Unicode box lines |

#### Examples
shellman dir_tree .
shellman dir_tree . --files --depth 2
shellman dir_tree . --output tree.txt
