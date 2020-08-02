__author__ = "Mohit Thakkar"

"""
WSGI config for smart_ai project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_ai.settings')

application = get_wsgi_application()
