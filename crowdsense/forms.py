from django import forms

from models import Tracker


class TrackerForm(forms.ModelForm):
    query = forms.CharField()

    class Meta:
        model = Tracker
        exclude = ('muaccount', 'slug')
