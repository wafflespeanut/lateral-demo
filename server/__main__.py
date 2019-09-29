from client import LateralApiClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

import endpoints
import os
import sys

DEFAULT_PORT = 8000


if __name__ == "__main__":
    apiKey = os.environ.get('API_KEY')
    if apiKey is None:
        sys.exit('API_KEY must be set as an environment variable.')
    client = LateralApiClient(apiKey=apiKey)

    app = Application(handlers=endpoints.getHandlers(apiClient=client))
    # Set `xheaders` so that it understands X-* headers from nginx
    server = HTTPServer(app, xheaders=True)
    port = DEFAULT_PORT

    try:
        portStr = os.environ.get('PORT')
        if portStr is not None:
            port = int(portStr)
    except ValueError:
        pass

    print('Listening on port', port)
    server.listen(port, address='127.0.0.1')
    IOLoop.current().start()
