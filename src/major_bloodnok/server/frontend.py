"""Frontend handler classes."""
from mimetypes import guess_type
from importlib import resources
from tornado.web import RequestHandler, HTTPError


class FrontendHandler(RequestHandler):
    """Handler for the frontend application files."""

    def get(self, path: str):
        """Get the file at the given path.

        :param path: The path to get.
        :type: path: str
        """
        if not path.strip():
            path = '/'
        base = resources.files('major_bloodnok')
        public = base / 'frontend' / 'public'
        try:
            self._get_resource(public, path.split('/')[1:])
        except FileNotFoundError:
            try:
                self._get_resource(public, path.split('/')[1:] + ['index.html'])
            except FileNotFoundError:
                raise HTTPError(404)

    def _get_resource(self, resource, path: list[str]):
        """Send a file.

        Performs mimetype guessing and sets the appropriate Content-Type header.

        :param resource: The root resource to serve files from
        :type resource: importlib.Traversable
        :param path: The path to the file to send
        :type path: list[str]
        """
        for part in path:
            resource = resource / part
        data = resource.read_bytes()
        mimetype = guess_type(path[-1])
        if mimetype:
            self.set_header('Content-Type', mimetype[0])
        self.write(data)
