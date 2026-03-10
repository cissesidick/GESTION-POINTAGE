import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.accounts.models import Utilisateur

u = Utilisateur.objects.filter(username='admin_projet').first()
if u:
    u.role = 'admin'
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print(f"CONFIRMATION: {u.username} a le role: {u.role}")
else:
    print("UTILISATEUR NON TROUVE")
