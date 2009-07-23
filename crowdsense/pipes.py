from django.template.loader import render_to_string
from django.utils.safestring import SafeUnicode

import django_pipes

# TODO: detailed multi-pipe query string API

class TwitterSearch(django_pipes.Pipe):
    name = "Social Updates"
    slug = "social-updates"            # used in template and url path
    uri = "http://search.twitter.com/search.json"
    cache_expiry = 30                   # in seconds

    ## API for Tracker

    # Let's get around django-pipes API's unnecesarry model-likeness
    @classmethod
    def query(cls, query):
        return cls.objects.get( { 'q' : query } )

    def __unicode__(self):
        return self.name

    def get_result_list(self):
        return self.items['results']

    def render_result_list(self):
        return ((
            render_to_string('pipe/twitter/single-result.inc.html', {'object':r})
            for r in self.get_result_list()
            ))
