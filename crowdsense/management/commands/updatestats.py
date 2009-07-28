from django.conf import settings
from django.core.management.base import BaseCommand

import pysolr

from crowdsense.models import Tracker

class Command(BaseCommand):
    help = "Update trackers' Solr stats"
    args = ''

    def handle(self, *files, **options):
        self.validate()

        solr = pysolr.Solr(settings.SOLR_URL)

        results = []
        for tracker in Tracker.objects.all():
            for channel in tracker.get_channels():
                if hasattr(channel, 'exception'):
                    # fake channel
                    print 'Account %s#%d tracker %s#%d channel %s: %s' % (
                        tracker.muaccount,
                        tracker.muaccount.id,
                        tracker,
                        tracker.id,
                        channel.name,
                        channel.exception)
                else:
                    try:
                        results.extend(((
                            result.get_indexing_data()
                            for result in channel.get_results(unsorted=True))))
                    except:
                        import traceback
                        print 'Tracker#%d (%s) channel %s failed:' % (
                            tracker.id, tracker.query, channel.name)
                        traceback.print_exc()

        print 'Adding %d results...' % len(results)
        solr.add(results)
