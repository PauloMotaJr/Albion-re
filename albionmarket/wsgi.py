"""
WSGI config for Albion Market & Craft project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albionmarket.settings.base")

application = get_wsgi_application()