"""Frontend web server."""
import asyncio
import logging

from tornado.web import Application, RedirectHandler

from .frontend import FrontendHandler
from .api import (DashboardCollectionHandler, TransactionCollectionHandler, TransactionItemHandler,
                  UncategorisedTransactionCollectionHandler, CategoriesCollectionHandler, CategoriesItemHandler,
                  RulesCollectionHandler)


logger = logging.getLogger(__name__)


def run_server(config):
    """Run the web server."""
    logger.debug('Setting up the web server')
    app = Application(
        [
            ('/', RedirectHandler, {'url': '/app', 'permanent': False}),
            ('/app(.*)', FrontendHandler),
            ('/api/dashboards', DashboardCollectionHandler, {'config': config}),
            ('/api/transactions', TransactionCollectionHandler, {'config': config}),
            ('/api/transactions/(?P<id>[0-9]+)', TransactionItemHandler, {'config': config}),
            ('/api/uncategorised', UncategorisedTransactionCollectionHandler, {'config': config}),
            ('/api/categories', CategoriesCollectionHandler, {'config': config}),
            ('/api/categories/(?P<id>[0-9]+)', CategoriesItemHandler, {'config': config}),
            ('/api/rules', RulesCollectionHandler, {'config': config})
        ],
        debug=True
    )
    app.listen(6543)
    logger.debug('Starting the web server')
    asyncio.get_event_loop().run_forever()
