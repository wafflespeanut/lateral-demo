import React from 'react';
import { shallow } from 'enzyme';
import App from './App';
import ApiClient from '../api/client';
import Recommendation from '../api/models/recommendation';

const TEST_DATE: Date = new Date('2019-09-28 23:59:59+0000');

/** Test API client. */
class TestApiClient implements ApiClient {
  getServerTime(): Promise<Date> {
    return new Promise((resolve) => resolve(TEST_DATE));
  }

  getSimilarNews(text: string): Promise<Array<Recommendation<Date>>> {
    return new Promise((resolve) => resolve([{
      document_id: 5225542,
      similarity: 0.65,
      title: text,
      url: 'http://foo.bar',
      published: TEST_DATE,
      author: null,
      image: null,
      thumbnail: false,
      summary: 'Hello, world!',
      source_name: 'unknown',
      source_slug: 'unknown',
    }]))
  }
}

/** Wrapper for `App` to aid unit testing. */
class TestApp extends App {
  client: ApiClient = new TestApiClient();
}

it('sets server time on mount', () => {
  const app = shallow(<TestApp />);
  const instance = app.instance() as any;
  const spy = jest.spyOn(instance, 'setServerTime');
  instance.componentDidMount();
  expect(spy).toHaveBeenCalled();
});
