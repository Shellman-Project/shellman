import click
import json
import yaml
import toml
from pathlib import Path
import sys
import os

@click.command(help="""Converts between JSON, YAML, and TOML formats.

Examples:
  shellman file_convert config.json --from json --to yaml
  shellman file_convert config.toml --from toml --to json --pretty --output out.json
""")
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--from", "from_format", required=True, type=click.Choice(["json", "yaml", "toml"]), help="Input format")
@click.option("--to", "to_format", required=True, type=click.Choice(["json", "yaml", "toml"]), help="Output format")
@click.option("--output", "output_file", type=click.Path(), help="Save to file instead of stdout")
@click.option("--pretty", is_flag=True, help="Pretty print output (if supported)")
@click.option("--interactive", is_flag=True, default=False, help="Pipe output to less (if no --output)")
def cli(file, from_format, to_format, output_file, pretty, interactive):
    path = Path(file)

    with path.open("r", encoding="utf-8") as f:
        raw = f.read()

    # Load data
    if from_format == "json":
        data = json.loads(raw)
    elif from_format == "yaml":
        data = yaml.safe_load(raw)
    elif from_format == "toml":
        data = toml.loads(raw)
    else:
        click.echo(f"Unsupported input format: {from_format}", err=True)
        raise click.Abort()

    # Convert
    if to_format == "json":
        kwargs = {"indent": 2, "ensure_ascii": False} if pretty else {"separators": (",", ":")}
        result = json.dumps(data, **kwargs)
    elif to_format == "yaml":
        kwargs = {"indent": 2, "allow_unicode": True} if pretty else {}
        result = yaml.safe_dump(data, **kwargs)
    elif to_format == "toml":
        result = toml.dumps(data)
    else:
        click.echo(f"Unsupported output format: {to_format}", err=True)
        raise click.Abort()

    # Output
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        click.echo(f"Saved to {output_file}")
        if interactive:
            os.system(f"less -S {output_file}")
    elif interactive:
        click.echo_via_pager(result)
    else:
        click.echo(result)
