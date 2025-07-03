🔄 **file_convert – Convert between JSON, YAML and TOML**

Convert any supported text-based configuration file from one format to another.

---

### 🔧 Options

| option | required | description |
|--------|----------|-------------|
| `--from json|yaml|toml` | ✔ | Input format |
| `--to   json|yaml|toml` | ✔ | Output format |
| `--output FILE` | ✗ | Write result to file instead of stdout |
| `--pretty` | ✗ | Pretty-print (indent / unicode) where supported |
| `--interactive` | ✗ | Pipe result to `less -S` (ignored if `--output` given) |
| `--lang-help pl/eng` | ✗ | Show this help in Polish / English |

---

### 📦 Examples

Convert TOML → JSON (pretty) and save:

shellman file_convert pyproject.toml --from toml --to json --pretty --output config.json
YAML → TOML, view interactively:
shellman file_convert pipeline.yaml --from yaml --to toml --interactive
