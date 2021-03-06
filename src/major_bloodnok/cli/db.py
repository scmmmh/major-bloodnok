"""Database cli commands."""
import asyncio
import click
import logging

from sqlalchemy import select

from ..models import create_engine, create_sessionmaker, Base, Category


logger = logging.getLogger(__name__)


async def cmd_init(config: dict, drop_existing: bool):
    """Initialise the database.

    @param config The configuration to use
    @type config dict
    @param drop_existing Drop existing database tables
    @type drop_existing bool
    """
    engine = create_engine(config['database']['dsn'])
    async with engine.begin() as conn:
        if drop_existing:
            logger.debug('Dropping existing database tables')
            await conn.run_sync(Base.metadata.drop_all)
        logger.debug('Creating the database')
        await conn.run_sync(Base.metadata.create_all)
        async with create_sessionmaker(config['database']['dsn'])() as session:
            async with session.begin():
                stmt = select(Category).filter(Category.title == 'Uncategorised')
                result = await conn.execute(stmt)
                if not result.scalars().first():
                    session.add(Category(title='Uncategorised', parent_id=None))
    logger.debug('Database created')


@click.command()
@click.option('--drop-existing', is_flag=True, default=False, help='Drop any existing tables')
@click.pass_context
def init(ctx, drop_existing):
    """Initialise the database."""
    asyncio.run(cmd_init(ctx.obj['config'], drop_existing))


@click.group()
def db():
    """Database commands."""
    pass


db.add_command(init)
