from django.urls import path
from . import views

app_name = 'pointages'

urlpatterns = [
    path('dashboard/',         views.dashboard,          name='dashboard'),
    path('pointer/',           views.pointer,            name='pointer'),
    path('historique/',        views.historique,         name='historique'),
    path('rapport/',           views.rapport,            name='rapport'),
    path('rapport/export/',    views.export_rapport_csv, name='export_rapport_csv'),
    path('api/verifier-zone/', views.api_verifier_zone,  name='api_verifier_zone'),
]
