# Django settings
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Syed Iqbal', 'contact@youalpha.com'),
    ('Terry Go', 'terry_go@yahoo.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = 'media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mk+!85d%spe439mm_h(@6h39)#gytfygl5y$(&28s_%zjw8yqa'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
		'django.template.loaders.filesystem.load_template_source',
		'django.template.loaders.app_directories.load_template_source',
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
		os.path.join(os.path.dirname(__file__), "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
		"django.core.context_processors.auth",
		"django.core.context_processors.debug",
		"django.core.context_processors.i18n",
		"django.core.context_processors.media",
		"django.core.context_processors.request",
		"tools.context_processors.site_name",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
#    'django.contrib.messages',
		'product',
		'account',
		'tools',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
)

SESSION_COOKIE_AGE = 60 * 20 #20 mins
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

AUTH_PROFILE_MODULE = "account.Profile"
EMAIL_DEBUG = DEBUG
SITE_NAME = "Alpha"
LOGIN_URL = "/account/login"
LOGIN_REDIRECT_URLNAME = "home"
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'pricentalk'
EMAIL_HOST_PASSWORD = 'priceandtalk'
DEFAULT_FROM_EMAIL = 'contact@pricentalk.webfactional.com'
SERVER_EMAIL = 'contact@pricentalk.webfactional.com'
BUY_URL_FORMAT = "http://secure.ultracart.com/cgi-bin/UCEditor?merchantId=AMSLL&ADD="
DATE_FORMAT = "F d, Y P"
TIME_FORMAT = "P"

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
