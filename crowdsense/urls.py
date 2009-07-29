from django.conf.urls.defaults import *

import views

urlpatterns = patterns(
    '',
    url(r'^(?P<slug>[-\w]+)/$', views.tracker_main, name='tracker_main'),
    url(r'^(?P<slug>[-\w]+)/(?P<channel_slug>[-\w]+)/((?P<source_slug>[-\w]+)/)?$',
        views.tracker_channel, name='tracker_channel'),
    # dot character does not occur in slugs, we use it in special urls
    url(r'^.create/$', views.tracker_create, name='tracker_create'),
    url(r'^(?P<slug>[-\w]+)/.edit/$', views.tracker_edit, name='tracker_edit'),
    url(r'^(?P<slug>[-\w]+)/.delete/$', views.tracker_delete,
        name='tracker_delete'),
    )
