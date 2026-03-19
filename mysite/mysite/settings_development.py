from .settings_base import *

DEBUG = env_bool("DJANGO_DEBUG", default=True)

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
