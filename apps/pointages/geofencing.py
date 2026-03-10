import math
from django.conf import settings
from functools import wraps


def calculer_distance_metres(lat1, lng1, lat2, lng2):
    R = 6371000

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )

    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def verifier_zone(latitude, longitude):
    geo = settings.GEOFENCING

    dist = calculer_distance_metres(
        latitude,
        longitude,
        geo["LATITUDE"],
        geo["LONGITUDE"],
    )

    autorise = dist <= geo["RAYON_METRES"]

    return {
        "autorise": autorise,
        "distance_metres": round(dist, 1),
        "rayon_metres": geo["RAYON_METRES"],
        "message": f"Dans l'entreprise ({round(dist)}m)"
        if autorise
        else f"Hors zone ({round(dist)}m)",
    }


def geofencing_requis(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # valeur par défaut
        request.geo_status = {
            "autorise": False,
            "mode_lecture_seule": True,
            "message": "GPS non détecté",
        }

        pos = request.session.get("position_gps")

        if not pos:
            return view_func(request, *args, **kwargs)

        try:
            res = verifier_zone(pos["lat"], pos["lng"])

            request.geo_status = {
                **res,
                "mode_lecture_seule": not res["autorise"],
            }

        except Exception:
            request.geo_status = {
                "autorise": False,
                "mode_lecture_seule": True,
                "message": "Erreur GPS",
            }

        return view_func(request, *args, **kwargs)

    return wrapper