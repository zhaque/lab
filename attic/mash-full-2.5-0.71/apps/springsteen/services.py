"""Services for querying search APIs. 

How to add a service:
* derive a class from Service, here
* add your service's options to mashapp.models.mashup (at least an _enabled option)
* add those options to mashapp.admin for the Django admin
* add your service to the services in mashapp.views.search()
* render your service in springsteen/results.html template

"""



from urllib import urlencode, quote, quote_plus
import urllib2
from threading import Thread
import re
from django.utils import simplejson
from django.utils.html import strip_tags
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import md5
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

from mashapp.models import *
from voting.models import *
from springsteen.utils import cache_get, cache_put
import settings


# Important: Be sure to update the documentation in mashapp.templates.springsteen
# if you modify the results made available.


# Performance: The very first thing to optimize when necessary is the fact
# that now we are creating a thread for each and every HTTP request!
# We should have a thread pool.
class Service(Thread):
    """Abstract base service for querying an API."""
    
    def __init__(self, query, mashup, start=0, count=3):
        """

        start -- 0-based index to the results
        mashup -- a Mashup object that provides the parameters for APIs
        
        """
        super(Service, self).__init__()

        self.exception_occurred = False
        self.total_results = 0
        self._results = []
        self._qty = None  # If set, limits total results to this number

        self._query = self.rewrite_query(query)
        self._start = start
        self._count = count
        self._mashup = mashup  # Mashup -- the current mashup site's parameters

    def rewrite_query(self, query):
        """Return query encoded in UTF-8 and other necessary processing applied.
        
        """
        # When the search string contains a plus (+),
        #  we must re-write it with a space ( ), before urlencoding it,
        #  so that we don't end up with %2B, which Solr doesn't like
        query = query.encode('utf-8').replace('+',' ')
        
        return query

    def run(self):
        return False

    def filter_results(self):
        'Limits maximum results fetched from  a given source.'
        if self._qty:
            self._results = self._results[:self._qty]
            self.total_results = len(self._results)

    def count(self):
        return len(self._results)

    def results(self):
        return self._results

    def exhausted(self):
        'Return whether a service has no additional results for query.'
        start = self._start
        count = self._count
        return start+count >= self.total_results 


class CachableService(Service):
    """Abstract service base. Provides cache functionality."""
    
    _cache_duration = settings.DEFAULT_CACHE_DURATION

    def make_cache_key(self):
        # Following is the Springsteen implementation. It doesn't work with
        # us any more because the params that can vary, depend on the specific
        # service...
#        key = "%s,%s,%s,%s" % (self.__class__, self._query, self.start, self.count)

        # ... So now we have to use the whole URI.
        # Performance: The URI could be cached
        key = self.uri()
        
        return key.replace(" ","")

    def retrieve_cache(self):
        "Need to overload to decode cached data properly."
        pass

    def store_cache(self, raw):
        cache_put(self.make_cache_key(), raw, self._cache_duration)


#  Words and regex can be configured in settings.py.
#  Our code improves on the contrib.comments profanity filter by avoiding the
#  false positives of Scunthorpe (the name of a town that contains the substring "cunt")
#  and the like
#  
# Performant! We pre-compile the regex
COMPILED_PROFANITIES_RE = re.compile(settings.PROFANITIES_RE, re.IGNORECASE)

def is_result_decent(result):
    """Return True if result (a dict) doesn't contain profanity.
    
    """
    try:
        # Performance: Instead of dumping to json, write a recursive function
        # that examines the recursive dicts
        return COMPILED_PROFANITIES_RE.search( \
                                  simplejson.dumps(result) \
                                  ) is None
    except:
        print "Result could not be dumped to json: %s" % (result, )
        return True


class HttpCachableService(CachableService):
    """Abstract base service. Adds HTTP functionality."""
    
    _source = 'web'  # Springsteen cruft
    
    def base_uri(self):
        "Return base URI of the service. To be overridden."
        pass

    def uri(self):
        """Return the URI, including encoded params.
        
        Params that are empty are not included in the URI, because some APIs
        don't like empty params.
        
        """
        params = self.get_params()
        
        # clean_params will have only the params that are not empty
        clean_params = {}
        
        for p in params:
            if params[p]:
                clean_params.update({p: params[p]})
        
        u = self.base_uri() + "?" + urlencode(clean_params, 
            doseq=1 # Must use this because urlencode doesn't handle Unicode otherwise
                                              )
        return u

    def get_params(self):
        """Return a dictionary of params for the service.
        
        To be overridden. Note: Only those params that are not empty will
        be included in the request URL, because some APIs don't like empty params.
        
        """
        return {}

    def decode(self, results):
        pass

    def get_result_id(self, result):
        """Return an ID unique to the service result.
        
        Must be overridden. It's used to track votes.
        
        """
        pass

    def process_result_share(self, result):
        """Set share_url and and share_title on result and return None.
        
        Called by process_result(). Override if needed.
        
        """
        
        result['share_url'] = result['url']
        result['share_title'] = strip_tags(result['title'])

    def process_result(self, result):
        """Generate voting data, AddToAny data, etc..
        
        May be overridden to process each result. Must be called for each result.
        
        """
        #
        # AddToAny data
        #
        self.process_result_share(result)
        
        try:
            # share_url_params is passed to the href of the AddToAny button
            # after the "?" (as params)
            result['share_url_params'] = urlencode(dict(
                                                    linkname=result['share_title'].encode('utf-8'),
                                                    linkurl=result['share_url'].encode('utf-8'),
                                                    ))
        except Exception:
            print "Can't encode %s and %s" % (result['share_title'], result['share_url'])
            
            result['share_url_params'] = ""
        
        #
        # Generate voting data
        #
        raw_id = self.get_result_id(result)
        
        # Generate the MD5 hash of it (it must be a string for md5 to work)
        if type(raw_id) is int:
            raw_id = "%s" % raw_id
        id = md5.new(raw_id).hexdigest()
        
        try:
            # A result by this ID already exists, ...
            serviceresult = ServiceResult.objects.get(result_id=id)
            
            # ... pass the id of it (to avoid another lookup in the view)
            result['serviceresult_id'] = serviceresult.id
            result['serviceresult_score'] = Vote.objects.get_score(serviceresult)
            result['serviceresult_slug'] = 'byserviceresult_id'  # And let the view know that we're passing a ServiceResult.id
            
        except ObjectDoesNotExist:
            # ... If not, pass the id returned by the service
            # We don't create an empty ServiceResult because for
            # ~ 90% of results there will never be a vote, so we don't want to
            # litter our DB with results with no votes.
            result['serviceresult_id'] = id
            result['serviceresult_score'] = dict(score=0, num_votes=0)
            result['serviceresult_slug'] = ''  # And let the view know that it'll have to create a new ServiceResult
#            serviceresult = ServiceResult(result_id=id)
#            serviceresult.save()


        # Springsteen code
        #        
#        if result.has_key('source'):
#            result['_source'] = result['source']
#        result['source'] = self._source
        
        return result


    def retrieve_cache(self):
        cached = cache_get(self.make_cache_key())
        if cached != None:
            self.decode(cached)

    def set_up_request(self, request):
        """Optionally perform additional set up on the urllib2.Request object.
        
        Override this if you need, for example, to add HTTP headers to the request.
        
        """
        pass

    def run(self):
        try:
            if settings.DEBUG:
                print self.__class__.__name__ + ": " + self.uri() + "\n"
                
            self.retrieve_cache()
            if not self._results:
                open_req = urllib2.Request(self.uri())
                self.set_up_request(open_req)
                request = urllib2.urlopen(open_req)
                
                raw = request.read()
                self.store_cache(raw)
                self.decode(raw)
            self.filter_results()
            
        except Exception:
            self.exception_occurred = True
            if settings.DEBUG:
                print "Exception in " + self.__class__.__name__ + ": " + self.uri() + "\n"
            raise

    def results(self):
        # Performance: Mesh this [for] in the loops used to apply process_result
        # TODO: If a result gets filtered out, must request more results to fill our quota? Maybe this depends on design.
        
        return [result for result in self._results if is_result_decent(result)]


# Params: http://developer.yahoo.com/search/boss/boss_guide/univer_api_args.html
class BOSSSearch(HttpCachableService):

    def base_uri(self):
        query = quote(self._query.replace(' ','+'),
              safe=""  # By default slash '/' is not encoded. With "" we make it be encoded.
              )  

        return "http://boss.yahooapis.com/ysearch/%s/v1/%s" \
            % (self._source, query)

    def decode(self, results):
        results = simplejson.loads(results)
        self.total_results = int(results['ysearchresponse']['totalhits'])
        if 'resultset_%s' % self._source in results['ysearchresponse']:
            self._results = [self.process_result(result) 
                             for result in results['ysearchresponse']['resultset_%s' % self._source]]
                             
        else:
            self._results = {}

    def get_params(self):
        return {'start': self._start,
                'count': self._count,
                'format': 'json',
                'appid': settings.BOSS_APP_ID
                }

    def get_result_id(self, result):
        return result['url']

    # Note: Default process_result_share() works for us
    

# Params: http://developer.yahoo.com/search/boss/boss_guide/Web_Search.html#optional_args_web
class Web(BOSSSearch):
    _source = "web"
    
    def get_params(self):
        params = BOSSSearch.get_params(self)
        params.update({
                'sites': self._mashup.BOSS_sites,
                'lang': self._mashup.BOSS_lang,
                'region': self._mashup.BOSS_region,
                'abstract': self._mashup.BOSS_web_abstract,
                'filter': self._mashup.BOSS_web_filter,
                })
        return params


# Params: http://developer.yahoo.com/search/boss/boss_guide/Web_Search.html#optional_args_images
class Images(BOSSSearch):
    _source = "images"
    
    def get_params(self):
        params = BOSSSearch.get_params(self)
        params.update({
                'sites': self._mashup.BOSS_sites,
                'lang': self._mashup.BOSS_lang,
                'region': self._mashup.BOSS_region,
                'filter': self._mashup.BOSS_images_filter,
                'dimensions': self._mashup.BOSS_images_dimensions,
                })
        return params


# Params: http://developer.yahoo.com/search/boss/boss_guide/Web_Search.html#optional_args_news
class News(BOSSSearch):
    _source = "news"
    
    def get_params(self):
        params = BOSSSearch.get_params(self)
        params.update({
                'sites': self._mashup.BOSS_sites,
                'lang': self._mashup.BOSS_lang,
                'region': self._mashup.BOSS_region,
                'filter': self._mashup.BOSS_news_filter,
                'age': self._mashup.BOSS_news_age,
                })
        return params

    

class TwitterSearchService(HttpCachableService):
    """
    Returns Twitter search results in SpringsteenService compatible format.

    """

    _cache_duration = settings.TWITTER_CACHE_DURATION
    _source = 'springsteen'
    
    def base_uri(self):
        return 'http://search.twitter.com/search.json'

    def get_params(self):
        return {'q': self._query,
                'lang': self._mashup.twitter_lang,
                }

    def decode(self, results):
        def transform(result):
            result.update({
                'title': "Twitter: %s" % result['from_user'],
                'image': result['profile_image_url'],
                'url': "http://twitter.com/%s/" % result['from_user'],
                'text': result['text'],
                })
            result = self.process_result(result)
            return result

        data = simplejson.loads(results)
        self._results = [ transform(x) for x in data['results'][:self._count] ]
        self.total_results = len(self._results)

    def get_result_id(self, result):
        return result['id']

# Not used
class TwitterLinkSearchService(TwitterSearchService):
    'Returns only Tweets that contain a link.'

    def filter_results(self):
        self._results = [ x for x in self._results if 'http://' in x['text'] ]
        super(TwitterLinkSearchService, self).filter_results()
        


# http://www.freebase.com/view/en/api_service_search
class MetawebService(HttpCachableService):
    _source = 'metaweb'

    def base_uri(self):
        return  'http://www.freebase.com/api/service/search'

    def get_params(self):
        return {
                'query': self._query,
                'type': self._mashup.freebase_type,
                'type_strict': self._mashup.freebase_type_strict,
                'domain': self._mashup.freebase_domain,
                'domain_strict': self._mashup.freebase_domain_strict,
                'start': self._start,
                'limit': self._count,
#                'mql_output': """[{
#"guid": null,
#"id": null,
#"name": null,
#"type": [],
#"/common/topic/image": [{
#"guid": null,
#"id": null,
#"type": "/common/image",
#"optional": true,
#"limit": 1,
#"index": null,
#"sort": "index"
#}]
#}]"""
                }
        
    def decode(self, results):
        self._results = simplejson.loads(results)['result']
        def convert(result):
            title = result['name']
            topics = result['type']
            id = result['id']
            aliases = result['alias']
            image = result['image']
            
            #
            # Result
            #
            data =  {
                'id': id,
                'title':title,
                'text':'',
                'url': u"http://www.freebase.com/view%s" % id,
                }
            if aliases:
                data['alias'] = aliases
            if topics:
                data['tags'] = [ x['name'] for x in topics ]
            if image:
                # Note: We can adjust the maxwidth/height parameters
                data['thumbnail_url'] = u"http://www.freebase.com/api/trans/image_thumb%s?maxheight=70&maxwidth=70&mode=fillcrop" % image['id']

            data = self.process_result(data)

            return data


        self._results = [ convert(x) for x in self._results ]
        self.total_results = len(self._results)

    def get_result_id(self, result):
        return result['id']


# Params: http://delicious.com/help/feeds (from http://delicious.com/help/tools)
# TODO: Delicious search only works by tags, which fails misserably if you
# query a phrase (the service thread throws an exception)
class DeliciousPopularService(HttpCachableService):
    _source = 'delicious'
    
    _cache_duration = settings.DELICIOUS_POPULAR_CACHE_DURATION


    def rewrite_query(self, query):
        """Perform delicious-specific query rewriting.
        
        Tags never have spaces, so since the service searches tags, we must strip spaces
        
        """
        query = quote(query.encode('utf-8').replace(' ',''), 
                      safe=""  # By default slash '/' is not encoded. With "" we make it be encoded.
                      )  
        
        return query

    def base_uri(self):
        return 'http://feeds.delicious.com/v2/json/popular/%s' % self._query

    def get_params(self):
        return {'count': self._count,
                }
    
    def uri(self):
        markup = (self._mashup.delicious_markup=='fancy' and ['fancy'] or ['plain'])[0]
        return "%s&%s" % (HttpCachableService.uri(self), markup, )

    def decode(self, raw):
        def convert(result):
            return self.process_result({
                'title':result['d'],
                'url':result['u'],
                'text':'',
                'tags':result['t'],
                'datetime':result['dt'],
                })

        results = simplejson.loads(raw)
        self._results = [ convert(x) for x in results ]
        self.total_results = len(self._results)
        
    def get_result_id(self, result):
        return result['url']


class DeliciousRecentService(DeliciousPopularService):
    def base_uri(self):
        return 'http://feeds.delicious.com/v2/json/%s' % self._query

    _cache_duration = settings.DELICIOUS_RECENT_CACHE_DURATION


# http://docs.amazonwebservices.com/AWSEcommerceService/2005-02-23/
class AmazonProductService(HttpCachableService):
    def base_uri(self):
        return 'http://ecs.amazonaws.com/onca/xml'

    def get_params(self):
        return {
                  'Service': 'AWSECommerceService',
                  'AWSAccessKeyId': settings.AMAZON_ACCESS_KEY,
                  'Operation': 'ItemSearch',
                  'SearchIndex': self._mashup.amazon_search_index,
                  'Keywords': self._query,
                  'ItemPage': (self._start / 10) + 1,
                  'ResponseGroup': 'Small,Images',
                 }

    def decode(self, results):
        def tag(name):
            return '{http://webservices.amazon.com/AWSECommerceService/2005-10-05}%s' % name
        
        self._results = []
        elem = ElementTree.XML(results)
        
        for item in elem.find(tag('Items')).findall(tag('Item')):
            #asin = item.find(tag('ASIN')).text
            url = item.find(tag('DetailPageURL')).text
            attrs = item.find(tag('ItemAttributes'))
            authors = (attrs.findall(tag('Author')))
            author = ', '.join([x.text for x in authors])
            title = attrs.find(tag('Title')).text
            
            # Images. Also available: MediumImage, LargeImage.
            # http://docs.amazonwebservices.com/AWSEcommerceService/2005-02-23/ApiReference/ImagesResponseGroup.html
            small_image = item.find(tag('SmallImage'))
            if small_image is not None:
                thumbnail_url = small_image.find(tag('URL')).text
            else:
                thumbnail_url = ""
            
            self._results.append(self.process_result({'title': "%s: %s" % (author, title),
                                  'text':'',
                                  'url':url,
                                  'thumbnail_url': thumbnail_url
                                  }))
        
        self._results = self._results[:self._count]
        self.total_results = len(self._results)

    def get_result_id(self, result):
        return result['url']



# Other params: http://code.google.com/apis/ajaxsearch/documentation/reference.html#_intro_fonje
# IMPORTANT: If you add new Google services, make sure that get_result_id works for that service.
# Not all services return unescapedUrl (see for example GoogleVideo).
class GoogleSearch(HttpCachableService):
    """Base Google search service"""

    def base_uri(self):
        return "http://ajax.googleapis.com/ajax/services/search/%s" % \
            (self._source)

    def set_up_request(self, request):
        """Override this if you need, for example, to add HTTP headers to the request."""

        # "Applications MUST always include a valid and accurate http referer header in their requests."
        # http://code.google.com/apis/ajaxsearch/documentation/reference.html#_intro_fonje
        request.add_header('Referer', settings.GOOGLE_HTTP_REFERER_HEADER)

    def decode(self, results):
        try:
            results = simplejson.loads(results)
        except ValueError:
            print self.__class__.__name__ + ": Could not decode json response: " + results
            self._results = []
            self.total_results = 0
            return

        if results['responseStatus'] != 200:
            print "Google search error: %d -- %s" % \
                (results['responseStatus'], results['responseDetails'])
            return
        
        resp = results['responseData']
        self.total_results = int(resp['cursor'].get('estimatedResultCount', 0))
        #  "moreResultsUrl": "http://www.google.com/search?oe\u003dutf8\u0026ie\u003dutf8..."
        self._results = [self.process_result(result) for result in resp['results'][:self._count]]

# TODO: Paging. 
    def get_params(self):
        params = {
                'v': '1.0',
                'q': self._query,
                'hl': self._mashup.google_search_HL,
                'key': settings.GOOGLE_APPLICATION_KEY,
                }
        return params

    def get_result_id(self, result):
        return result['unescapedUrl']

    def process_result_share(self, result):
        """Set share_url and and share_title on result and return None.
        
        Called by process_result(). Override if needed.
        
        """
        
        result['share_url'] = result['unescapedUrl']
        result['share_title'] = result['titleNoFormatting']


class GoogleWeb(GoogleSearch):
    _source = "web"
    
    def get_params(self):
        params = GoogleSearch.get_params(self)
        params.update(dict(
                           safe=self._mashup.google_web_safe,
                           lr=self._mashup.google_web_LR,
                           ))
        return params


class GoogleImages(GoogleSearch):
    _source = "images"
    
    def get_params(self):
        params = GoogleSearch.get_params(self)
        params.update(dict(
                           safe=self._mashup.google_image_safe,
                           imgsz=self._mashup.google_image_imgsz,
                           imgc=self._mashup.google_image_imgc,
                           imgtype=self._mashup.google_image_imgtype,
                           as_filetype=self._mashup.google_image_as_filetype,
                           as_sitesearch=self._mashup.google_image_as_sitesearch,
                           ))
        return params


class GoogleNews(GoogleSearch):
    _source = "news"
    
    def get_params(self):
        params = GoogleSearch.get_params(self)
        params.update(dict(
                           geo=self._mashup.google_news_geo,
                           qsid=self._mashup.google_news_qsid,
                           topic=self._mashup.google_news_topic,
                           ned=self._mashup.google_news_ned,
                           scoring=self._mashup.google_news_scoring,
                           ))
        return params

class GoogleBlog(GoogleSearch):
    _source = "blogs"
    
    def get_params(self):
        params = GoogleSearch.get_params(self)
        if self._mashup.google_blog_scoring:
            params.update(dict(scoring=self._mashup.google_blog_scoring,))
        return params

    def get_result_id(self, result):
        return result['postUrl']

    def process_result_share(self, result):
        """Set share_url and and share_title on result and return None.
        
        Called by process_result(). Override if needed.
        
        """
        
        result['share_url'] = result['postUrl']
        result['share_title'] = result['titleNoFormatting']

class GoogleVideo(GoogleSearch):
    _source = "video"
    
    def get_params(self):
        params = GoogleSearch.get_params(self)
        if self._mashup.google_blog_scoring:
            params.update(dict(scoring=self._mashup.google_video_scoring,))
        return params

    def decode(self, results):
        def format_duration(seconds):
            """Take the number of seconds and format it as a string.
            
            Sample input / output:
            30   / 00:30
            65   / 01:05
            7503 / 2:05:03
            
            """
            _str = ""
            if seconds >= 3600:
                _str += "%d:" % (seconds / 3600)
                seconds %= 3600
            
            _str += "%02d:%02d" % ((seconds / 60), (seconds % 60),)
            return _str
        
        GoogleSearch.decode(self, results)
        
        if self._results:
            for video in self._results:
                video['duration_string'] = format_duration(int(video['duration']))

    def get_result_id(self, result):
        return result['url']

    def process_result_share(self, result):
        """Set share_url and and share_title on result and return None.
        
        Called by process_result(). Override if needed.
        
        """
        
        result['share_url'] = result['url']
        result['share_title'] = result['titleNoFormatting']

# Other params: http://code.google.com/apis/picasaweb/reference.html#Parameters
class PicasaWebSearchService(HttpCachableService):
    
    _cache_duration = settings.PICASA_CACHE_DURATION

    def base_uri(self):
        return "http://picasaweb.google.com/data/feed/base/all"
    
    def get_params(self):
        return {'q': self._query,
                'alt': 'json',  # http://code.google.com/apis/gdata/json.html#Request
                'start-index': self._start + 1,  # it's a 1-based index
                'max-results': self._count,
                'thumbsize': 144,
               }

    def decode(self, results):
        def process_entry(entry):
            entry['title'] = entry['title']['$t']

            # In get_params we asked for thumbsize=144, so that thumbnail
            # should be the first one -- [0]
            # We could use another thumbsize.
            entry['tbUrl'] = entry['media$group']['media$thumbnail'][0]['url']
            
            entry['unescapedUrl'] = [link['href'] for link in entry['link'] if link['type'] == 'text/html'][0]

            # Must go here, after we set 'unescapedUrl'
            entry = self.process_result(entry)
            
            return entry
            
        try:
            results = simplejson.loads(results)
        except ValueError:
            print self.__class__.__name__ + ": Could not decode json response: " + results
            self._results = []
            self.total_results = 0
            return

        resp = results['feed']
        
        self.total_results = int(resp['openSearch$totalResults']['$t'])
        
        if self.total_results:
            # If zero results, ['entry'] does not exist, that's why we ask "if"
            self._results = [process_entry(entry) for entry in resp['entry'][:self._count]]
        
    def get_result_id(self, result):
        return result['unescapedUrl']
        
    def process_result_share(self, result):
        """Set share_url and and share_title on result and return None.
        
        Called by process_result(). Override if needed.
        
        """
        
        result['share_url'] = result['unescapedUrl']
        result['share_title'] = strip_tags(result['title'])


    


# TODO: Should Solr search be http cacheable?
class SolrService(HttpCachableService):
    """Base solr search service.
    
    Different solr services customize the _field to search a different field.
    
    """
    # param q will be _field + self._query
    _field = ""
    
    def base_uri(self):
        return settings.SOLR_SERVER
    
    def get_params(self):
        return {'q': self._field + self._query,
                'wt': 'json',
                'start': self._start,
                'rows': self._count,
                'version': '2.2',
               }

    def decode(self, results):
        try:
            json = simplejson.loads(results)
        except ValueError:
            print "Could not decode json response: " + results
            self._results = []
            self.total_results = 0
            return
        
        response = json['response']
        self._results = [self.process_result(doc)  for doc in response['docs']]
        self.total_results = response['numFound']

    def get_result_id(self, result):
        return result['id']


class SolrWikiService(SolrService):
    _field = "wiki_search:"

    def process_result(doc):
        URL = 'http://en.wikipedia.org/wiki/' + doc['wiki_title'].replace(' ', '_')
        doc.update({'url': URL})

        doc = super(SolrWikiService, self).process_result(doc)
        
        return doc

    def process_result_share(self, result):
        """Set share_url and and share_title on result and return None.
        
        Called by process_result(). Override if needed.
        
        """
        
        result['share_url'] = result['url']
        result['share_title'] = strip_tags(result['wiki_title'])



class SolrTwitterService(SolrService):
    _field = "text:"
    _cache_duration = 1

    def get_params(self):
        params = super(SolrTwitterService, self).get_params();
        params.update({
                       'q': self._field + self._query, #+ ' _val_:"scale(created_at_dt,0,1)"',
                       'sort': 'created_at_dt desc',
                       })
        return params

    def process_result(self, doc):
        URL = "http://twitter.com/%s/statuses/%s/" % \
            (doc['author_screen_name_s'],
             doc['id'],
            )
        doc.update({'url': URL})

        doc = super(SolrTwitterService, self).process_result(doc)
        return doc

    def process_result_share(self, result):
        """Set share_url and and share_title on result and return None.
        
        Called by process_result(). Override if needed.
        
        """
        
        result['share_url'] = result['url']
        result['share_title'] = strip_tags(result['title_t'])

        


class SolrVerticalService(SolrService):
    _field = "text:"

    def process_result_share(self, result):
        """Set share_url and and share_title on result and return None.
        
        Called by process_result(). Override if needed.
        
        """
        
        # TODO: Vertical search Share
        result['share_url'] = ""
        result['share_title'] = ""

    

# Other params: http://technorati.com/developers/api/search.html
class TechnoratiSearchService(HttpCachableService):

    _cache_duration = settings.TECHNORATI_CACHE_DURATION

    def base_uri(self):
        return "http://api.technorati.com/search"
    
    def get_params(self):
        return {'query': self._query, 'start':self._start,
                'limit': self._count, 'format':"xml", 
                'key': settings.TECHNORATI_LICENSE_KEY,
                'lang': self._mashup.technorati_lang,
                'authority': self._mashup.technorati_authority,
                'claim': self._mashup.technorati_claim,
                }

    def decode(self, results):
        self._results = []
        elem = ElementTree.XML(results)
        doc = elem.find('document')
        for item in doc.findall('item'):
            self._results.append(self.process_result({'title': item.find('title').text,
                                  'url': item.find('permalink').text,
                                  'abstract': item.find('excerpt').text
                                  }))
        self.total_results = int(doc.find('result').find('querycount').text)

    def get_result_id(self, result):
        return result['url']

    
# http://apiwiki.twitter.com/Search+API+Documentation#current
class TwitterTrendsService(HttpCachableService):
    """Query Twitter current Trends service.

    """
    _cache_duration = settings.TWITTER_TRENDS_CACHE_DURATION
    
    def base_uri(self):
        return 'http://search.twitter.com/trends/current.json'

    def get_params(self):
        return {}

    def decode(self, results):
        data = simplejson.loads(results)
        
        # This could be useful, the time the trends were updated
        date = data['trends'].keys()[0]
        
        self._results = [self.process_result(x) for x in data['trends'][date]]
        self.total_results = len(self._results)

    def process_result(self, result):
        result = super(TwitterTrendsService, self).process_result(result)
        result['query_encoded'] = quote_plus(result['query'].encode('utf-8'))
        return result

    def get_result_id(self, result):
        return result['query']

    def process_result_share(self, result):
        # Trends can't be "added to any"
        result['share_title'] = ""
        result['share_url'] = ""
        pass

