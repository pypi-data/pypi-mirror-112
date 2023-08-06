import httpx

import hashlib
import time


class PodcastIndex:
  def __init__(self, api_key=None, api_secret=None, client=None):
    if client:
      self.client = client

    else:
      self.client = httpx.Client()

    self.api_key = api_key
    self.api_secret = api_secret

  def method(self, m, url, **kwargs):
    url = 'https://api.podcastindex.org/api/1.0' + url

    headers = kwargs.get('headers', {})
    headers['User-Agent'] = 'NeutronCast/1.0'
    headers['X-Auth-Date'] = str(int(time.time()))
    headers['X-Auth-Key'] = self.api_key
    shash = self.api_key + self.api_secret + headers['X-Auth-Date']
    headers['Authorization'] = hashlib.sha1(shash.encode()).hexdigest()
    kwargs['headers'] = headers

    self.last_response = getattr(self.client, m)(url, **kwargs)
    return self.last_response.json()

  def get_podcast(self, id=None, url=None, itunes=None, guid=None, ):
    if id:
      return self.method('get', '/podcasts/byfeedid', params={'id': str(id)})

    if url:
      return self.method('get', '/podcasts/byfeedurl', params={'url': url})

    if itunes:
      return self.method('get', '/podcasts/byitunesid', params={'id': str(itunes)})

    if guid:
      return self.method('get', '/podcasts/byguid', params={'guid': guid})

    raise Exception('Invalid lookup')

  def get_podcasts_bytag(self):
    return self.method('get', '/podcasts/bytag', params={'podcast-value': ''})
