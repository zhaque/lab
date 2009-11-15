# This module is available as common_settings from projects' settings module.
# It contains settings used in all projects.

import os.path
from django.conf import global_settings

KIT_ROOT=os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

DEBUG = True 

ADMINS = (
    # ('SaaSKit Admin', 'admin@saaskit.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME =  'saaskit'  # Or path to database file if using sqlite3.
DATABASE_USER = 'saaskit'             # Not used with sqlite3.
DATABASE_PASSWORD = 'saaskitS3n89mkk'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False 

COMPRESS = True 
COMPRESS_VERSION = True 

_default_css_files = ('yui-app-theme/yuiapp.css',
                      'authopenid/css/openid.css',
                      'uni_form/uni-form-generic.css',
                      'uni_form/uni-form.css',
                      'saaskit/css/shadowbox.css',
                      )

_main_css_files = ('saaskit/css/main.css',)

_user_sites_css_files = ('saaskit/css/user_sites.css',)

COMPRESS_CSS = {                        # different themes for MUAs
    'default': {
        'name': 'default',
        'source_filenames': _default_css_files,
        'output_filename': 'default.style.css'
        },

    'main': {
        'name': 'main',
        'source_filenames': _main_css_files,
        'output_filename': 'main.style.css'
        },

    'user_sites': {
        'name': 'user_sites',
        'source_filenames': _user_sites_css_files,
        'output_filename': 'user_sites.style.css'
        },
    }

MUACCOUNTS_THEMES = (
    # color css
    ('color_scheme', 'Color scheme', (
        ('aqua', 'Aqua', 'yui-app-theme/aqua.css'),
        ('green', 'Green', 'yui-app-theme/green.css'),
        ('purple', 'Purple', 'yui-app-theme/purple.css'),
        ('red', 'Red', 'yui-app-theme/red.css'),
        ('tan-blue', 'Tan Blue', 'yui-app-theme/tan_blue.css'),
        ('saaskit', 'SaaSkit', 'saaskit/css/saaskit.css'),
        ('fireflynight', 'Firefly Night', 'saaskit/css/fireflynight.css'),
        ('grayscale', 'Grayscale', 'saaskit/css/grayscale.css'),
        ('grayscalem', 'Grayscale Modified', 'saaskit/css/grayscalemodified.css'),
        ('overcast', 'Overcast', 'saaskit/css/overcast.css'),
        ('sunshine', 'Sunshine', 'saaskit/css/sunshine.css'),
        )),
    # <body> id
    ('page_width', 'Page widgh', (
        ('doc3', '100% fluid'),
        ('doc', '750px centered'),
        ('doc2', '950px centered'),
        ('doc4', '974px fluid'),
        )),         
    # Outermost <div> class
    ('layout', 'Layout', (
        ('yui-t6', 'Right sidebar, 300px'),
        ('yui-t1', 'Left sidebar, 160px'),
        ('yui-t2', 'Left sidebar, 180px'),
        ('yui-t3', 'Left sidebar, 300px'),
        ('yui-t4', 'Right sidebar, 180px'),
        ('yui-t5', 'Right sidebar, 240px'),
        ('yui-t0', 'Single Column'),
        )),
    # <body> class
    ('rounded_corners', 'Rounded corners', (
        ('on', 'On', 'rounded'),
        ('off', 'Off', ''),
        )),
    )

# Prepare CSS files for configured color schemes
for codename, _, css_file in MUACCOUNTS_THEMES[0][2]:
     COMPRESS_CSS[codename] = {
         'source_filenames' : ( (_default_css_files[0], css_file,) + _default_css_files[1:]), 
         'output_filename' :  'style.%s.css' % codename,
         }

COMPRESS_JS = {
    'all' : {
        'source_filenames' : ('authopenid/js/jquery-1.3.2.min.js',
                              'uni_form/uni-form.jquery.js',
                              ),
        'output_filename' : 'scripts.js'},
    }

NOTICE_TYPES = (
     ("welcome", "Welcome to SaaSkit!", "you have successfully registered"),
     ("member_add", "Added to site", "you were added as a member to a site"),
     ("member_remove", "Removed from site", "you were removed from membership in a site"),
     )

PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL='admin@saaskit.org'
ACCOUNT_ACTIVATION_DAYS=7
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/signin/'
SUBSCRIPTION_PAYPAL_SETTINGS = {
    'business' : PAYPAL_RECEIVER_EMAIL,
    }

QUOTAS = {
    'muaccount_members' : (3, 10, 50),
    }

MUACCOUNTS_ROOT_DOMAIN = 'saaskit.org'
MUACCOUNTS_DEFAULT_URL = 'http://saaskit.org/'
MUACCOUNTS_PORT=80
