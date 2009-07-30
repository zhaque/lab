# imports for side effects
import signal_handlers
from user_profile import UserProfile

# actual content
from django.db import models

from autoslug.fields import AutoSlugField

from muaccounts.models import MUAccount

import channels


class Channels(models.Model):
    """MUAccount's channel set"""

    muaccount = models.OneToOneField(MUAccount, primary_key=True)
    channel_slugs = models.TextField(default='')     # space-separated slugs

    def _reset(self):
        self._slugs_set = None
        self._channels = None

    def __init__(self, *args, **kwargs):
        super(Channels, self).__init__(*args, **kwargs)
        self._reset()

    def save(self, *args, **kwargs):
        super(Channels, self).save(*args, **kwargs)
        self._reset()

    def get_slug_set(self):
        if self._slugs_set is None:
            self._slugs_set = set(self.channel_slugs.split())
        return self._slugs_set

    def get_channel_classes(self):
        if self._channels is None:
            cc, slugs = [], self.get_slug_set()
            for channel in channels.ALL_CHANNELS:
                if channel.slug in slugs:
                    cc.append(channel)
            self._channels = cc
        return self._channels

    def set_channel_slugs(self, slugs):
        if isinstance(slugs, basestring):
            slugs = slugs.split()
        if self.muaccount.owner.quotas.crowdsense_channels < len(slugs):
            raise ValueError('You cannot choose more than %s accounts'
                             % self.muaccount.owner.quotas.crowdsense_channels)
        valid_slugs = set(channel.slug for channel in channels.ALL_CHANNELS)
        for slug in slugs:
            if slug not in valid_slugs:
                raise ValueError("%s is not a valid channel slug." % slug)
        # if len(slugs) > self.muaccount.
        self.channel_slugs = ' '.join(slugs)
        self.save()


class Tracker(models.Model):
    muaccount = models.ForeignKey(MUAccount)
    slug = AutoSlugField(populate_from='name', unique_with='muaccount')
    name = models.CharField(max_length=255)
    query = models.TextField() # may get complicated later on
                               # (optional parameters for different
                               # engines), let's start with a text
                               # field now.

    def get_channel_classes(self):
        if not hasattr(self, '_channels'):
            try:
                self._channels = self.muaccount.channels.get_channel_classes()
            except Channels.DoesNotExist:
                Channels.objects.create(muaccount=self.muaccount).save()
                self._channels = ()
        return self._channels

    @models.permalink
    def get_absolute_url(self):
        return ('tracker_main', (), {'slug': self.slug})

    def __unicode__(self):
        return self.name

    def get_channel_class(self, slug):
        for channel in self.get_channel_classes():
            if channel.slug == slug:
                return channel
        raise self.__class__.DoesNotExist

    def get_channel(self, slug, subslug=None):
        cls = self.get_channel_class(slug)
        try:
            return cls(self, subslug)
        except ValueError:
            raise self.__class__.DoesNotExist

    def get_channels(self):
        return ((cls(self) for cls in self.get_channel_classes()))
