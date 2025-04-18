#!/usr/bin/env python3
import sys
import json
import yaml
import toml

args = sys.argv[1:]
if len(args) < 3:
    sys.exit("Usage: convert_file.py <file> <from> <to> [--pretty]")

in_path, fmt_in, fmt_out = args[0], args[1].lower(), args[2].lower()
pretty = "--pretty" in args

# -------- load -------- 
with open(in_path, 'r') as f:
    raw = f.read()

if fmt_in == "json":
    data = json.loads(raw)
elif fmt_in == "yaml":
    data = yaml.safe_load(raw)
elif fmt_in == "toml":
    data = toml.loads(raw)
else:
    sys.exit(f"Unsupported input format: {fmt_in}")

# -------- save --------
if fmt_out == "json":
    kwargs = {"indent": 2, "ensure_ascii": False} if pretty else {"separators": (",", ":")}
    print(json.dumps(data, **kwargs))
elif fmt_out == "yaml":
    kwargs = {"indent": 2, "allow_unicode": True} if pretty else {}
    print(yaml.safe_dump(data, **kwargs))
elif fmt_out == "toml":
    print(toml.dumps(data))
else:
    sys.exit(f"Unsupported output format: {fmt_out}")
