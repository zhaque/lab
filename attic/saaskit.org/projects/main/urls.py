from django.conf import settings
from django.conf.urls.defaults import *

handler404 = 'perfect404.views.page_not_found'

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', dict(template='index.html')),
    (r'^about/$', 'django.views.generic.simple.direct_to_template', dict(template='about.html')),
    (r'^support/$', 'django.views.generic.simple.direct_to_template', dict(template='support.html')),
    (r'^privacy/$', 'django.views.generic.simple.direct_to_template', dict(template='tc.html')),
    (r'^results.html/$', 'django.views.generic.simple.direct_to_template', dict(template='results.html')),
    (r'^downloads/$', 'django.views.generic.simple.direct_to_template', dict(template='downloads.html')),
    (r'^tutorials/$', 'django.views.generic.simple.direct_to_template', dict(template='tutorials.html')),
    (r'^deploying_saaskit/$', 'django.views.generic.simple.direct_to_template', dict(template='deploying_saaskit.html')),
    (r'^enforcing_quotas_in_saaskit/$', 'django.views.generic.simple.direct_to_template', dict(template='enforcing_quotas_in_saaskit.html')),
    (r'^getting_started_with_saaskit/$', 'django.views.generic.simple.direct_to_template', dict(template='getting_started_with_saaskit.html')),
    (r'^integrating_the_polls_app_part_one/$', 'django.views.generic.simple.direct_to_template', dict(template='integrating_the_polls_app_part_one.html')),
    (r'^integrating_the_polls_app_part_two/$', 'django.views.generic.simple.direct_to_template', dict(template='integrating_the_polls_app_part_two.html')),
    url(r'^sso/$', 'sso.views.sso', name="sso"),
    (r'^accounts/', include('django_authopenid.urls')),
    (r'^accounts/create-site/$', 'muaccounts.views.create_account'),
    (r'^profiles/', include('profiles_urls')),
    (r'^tryitout/', include('subscription.urls')),
    (r'^dashboard/', include('notification.urls')),
    (r'^contact/', include('contact_form.urls')),
    (r'^admin/templatesadmin/', include('templatesadmin.urls')),
    (r'^admin/rosetta/', include('rosetta.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    # Currently disabled
    # (r'^pages/', include('pages.urls')),
)

# serve static files in debug mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
