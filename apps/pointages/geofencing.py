import math
from django.conf import settings
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def calculer_distance_metres(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371000  # Rayon de la Terre en mètres
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )

    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def verifier_zone(latitude: float, longitude: float) -> dict:
    geo = settings.GEOFENCING

    distance = calculer_distance_metres(
        latitude,
        longitude,
        geo["LATITUDE"],
        geo["LONGITUDE"]
    )

    autorise = distance <= geo["RAYON_METRES"]

    return {
        "autorise": autorise,
        "distance_metres": round(distance, 1),
        "rayon_metres": geo["RAYON_METRES"],
        "message": f"Dans l'entreprise ({round(distance)}m)"
        if autorise
        else f"Hors zone ({round(distance)}m)",
    }


def geofencing_requis(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # Vérifier si la position GPS est dans la session
        pos = request.session.get("position_gps")

        if not pos:
            request.geo_status = {
                "autorise": False,
                "mode_lecture_seule": True,
                "message": "GPS requis pour pointer."
            }
            return view_func(request, *args, **kwargs)

        # Vérification de la zone
        resultat = verifier_zone(pos["lat"], pos["lng"])

        request.geo_status = {
            **resultat,
            "mode_lecture_seule": not resultat["autorise"]
        }

        return view_func(request, *args, **kwargs)

    return wrapper