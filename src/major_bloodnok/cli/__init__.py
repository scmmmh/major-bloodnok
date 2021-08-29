"""Commandline-interface package."""
import click
import logging
import logging.config

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .db import db


logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def main(ctx):
    """Major Bloodnok application."""
    with open('config.yml') as in_f:
        config = load(in_f, Loader=Loader)
    if 'logging' in config:
        config['logging']['disable_existing_loggers'] = False
        logging.config.dictConfig(config['logging'])
        logger.debug('Logging set up')
    ctx.obj = {'config': config}


main.add_command(db)
