from django.conf.urls.defaults import *
from django.views.generic.simple import *

from mashapp import views
from mashapp.models import *


from django.views.generic.list_detail import object_list

urlpatterns = patterns('',
#    (r'^$', direct_to_template, {'template': 'index.html'}),

    (r'^search/$', views.search),
    (r'^results/$', views.results),

    (r'^autocomplete/$', views.autocomplete),

    (r'^twitter/poll/$', views.twitter_poll),
    (r'^twitter/user/(?P<user_id_to_follow>[^\/]+)/follow/$', views.follow_on_twitter),
#    (r'^twitter/tweet/(?P<tweet_id>[^\/]+)/reply/$', views.twitter_reply),
    (r'^twitter/log_out/$', views.twitter_log_out),

    # Views to accept votes on results
    (r'^resultsbyserviceresult_id/(?P<serviceresult_id>[a-zA-Z0-9]+)/(?P<direction>up|down|clear)vote/?$',
        views.xmlhttprequest_vote_on_object, dict(model=ServiceResult)),
    (r'^results/(?P<result_id_>[a-zA-Z0-9]+)/(?P<direction>up|down|clear)vote/?$',
        views.xmlhttprequest_vote_on_object, dict(model=ServiceResult)),
)
