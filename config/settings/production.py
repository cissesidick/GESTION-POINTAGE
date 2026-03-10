from .base import *
import os

DEBUG = False  # ← était True, c'est le bug principal

ALLOWED_HOSTS = ['.vercel.app', 'now.sh', 'localhost', '127.0.0.1']

# Sécurité
CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app']
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Statiques — override explicite ici pour être sûr
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'