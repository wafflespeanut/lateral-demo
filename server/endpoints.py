from client import LateralApiClient
from datetime import datetime
from tornado.escape import json_encode
from tornado.web import RequestHandler


class MainHandler(RequestHandler):
    '''
    Root handler which responds with the current UTC datetime in a JSON object.
    '''

    def get(self):
        currentTime = datetime.utcnow()
        self.write({
            'message': datetime.strftime(currentTime, '%Y-%m-%d %H:%M:%S+0000')
        })


class RecommendationsHandler(RequestHandler):
    '''
    Handler which gets text from the incoming request body
    and responds with news similar to that text using Lateral API.
    '''

    def initialize(self, client: LateralApiClient):
        self.client = client

    async def post(self):
        text = self.request.body.decode('utf-8')
        text = text.strip()
        if text == '':
            self.set_status(400,  'Text must not be empty.')
            return

        news = await self.client.getRecommendedNews(similarToText=text)
        self.write(json_encode(news))


def getHandlers(apiClient):
    '''Returns the handlers to be registered with the Tornado application.'''

    return [
        (r"/", MainHandler),
        (r"/recommendations", RecommendationsHandler, dict(client=apiClient)),
    ]
