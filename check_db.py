import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables existantes : {tables}")

if 'django_session' not in tables:
    print("❌ django_session manquante. Tentative de migration...")
else:
    print("✅ django_session est présente.")
