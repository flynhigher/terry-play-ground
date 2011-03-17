# -*- coding: utf-8 -*-
# Django settings for basic pinax project.

import os.path
#import pinax

#PINAX_ROOT = os.path.abspath(os.path.dirname(pinax.__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# tells Pinax to use the default theme
#PINAX_THEME = 'default'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through django.views.static.serve.
SERVE_MEDIA = DEBUG

ADMINS = (
    ('RateMeAdmin', 'terry_go@yahoo.com'),
)

MANAGERS = ADMINS

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

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hu%jqdxu_w8bs@$j5=@dm2#5))es+dma6gho*t)aq-s$&5g%m@'

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
#    'pinax.middleware.security.HideSensistiveFieldsMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
#    os.path.join(PINAX_ROOT, "templates", PINAX_THEME),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    
#    "pinax.core.context_processors.pinax_settings",
    
    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",
    "account.context_processors.openid",
    "account.context_processors.account",
)

INSTALLED_APPS = (
    # included
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
#    'pinax.templatetags',
    'templatetags',

    # external
    'notification', # must be first
    'django_openid',
    'emailconfirmation',
    'announcements',
    'pagination',
#    'threadedcomments',
#    'threadedcomments_extras',
    'timezones',
    'tagging',
    'ajax_validation',
    'photologue',
    'avatar',
    'uni_form',
#    'staticfiles',
    
    # internal (for now)
    'rateme_profiles',
    'account',
    'signup_codes',
    'pictures',
    'reviews',
    'judges',
    'about',
    'django.contrib.admin',

)

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
}

MARKUP_FILTER_FALLBACK = 'none'
MARKUP_CHOICES = (
    ('restructuredtext', u'reStructuredText'),
    ('textile', u'Textile'),
    ('markdown', u'Markdown'),
    ('creole', u'Creole'),
)
WIKI_MARKUP_CHOICES = MARKUP_CHOICES

AUTH_PROFILE_MODULE = 'rateme_profiles.Profile'
NOTIFICATION_LANGUAGE_MODULE = 'account.Account'

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = False

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG
EMAIL_HOST_USER = 'pricentalk'
EMAIL_HOST_PASSWORD = 'priceandtalk'
DEFAULT_FROM_EMAIL = 'contact@pricentalk.webfactional.com'
SERVER_EMAIL = 'contact@pricentalk.webfactional.com'
CONTACT_EMAIL = "contact@pricentalk.webfactional.com"
SITE_NAME = "Rate Me Popular"
LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URLNAME = "what_next"
REVIEWS_MAX_SCORE = 10
REVIEWS_CAN_CHANGE_VOTE = True

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
