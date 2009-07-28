from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.safestring import SafeUnicode

import django_pipes


class Source(django_pipes.Pipe):
    name = None
    slug = None
    uri = None

    class Result(object):

        def __init__(self, source, data):
            self.source = source
            self.data = data

        def indexing_data(self):
            raise NotImplementedError

        def get_indexing_data(self):
            data = self.source.get_indexing_data().copy()
            data.update(self.indexing_data())
            data['id'] = u'/'.join(((
                unicode(data['tracker_id']),
                unicode(data['channel_id']),
                unicode(data['source_id']),
                unicode(data['result_id']),
                )))
            return data

        def render(self):
            return render_to_string(
                'source/%s/single-result.inc.html' % self.source.slug,
                {'object': self})

    @classmethod
    def has_slug(cls, slug):
        return cls.slug == slug

    @classmethod
    def query(cls, query):
        try:
            return cls.objects.get(cls.query_dict(query))
        except Exception, e:
            # return fake source object for this class to display
            # error message

            class _FakeSource(cls):
                name = '%s [not available]' % cls.name
                exception = e

                class Result(Source.Result):

                    def __cmp__(self, other):
                        return -1

                    def render(self):
                        return SafeUnicode(
                            u'<div class="error">%s not available: %s</div>'
                            % (cls.name, self.source.exception))

                def get_raw_results(self):
                    return (None, )
            return _FakeSource()

    @classmethod
    def query_dict(cls, query):
        raise NotImplementedError

    def __unicode__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Source, self).__init__(*args, **kwargs)
        self.indexing_data = {'source_id': self.slug}

    def get_raw_results(self):
        raise NotImplementedError

    def get_results(self):
        return ((self.Result(self, raw_result)
                 for raw_result in self.get_raw_results()))

    def get_indexing_data(self):
        return self.indexing_data

    def set_indexing_data(self, data):
        self.indexing_data.update(data)


class Channel(object):
    source_classes = ()

    def __unicode__(self):
        return self.name

    def __init__(self, slug, tracker):
        self.tracker = tracker
        if slug == self.slug:
            self.sources = tuple(((
                cls.query(tracker.query) for cls in self.source_classes)))
        else:
            S = self.__class__.has_slug(slug)
            if S:
                self.sources = (S.query(tracker.query), )
            else:
                raise ValueError('invalid slug')

        self.indexing_data = {
            'channel_id': self.slug,
            'tracker_id': self.tracker.id,
            }

        for s in self.sources:
            s.set_indexing_data(self.indexing_data)

    @classmethod
    def has_slug(cls, slug):
        if slug == cls.slug:
            return True
        if slug.startswith(cls.slug+'/'):
            subslug = slug[len(cls.slug)+1:]
            for source in cls.source_classes:
                if source.has_slug(subslug):
                    return source

    def get_results(self):
        for source in self.sources:
            for result in source.get_results():
                yield result

    def render_tabs(self):
        rv = []
        if len(self.sources) == 1:
            rv.append(u'<li><a href="%s%s/">Overview</a></li>' % (
                self.tracker.get_absolute_url(), self.slug, ))
            for pc in self.source_classes:
                if pc == self.sources[0].__class__:
                    cls = ' class="active"'
                else:
                    cls = ''
                rv.append(u'<li%s><a href="%s%s/%s/">%s</a></li>' % (
                    cls, self.tracker.get_absolute_url(), self.slug,
                    pc.slug, escape(pc.name), ))
        else:
            rv.append(
                u'<li class="active"><a href="%s%s/">Overview</a></li>' % (
                    self.tracker.get_absolute_url(), self.slug, ))
            for pc in self.source_classes:
                rv.append(u'<li><a href="%s%s/%s/">%s</a></li>' % (
                    self.tracker.get_absolute_url(), self.slug,
                    pc.slug, escape(pc.name), ))
        return SafeUnicode(u''.join(rv))


class SortedChannel(Channel):

    def get_results(self):
        rv = list(super(SortedChannel, self).get_results())
        rv.sort()
        return rv
