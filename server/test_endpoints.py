from datetime import datetime
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from server import endpoints
import json


class TestHandlers(AsyncHTTPTestCase):
    def get_app(self):
        return Application(handlers=endpoints.getHandlers())

    def test_root_handler_current_time(self):
        '''
        Expects the root handler to return current time
        in JSON format.
        '''

        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        body = response.body.decode('utf-8')
        obj = json.loads(body)
        now = datetime.now()
        then = datetime.strptime(obj['message'], '%Y-%m-%d %H:%M:%S')
        # Verify that the seconds difference is atmost 1.
        self.assertTrue(
            now.second == then.second or now.second - then.second == 1)
        # Replace seconds so that we can compare the rest of the object
        self.assertEqual(now.replace(second=0, microsecond=0),
                         then.replace(second=0))
