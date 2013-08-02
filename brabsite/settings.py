# Django settings for brabsite project.
import os.path
import json
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    )

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
try:
    # This will check if app has been deployed on dotCloud
    # by attempting to open json environment settings file
    with open('/home/dotcloud/environment.json') as f:
        env = json.load(f)
    print 'Detected dotCloud deployment...'
    # Assumes dotCloud database service is called "data"
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.mysql',
            'NAME':     'brabout',
            'USER':     env[u'DOTCLOUD_DATA_MYSQL_LOGIN'],
            'PASSWORD': env[u'DOTCLOUD_DATA_MYSQL_PASSWORD'],
            'HOST':     env[u'DOTCLOUD_DATA_MYSQL_HOST'],
            'PORT':     int(env[u'DOTCLOUD_DATA_MYSQL_PORT']),
        }
    }
    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # Example: "/home/media/media.lawrence.com/media/"
    MEDIA_ROOT = '/home/dotcloud/data/media/'

    # Absolute path to the directory where collectstatic.py will collect all static
    # files when being run by dotCloud postinstall script. dotCloud web server
    #  will then serve all static files from that folder. Note: all admin related
    # static files will be placed into admin subfolder of this path. Django 1.4
    # uses this default instead of depriciated variable ADMIN_MEDIA_PREFIX
    # Another note: earlier tutorials suggested using '/home/dotcloud/data/static/'
    # but they changed a bit the way we build Django apps on dotCloud because of their
    #  new Granite Builder. The ~/data/ is indeed persisted across pushes by Granite.
    # However, since the build is done in a separate service in the background
    # (that is while ourr application is running), we can't access ~/data/ because
    # ~/data/ is already attached to our production service. In other word we can't
    # write into ~/data/ during the build, except for the first build.

    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    STATIC_ROOT = '/home/dotcloud/volatile/static/'

except:
    # no json environment file found - app is running locally in development
    #  environment
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'brabout',                      # Or path to database file if using sqlite3.
            'USER': 'root',                      # Not used with sqlite3.
            'PASSWORD': 'Diamonds1',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # Example: "/home/media/media.lawrence.com/media/"
    MEDIA_ROOT = (
        os.path.join(os.path.dirname(__file__), 'media').replace('\\','/')
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )

    # Absolute path to the directory static files should be collected to.
    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/home/media/media.lawrence.com/static/"
    STATIC_ROOT = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True



# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'static').replace('\\','/'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4*u%76x4_v06u(odx7u-2sr!alf1&amp;*dy3@)16#f9elvlc@ij08'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

MIDDLEWARE_CLASSES = (
    'brabsite.middleware.MobileTemplatesMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'brabsite.disable.DisableCSRF',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )


ROOT_URLCONF = 'brabsite.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'brabsite.wsgi.application'

import os.path

DIRNAME = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')

TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates').replace('\\','/'),
    )

MOBILE_TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates', 'mobile').replace('\\','/'),
)
DESKTOP_TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates', 'desktop').replace('\\','/'),
)

MOBILE_USER_AGENTS_FILE =  os.path.join(DIRNAME, 'mobile_agents.txt').replace('\\','/')

MOBILE_IGNORE_LIST =  [#tuple of browsers to ignore
                      'palm',
                      'wap']

                      # 'ipad',



INSTALLED_APPS = (
    'registration',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'imagekit',
    'storages',
    'brabs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        }
}

#registration settings
ACCOUNT_ACTIVATION_DAYS=7
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS = True
EMAIL_HOST_USER='registered.brabout@gmail.com'
EMAIL_HOST_PASSWORD='RegisteredBragAboutIt'

# python -m smtpd -n -c DebuggingServer localhost:1025
# pip install django-registration

# eventually we should be using s3Storage.py from  mstarinc / django-s3storage,
# but for now we are using s3boto original
# pip install django-storages
# pip install boto

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#
AWS_ACCESS_KEY_ID = "AKIAIAMDCZFLG7JZFMHQ"
#
AWS_SECRET_ACCESS_KEY = "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"
#
AWS_STORAGE_BUCKET_NAME = "brabout"
#
AWS_S3_SECURE_URLS = True
#
## stops IK checking S3 all the time
IMAGEKIT_DEFAULT_IMAGE_CACHE_BACKEND = 'imagekit.imagecache.NonValidatingImageCacheBackend'


