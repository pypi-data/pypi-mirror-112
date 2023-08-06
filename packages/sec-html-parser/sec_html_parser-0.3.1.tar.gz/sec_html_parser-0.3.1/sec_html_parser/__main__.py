import click
from pathlib import Path

from sec_html_parser.parser import Parser


@click.command()
@click.argument("target", type=Path)
@click.option(
    "-o",
    "--output",
    type=Path,
    help="Path to output file, will print to stdout if not specified",
    required=False,
    default=None,
)
def main(target: Path, output: Path):
    p = Parser()
    h = p.get_hierarchy_html(target)
    if output is not None:
        output.write_text(h)
    else:
        print(h)


if __name__ == "__main__":
    main()
