"""API Handlers."""
import logging

from sqlalchemy import select
from tornado.web import RequestHandler, HTTPError

from ..models import create_sessionmaker, Transaction


logger = logging.getLogger(__name__)


class CollectionHandler(RequestHandler):
    """Generic handler for JSONAPI collections."""

    def initialize(self, config):
        """Initialise with the given ``config``.

        :param config: The configuration to use
        :type config: dict
        """
        self._config = config

    async def get(self, cls):
        """Fetch all entries of the given ``cls``.

        :param cls: The class of objects to fetch
        :type cls: class
        """
        logger.debug(f'GET {cls.__name__}')
        async with create_sessionmaker(self._config['database']['dsn'])() as session:
            stmt = select(cls)
            result = await session.execute(stmt)
            self.write({'data': [item.jsonapi() for item in result.scalars()]})


class ItemHandler(RequestHandler):
    """Generic handler for a single JSONAPI item."""

    def initialize(self, config):
        """Initialise with the given ``config``.

        :param config: The configuration to use
        :type config: dict
        """
        self._config = config

    async def get(self, cls, id):
        """Fetch the entry of the given ``cls`` with the given ``id``.

        :param cls: The class of objects to fetch
        :type cls: class
        """
        logger.debug(f'GET {cls.__name__} {id}')
        async with create_sessionmaker(self._config['database']['dsn'])() as session:
            stmt = select(cls).filter(getattr(cls, 'id') == id)
            result = await session.execute(stmt)
            obj = result.scalars().first()
            if obj:
                self.write({'data': obj})
            else:
                raise HTTPError(404)


class TransactionCollectionHandler(CollectionHandler):
    """Collection handler for Transactions."""

    async def get(self):
        """Fetch all Transactions."""
        await super().get(Transaction)


class TransactionItemHandler(ItemHandler):
    """Item handler for Transactions."""

    async def get(self, id):
        """Fetch the Transaction with the given ``id``."""
        await super().get(Transaction, id)
