from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.escape import json_encode, json_decode


class LateralApi(object):
    '''
    Client interface for Lateral API to aid testing. Errors should be
    propagated and handled outside the subclasses.
    '''

    def __init__(self, apiKey):
        '''Initialize this object with an API key.'''
        self.apiKey = apiKey

    async def getRecommendedNews(self, similarToText):
        '''
        Given a non-empty text, get recommended news for that text
        using Lateral API.
        '''
        raise NotImplementedError


class LateralApiClient(LateralApi):
    '''Actual HTTP client for Lateral API.'''

    # Type-level constants
    baseUrl = 'https://news-api.lateral.io'

    # Relative paths
    similarNewsPath = '/documents/similar-to-text'

    def __init__(self, apiKey):
        super(LateralApiClient, self).__init__(apiKey)
        # Also initialize the async HTTP client (singleton).
        self.client = AsyncHTTPClient()
        self.headers = {
            'subscription-key': self.apiKey,
            'content-type': 'application/json',
        }

    async def getRecommendedNews(self, similarToText):
        req = HTTPRequest(url='%s%s' % (self.baseUrl, self.similarNewsPath),
                          method='POST',
                          headers=self.headers,
                          body=json_encode({'text': similarToText}))
        resp = await self.client.fetch(req)
        return json_decode(resp.body)
