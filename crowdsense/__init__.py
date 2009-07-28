from django.conf import settings

from django.core.exceptions import ImproperlyConfigured

try:
    settings.BING_APP_ID
except:
    raise ImproperlyConfigured("BING_APP_ID setting not found.")

# monkey-patch silence into django-pipes
import django_pipes.main
django_pipes.main._log = lambda msg: None
