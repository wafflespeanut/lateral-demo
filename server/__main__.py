from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

import endpoints
import os

DEFAULT_PORT = 8080


if __name__ == "__main__":
    app = Application(handlers=endpoints.getHandlers())
    server = HTTPServer(app)
    port = DEFAULT_PORT

    try:
        portStr = os.environ.get('PORT')
        if portStr is not None:
            port = int(portStr)
    except ValueError:
        pass

    print('Listening on port', port)
    server.listen(port)
    IOLoop.current().start()
