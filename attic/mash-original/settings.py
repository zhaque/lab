import os

ROOT_PATH = os.path.dirname(__file__)



# Django settings for mashup project.
PINAX_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/pinax/pinax"))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# tells Pinax to use the default theme
PINAX_THEME = 'default'


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# TODO: (Matt) ? tells Pinax to serve media through django.views.static.serve.
SERVE_MEDIA = DEBUG



ADMINS = (
    # ('Mashup Administrator', 'mashup@koonen.com'),
)

MANAGERS = ADMINS

# I can't get psycopg2 to work. I will be swapping development laptops over the weekend anyway,
# so until then, we can just use sqlite
#DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'mashup'                          # Or path to database file if using sqlite3.
DATABASE_USER = 'django'                          # Not used with sqlite3.
DATABASE_PASSWORD = 'mashup'                      # Not used with sqlite3.
DATABASE_HOST = ''                                # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                                # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

DEFAULT_CHARSET = 'utf-8'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT_PATH,'media')

# TODO: (Matt) basic-project comes with this setting, but their dir is not named site_media
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "site_media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'iou$huz6qy&40*(m#wcz-f46&y7#bp0ov%b2u-n*aes&%l!7ey'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_openid.consumer.SessionConsumer',
    'account.middleware.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'mashup.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), "templates"),
    os.path.join(PINAX_ROOT, "templates", PINAX_THEME),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    
    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",
    "account.context_processors.openid",
    "account.context_processors.account",
    "misc.context_processors.contact_email",
    "misc.context_processors.site_name",
)


INSTALLED_APPS = (
    # included
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    
    # external
    'notification', # must be first
    'django_openid',
    'emailconfirmation',
    'mailer',
    'announcements',
    'pagination',
    'timezones',
    'ajax_validation',
    'uni_form',
    
    # internal (for now)
    'basic_profiles',
    'account',
    'misc',
    
    'about',
    'django.contrib.admin',

    'mashapp',
    'voting',
    'django_monetize',
#    'cms',
)

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/%s/" % o.username,
}

AUTH_PROFILE_MODULE = 'basic_profiles.Profile'
NOTIFICATION_LANGUAGE_MODULE = 'account.Account'

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG
CONTACT_EMAIL = "feedback@example.com"
SITE_NAME = "Pinax"
LOGIN_URL = "/account/login"
LOGIN_REDIRECT_URLNAME = "what_next"

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass


#
# Profanity filter params
#

PROFANITIES_LIST = ('asshat', 'asshead', 'asshole', 'cunt', 'fuck', 'gook', 'nigger', 'shit')

# Reg ex used. Note that the "+" in the regex makes combinations of the words also match:
#  niggergook become a profanity too.
# The \b --match beginning and ending of word-- avoid the Scunthorpe Syndrome 
# (http://code.djangoproject.com/ticket/8794)
PROFANITIES_RE = r"\b(%s)+\b" % ("|".join(PROFANITIES_LIST), )



#
# Springsteen & APIs params
#
SPRINGSTEEN_LOG_QUERIES = True
SPRINGSTEEN_LOG_DIR = ROOT_PATH#os.path.join(ROOT_PATH,'logs')

# Timeout for each search service, in miliseconds.
SERVICE_REQUEST_TIMEOUT_MS = 2500

# Seconds that results from APIs are cached.
DEFAULT_CACHE_DURATION = 60 * 30
TWITTER_CACHE_DURATION = 60 * 5
DELICIOUS_POPULAR_CACHE_DURATION = 60 * 30
DELICIOUS_RECENT_CACHE_DURATION = 60 * 30
PICASA_CACHE_DURATION = 60 * 5
TECHNORATI_CACHE_DURATION = 60 * 5

TWITTER_TRENDS_CACHE_DURATION = 60 * 2


BOSS_APP_ID = "BJhB2hvV34HwFZ8fB08QdEneVjU6d2h3XV_4U.EzEruabMcj1qBQSvWwrHU.wi_tS6k-" # replace with your BOSS APP ID


TECHNORATI_LICENSE_KEY = "024133cb6f47caf3984360fbd530737b"


AMAZON_ACCESS_KEY = '0893AYGW9JCZCQ1TVS02'


if os.path.isfile('/home/matt/thisismyserver.txt'):
    SOLR_SERVER = "http://localhost:8983/solr/select"
    
else:
    SOLR_SERVER = "http://ec2-174-129-235-249.compute-1.amazonaws.com:8983/solr/select"

# How deep to dig for in_reply_to_status_id tweets. Each unit of depth implies another query to solr.
MAX_TWITTER_CONVERSATION_DEPTH = 20


# This optional argument supplies the application's key. If specified, it must be a valid key associated with your site which is validated against the passed referer header. The advantage of supplying a key is so that we can identify and contact you should something go wrong with your application. Without a key, we will still take the same appropriate measures on our side, but we will not be able to contact you. It is definitely best for you to pass a key. 
# http://code.google.com/apis/ajaxsearch/documentation/reference.html
GOOGLE_APPLICATION_KEY = ""

# "Applications MUST always include a valid and accurate http referer header in their requests."
# http://code.google.com/apis/ajaxsearch/documentation/reference.html#_intro_fonje
GOOGLE_HTTP_REFERER_HEADER = "http://www.ikhronos.com/"



#
# django-monetize
#
MONETIZE_DEFAULT = (
    'django_monetize/amazon_search.html',
    ('amazon_search_terms','Django book'),
    ('amazon_search_title','Search for Django books!')
)

MONETIZE_TARGET = {
    'adsense': 'django_monetize/adsense_ad_unit.html',
                   
    'django':'django_monetize/paypal_donate.html',
    'Author (Will Larson)':'django_monetize/amazon_honor.html',
    'Author (Joe Somebody)':(
        'django_monetize/amazon_honor.html',
        ('amazon_paypage','Joe Somebodys Amazon Honor Paypage url'),
    ),
    'tutorial':{
        'header':'django_monetize/paypal_donate.html',
        'footer':'django_monetize/amazon_omakase.html',
        None:(
            'django_monetize/amazon_search.html',
            ('amazon_search_terms','JQuery'),
            ('amazon_search_title','Buy books on JQuery!'),
        ),
    },
}

MONETIZE_CONTEXT = {
    'amazon_affiliates_id':'your affiliates tracking id',
    'amazon_paypage':'default amazon paypages url',
    'paypal_business':'paypal accounts email address',
    'paypal_item_name':'My website',
    'paypal_currency_code':'USD',
    'paypal_tax':'0',
    'paypal_lc':'US',
    'paypal_bn':'PP-DonationsBF',
    'paypal_image':'http://www.paypal.com/en_US/i/btn/btn_donate_LG.gif',
}
