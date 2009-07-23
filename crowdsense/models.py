# imports for side effects
import signal_handlers
from user_profile import UserProfile

# actual content
from django.db import models

from autoslug.fields import AutoSlugField

from muaccounts.models import MUAccount

from pipes import TwitterSearch


class Tracker(models.Model):
    muaccount = models.ForeignKey(MUAccount)
    slug = AutoSlugField(populate_from='name', unique_with='muaccount')
    name = models.CharField(max_length=255)
    query = models.TextField() # may get complicated later on
                               # (optional parameters for different
                               # engines), let's start with a text
                               # field now.

    # temporarily hard-coded; eventually MUA's selected Channels will be used
    channels = (TwitterSearch, )

    @models.permalink
    def get_absolute_url(self):
        return ('tracker_main', (), {'slug': self.slug})

    def __unicode__(self):
        return self.name

    def get_channel_class(self, slug):
        for channel in self.channels:
            if channel.slug == slug:
                return channel
        raise self.__class__.DoesNotExist

    def get_channel(self, slug):
        cls = self.get_channel_class(slug)
        return cls.query(self.query)
