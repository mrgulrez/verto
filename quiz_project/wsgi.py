"""
WSGI config for quiz_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use single settings file for both development and production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')

application = get_wsgi_application()

# Expose app for Vercel
app = application
