from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound, \
     HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

from forms import TrackerForm
from models import Tracker


@login_required
def tracker_create(request):
    if request.user <> request.muaccount.owner:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = TrackerForm(request.POST)
        if form.is_valid():
            tracker = form.save(commit=False)
            tracker.muaccount = request.muaccount
            tracker.save()
            return HttpResponseRedirect(tracker.get_absolute_url())
    else:
        form = TrackerForm()
    return direct_to_template(
        request, 'crowdsense/tracker_create.html',
        extra_context = dict(form=form))


@login_required
def tracker_edit(request, slug):
    if request.user <> request.muaccount.owner:
        return HttpResponseForbidden()
    tracker = get_object_or_404(Tracker,
                                muaccount=request.muaccount, slug=slug)
    if request.method == 'POST':
        form = TrackerForm(request.POST, instance=tracker)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(tracker.get_absolute_url())
    else:
        form = TrackerForm(instance=tracker)
    return direct_to_template(
        request, 'crowdsense/tracker_edit.html',
        extra_context = dict(form=form, tracker=tracker))


def tracker_main(request, slug):
    tracker = get_object_or_404(Tracker,
                                muaccount=request.muaccount, slug=slug)
    return HttpResponseRedirect(reverse(
        'tracker_channel', kwargs={'slug': tracker.slug,
                                   'channel_slug': tracker.channels[0].slug}))


def tracker_channel(request, slug, channel_slug):
    tracker = get_object_or_404(Tracker,
                                muaccount=request.muaccount, slug=slug)
    try:
        channel = tracker.get_channel(channel_slug)
    except Tracker.DoesNotExist:
        return HttpResponseNotFound()
    print tracker, channel
    return direct_to_template(
        request, 'crowdsense/tracker_channel.html',
        extra_context=dict(
            tracker=tracker, channel=channel))
