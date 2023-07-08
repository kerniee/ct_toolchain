from os.path import splitext, basename

import click

from xml_to_acts.drawio import xml_to_acts


@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.File("w"))
def main_cli(input, output):
    with open(input, "r", encoding="utf-8") as f:
        name, _ = splitext(input)
        result = xml_to_acts(f.read(), basename(name))
    output.write(result)


if __name__ == '__main__':
    main_cli()
