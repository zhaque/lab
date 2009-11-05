from django.conf.urls.defaults import *
from django.conf import settings

from django.views.generic.simple import *

from account.openid_consumer import PinaxConsumer

from django.contrib import admin
admin.autodiscover()

import os

urlpatterns = patterns('',
    (r'^app/', include('mashapp.urls')),

    
    url(r'^$', direct_to_template, {"template": "homepage.html"}, name="home"),
    
    (r'^about/', include('about.urls')),
    (r'^account/', include('account.urls')),
    (r'^openid/(.*)', PinaxConsumer()),
    (r'^profiles/', include('basic_profiles.urls')),
    (r'^notices/', include('notification.urls')),
    (r'^announcements/', include('announcements.urls')),
    
    # http://django-cms.org/installation/
#    (r'^admin/', include('cms.admin_urls')),

    (r'^admin/(.*)', admin.site.root),


#    (r'^$', redirect_to, {'url': 'app/search'}),

     # configure django-cms at the page root / 
#    (r'^((.*)/)?$', include('cms.urls')),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('', 
        (r'^site_media/(?P<path>.*)$', 'misc.views.serve')
    )
