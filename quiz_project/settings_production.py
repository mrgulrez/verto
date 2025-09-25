"""
Production settings for quiz_project - extends base settings.py
"""

import os
import dj_database_url
from pathlib import Path

# Import everything from base settings
from .settings import *

# Override settings for production

# Security
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# Allowed hosts - Vercel domains
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '.vercel.app,.vercel.now.sh').split(',')

# Database
# Use PostgreSQL in production (you can use Vercel's PostgreSQL or any external service)
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = Path(BASE_DIR) / 'staticfiles'
STATICFILES_DIRS = []

# Whitenoise for serving static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS settings for production
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS', 
    'https://your-frontend.vercel.app'
).split(',')

# Additional security settings for production
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.vercel.now.sh',
]
