import importlib.resources
import json
import os
from pathlib import Path

import click
import toml
import yaml


@click.command(
    help="Convert between JSON, YAML and TOML formats."
)
@click.argument("file", required=False)
@click.option("--from", "-f", "from_format",
              required=False,
              type=click.Choice(["json", "yaml", "toml"]),
              help="Input format (required unless using --lang-help)")
@click.option("--to", "-t", "to_format",
              required=False,
              type=click.Choice(["json", "yaml", "toml"]),
              help="Output format (required unless using --lang-help)")
@click.option("--output", "-o", "output_file", type=click.Path(), help="Save to file instead of stdout")
@click.option("--pretty", "-p", is_flag=True, help="Pretty-print output (where supported)")
@click.option("--interactive", "-i", is_flag=True, help="Pipe output to less (if no --output)")
@click.option("--lang-help", "-lh", "lang", help="Show localized help (pl, eng) instead of executing")
def cli(file, from_format, to_format, output_file, pretty, interactive, lang):
    """
    Command-line interface for converting between JSON, YAML, and TOML formats.

    Reads a configuration file in one format and converts it to another format.
    Supports pretty-printing, interactive viewing with pager, and saving to files.
    Args:
        file (str | None): Path to the input file to convert.
        from_format (str | None): Source format ("json", "yaml", or "toml").
            Required unless `lang` is provided.
        to_format (str | None): Target format ("json", "yaml", or "toml").
            Required unless `lang` is provided.
        output_file (str | None): Path to save converted output. If not provided,
            prints to stdout or uses pager if `interactive` is True.
        pretty (bool): Enable pretty-printing with indentation and formatting.
            Affects JSON and YAML output.
        interactive (bool): Use pager (less) to display output. If `output_file`
            is specified, opens the saved file in pager after writing.
        lang (str | None): Print localized help ("pl", "eng") instead of executing
            the conversion.

    Raises:
        click.UsageError: If required arguments `file`, `from_format`, or
            `to_format` are missing (unless using `--lang-help`).
        click.ClickException: If an unsupported format is specified or if
            file parsing fails.

    Examples:
        Convert JSON to YAML with pretty formatting:
            $ shellman file_convert config.json --from json --to yaml --pretty

        Convert TOML to JSON and save to file:
            $ shellman file_convert settings.toml --from toml --to json -o config.json

        View conversion interactively:
            $ shellman file_convert data.yaml --from yaml --to json --interactive
    """
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
    """Print localized help text for the `file_convert` command."""
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/file_convert/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
