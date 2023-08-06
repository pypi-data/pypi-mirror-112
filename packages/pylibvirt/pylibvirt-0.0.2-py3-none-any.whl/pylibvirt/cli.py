#! /usr/bin/python
"""Console script for pylibvirt_."""
import sys
import click

from pylibvirt import Manager


@click.command()
@click.option('--template', '-t', help='hypervisor connection URI', required=True,
              default="./template/template.yml")
@click.option('--force-redefine', '-f', help='Force to redefine XML Element if it already exist', is_flag=True)
def main(args=None, **kwargs):
    """Console script for pylibvirt_."""
    click.echo("Replace this message by putting your code into "
               "pylibvirt_.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    m = Manager(template=kwargs['template'], force_redefine=kwargs['force_redefine'])
    m.print()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
