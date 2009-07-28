import datetime
import rfc822

import dateutil.parser

from django.conf import settings

from baseclasses import *


class TwitterSearch(Source):
    name = "Twitter"
    slug = "twitter"
    uri = "http://search.twitter.com/search.json"
    cache_expiry = 30

    class Result(Source.Result):

        def __init__(self, source, data):
            super(TwitterSearch.Result, self).__init__(source, data)

            # parse Twitter's timestamp
            self.timestamp = datetime.datetime(
                *rfc822.parsedate(data.created_at)[:6])

        def __cmp__(self, other):
            # sort by reverse timestamp
            return -cmp(self.timestamp, other.timestamp)

        def indexing_data(self):
            return {
                'result_id': self.data.id,
                'result_text': self.data.text,
                'result_timestamp': self.timestamp,
                'author_s': self.data.from_user,
                }

    @classmethod
    def query_dict(cls, query):
        return {'q': query}

    def get_raw_results(self):
        return self.results


class IdenticaSearch(TwitterSearch):
    name = 'Identi.ca'
    slug = 'identica'
    uri = 'http://identi.ca/api/search.json'


class BingNews(Source):
    name = "News"
    slug = "news"

    uri = 'http://api.bing.net/json.aspx'
    query_base = {
        'AppId': settings.BING_APP_ID,
        'Version': '2.2',
        'Sources': 'news',
        }
    cache_expiry = 1800

    class Result(Source.Result):

        def indexing_data(self):
            return {
                'result_id': self.data.Url,
                'result_text': self.data.Title + "\n" + self.data.Snippet,
                'result_timestamp': dateutil.parser.parse(self.data.Date),
                'source_s': self.data.Url,
                'breaking_b': bool(self.data.BreakingNews),
                'title_s': self.data.Title,
                'snippet_t': self.data.Snippet,
                }

    @classmethod
    def query_dict(cls, query):
        q = cls.query_base.copy()
        q.update(Query=query)
        return q

    def get_raw_results(self):
        if hasattr(self.SearchResponse, 'News'):
            return self.SearchResponse.News.Results
        return ()
