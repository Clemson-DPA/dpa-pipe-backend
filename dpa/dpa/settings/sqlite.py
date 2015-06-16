# inherit the base settings
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_TOOLBAR_PATCH_SETTINGS = False

# db connection for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(SITE_ROOT, 'db.sqlite3'),
    }
}

# build a new tuple with local dev apps added
INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)

