from pathlib import Path
import json
import os
import importlib.resources

import click
import yaml
import toml


@click.command(
    help="Convert between JSON, YAML and TOML formats."
)
@click.argument("file", required=False)
@click.option("--from", "from_format",
              required=False,
              type=click.Choice(["json", "yaml", "toml"]),
              help="Input format (required unless using --lang-help)")

@click.option("--to", "to_format",
              required=False,
              type=click.Choice(["json", "yaml", "toml"]),
              help="Output format (required unless using --lang-help)")

@click.option("--output", "output_file", type=click.Path(), help="Save to file instead of stdout")
@click.option("--pretty", is_flag=True, help="Pretty-print output (where supported)")
@click.option("--interactive", is_flag=True, help="Pipe output to less (if no --output)")
@click.option("--lang-help", "lang", help="Show localized help (pl, eng) instead of executing")
def cli(file, from_format, to_format, output_file, pretty, interactive, lang):
    # ---------- lokalizowana pomoc ---------- #
    if lang:
        _print_help_md(lang)
        return

    # ---------- walidacja ---------- #
    if not file:
        raise click.UsageError("Missing required argument 'file'")
    if not from_format:
        raise click.UsageError("Missing required option '--from'")
    if not to_format:
        raise click.UsageError("Missing required option '--to'")

    path = Path(file)
    raw = path.read_text(encoding="utf-8")

    # ---------- parse input ---------- #
    if from_format == "json":
        data = json.loads(raw)
    elif from_format == "yaml":
        data = yaml.safe_load(raw)
    elif from_format == "toml":
        data = toml.loads(raw)
    else:
        raise click.ClickException(f"Unsupported input format: {from_format}")

    # ---------- convert ---------- #
    if to_format == "json":
        kwargs = {"indent": 2, "ensure_ascii": False} if pretty else {"separators": (",", ":")}
        result = json.dumps(data, **kwargs)
    elif to_format == "yaml":
        kwargs = {"indent": 2, "allow_unicode": True} if pretty else {}
        result = yaml.safe_dump(data, **kwargs)
    elif to_format == "toml":
        result = toml.dumps(data)
    else:
        raise click.ClickException(f"Unsupported output format: {to_format}")

    # ---------- output ---------- #
    if output_file:
        Path(output_file).write_text(result, encoding="utf-8")
        click.echo(f"Saved to {output_file}")
        if interactive:
            os.system(f"less -S {output_file}")
    elif interactive:
        click.echo_via_pager(result)
    else:
        click.echo(result)


# ---------- Markdown help loader ---------- #
def _print_help_md(lang: str = "eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/file_convert/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
