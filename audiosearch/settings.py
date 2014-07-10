from __future__ import absolute_import

"""
Django settings for audiosearch project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# this is changed for production and test 
SECRET_KEY = 'vchh__-$5w79n9h$o03gsdgSDgl1o=)m$h(45!!7)l@1ajce7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =  True
TEMPLATE_DEBUG = True

ADMINS = (
    ('Brad', 'bradleydchambers@gmail.com'),
)

ALLOWED_HOSTS = [
    '127.0.0.1',
    '127.0.0.1:8888'
    'http://wwww.audiosearch.net',
]

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    'templates'
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'src',
    'src.templatetags.audiosearch_extras',
    'pyechonest',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'audiosearch.urls'

WSGI_APPLICATION = 'audiosearch.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '/data/db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_FINDERS = ( 
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "static"),
)

STATIC_URL = '/static/'

#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# celery config
BROKER_URL = 'redis://localhost:6379/0'

CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_IMPORTS = ("src.tasks", )

# Audiosearch settings
SEARCH_RESULT_DISPLAYED = 15
MORE_RESULTS = 10
ARTIST_SONGS_DISPLAYED = 15
SIMILAR_ARTIST_DISPLAYED = 5

# set to True to delete cached data before serving page requests
REDIS_DEBUG = False


