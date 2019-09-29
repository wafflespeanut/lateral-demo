from client import LateralApi
from datetime import datetime
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

import endpoints
import json


class TestApiClient(LateralApi):
    '''Test client wrapper for Lateral API.'''

    def __init__(self):
        self.similarNews = [{
            'foo': 'bar'
        }]

    async def getRecommendedNews(self, similarToText):
        return self.similarNews


class TestHandlers(AsyncHTTPTestCase):
    '''Tests associated with endpoints.'''

    def get_app(self):
        client = TestApiClient()
        return Application(handlers=endpoints.getHandlers(apiClient=client))

    def test_root_handler_current_time(self):
        '''
        Expects the root handler to return current time
        in JSON format.
        '''

        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        body = response.body.decode('utf-8')
        obj = json.loads(body)
        now = datetime.utcnow()
        then = datetime.strptime(obj['message'], '%Y-%m-%d %H:%M:%S+0000')
        # Verify that the seconds difference is atmost 1.
        self.assertTrue(
            now.second == then.second or now.second - then.second == 1)
        # Replace seconds so that we can compare the rest of the object
        self.assertEqual(now.replace(second=0, microsecond=0),
                         then.replace(second=0))

    def test_similar_news_empty_body(self):
        '''
        If the recommendations handler gets an empty text, then it should
        respond with 400 status code.
        '''
        response = self.fetch('/recommendations', method='POST', body='')
        self.assertEqual(response.code, 400)

    def test_similar_news(self):
        '''
        Expects the recommendations handler to proxy JSON object
        from TestApiClient.
        '''

        response = self.fetch('/recommendations', method='POST', body='foobar')
        self.assertEqual(response.code, 200)
        body = response.body.decode('utf-8')
        obj = json.loads(body)
        self.assertEqual(obj, [{'foo': 'bar'}])
