import importlib.resources
import json
from pathlib import Path

import click


@click.command(
    help="Extract and filter JSON data with optional field selection."
)
@click.argument("file", required=False)
@click.option("--path", "-p", "path_expr", help="Dot-separated key path to list/obj, e.g. 'items' or 'root.nested.items'")
@click.option("--filter", "-fl", "filter_expr", help="Filter: key=value to match (string compare)")
@click.option("--fields", "-fld", help="Comma-separated list of fields to include in output")
@click.option("--output", "-o", "output_file", type=click.Path(), help="Save result to file")
@click.option("--interactive", "-i", is_flag=True, help="Pipe result through pager")
@click.option("--lang-help", "-lh", "lang", help="Show localized help (pl, eng) instead of executing")
def cli(file, path_expr, filter_expr, fields, output_file, interactive, lang):
    if lang:
        _print_help_md(lang)
        return

    if not file:
        raise click.UsageError("Missing required argument 'file'")

    file_path = Path(file)
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception as e:
        raise click.ClickException(f"Failed to read/parse JSON: {e}") from e

    if path_expr:
        for key in path_expr.split("."):
            if key:
                try:
                    data = data[key]
                except Exception as e:
                    raise click.ClickException(f"Key '{key}' not found in path '{path_expr}'") from e

    if not isinstance(data, list):
        data = [data]

    if filter_expr and "=" in filter_expr:
        key, value = filter_expr.split("=", 1)
        data = [entry for entry in data if str(entry.get(key)) == value]

    if fields:
        field_list = [f.strip() for f in fields.split(",")]
        data = [{k: v for k, v in entry.items() if k in field_list} for entry in data]

    output_text = "\n".join(json.dumps(d, ensure_ascii=False) for d in data)

    if output_file:
        Path(output_file).write_text(output_text, encoding="utf-8")
        click.echo(f"Saved to {output_file}")
        if interactive:
            click.echo_via_pager(output_text)
    else:
        if interactive:
            click.echo_via_pager(output_text)
        else:
            click.echo(output_text)


# ---------- Markdown help loader ---------- #
def _print_help_md(lang: str = "eng"):
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(
            f"help_texts/json_extract/{lang_file}"
        )
        click.echo(help_path.read_text(encoding="utf-8"))
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
