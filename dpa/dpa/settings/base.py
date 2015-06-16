# -----------------------------------------------------------------------------
# Module: dpa.settings.base
# Author: Josh Tomlinson (jtomlin)
# -----------------------------------------------------------------------------
"""Common settings for all environments."""

# ----------------------------------------------------------------------------
# Imports:
# ----------------------------------------------------------------------------
from os.path import abspath, basename, dirname, join, normpath
import errno
import os
import sys
from django.utils.crypto import get_random_string
from django.core.urlresolvers import reverse_lazy

# ----------------------------------------------------------------------------
# Settings:
# ----------------------------------------------------------------------------

# ---- path configuration

DPA_ROOT = dirname(dirname(abspath(__file__)))
SITE_NAME = basename(DPA_ROOT)
SITE_ROOT = dirname(DPA_ROOT)
SECRET_FILE = normpath(join(SITE_ROOT, 'deploy', 'SECRET'))

# append so that imports work within the apps
sys.path.append(DPA_ROOT)

# ---- debug configuration 

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# ---- app configuration 

INSTALLED_APPS = ( 
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    # ---- 
    '_site',
    'django_mptt_admin',
    'locations',
    'mptt',
    'products',
    'ptasks',
    'rest_framework',
    'rest_framework_swagger',
    'users',
)

# ---- template context processors

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)

# ---- template directories

TEMPLATE_DIRS = (
    normpath(join(DPA_ROOT, 'templates/')),
    normpath(join(SITE_ROOT, 'products/templates/products')),
    normpath(join(SITE_ROOT, 'ptasks/templates/ptasks')),
)

# ---- middleware configuration 

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# ---- url configuration

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_URL = "/auth/logout/"

ROOT_URLCONF = 'dpa.urls'

# ---- static file configuration

STATIC_URL = '/static/'
STATICFILES_DIRS = (
  normpath(join(SITE_ROOT, 'static/')),
)

# ---- general configuration

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'EST'
USE_I18N = True
USE_L10N = True
USE_TZ = True
WSGI_APPLICATION = 'dpa.wsgi.application'

# ---- secret key configuration

# try to load the SECRET_KEY from our SECRET_FILE. If that fails, then generate
# a random SECRET_KEY and save it into our SECRET_FILE for future loading. If
# everything fails, then just raise an exception.
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        try:
            os.makedirs(dirname(SECRET_FILE))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Cannot open file `%s` for writing.' % SECRET_FILE)

