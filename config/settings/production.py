from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = ['.vercel.app', 'now.sh', 'localhost', '127.0.0.1']

# Sécurité
CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
