import datetime
import rfc822

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import SafeUnicode

import django_pipes


# TODO: detailed multi-pipe query string API


class CSPipeBase(django_pipes.Pipe):
    class Result(object):
        def __init__(self, pipe, data):
            self.pipe = pipe
            self.data = data

        def render(self):
            return render_to_string(
                'pipe/%s/single-result.inc.html' % self.pipe.slug,
                {'object': self})

    def __unicode__(self):
        return self.name

    @classmethod
    def has_slug(cls, slug):
        return cls.slug == slug

    @classmethod
    def query(cls, query):
        raise NotImplementedError

    def get_raw_results(self):
        raise NotImplementedError

    def get_results(self):
        return (( self.Result(self, raw_result)
                  for raw_result in self.get_raw_results() ))


class TwitterSearch(CSPipeBase):
    name = "Twitter"
    slug = "twitter"
    uri = "http://search.twitter.com/search.json"
    cache_expiry = 30

    class Result(CSPipeBase.Result):
        def __init__(self, pipe, data):
            super(TwitterSearch.Result, self).__init__(pipe, data)
            self.timestamp = datetime.datetime(
                *rfc822.parsedate(data.created_at)[:6])

    @classmethod
    def query(cls, query):
        return cls.objects.get({'q': query})

    def get_raw_results(self):
        return self.results


class IdenticaSearch(TwitterSearch):
    name = 'Identi.ca'
    slug = 'identica'
    uri = 'http://identi.ca/api/search.json'


class BingNews(CSPipeBase):
    name = "News"
    slug = "news"

    uri = 'http://api.bing.net/json.aspx'
    query_base = {
        'AppId': settings.BING_APP_ID,
        'Version': '2.2',
        'Sources': 'news',
        }
    cache_expiry = 1800

    @classmethod
    def query(cls, query):
        q = cls.query_base.copy()
        q.update(Query=query)
        return cls.objects.get(q)

    def get_raw_results(self):
        return self.SearchResponse.News.Results
