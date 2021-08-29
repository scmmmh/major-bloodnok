"""Frontend web server."""
import asyncio
import logging

from tornado.web import Application, RedirectHandler

from .frontend import FrontendHandler


logger = logging.getLogger(__name__)


def run_server(config):
    """Run the web server."""
    logger.debug('Setting up the web server')
    app = Application(
        [
            ('/', RedirectHandler, {'url': '/app', 'permanent': False}),
            ('/app(.*)', FrontendHandler),
        ],
        debug=True
    )
    app.listen(6543)
    logger.debug('Starting the web server')
    asyncio.get_event_loop().run_forever()
