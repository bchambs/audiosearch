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

SECRET_KEY = 'vchh__-$5w79n9h$o03gsdgSDgl1o=)m$h(45!!7)l@1ajce7'

DEBUG =  True
TEMPLATE_DEBUG = True

ADMINS = (
    ('Brad', 'bradleydchambers@gmail.com'),
)

ALLOWED_HOSTS = [
    '127.0.0.1',
    '127.0.0.1:8888',
    'http://wwww.audiosearch.net',
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    ''
)

TEMPLATE_DIRS = (
    '/audiosearch/templates',
    '/audiosearch/templates/artist',
    '/audiosearch/templates/content',
    '/audiosearch/templates/general',
    '/audiosearch/templates/song',
    '/audiosearch/templates/static',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'audiosearch',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'audiosearch.middleware.preprocess.Normalizer',
)

ROOT_URLCONF = 'audiosearch.urls'

WSGI_APPLICATION = 'audiosearch.wsgi.application'

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
    os.path.join(PROJECT_ROOT, "/audiosearch/static/"),
)

STATIC_URL = '/audiosearch/static/'

#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


# Echo Nest
ECHO_API_KEY = 'QZQG43T7640VIF4FN'


# Redis 
RESOURCE_CACHE = {
    'audiosearch': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DATABASE': 0,
    }
}


# Celery
BROKER_URL = 'redis://localhost:6379/0'

CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']
CELERY_IMPORTS = ("audiosearch.tasks", )
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_TIMEZONE = 'EST'


# from datetime import timedelta

# CELERYBEAT_SCHEDULE = {
#     'dbsize-tracker': {
#         'task': 'src.tasks.log_dbsize',
#         'schedule': timedelta(hours=1),
#     },
# }


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'general_': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/general.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers':['file'],
        #     'propagate': True,
        #     'level':'DEBUG',
        # },
        'general_logger': {
            'handlers': ['general_'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}


'''MISC'''
APPEND_SLASH = True


