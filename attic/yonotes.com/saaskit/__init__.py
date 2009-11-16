# monkey-patch silence into django-pipes
import django_pipes.main
django_pipes.main._log = lambda msg: None
