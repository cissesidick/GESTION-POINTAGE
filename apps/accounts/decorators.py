from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_requis(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if not request.user.is_superuser and request.user.role not in roles:
                messages.error(request, "Accès non autorisé.")
                return redirect('pointages:dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
