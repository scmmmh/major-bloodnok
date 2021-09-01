"""API Handlers."""
import logging
import dateparser

from csv import DictReader
from datetime import date, timedelta
from io import StringIO
from sqlalchemy import select, and_, func, desc
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

    async def get(self, cls, order=None):
        """Fetch all entries of the given ``cls``.

        :param cls: The class of objects to fetch
        :type cls: class
        """
        logger.debug(f'GET {cls.__name__}')
        async with create_sessionmaker(self._config['database']['dsn'])() as session:
            stmt = select(cls)
            if order is not None:
                stmt = stmt.order_by(order)
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


class DashboardCollectionHandler(CollectionHandler):
    """Collection handler for Dashboards.

    This is currently implemented as a static API.
    """
    async def _month_total(self, month, direction, session):
        stmt = select(func.sum(Transaction.amount)).filter(and_(
            Transaction.direction == direction,
            func.DATE(Transaction.date) >= func.DATE(month),
            func.DATE(Transaction.date) < func.DATE((month + timedelta(days=33)).replace(day=1)),
        ))
        result = await session.execute(stmt)
        return result.scalars().first()

    async def _month_out_total(self, session):
        pass

    async def get(self):
        """Fetch all Dashboards."""
        async with create_sessionmaker(self._config['database']['dsn'])() as session:
            month_1 = date.today().replace(day=1)
            month_2 = (month_1 - timedelta(days=1)).replace(day=1)
            month_3 = (month_2 - timedelta(days=1)).replace(day=1)

            self.write({
                'data': [
                    {
                        'name': 'Account',
                        'labels': [month_3.strftime('%B'), month_2.strftime('%B'), month_1.strftime('%B')],
                        'income': [
                            await self._month_total(month_3, 'in', session),
                            await self._month_total(month_2, 'in', session),
                            await self._month_total(month_1, 'in', session)
                        ],
                        'outgoing': [
                            await self._month_total(month_3, 'out', session),
                            await self._month_total(month_2, 'out', session),
                            await self._month_total(month_1, 'out', session)
                        ],
                    }
                ]
            })


class TransactionCollectionHandler(CollectionHandler):
    """Collection handler for Transactions."""

    async def get(self):
        """Fetch all Transactions."""
        await super().get(Transaction, desc(Transaction.date))

    async def post(self):
        """Add new Transactions."""
        logger.debug('POST Transaction')
        if self.request.headers['Content-Type'] == 'text/csv':
            async with create_sessionmaker(self._config['database']['dsn'])() as session:
                async with session.begin():
                    for line in DictReader(StringIO(self.request.body.decode())):
                        data = {
                            'date': dateparser.parse(line['Date'], settings={'PREFER_DAY_OF_MONTH': 'last'}),
                            'description': line['Description'],
                            'initiator': line['Type']
                        }
                        if 'Money In' in line and line['Money In']:
                            data['amount'] = float(line['Money In'])
                            data['direction'] = 'in'
                        elif ' Money Out' in line and line[' Money Out']:
                            data['amount'] = float(line[' Money Out'])
                            data['direction'] = 'out'
                        if line['Type'] == 'TRANSFER':
                            data['direction'] = 'trans'
                        if 'amount' in data:
                            stmt = select(Transaction).filter(and_(
                                func.DATE(Transaction.date) == func.DATE(data['date']),
                                Transaction.description == data['description'],
                                Transaction.amount == data['amount'],
                                Transaction.direction == data['direction']
                            ))
                            if (await session.execute(stmt)).scalars().first() is None:
                                session.add(Transaction(**data))


class TransactionItemHandler(ItemHandler):
    """Item handler for Transactions."""

    async def get(self, id):
        """Fetch the Transaction with the given ``id``."""
        await super().get(Transaction, id)
