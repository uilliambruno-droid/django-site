import os

django_env = os.getenv("DJANGO_ENV", "development").lower()

if django_env == "production":
    from .settings_production import *
else:
    from .settings_development import *
