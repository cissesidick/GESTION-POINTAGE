from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',      include('apps.accounts.urls',  namespace='accounts')),
    path('employes/',  include('apps.employes.urls',  namespace='employes')),
    path('pointages/', include('apps.pointages.urls', namespace='pointages')),
    path('', RedirectView.as_view(url='/auth/login/', permanent=False)),
]

# Servir les fichiers statiques en développement
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
