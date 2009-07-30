from django import forms

import channels
from models import Channels, Tracker


class ChannelsForm(forms.Form):
    is_channels_form = forms.CharField(initial='yes', widget=forms.HiddenInput)

    def __init__(self, muaccount, *args, **kwargs):
        super(ChannelsForm, self).__init__(*args, **kwargs)
        self.muaccount = muaccount

        try:
            classes = muaccount.channels.get_channel_classes()
        except Channels.DoesNotExist:
            Channels.objects.create(muaccount=muaccount)
            classes = ()

        for cls in channels.ALL_CHANNELS:
            self.fields[cls.slug] = forms.BooleanField(
                label=cls.name,
                required=False,
                initial=cls in classes,
                )

    def cleaned_slugs(self):
        return [key
                for key in self.cleaned_data
                if self.cleaned_data[key] is True]

    def clean(self):
        if len(self.cleaned_slugs()) \
                > self.muaccount.owner.quotas.crowdsense_channels:
            raise forms.ValidationError("Too many channels selected")
        return self.cleaned_data

    def save(self):
        self.muaccount.channels.set_channel_slugs(self.cleaned_slugs())


class TrackerForm(forms.ModelForm):
    query = forms.CharField()

    class Meta:
        model = Tracker
        exclude = ('muaccount', 'slug')
