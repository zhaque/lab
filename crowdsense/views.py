import urlparse

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound, \
     HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

from muaccounts.models import MUAccount
from muaccounts.views import account_detail

from forms import TrackerForm, ChannelsForm
from models import Tracker


@login_required
def account_detail_override(request, return_to=None):
    # We edit current user's MUAccount
    account = get_object_or_404(MUAccount, owner=request.user)

    # but if we're inside a MUAccount, we only allow editing that muaccount.
    if getattr(request, 'muaccount', account) <> account:
        return HttpResponseForbidden()

    if 'is_channels_form' in request.POST:
        cf = ChannelsForm(account, request.POST)
        if cf.is_valid():
            cf.save()
    else:
        cf = ChannelsForm(account)

    return account_detail(request,
                          extra_context={'channels_form': cf})

@login_required
def tracker_create(request):
    if request.user <> request.muaccount.owner:
        return HttpResponseForbidden()
    if Tracker.objects.filter(muaccount=request.muaccount).count() \
           >= request.user.quotas.crowdsense_trackers:
        return HttpResponseRedirect('/')
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


@login_required
def tracker_delete(request, slug):
    if request.user <> request.muaccount.owner:
        return HttpResponseForbidden()
    tracker = get_object_or_404(Tracker,
                                muaccount=request.muaccount, slug=slug)
    if request.method <> 'POST':
        return HttpResponseForbidden()

    referer = urlparse.urlparse(request.META.get('HTTP_REFERER', '/')).path
    if referer.startswith(tracker.get_absolute_url()):
        referer = '/'

    tracker.delete()
    return HttpResponseRedirect(referer)


def tracker_main(request, slug):
    tracker = get_object_or_404(Tracker,
                                muaccount=request.muaccount, slug=slug)
    return HttpResponseRedirect(reverse(
        'tracker_channel', kwargs={
            'slug': tracker.slug,
            'channel_slug': tracker.get_channel_classes()[0].slug}))


def tracker_channel(request, slug, channel_slug, source_slug=None):
    tracker = get_object_or_404(Tracker,
                                muaccount=request.muaccount, slug=slug)
    try:
        channel = tracker.get_channel(channel_slug, source_slug)
    except Tracker.DoesNotExist:
        return HttpResponseNotFound()
    return direct_to_template(
        request, 'crowdsense/tracker_channel.html',
        extra_context=dict(
            tracker=tracker, channel=channel))
