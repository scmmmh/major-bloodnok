"""API Handlers."""
import logging
import dateparser
import re

from csv import DictReader
from datetime import date, timedelta
from io import StringIO
from sqlalchemy import select, and_, func, desc
from tornado.web import RequestHandler, HTTPError

from ..models import create_sessionmaker, Transaction, Category, Rule


logger = logging.getLogger(__name__)


async def apply_rule(session, rule):
    async with session.begin():
        uncategorised = (await session.execute(select(Category).
                         filter(Category.title == 'Uncategorised'))).scalars().first()
        transactions = (await session.execute(select(Transaction).
                        filter(Transaction.category_id == uncategorised.id))).scalars()
        for transaction in transactions:
            if re.match(rule.description, transaction.description) and rule.direction == transaction.direction:
                transaction.category_id = rule.category_id
                session.add(transaction)


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
            if self.get_argument('page[offset]', default=None):
                stmt = stmt.offset(int(self.get_argument('page[offset]', '0')))
                stmt = stmt.limit(int(self.get_argument('page[limit]', '30')))
            result = await session.execute(stmt)
            self.write({'data': [item.jsonapi() for item in result.scalars()]})

    async def post(self, cls):
        """Create a new instance of the given ``cls``.

        :param cls: The class of object to create
        :type cls: class
        """
        logger.debug(f'POST {cls.__name__}')
        async with create_sessionmaker(self._config['database']['dsn'])() as session:
            async with session.begin():
                obj = cls.from_jsonapi(self.request.body)
                session.add(obj)
            self.write({'data': obj.jsonapi()})
        return obj


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
                self.write({'data': obj.jsonapi()})
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
                    unclassified = (await session.execute(select(Category).
                                    filter(Category.title == 'Uncategorised'))).scalars().first()
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
                        data['category_id'] = unclassified.id
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


class UncategorisedTransactionCollectionHandler(CollectionHandler):
    """Collection handler for uncategorised Transactions."""

    async def get(self):
        """Fetch all uncategorised Transactions."""
        logger.debug('GET uncategorised Transaction')
        async with create_sessionmaker(self._config['database']['dsn'])() as session:
            stmt = select(Category).filter(Category.title == 'Uncategorised')
            uncategorised = (await session.execute(stmt)).scalars().first()
            if uncategorised:
                stmt = select(Transaction).filter(Transaction.category_id == uncategorised.id).\
                    order_by(desc(Transaction.date))
                if self.get_argument('page[offset]', default=None):
                    stmt = stmt.offset(int(self.get_argument('page[offset]', '0')))
                    stmt = stmt.limit(int(self.get_argument('page[limit]', '30')))
                result = await session.execute(stmt)
                self.write({'data': [item.jsonapi() for item in result.scalars()]})
            else:
                self.write({'data': []})


class CategoriesCollectionHandler(CollectionHandler):
    """Collection handler for Categories."""

    async def get(self):
        """Get all Categories."""
        await super().get(Category)

    async def post(self):
        """Create a new Category."""
        await super().post(Category)


class CategoriesItemHandler(ItemHandler):
    """Item handler for Categories."""

    async def get(self, id):
        """Get a single Category with the given ``id``."""
        await super().get(Category, id)


class RulesCollectionHandler(CollectionHandler):
    """Collection handler for Rules."""

    async def get(self):
        """Get all Rules."""
        await super().get(Rule)

    async def post(self):
        """Create a new Rule."""
        rule = await super().post(Rule)
        async with create_sessionmaker(self._config['database']['dsn'])() as session:
            await apply_rule(session, rule)
