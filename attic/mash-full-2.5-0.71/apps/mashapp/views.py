
from django.utils import simplejson
from django import forms
import md5
import re

from springsteen.views import *
from springsteen.services import *
from springsteen import utils
from mashapp.models import *
from voting.views import json_error_response
from django.core.exceptions import ObjectDoesNotExist
from voting.models import *

import twitter
import settings


class NewTabForm(forms.Form):
    """Submitted from the "new tab" AJAX tab."""
    twitter = forms.BooleanField(required=False, initial=True, label='Search Twitter')
    news = forms.BooleanField(required=False, initial=True, label='Search news')
    blog = forms.BooleanField(required=False, initial=True, label='Search blogs')
    video = forms.BooleanField(required=False, initial=True, label='Search videos')
    images = forms.BooleanField(required=False, initial=True, label='Search images')


class TwitterForm(forms.Form):
    username_to_follow = forms.CharField(required=True)


class TwitterLoginForm(forms.Form):
    username = forms.CharField(required=True, label='Twitter User Name')
    password = forms.CharField(required=True, label='Twitter Password', widget=forms.PasswordInput())


# NOTE: Basic Auth does not seem to work with unicode strings (Try to spell the word "year" in Spanish as a password)
# _AddAuthorizationHeader in twitter.py has to call encodestring on the user/password
# and this fails as described here: http://bugs.python.org/issue3613
# To-do: We could catch the error and display a nice message.
def twitter_login(request, form):
    """Handle Twitter login.
    
    How to use this function:
        form = <mytwitterformclass>(request.GET)
        return_value, form = twitter_login(request, form)
        if return_value:
            return return_value
            
        # Now whatever with the form: form['<mycleanedfield>']
        # Also use:
        #  request.session['twitter_user']
        #  request.session['twitter_password']


    After the above code (if it did not "return"), you know that form
    has validates and is clean.
    
    """
    # Try decoding the TwitterLoginForm
    # Note that this same view under some conditions renders to
    # twitter_login.html, which produces this form
    login_form = TwitterLoginForm(request.POST)
    
    if login_form.is_valid():
        # Now access as login_form['field']
        login_form = login_form.cleaned_data
        
        # Save login in the session
        request.session['twitter_user'] = login_form['username']
        request.session['twitter_password'] =  login_form['password']
        
        # This had been saved in the session when we rendered twitter_login.html
        return None, request.session['saved_form']


    if not form.is_valid():
        # The Django form received as argument didn't validate
        raise Exception, "Invalid Twitter form data"
    form_clean = form.cleaned_data

    if 'twitter_user' not in request.session:
        #
        # We have to create a dict because the session middleware refuses to
        # save the form
        #
        form_dict = {}
        for f in form.fields.keys():
            form_dict[f] = str(form_clean[f])
        
        request.session['saved_form'] = form_dict

        return render_to_response("twitter_login.html", dict(form=TwitterLoginForm())), None
    
    else:
        return None, form_clean



def twitter_poll(request):
    """Run the twitter search (query in request param 'q') again and return a json string from {'new': new_results}
    
    """
    q = request.GET['q'];
    
    # __search() saves the twitter results for the query in the user's session.
    # We must run the solr query again, and compare the new results.
    # We can't just assume that the query is ordered in reverse chronological order,
    # which would make our code much simpler.
    prev_results = request.session['twitter%s' % q]

    mashup = get_mashup()
    # TODO: I hard-coded count=3
    service = SolrTwitterService(q, mashup, start=0, count=3)
    service.run()
    results = service.results()
    
    #
    # Count new results
    #
    new = 0
    for r in results:
        exists = False
        for p in prev_results:
            if p['id'] == r['id']:
                exists = True
                break;
        
        if not exists:
            new += 1
    
    json = simplejson.dumps({'new': new})
    return HttpResponse(json, mimetype='application/json')
    



def follow_on_twitter(request, user_id_to_follow):
    """
    
    This view actually handles two types of request:
    1) Twitter login
    2) Create friendship on twitter (responds 1) if we don't have twitter login)
    
    """
    form = TwitterForm(request.GET)
    
    return_value, form = twitter_login(request, form)
    if return_value:
        return return_value

    
    username_to_follow = form['username_to_follow']
    
    #
    # Create friendship
    #
    api = twitter.Api()
    api.SetCredentials(request.session['twitter_user'], request.session['twitter_password'])
    
    resp = api.CreateFriendship(user_id_to_follow)
    
    if isinstance(resp, str):
        # CreateFriendship returned an error
        
        if re.search("could not authenticate", resp, re.IGNORECASE):
            # Log out
            del request.session['twitter_user']
            del request.session['twitter_password']
            
            # Render log in
            request.session['saved_form'] = form
    
            context = {
                       'form': TwitterLoginForm(),
                       'error': 'Your user/password is invalid. Please try again.'
                    }
            return render_to_response("twitter_login.html", context)
        
        else:
            context = {'error': resp}
    
    else:
        context = {'name': username_to_follow,
                   'twitter_user': request.session['twitter_user']
                   }
   
     # Some other code that works to, from     
#  http://uswaretech.com/blog/2009/02/how-we-built-a-twitter-application/
#
#import urllib2,base64,simplejson
#    theurl = 'http://twitter.com/friendships/create/%s.json?follow=true'%(user_id_to_follow, )
#    handle = urllib2.Request(theurl)
#
#    authheader =  "Basic %s" % base64.encodestring('%s:%s' % (form['username'], form['password']))
#
#    handle.add_header("Authorization", authheader)
#
##    try:
#    resp = simplejson.load(urllib2.urlopen(handle, ""))
##    except IOError, e:
##        # TODO: This is reached when allocated API requests to IP are completed.
##        print "parsing the is_follows json from twitter, failed"
##        return
    
    return render_to_response("follow_on_twitter_response.html", context)



def twitter_log_out(request):
    del request.session['twitter_user']
    del request.session['twitter_password']
    
    return render_to_response("twitter_log_out_response.html")



#class TwitterReplyForm(forms.Form):
#    screen_name_to_reply = forms.CharField(required=True)
#
#def twitter_reply(request, user_id_to_follow):
#    """
#    
#    This view actually handles two types of request:
#    1) Twitter login
#    2) Twitter reply (responds 1) if we don't have twitter login)
#    
#    """
#    form = TwitterReplyForm(request.GET)
#    
#    return_value, form = twitter_login(request, form)
#    if return_value:
#        return return_value
#
#    
#    
#    return render_to_response("follow_on_twitter_response.html", 
#                              dict(name=username_to_follow))




VOTE_DIRECTIONS = (('up', 1), ('down', -1), ('clear', 0))


def xmlhttprequest_vote_on_object(request, model, direction, serviceresult_id=None, 
    result_id_=None):
    """
    Generic object vote function for use via XMLHttpRequest.
    
    Parameters:
    serviceresult_id -- If this is not None, it's a ServiceResult.id (from mashapp.models)
    result_id_ -- If this is not None, it's the id returned by the specific service (say TwitterSearchService)

    Properties of the resulting JSON object:
        success
            ``true`` if the vote was successfully processed, ``false``
            otherwise.
        score
            The object's updated score and number of votes if the vote
            was successfully processed.
            It includes an additional field: myvote, which is the value of the
            vote just cast. It's important to note that if the user tried to cast an
            up vote (1), and it had already cast that vote, myvote is going to be
            0 (because it cleared the vote, reddit.com style).
        error_message
            Contains an error message if the vote was not successfully
            processed.
    """
    try:
        if request.method == 'GET':
            return json_error_response(
                'XMLHttpRequest votes can only be made using POST.')
        #We do allow anonymous voting
    #    if not request.user.is_authenticated():
    #        return json_error_response('Not authenticated.')
    
        try:
            vote = dict(VOTE_DIRECTIONS)[direction]
        except KeyError:
            return json_error_response(
                '\'%s\' is not a valid vote type.' % direction)
    
        if serviceresult_id is not None:
            # The ServiceResult is already stored
            # Look up the object to be voted on
            lookup_kwargs = {}
            lookup_kwargs['%s__exact' % model._meta.pk.name] = serviceresult_id

            try:
                obj = model._default_manager.get(**lookup_kwargs)
            except ObjectDoesNotExist:
                return json_error_response(
                    'No %s found for %s.' % (model._meta.verbose_name, lookup_kwargs))
        else:
            # The ServiceResult _may_ have been created later, but we'll
            # most likely have to create it.
            try:
                obj = model._default_manager.get(result_id=result_id_)
            except ObjectDoesNotExist:
                # Create it
                obj = ServiceResult(result_id=result_id_)
                obj.save()
            
        #
        # Vote and respond
        #
        
        # Allow anon voting
        user = request.user
        if user.is_anonymous():
            user = AnonymousVotingUser.get_or_create_anonymous_user(request)
        
        # A second vote in the same direction clears the vote, reddit.com style
        prev = Vote.objects.get_for_user(obj, user)
        if prev is not None and prev.vote == vote:
            vote = 0
            
        Vote.objects.record_vote(obj, user, vote)
        return HttpResponse(simplejson.dumps({
            'success': True,
            'score': Vote.objects.get_score(obj),
            'myvote': vote,
        }))
    except Exception, ex:
        import traceback
        import sys

        for msg in traceback.format_tb(sys.exc_info()[2]):
            sys.stderr.write("%s\n" % msg)
        raise


def search(request):
    """Show the front page.
    
    """
    #
    # Query Twitter current Trends
    #
    services = (TwitterTrendsService, )
    results, services = __fetch_results_batch(query="", timeout=settings.SERVICE_REQUEST_TIMEOUT_MS, 
        services=services, start=0, count=0)  # query, start and count are ignored
    results['form'] = NewTabForm()
    
    return render_to_response("search.html", results)


def get_mashup():
    #
    # Pull Mashup object (for now, just grab the first one -- if no Mashup, create one)
    #
    try:
        return Mashup.objects.all()[0]
    except Exception:
        mashup = Mashup(title="(Generated by default)")
        mashup.save()
        return mashup


def results(request):
    """Run search, or, if no query param, shows empty search box
    
    Request params:
    query -- query string or nothing 
    
    """
    
    try:
        mashup = get_mashup()
    
        form = NewTabForm(request.GET) # A form bound to the POST data
        
        # search.html passes _formenabled when using the AJAX (remote) new tab
        # to indicate that it's passing the form to enable/disable services.
        if form.is_valid() and request.GET.get('_formenabled', 'false') == 'true': # All validation rules pass
            # Now access as form['field']
            form = form.cleaned_data
            
            mashup.google_video_enabled = mashup.google_video_enabled and form['video']
            mashup.google_news_enabled = mashup.google_news_enabled and form['news']
            mashup.BOSS_news_enabled = mashup.BOSS_news_enabled and form['news']
            mashup.google_blog_enabled = mashup.google_blog_enabled and form['blog']
            mashup.technorati_enabled = mashup.technorati_enabled and form['blog']
            mashup.twitter_enabled = mashup.twitter_enabled and form['twitter']
            mashup.twitter_solr_enabled = mashup.twitter_solr_enabled and form['twitter']
            mashup.google_image_enabled = mashup.google_image_enabled and form['images']
            mashup.picasa_web_enabled = mashup.picasa_web_enabled and form['images']
            mashup.BOSS_images_enabled = mashup.BOSS_images_enabled and form['images']
    
        # Add services to query from springsteen.services or mashapp.services modules.
        services = ()
        # Pass mashup so that the template can query API options
        extra_context = {'mashup': mashup}
        
        if mashup.BOSS_web_enabled: services += (Web,)
        if mashup.BOSS_images_enabled: services += (Images,)
        if mashup.BOSS_news_enabled: services += (News,)
        if mashup.google_web_enabled: services += (GoogleWeb,)
        if mashup.google_image_enabled: services += (GoogleImages,)
        if mashup.google_news_enabled: services += (GoogleNews,)
        if mashup.google_blog_enabled: services += (GoogleBlog,)
        if mashup.google_video_enabled: services += (GoogleVideo,)
        if mashup.picasa_web_enabled: services += (PicasaWebSearchService,)
        if mashup.twitter_enabled: services += (TwitterSearchService,)
        if mashup.delicious_popular_enabled: services += (DeliciousPopularService,)
        if mashup.delicious_recent_enabled: services += (DeliciousRecentService,)
        if mashup.freebase_enabled: services += (MetawebService,)
        if mashup.amazon_enabled: services += (AmazonProductService,)
        if mashup.technorati_enabled: services += (TechnoratiSearchService,)
        if mashup.vertical_solr_enabled: services += (SolrVerticalService,)
        if mashup.wiki_enabled: services += (SolrWikiService,)
        if mashup.twitter_solr_enabled: services += (SolrTwitterService,)
        
        # Run the search and render the results
        # Note that each Service gets mashup as a parameter. This way,
        # each service can pull its own parameters.
        return __search(request, mashup, settings.SERVICE_REQUEST_TIMEOUT_MS, \
                       3, services, extra_context=extra_context)
    except Exception, ex:
        import traceback
        import sys

        for msg in traceback.format_tb(sys.exc_info()[2]):
            sys.stderr.write("%s\n" % msg)
        raise



# Modified from springsteen.views.fetch_results_batch()
def __fetch_results_batch(query, timeout, services, mashup=None, start=None, count=None):
    """Perform a batch of requests and return results.
    
    Returns results, unexhausted_services:
    results -- A dictionary of service results. For each service, a (key, value) entry:
      key is the service's class name.
      value is a dictionary of the service's results.
    unexhausted_services -- List of services that have more results to return.
    
    """
    threads = [ x(query, mashup, start, count) for x in services ]
    for thread in threads:
        thread.start()
    multi_join(threads, timeout=timeout)

    results = {}
    unexhausted_services = []
    if settings.DEBUG:
        results['exception_occurred'] = False
    
    for thread in threads:
        if thread.exception_occurred and settings.DEBUG:
            results['exception_occurred'] = True
            
        if not thread.exhausted():
            unexhausted_services.append(thread.__class__)
#        total_results = total_results + thread.total_results

    
        # Create results dict
        
        total_results = thread.total_results
        
        range = ( start+1, min(start+count,total_results) )
        next_start = start + count
        previous_start = start - count
        has_next = range[1] < total_results
        has_previous = range[0] > 1
        results[thread.__class__.__name__] = \
            {
                'count': count,
                'start': start,
                'range': range,
                'has_next': has_next,
                'has_previous': has_previous,
                'next_start': next_start,
                'previous_start': previous_start,
                'results': thread.results(),
                'total_results': total_results,
            }

    return results, unexhausted_services


# Copied from springsteen.views.search
def __search(request, mashup, timeout=2500, max_count=10, services=(), \
               extra_params={}, extra_context={}):
    """Run a search and render the results.

    Parameters:
    timeout -- a global timeout for all requested services
    mashup -- 
    max_count -- used to prevent resource draining URL hacking
    services -- services to query with search terms
    extra_params -- overrides and extra parameters for searches
    extra_context -- extra stuff passed to the template for rendering
    
    """
    query = request.GET.get('query',None)
    results = []
    total_results = 0
    try:
        count = int(request.GET.get('count','%s' % max_count))
    except ValueError:
        count = 10
    count = min(count, max_count)

    try:
        start = int(request.GET.get('start','0'))
    except ValueError:
        start = 0
    start = max(start, 0)

    results = {}

    if query:
        # log the query
        springsteen.utils.log_query(query)

        results, unexhausted_services = __fetch_results_batch(query, timeout, services, mashup, start, count)

    #
    # Save Twitter results for AJAX poller
    #
    if('SolrTwitterService' in results):
        request.session['twitter%s' % query] = results['SolrTwitterService']['results']
    

    # Render the template with the query and the results.
    context = {
               'query': query, 
              }
    context.update(results)
    context.update(extra_context)
    
    if settings.DEBUG and 'debuggin' in request.GET:
        return render_to_response("springsteen/debuggin.html",context)
    
    else:
        return render_to_response("springsteen/results.html",context)


