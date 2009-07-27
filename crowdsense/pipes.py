from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import SafeUnicode

import django_pipes


# TODO: detailed multi-pipe query string API


class CSPipeBase(django_pipes.Pipe):

    def __unicode__(self):
        return self.name

    @classmethod
    def has_slug(cls, slug):
        return cls.slug == slug

    # Let's get around django-pipes API's unnecesarry model-likeness

    @classmethod
    def query(cls, query):
        raise NotImplementedError

    def get_results(self):
        raise NotImplementedError


class IdenticaSearch(CSPipeBase):
    name = 'Identi.ca'
    slug = 'identica'
    uri = 'http://identi.ca/api/search.json'

    @classmethod
    def query(cls, query):
        return cls.objects.get({'q': query})

    def get_results(self):
        return self.results


class TwitterSearch(CSPipeBase):
    name = "Twitter"
    slug = "twitter"
    uri = "http://search.twitter.com/search.json"
    cache_expiry = 30                   # in seconds

    @classmethod
    def query(cls, query):
        return cls.objects.get({'q': query})

    def get_results(self):
        return self.results


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

    def get_results(self):
        return self.SearchResponse.News.Results
