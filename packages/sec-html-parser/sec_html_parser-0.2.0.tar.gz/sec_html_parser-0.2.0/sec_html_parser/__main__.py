import click
import json
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
    h = p.get_file_hierarchy(target)
    if output is not None:
        with output.open("w") as output_file:
            json.dump(h, output_file)
    else:
        print(json.dumps(h))


if __name__ == "__main__":
    main()
