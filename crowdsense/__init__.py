from django.conf import settings

from django.core.exceptions import ImproperlyConfigured

try:
    settings.BING_APP_ID
    settings.SOLR_URL
except Exception, e:
    raise ImproperlyConfigured("Misconfigured: %s" % e)

# monkey-patch silence into django-pipes
import django_pipes.main
django_pipes.main._log = lambda msg: None

import pysolr
solr = pysolr.Solr(settings.SOLR_URL)
