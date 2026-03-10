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
