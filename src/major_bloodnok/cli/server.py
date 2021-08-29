"""Server cli commands."""
import click

from ..server import run_server


@click.command()
@click.pass_context
def server(ctx: dict):
    """Run the application server."""
    run_server(ctx.obj['config'])
