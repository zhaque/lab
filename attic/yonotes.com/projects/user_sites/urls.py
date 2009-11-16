from django.conf import settings
from django.conf.urls.defaults import *

handler404 = 'perfect404.views.page_not_found'

from livesearch.models import SearchApi
from livesearch.forms import AdvancedSearchForm
search_apis = SearchApi.objects.all()
form = AdvancedSearchForm()
context_vars = {'search_apis': search_apis, 'search_prefs_form': form}

urlpatterns = patterns('',
#    url(r'^$', 'django.views.generic.simple.direct_to_template', dict(template='index.html'), name='notification_notices'), 
    url(r'^$', 'saaskit.views.user_sites_index', name='notification_notices'), 
    url(r'^sso/$', 'sso.views.sso', name="sso"),
    (r'^sorry/$', 'django.views.generic.simple.direct_to_template', dict(template='account_nam.html'), 'muaccounts_not_a_member'),
    (r'^accounts/', include('django_authopenid.urls')),
    url(r'^admin/saveapi/$', 'saaskit.views.save_apis', name='saaskit_save_api'),
    url(r'^admin/savesearchprefs/$', 'saaskit.views.save_search_prefs', name='saaskit_save_search_prefs'),
    (r'^admin/', include('muaccounts.urls'), {'extra_context':context_vars}),
    (r'^todo/', include('todo.urls')),
    (r'^thc/', include('threadedcomments.urls')),
    (r'^livesearch/', include('livesearch.urls')),
    (r'^scratchpad/', include('scratchpad.urls')),
)

# serve static files in debug mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
