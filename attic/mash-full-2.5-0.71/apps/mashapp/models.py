from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import random

class ServiceResult(models.Model):
    """Represents a result from some search API."""
    
    # An MD5 hash of some id returned by each service (maybe of a URL)
    result_id = models.CharField(max_length=50)
    
    first_vote_time = models.DateTimeField(auto_now_add=True)


class AnonymousVotingUser(User):
    """Represents a User that was created with the sole purpose of tracking anonymous votes.
    
    django-voting doesn't allow anon votes: it associates votes to a user. To get
    around this, when a an anon visitor casts a vote, an AnonymousVotingUser is
    created to represent him. The username is set to a random number, and
    this username is stored in the session. Sessions are persistent by
    default in Django.
    
    """
    @staticmethod
    def get_or_create_anonymous_user(request):
        if 'usertoken' in request.session:
            try:
                return User.objects.get(username=request.session['usertoken'])
            except ObjectDoesNotExist:
                pass  # Create a new user as if there had been no cookie
            
        return AnonymousVotingUser.__create_user(request)

    @staticmethod
    def __create_user(request):
        "Create a new AnonymousVotingUser, save it in the DB, and set the Django session to keep track of it."
        retries = 0
        
        while retries < 100:
            try:
                user = AnonymousVotingUser(username="__randusr%s" % random.randint(0, 1234567890123456), password="nopass")
                user.save()
            except Exception:
                ++retries
                if retries == 100:
                    raise Exception, "Can't create anonymous user."
            
            # username was unique. Break out of this retry loop.
            break;
        
        
        request.session['usertoken'] = user.username
        return user
   
    

class Mashup(models.Model):
    """A mashup is a vertical search site. The Mashup class stores parameters 
    for the search APIs.
    
    Note: If you add/modify fields, be sure to update mashapp.admin
    """
    
    title = models.CharField(max_length=250) 
    
    def __unicode__(self):
        return self.title
    
    
    #
    # Common BOSS paramters
    # http://developer.yahoo.com/search/boss/boss_guide/univer_api_args.html
    #
    BOSS_sites = models.TextField(default='', blank=True,
                             help_text="Sites to restrict the search to, separated with commas")
    BOSS_lang = models.CharField(max_length=2, default='', blank=True,
                            help_text="Search language. See http://developer.yahoo.com/search/boss/boss_guide/supp_regions_lang.html") 
    BOSS_region = models.CharField(max_length=2, default='', blank=True,
                              help_text="Search region. Must be paired with language.") 

    
    #
    # BOSS Web search parameters
    #
    BOSS_web_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    BOSS_web_abstract = models.CharField(max_length=5, default='', blank=True,
                                choices=(('','short'), ('long','long')),
                                help_text="Length of abstract")
    BOSS_web_filter = models.CharField(max_length=30, default='-porn-hate', blank=True,
                              choices=(
                                       ('-porn','-porn'),
                                       ('-hate','-hate'),
                                       ('-porn-hate','-porn-hate'),
                                       ),
                              help_text="Search filter. Available depending on the language.")
    

    #
    # BOSS Images search parameters
    #
    BOSS_images_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    BOSS_images_filter = models.CharField(max_length=3, default='yes', blank=False,
                              choices=(
                                       ('no','no'),
                                       ('yes','yes'),
                                       ),
                              help_text="Filter offensive images.")
    BOSS_images_dimensions = models.CharField(max_length=30, default='', blank=True,
                              choices=(
                                       ('','all'),
                                       ('small','small'),
                                       ('medium','medium'),
                                       ('large','large'),
                                       ('wallpaper','wallpaper'),
                                       ('widewallpaper','wide wallpaper'),
                                       ),
                              help_text="Search only images of this size.")


    #
    # BOSS News search parameters
    #
    BOSS_news_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    BOSS_news_filter = models.CharField(max_length=30, default='-porn-hate', blank=True,
                              choices=(
                                       ('-porn','-porn'),
                                       ('-hate','-hate'),
                                       ('-porn-hate','-porn-hate'),
                                       ),
                              help_text="Search filter. Available depending on the language.")
    BOSS_news_age = models.CharField(max_length=30, default='', blank=True,
                              help_text=
"""Age of news. Can be specified using a string made an integer and one of the letters "s", "m", "h", "d" and "w" representing seconds, minutes, hours, days and weeks. No spaces are allowed in the string. Some examples:
30d = 30 days 1w = One week (7 days) 12h = 12 hours. To specify an age range two values can be concatenated with a dash/hyphen, i.e.: 5d-10d = Between 5 and 10 days old 2w-30d = Between 2 weeks and 30 days old.
The default is 30 days, and valid values are [1-30]d. News Search maintains a 30-day index."""
                              )


    #
    # Google Search common parameters
    # http://code.google.com/apis/ajaxsearch/documentation/reference.html#_intro_fonje
    #
    google_search_HL = models.CharField(max_length=2, default='', blank=True,
                            help_text="This optional argument supplies the host language of the application making the request. If this argument is not present then the system will choose a value based on the value of the Accept-Language http header. If this header is not present, a value of en is assumed. ") 
    
    
    #
    # Google Web Search parameters
    # http://code.google.com/apis/ajaxsearch/documentation/reference.html#_fonje_web
    #
    google_web_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    google_web_safe = models.CharField(max_length=30, default='moderate', blank=False,
                              choices=(
                                       ('active','active - enables the highest level of safe search filtering'),
                                       ('moderate','moderate - enables moderate safe search filtering (default)'),
                                       ('off','off - disables safe search filtering'),
                                       ),
                              help_text="This optional argument supplies the search safety level.")
    google_web_LR = models.CharField(max_length=30, default='', blank=True,
                            help_text="This optional argument allows the caller to restrict the search to documents written in a particular language (e.g., lr=lang_ja). This list  contains the permissible set of values: http://www.google.com/coop/docs/cse/resultsxml.html#languageCollections . Example: lang_en") 

    
    #
    # Google Image Search parameters
    # http://code.google.com/apis/ajaxsearch/documentation/reference.html#_fonje_image
    #
    google_image_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    google_image_safe = models.CharField(max_length=30, default='moderate', blank=False,
                              choices=(
                                       ('active','active - enables the highest level of safe search filtering'),
                                       ('moderate','moderate - enables moderate safe search filtering (default)'),
                                       ('off','off - disables safe search filtering'),
                                       ),
                              help_text="This optional argument supplies the search safety level.")
    google_image_imgsz = models.CharField(max_length=30, default='', blank=True,
                              choices=(
                                       ('icon','icon - restrict to small images'),
                                       ('small', 'small'),
                                       ('medium', 'medium'),
                                       ('large', 'large'),
                                       ('xlarge', 'xlarge'),
                                       ('xxlarge', 'xxlarge - restrict to large images'),
                                       ('huge', 'huge - restrict to extra large images'),
                                       ),
                              help_text="This optional argument tells the image search system to restrict the search to images of the specified size")
    google_image_imgc = models.CharField(max_length=30, default='', blank=True,
                              choices=(
                                       ('color', 'color - restrict to color images'),
                                       ('gray', 'gray - restrict to grayscale images'),
                                       ),
                              help_text="This optional argument tells the image search system to restrict the search to images of the specified colorization.")
    google_image_imgtype = models.CharField(max_length=30, default='', blank=True,
                              choices=(
                                       ('face', 'face - restrict to images of faces'),
                                       ('photo', 'photo - restrict to photos'),
                                       ('clipart', 'clipart - restrict to clipart images'),
                                       ('lineart', 'lineart - restrict to images of line drawings'),
                                       ),
                              help_text="Experimental -- This optional argument tells the image search system to restrict the search to images of the specified type.")
    google_image_as_filetype = models.CharField(max_length=30, default='', blank=True,
                              choices=(
                                       ('jpg', 'jpg'),
                                       ('png', 'png'),
                                       ('gif', 'gif'),
                                       ('bmp', 'bmp'),
                                       ),
                              help_text="This optional argument tells the image search system to restrict the search to images of the specified filetype.")
    google_image_as_sitesearch = models.CharField(max_length=255, default='', blank=True,
                              help_text="This optional argument tells the image search system to restrict the search to images within the specified domain, e.g., as_sitesearch=photobucket.com. Note: This restriction may restrict results to images found on pages at the given URL and/or images with the given URL. ")

    
    #
    # Google Blog Search parameters
    # http://code.google.com/apis/ajaxsearch/documentation/reference.html#_fonje_blog
    #
    google_blog_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    google_blog_scoring = models.CharField(max_length=30, default='d', blank=True,
                              choices=(
                                       ('d','d - by date'),
                                       ),
                              help_text="This optional argument tells the blog search system how to order results. Results may be ordered by relevance (which is the default) or by date. To select ordering by relevance, do not supply this argument. To select ordering by date, set scoring as scoring=d.")
    
   
    #
    # Google news search parameters
    # http://code.google.com/apis/ajaxsearch/documentation/reference.html#_fonje_news
    #
    google_news_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    google_news_scoring = models.CharField(max_length=30, default='d', blank=True,
                              choices=(
                                       ('d','d - by date'),
                                       ),
                              help_text="This optional argument tells the news search system how to order results. Results may be ordered by relevance (which is the default) or by date. To select ordering by relevance, do not supply this argument. To select ordering by date, set scoring as scoring=d.")
    google_news_geo = models.CharField(max_length=255, 
        default='', blank=True,
        help_text=
"""This optional argument tells the news search system to scope search results to a particular location. With this argument present, the query argument (q) becomes optional. Note, this is a very new feature and locally scoped query coverage is somewhat sparse. You must supply either a city, state, country, or zip code as in geo=Santa%20Barbara or geo=British%20Columbia or geo=Peru or geo=93108.  """
        )
    google_news_qsid = models.CharField(max_length=255, 
        default='', blank=True,
        help_text=
"""This optional argument tells the news search system to scope search results to include only quote typed results (rather than classic news article style results). With this argument present, the query argument (q) becomes optional. The value of this argument designates a prominent individual whose quotes have been recognized and classified by the Google News search service. For instance, Barack Obama has a qsid value of tPjE5CDNzMicmM and John McCain has a value of lE61RnznhxvadM. Note, this is a very new feature and we currently do not have a good search or descovery mechanism for these qsid values.. """
        )
    google_news_topic = models.CharField(max_length=255, 
        default='', blank=True,
        help_text=
"""This optional argument tells the news search system to scope search results to a particular topic. The value of the argument specifies the topic in the current or selected edition:

    * h - specifies the top headlines topic
    * w - specifies the world topic
    * b - specifies the business topic
    * n - specifies the nation topic
    * t - specifies the science and technology topic
    * el - specifies the elections topic
    * p - specifies the politics topic
    * e - specifies the entertainment topic
    * s - specifies the sports topic
    * m - specifies the health topic

A topic selection can be used with our without a query. When used without a query, the entire topic is delivered (subject to &rsz), and when used with a query, the query is scoped to the specified topic.

Topics vary slightly from edition to edition. E.g., in African editions like Namibia or Zimbabwe(&ned=en_na, &ned=en_zw) the topic af is available and represents the African topic. In general, if you are viewing an edition of Google News and see a topic of interest, click on the topic header and view the &topic argument in the browser's address bar. """
        )
    google_news_ned = models.CharField(max_length=255, 
        default='', blank=True,
        help_text=
"""This optional argument tells the news search system which edition of news to pull results from. Values include:

    * us - specifies the US edition
    * uk - specifies the UK edition
    * fr_ca - specifies the French Canadian edition
    * etc.

The best way to understand the available set of editions is to look at the edition links at the bottom of Google News. After clicking on an edition, note the value of &ned argument in the browser's address bar. """
        )


    #
    # Google Video Search parameters
    # http://code.google.com/apis/ajaxsearch/documentation/reference.html#_fonje_video
    #
    google_video_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    google_video_scoring = models.CharField(max_length=30, default='d', blank=True,
                              choices=(
                                       ('d','d - by date'),
                                       ),
                              help_text="This optional argument tells the video search system how to order results. Results may be ordered by relevance (which is the default) or by date. To select ordering by relevance, do not supply this argument. To select ordering by date, set scoring as scoring=d.")


    #
    # Picasa Web Albums search parameters
    # http://code.google.com/apis/picasaweb/reference.html#Parameters
    #
    picasa_web_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")

    
    #
    # Twitter search parameters
    # http://apiwiki.twitter.com/Search+API+Documentation#Search
    #
    twitter_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    twitter_lang = models.CharField(max_length=2, default='', blank=True,
                            help_text="Search language in ISO 639-1 code: http://en.wikipedia.org/wiki/ISO_639-1") 
        
    
    #
    # Delicious search parameters
    # http://delicious.com/help/feeds (from http://delicious.com/help/tools)
    #
    delicious_popular_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    delicious_recent_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    delicious_markup = models.CharField(max_length=10, default='fancy', blank=False,
                                        choices = (('fancy', 'Fancy HTML markup'),
                                                   ('plain', 'Plain text'),
                                                   ),
                                        help_text="Whether to include HTML markup in results.") 
        
    
    #
    # Freebase search parameters
    # http://www.freebase.com/view/en/api_service_search    
    #
    freebase_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    
    freebase_type = models.TextField(default='', blank=True,
                                           help_text="Type value may be ids or guids of types in the graph. Separate with commas.")
    freebase_type_strict = models.CharField(max_length=10, default='any',
                                              choices=(('any', 'any -- at least one type value matches'),
                                                       ('all', 'all -- all types match'),
                                                       ('should', "should -- gives preference to matches by boosting their query score but doesn't require any"),
                                                       ),
                                           help_text="Controls how specific the type matches must be.")

    freebase_domain = models.TextField(default='', blank=True,
                                           help_text="Searches may be made more specific by matching against the domain(s) of the type(s) of topics by passing one more of domain values. Separate with commas.")
    freebase_domain_strict = models.CharField(max_length=10, default='any',
                                              choices=(('any', 'any -- at least one domain value matches'),
                                                       ('all', 'all -- all domains match'),
                                                       ('should', "should -- gives preference to matches by boosting their query score but doesn't require any"),
                                                       ),
                                           help_text="Controls how specific the domain matches must be.")
    
    
    #
    # Amazon search parameters
    # http://docs.amazonwebservices.com/AWSEcommerceService/2005-02-23/
    #
    amazon_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    amazon_search_index = models.CharField(max_length=255, default='Books', blank=False,
                                           help_text="The Amazon store you want products from. The list of available SearchIndex values, listed by locale, can be found on the search index values page. See: http://docs.amazonwebservices.com/AWSEcommerceService/2005-02-23/ApiReference/USSearchIndexMatrixArticle.html (for amazon.com); http://docs.amazonwebservices.com/AWSEcommerceService/2005-02-23/ (for other locales)")
    
    
    
    #
    # Technorati search parameters
    # http://technorati.com/developers/api/search.html
    #
    technorati_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    technorati_lang = models.CharField(max_length=2, default='', blank=True,
                                       help_text="Search language in ISO 639-1 code: http://en.wikipedia.org/wiki/ISO_639-1 -- this feature is currently beta and may not work for all languages.") 
    technorati_authority = models.CharField(max_length=2, default='n',
                                            choices=(('n', 'n -- All results'),
                                                     ('a1', 'a1 -- A little authority: Results from blogs with at least one link.'),
                                                     ('a4', 'a4 -- Some authority: Results from blogs with a handful of links.'),
                                                     ('a7', 'a7 -- A lot of authority: Results from blogs with hundreds of links.'),
                                                     ),
                                       help_text="Set this to filter results to those from blogs with at least the Technorati Authority specified. Technorati calculates a blog's authority by how many people link to it. Filtering by authority is a good way to refine your search results.") 
    technorati_claim = models.CharField(max_length=1, default='', blank=True,
                                        choices=(('', ''),
                                                 ('1', '1'),
                                                 ),
                                       help_text="Set this to 1 to have each link result embellished with any user information associated with a link result's parent blog.") 
    
    
    
    #
    # Solr search parameters
    #
    vertical_solr_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup. Vertical Solr is i.e. Cheese, Wine, etc.")
    wiki_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")
    twitter_solr_enabled = models.BooleanField(default=True,
                                           help_text="Include this API in this Mashup")



    