"""
ASGI config for hackernews project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from hackernews.settings import base

if base.DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackernews.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackernews.settings.production')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackernews.settings.')

application = get_asgi_application()
