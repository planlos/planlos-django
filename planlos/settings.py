# Django settings for kal project.

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('admin', 'termine@planlosbremen.de')
)

MANAGERS = ADMINS

# import passwords
from planlos.secrets import *

import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(PROJECT_DIR, 'planlosdev.db'),
#    }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'planlosdev_db',
        'USER': 'planlos',
        'PASSWORD': DATABASE_PASSWORD,
    }
}




# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'de-de'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/planlos/www/'

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n_yw3@c5kbjxmruo_nhnu!5awihp8*=8z)j_e784p+#x0aq8i5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',    
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'planlos.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/home/planlos/planlos-django/www/templates/",
    "../www/templates/"

)

#TEMPLATE_CONTEXT_PROCESSORS =  (
#    "django.contrib.auth.context_processors.auth",
#"django.core.context_processors.debug",
#"django.core.context_processors.i18n",
#"django.core.context_processors.media",
#"django.contrib.messages.context_processors.messages",
#"planlos.termine.context.ssl_media", 
#    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.syndication',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.markup',
    'planlos.extras',
    'planlos.termine',
    'planlos.blog',
    'planlos.polls',
)

LOGIN_URL = '/planlos/accounts/login/'
