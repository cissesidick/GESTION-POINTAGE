from functools import wraps
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
import math

def calculer_distance_metres(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calcule la distance en mètres entre deux points GPS
    """
    R = 6_371_000  # Rayon de la Terre en mètres
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi, d_lambda = math.radians(lat2 - lat1), math.radians(lng2 - lng1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

def verifier_zone(latitude: float, longitude: float) -> dict:
    """
    Vérifie si la position GPS est dans la zone définie
    """
    geo = settings.GEOFENCING
    dist = calculer_distance_metres(latitude, longitude, geo['LATITUDE'], geo['LONGITUDE'])
    autorise = dist <= geo['RAYON_METRES']
    return {
        'autorise': autorise,
        'distance_metres': round(dist, 1),
        'rayon_metres': geo['RAYON_METRES'],
        'message': f"Dans l'entreprise ({round(dist)}m)" if autorise else f"Hors zone ({round(dist)}m)"
    }

def geofencing_requis(view_func):
    """
    Décorateur pour restreindre l'accès si l'utilisateur est hors zone
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Les utilisateurs qui peuvent bypasser le geofencing
        if request.user.is_authenticated and getattr(request.user, 'peut_bypasser_geo', False):
            return view_func(request, *args, **kwargs)

        # Vérifier la position GPS dans la session
        pos = request.session.get('position_gps')
        if not pos:
            messages.error(request, "Vous devez être dans la zone pour pointer. GPS requis.")
            return redirect('pointages:pointer')  # <- page de pointage

        # Vérifier si la position est dans la zone
        res = verifier_zone(pos['lat'], pos['lng'])
        if not res['autorise']:
            messages.error(request, f"Impossible de pointer : {res['message']}")
            return redirect('pointages:pointer')  # <- page de pointage

        # Si tout est ok, l'utilisateur peut accéder à la vue
        return view_func(request, *args, **kwargs)

    return wrapper