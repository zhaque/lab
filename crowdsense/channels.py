from django.utils.html import escape
from django.utils.safestring import SafeUnicode

from pipes import *


class CSChannelBase(object):

    def __unicode__(self):
        return self.name

    def __init__(self, slug, tracker):
        self.tracker = tracker
        P = self.__class__.has_slug(slug)
        if P is True:
            self.pipes = tuple(((
                Pipe.query(tracker.query) for Pipe in self.pipe_classes)))
        elif P:
            self.pipes = (P.query(tracker.query), )
        else:
            raise ValueError('invalid slug')

    @classmethod
    def has_slug(cls, slug):
        if slug == cls.slug:
            return True
        if slug.startswith(cls.slug+'/'):
            subslug = slug[len(cls.slug)+1:]
            for pipe in cls.pipe_classes:
                if pipe.has_slug(subslug):
                    return pipe

    def get_results(self):
        for p in self.pipes:
            for r in p.get_results():
                yield r

    def render_tabs(self):
        rv = []
        if len(self.pipes) == 1:
            rv.append(u'<li><a href="%s%s/">Overview</a></li>' % (
                self.tracker.get_absolute_url(), self.slug, ))
            for pc in self.pipe_classes:
                if pc == self.pipes[0].__class__:
                    cls = ' class="active"'
                else:
                    cls = ''
                rv.append(u'<li%s><a href="%s%s/%s/">%s</a></li>' % (
                    cls, self.tracker.get_absolute_url(), self.slug,
                    pc.slug, escape(pc.name), ))
        else:
            rv.append(u'<li class="active"><a href="%s%s/">Overview</a></li>' % (
                self.tracker.get_absolute_url(), self.slug, ))
            for pc in self.pipe_classes:
                rv.append(u'<li><a href="%s%s/%s/">%s</a></li>' % (
                    self.tracker.get_absolute_url(), self.slug,
                    pc.slug, escape(pc.name), ))
        return SafeUnicode(u''.join(rv))
    

class SocialUpdatesChannel(CSChannelBase):
    name = "Social Updates"
    slug = "social-updates"

    pipe_classes = (TwitterSearch, IdenticaSearch, )

    def get_results(self):
        s = super(SocialUpdatesChannel, self).get_results()
        print s
        
        if len(self.pipes) == 1:
            return s

        # more than one channel -> re-sort by timestamp
        rv = list(s)
        rv.sort(key=lambda e: e.timestamp, reverse=True)
        return rv



class NewsChannel(CSChannelBase):
    name = 'News'
    slug = 'news'

    pipe_classes = (BingNews, )
