from django.conf.urls.defaults import *

import views

urlpatterns = patterns(
    '',
    url(r'^(?P<slug>[-\w]+)/$', views.tracker_main, name='tracker_main'),
    url(r'^(?P<slug>[-\w]+)/(?P<channel_slug>[-\w]+)/$', views.tracker_channel, name='tracker_channel'),

     # _ character does not occur in slugs, we use it in special urls
    url(r'^__create__/$', views.tracker_create, name='tracker_create'),
    url(r'^__edit__/(?P<slug>[-\w]+)/$', views.tracker_edit, name='tracker_edit'),
    )
