from .base import *
import os
from dotenv import load_dotenv

load_dotenv()  # charge les variables du .env

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# --- Geofencing ---
GEOFENCING = {
    'LATITUDE': float(os.environ.get('ENTREPRISE_LATITUDE', 5.369121)),
    'LONGITUDE': float(os.environ.get('ENTREPRISE_LONGITUDE', -4.0083)),
    'RAYON_METRES': float(os.environ.get('ENTREPRISE_RAYON_METRES', 150)),
    'NOM': os.environ.get('ENTREPRISE_NOM', 'ELITE SAT CANAL PLUS'),
}