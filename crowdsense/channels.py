from baseclasses import *
import sources


class SocialUpdatesChannel(SortedChannel):
    name = "Social Updates"
    slug = "social-updates"
    source_classes = (sources.TwitterSearch, sources.IdenticaSearch, )


class NewsChannel(Channel):
    name = 'News'
    slug = 'news'
    source_classes = (sources.BingNews, )
