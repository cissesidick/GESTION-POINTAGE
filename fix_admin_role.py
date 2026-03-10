import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.accounts.models import Utilisateur

username = 'admin_projet'
password = 'Password123!'

u = Utilisateur.objects.filter(username=username).first()
if u:
    u.role = 'admin'
    u.is_superuser = True
    u.is_staff = True
    u.set_password(password)
    u.save()
    print(f"✅ Utilisateur '{username}' mis à jour avec le rôle ADMIN et accès Superuser !")
else:
    u = Utilisateur.objects.create_superuser(username=username, email='admin@example.com', password=password, role='admin')
    print(f"✅ Utilisateur '{username}' créé avec le rôle ADMIN !")
