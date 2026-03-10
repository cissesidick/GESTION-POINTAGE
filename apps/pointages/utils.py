import csv, io
from datetime import date, timedelta
from django.utils import timezone
from .models import Pointage, SeanceTravail

def get_statut_employe(employe_id: int, jour: date = None) -> str:
    if jour is None: jour = timezone.localdate()
    p = Pointage.objects.filter(employe_id=employe_id, horodatage__date=jour).order_by('-horodatage').first()
    if not p: return 'absent'
    return 'present' if p.type_pointage == 'entree' else 'sorti'

def enregistrer_pointage(employe, type_p: str, geo_data: dict = None) -> Pointage:
    geo = geo_data or {}
    p = Pointage.objects.create(
        employe=employe, type_pointage=type_p,
        latitude_pointage=geo.get('lat'), longitude_pointage=geo.get('lng'),
        distance_bureau=geo.get('distance'), dans_zone=geo.get('dans_zone', True)
    )
    if type_p == 'entree':
        SeanceTravail.objects.create(employe=employe, pointage_entree=p, date=timezone.localdate(), heure_entree=p.horodatage.time())
    else:
        s = SeanceTravail.objects.filter(employe=employe, est_complete=False).order_by('-date', '-heure_entree').first()
        if s:
            s.pointage_sortie, s.heure_sortie = p, p.horodatage.time()
            s.duree_minutes = int((p.horodatage - s.pointage_entree.horodatage).total_seconds() / 60)
            s.est_complete = True
            s.save()
    return p

def calculer_heures_jour(employe_id: int, jour: date) -> float:
    s = SeanceTravail.objects.filter(employe_id=employe_id, date=jour, est_complete=True)
    return round(sum(i.duree_minutes or 0 for i in s) / 60, 2)
