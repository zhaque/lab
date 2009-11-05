# -*- coding: utf-8 -*-
# Django settings for basic pinax project.

import os.path
import pinax

PINAX_ROOT = os.path.abspath(os.path.dirname(pinax.__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# tells Pinax to use the default theme
PINAX_THEME = 'default'

DEBUG = True 
TEMPLATE_DEBUG = True 

# tells Pinax to serve media through django.views.static.serve.
SERVE_MEDIA = True 

ADMINS = (
    # ('CrowdSense Admin', 'admin@crowdsense.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = '/ebs/web/pinax/crowdsense/dev.db'       # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True 

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "site_media")

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/admin".
ADMIN_MEDIA_PREFIX = '/media/admin'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%2ezl^m8li6m34=#5%c(k4aj@n&jc!k=a!2_)r##mf@yolekp3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
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

ROOT_URLCONF = 'crowdsense.urls'

TEMPLATE_DIRS = (
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
    'analytics',
    'basic_profiles',
    'staticfiles',
    'account',
    'misc',
    'waitinglist',
    'signup_codes',

    # content management system     
    'about',

    # CrowdSense application
    'mashapp', 
    'voting', 
    'django_monetize', 

    # admin 
    'django.contrib.admin',

)

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/%s/" % o.username,
}

AUTH_PROFILE_MODULE = 'basic_profiles.Profile'
NOTIFICATION_LANGUAGE_MODULE = 'account.Account'

ACCOUNT_OPEN_SIGNUP = False

URCHIN_ID = "UA-8522322-1"

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG
CONTACT_EMAIL = "feedback@crowdsense.com"
SITE_NAME = "CrowdSense"
LOGIN_URL = "/account/login"
LOGIN_REDIRECT_URLNAME = "what_next"

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass

# Profanity filter params
PROFANITIES_LIST = ('asshat', 'asshead', 'asshole', 'cunt', 'fuck', 'gook', 'nigger', 'shit')
 
# (http://code.djangoproject.com/ticket/8794)
PROFANITIES_RE = r"\b(%s)+\b" % ("|".join(PROFANITIES_LIST), )
 
# Springsteen & APIs params
SPRINGSTEEN_LOG_QUERIES = True
SPRINGSTEEN_LOG_DIR = PROJECT_ROOT#os.path.join(PROJECT_ROOT,'logs')
 
# Timeout for each search service, in miliseconds.
SERVICE_REQUEST_TIMEOUT_MS = 2500

# Seconds that results from APIs are cached.
DEFAULT_CACHE_DURATION = 60 * 30
TWITTER_CACHE_DURATION = 60 * 5
DELICIOUS_POPULAR_CACHE_DURATION = 60 * 30
DELICIOUS_RECENT_CACHE_DURATION = 60 * 30
 
TWITTER_TRENDS_CACHE_DURATION = 60 * 2

# Items listed below are bugs -- which means we should remove the API's we are not using.
PICASA_CACHE_DURATION = 60 * 5
 
SOLR_SERVER = "http://localhost:8983/solr/select"
 
# How deep to dig for in_reply_to_status_id tweets. Each unit of depth implies another query to solr.
MAX_TWITTER_CONVERSATION_DEPTH = 20
 
# http://code.google.com/apis/ajaxsearch/documentation/reference.html
GOOGLE_APPLICATION_KEY = "ABQIAAAARXZUebE4680nIb0zojJzIhRMOHvbw4fuhdsMIKzsLLCnZDdd8xQkGXblxwDvdBp9DFUAVkQAa8wVEw"
 
# http://code.google.com/apis/ajaxsearch/documentation/reference.html#_intro_fonje
GOOGLE_HTTP_REFERER_HEADER = "http://crowdsense.com/"

# django-monetize
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
