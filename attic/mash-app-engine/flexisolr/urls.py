# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('flexisolr.views',
    (r'^options.js$', 'options'),
    (r'^data.json$', 'data'),
                       
    (r'^render.js$', 'render'),
)

urlpatterns += patterns('',
    ('^yui-demo/$','django.views.generic.simple.direct_to_template',
     {'template': 'flexisolr/yui-demo.html'})
                        )
