# -*- python; coding: utf-8 -*-

from baseclasses import *
import sources

from crowdsense import solr


class SocialUpdatesChannel(SortedChannel):
    name = "Social Updates"
    slug = "social-updates"
    source_classes = (sources.TwitterSearch, sources.IdenticaSearch, )

    def get_statistics(self):
        today = solr.search('result_timestamp:[NOW-1DAY TO NOW]', rows=0, fq=self.facet).hits
        yesterday = solr.search('result_timestamp:[NOW-2DAY TO NOW-1DAY]', rows=0, fq=self.facet).hits

        if yesterday:
            change = '%.02f%%' % (
                100 * float(today - yesterday) / yesterday)
        else:
            change = '—'

        return ((('Today', today), ('Yesterday', yesterday), ('Change', change)),
                )


class NewsChannel(Channel):
    name = 'News'
    slug = 'news'
    source_classes = (sources.BingNews, )

    def get_statistics(self):
        today = solr.search('result_timestamp:[NOW-1DAY TO NOW]', rows=0, fq=self.facet).hits
        yesterday = solr.search('result_timestamp:[NOW-2DAY TO NOW-1DAY]', rows=0, fq=self.facet).hits

        if yesterday:
            change = '%.02f%%' % (
                100 * float(today - yesterday) / yesterday)
        else:
            change = '—'

        return ((('Today', today), ('Yesterday', yesterday), ('Change', change)),
                )
