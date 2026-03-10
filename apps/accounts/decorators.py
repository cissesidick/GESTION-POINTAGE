from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .geofencing import verifier_zone

def role_et_zone_requis(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')

            # Vérification du rôle
            if not request.user.is_superuser and request.user.role not in roles:
                messages.error(request, "Accès non autorisé.")
                return redirect('pointages:dashboard')

            # Vérification de la zone
            pos = request.session.get('position_gps')
            if not pos:
                messages.error(request, "Vous devez être dans la zone pour pointer. GPS requis.")
                return redirect('pointages:pointer')

            res = verifier_zone(pos['lat'], pos['lng'])
            if not res['autorise']:
                messages.error(request, f"Impossible de pointer : {res['message']}")
                return redirect('pointages:pointer')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator