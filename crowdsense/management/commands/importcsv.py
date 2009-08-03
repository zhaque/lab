import csv
import sys

from django.core.management.base import BaseCommand
from django.db import transaction
from django.template.defaultfilters import slugify

from muaccounts.models import MUAccount
import muaccounts.themes
from crowdsense.channels import ALL_CHANNELS
from crowdsense.models import Channels, Tracker

LEGEND = ['name', 'subdomain', 'theme', 'tracker_name', 'query']

class Command(BaseCommand):
    help = 'Import CrowdSense accounts from CSV file'
    args = 'file [file ...]'

    def handle(self, *files, **options):
        self.validate()
        for fn in files:
            self.import_file(fn)

    @transaction.commit_manually
    def import_file(self, filename):
        print 'Importing', filename
        reader = csv.reader(open(filename))
        legend = reader.next()

        if legend <> LEGEND:
            raise ValueError("Incorrect legend row, should be %s" % LEGEND)

        mua = None
        ln = 1
        def _warn(msg, type='Warning'):
            print >>sys.stderr, '%s:%d: %s: %s' % ( filename, ln, type, msg )
        for name, subdomain, theme, tracker_name, query in reader:
            try:
                ln += 1
                if name:
                    themedict = muaccounts.themes.DEFAULT_THEME_DICT.copy()
                    for themespec in theme.strip().split('|'):
                        if themespec:
                            k, v = themespec.split(':',1)
                            if k in themedict:
                                if v in muaccounts.themes.THEMES_DICT[k][1]:
                                    themedict[k]=v
                                else:
                                    _warn('Unknown theme value %s' % themespec)
                            else:
                                _warn('Unknown theme key %s' % themespec)

                    mua = MUAccount.objects.create(
                        name=name,
                        subdomain=subdomain or slugify(name),
                        is_public=True,
                        theme=themedict,
                        )
                    channels = Channels.objects.create(muaccount=mua)
                    channels.channel_slugs = ' '.join(c.slug for c in ALL_CHANNELS)
                    channels.save()
                elif subdomain or theme:
                    raise ValueError("At least the plan name is required for account creation.")
                if not mua:
                    _warn('skipped tracker')
                    continue
                if not tracker_name:
                    raise ValueError("Tracker name is required.")
                tracker = Tracker.objects.create(
                    muaccount=mua,
                    name=tracker_name,
                    query=query or tracker_name,
                    )
            except Exception, e:
                _warn(unicode(e).strip(), 'Error')
                transaction.rollback()
                mua = None
            else:
                transaction.commit()
    
