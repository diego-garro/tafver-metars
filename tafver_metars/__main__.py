import click

from . import __version__

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()

@click.group()
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def taf_ver():
    pass

if __name__ == '__main__':
    taf_ver()