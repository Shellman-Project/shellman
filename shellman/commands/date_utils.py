import importlib.resources
import re
from datetime import datetime, timedelta

import click
from dateutil.relativedelta import relativedelta


@click.command(
    help="Work with dates: add/subtract time, compare or format."
)
@click.option("--date","-d", "base_date", help="Base date (default: now)", default=None)
@click.option("--add","-a", "add_input", help="Add duration (e.g. 5d, 3w, 2h, 10min)")
@click.option("--sub","-s", "sub_input", help="Subtract duration")
@click.option("--diff","-df", "diff_date", help="Date to compare to (diff mode)")
@click.option("--format","-f", "format_pattern", help="Format output using strftime")
@click.option("--lang-help","-lh", "lang", help="Show localized help (pl, eng) instead of executing the command")
def cli(base_date, add_input, sub_input, diff_date, format_pattern, lang):
    """
    Command-line tool for date and time calculations.

    Supports:
      • Parsing a base date (or using current time by default).
      • Adding or subtracting durations (days, weeks, months, years, hours, etc.).
      • Calculating the difference between two dates.
      • Formatting dates using strftime patterns.

    Args:
        base_date (str | None): Base date as "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS".
            Defaults to now if not provided.
        add_input (str | None): Duration to add (e.g. "5d", "3w", "2h", "10min").
        sub_input (str | None): Duration to subtract in the same format as `add_input`.
        diff_date (str | None): Second date to compare to base date.
        format_pattern (str | None): Output format (strftime).
        lang (str | None): Show localized help ("pl" or "eng") instead of executing.

    Raises:
        click.ClickException: If date parsing fails, or invalid duration format/unit is given.

    Examples:
        Add 7 days to current date:
            $ shellman date_utils --add 7d

        Subtract 2 months from a given date:
            $ shellman date_utils -d "2025-01-15" --sub 2m

        Compare two dates:
            $ shellman date_utils -d "2025-01-01" --diff "2025-01-10"

        Format output date:
            $ shellman date_utils --add 1y --format "%A, %d %B %Y"
    """
    if lang:
        print_help_md(lang)
        return

    if base_date:
        try:
            dt = datetime.strptime(base_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                dt = datetime.strptime(base_date, "%Y-%m-%d")
            except ValueError:
                raise click.ClickException(f"Invalid base date: {base_date}")
    else:
        dt = datetime.now()

    result = dt

    def parse_duration(dur):
        match = re.match(r"(\d+)([a-zA-Z]+)", dur)
        if not match:
            raise click.ClickException(f"Invalid duration format: {dur}")
        num = int(match.group(1))
        unit = match.group(2).lower()
        return num, unit

    def apply_delta(dt, num, unit, sign):
        if sign == "-":
            num *= -1
        if unit == "d":
            return dt + timedelta(days=num)
        elif unit == "w":
            return dt + timedelta(weeks=num)
        elif unit == "m":
            return dt + relativedelta(months=num)
        elif unit == "y":
            return dt + relativedelta(years=num)
        elif unit == "q":
            return dt + relativedelta(months=3 * num)
        elif unit == "h":
            return dt + timedelta(hours=num)
        elif unit == "min":
            return dt + timedelta(minutes=num)
        elif unit == "s":
            return dt + timedelta(seconds=num)
        else:
            raise click.ClickException(f"Unsupported unit: {unit}")

    if add_input:
        n, u = parse_duration(add_input)
        result = apply_delta(dt, n, u, "+")
        click.echo(f"→ {n}{u} after {dt.strftime('%F %T')}: {result.strftime('%F %T')}")

    if sub_input:
        n, u = parse_duration(sub_input)
        result = apply_delta(dt, n, u, "-")
        click.echo(f"→ {n}{u} before {dt.strftime('%F %T')}: {result.strftime('%F %T')}")

    if diff_date:
        try:
            other = datetime.strptime(diff_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                other = datetime.strptime(diff_date, "%Y-%m-%d")
            except ValueError:
                raise click.ClickException(f"Invalid comparison date: {diff_date}")
        delta = other - dt
        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        click.echo(f"→ Difference between {dt.strftime('%F %T')} and {other.strftime('%F %T')}:\n  {days} days, {hours} hours, {minutes} minutes, {secs} seconds")

    if format_pattern:
        if result != dt:
            click.echo(f"→ base:    {dt.strftime(format_pattern)}")
            click.echo(f"→ result:  {result.strftime(format_pattern)}")
        else:
            click.echo(f"→ formatted: {dt.strftime(format_pattern)}")


def print_help_md(lang="eng"):
    """Print localized help text for the `date_utils` command."""
    lang_file = f"help_{lang.lower()}.md"
    try:
        help_path = importlib.resources.files("shellman").joinpath(f"help_texts/date_utils/{lang_file}")
        content = help_path.read_text(encoding="utf-8")
        click.echo(content)
    except Exception:
        click.echo(f"⚠️ Help not available for language: {lang}", err=True)
