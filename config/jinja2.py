from django.templatetags.static import static
from django.urls import reverse
from django.contrib.messages import get_messages
from django.middleware.csrf import get_token
from django.utils.safestring import mark_safe
from jinja2 import Environment
import json

def environment(**options):
    env = Environment(**options)
    
    # On définit une fonction reverse personnalisée qui accepte les arguments nommés (ex: pk=1)
    def url_reverse(viewname, *args, **kwargs):
        return reverse(viewname, args=args, kwargs=kwargs)

    env.globals.update({
        'static': static,
        'url': url_reverse,
        'get_messages': get_messages,
        'django_csrf_token': get_token,
        'django_csrf_input': lambda request: mark_safe(f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'),
    })
    env.filters['tojson'] = lambda v: json.dumps(v)
    return env
