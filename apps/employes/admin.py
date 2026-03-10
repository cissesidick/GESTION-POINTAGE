from django.contrib import admin
from .models import Departement, Employe

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'created_at')

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'poste', 'departement', 'statut')
    list_filter = ('departement', 'statut')
    search_fields = ('nom', 'prenom', 'matricule')
