import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.accounts.models import Utilisateur

username = 'admin_projet'
email = 'admin@admin.com'
password = 'Password123!'

if not Utilisateur.objects.filter(username=username).exists():
    Utilisateur.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Utilisateur '{username}' créé avec succès !")
else:
    u = Utilisateur.objects.get(username=username)
    u.set_password(password)
    u.save()
    print(f"✅ Mot de passe de '{username}' mis à jour !")
