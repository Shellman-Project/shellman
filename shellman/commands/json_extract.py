import click
import json
from pathlib import Path

@click.command(help="""Extract and filter JSON data with optional field selection.

Examples:
  shellman json_extract data.json --path items --fields id,name
  shellman json_extract data.json --filter status=ERROR --fields id,msg --output errors.json
""")
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--path", "path_expr", help="Key path to list, e.g. 'items'")
@click.option("--filter", "filter_expr", help="Filter: key=value to match")
@click.option("--fields", help="Comma-separated list of fields to select")
@click.option("--output", "output_file", type=click.Path(), help="Save result to file")
@click.option("--interactive", is_flag=True, default=False, help="Pipe output through pager")
def cli(file, path_expr, filter_expr, fields, output_file, interactive):
    file_path = Path(file)
    data = json.loads(file_path.read_text(encoding="utf-8"))

    if path_expr:
        for key in path_expr.split("."):
            if key:
                data = data[key]

    if not isinstance(data, list):
        data = [data]

    if filter_expr and "=" in filter_expr:
        key, value = filter_expr.split("=", 1)
        data = [entry for entry in data if str(entry.get(key)) == value]

    if fields:
        field_list = [f.strip() for f in fields.split(",")]
        data = [{k: v for k, v in entry.items() if k in field_list} for entry in data]

    output = "\n".join(json.dumps(d, ensure_ascii=False) for d in data)

    if output_file:
        Path(output_file).write_text(output, encoding="utf-8")
        click.echo(f"Saved to {output_file}")
        if interactive:
            click.echo_via_pager(output)
    else:
        if interactive:
            click.echo_via_pager(output)
        else:
            click.echo(output)
