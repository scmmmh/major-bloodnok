"""Database models."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .meta import Base  # noqa
from .transaction import Transaction  # noqa
from .category import Category  # noqa
from .rule import Rule  # noqa


logger = logging.getLogger(__name__)


def create_engine(dsn: str):
    """Create a database engine."""
    logger.debug(f'Creating engine for {dsn}')
    return create_async_engine(dsn)


def create_sessionmaker(dsn: str):
    """Create a database session."""
    logger.debug('Creating sessionmaker')
    return sessionmaker(
        create_engine(dsn),
        expire_on_commit=False,
        class_=AsyncSession
    )
