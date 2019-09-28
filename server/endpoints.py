from datetime import datetime
from tornado.web import RequestHandler


class MainHandler(RequestHandler):
    '''
    Root handler which responds with the current time in a JSON object.
    '''

    def get(self):
        currentTime = datetime.now()
        self.write({
            'message': datetime.strftime(currentTime, '%Y-%m-%d %H:%M:%S')
        })


class RecommendationsHandler(RequestHandler):
    '''
    Handler which gets text from the incoming request body
    and responds with news similar to that text using Lateral API.
    '''

    def post(self):
        # body = self.request.body.decode('utf-8')
        pass


def getHandlers():
    '''Returns the handlers to be registered with the Tornado application.'''

    return [
        (r"/", MainHandler),
        (r"/recommendations", RecommendationsHandler),
    ]
