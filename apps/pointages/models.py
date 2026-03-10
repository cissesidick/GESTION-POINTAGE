from django.db import models
from django.utils import timezone
from apps.employes.models import Employe

class Pointage(models.Model):
    TYPE_CHOICES = [('entree', 'Entrée'), ('sortie', 'Sortie')]
    MOTIF_CHOICES = [
        ('normal',     'Normal'),
        ('mission',    'Mission'),
        ('heures_sup', 'Heures supplémentaires'),
        ('rattrapage', 'Rattrapage'),
    ]

    employe           = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='pointages')
    type_pointage     = models.CharField(max_length=10, choices=TYPE_CHOICES)
    horodatage        = models.DateTimeField(default=timezone.now)
    motif             = models.CharField(max_length=20, choices=MOTIF_CHOICES, default='normal')
    note              = models.TextField(blank=True, default='')
    latitude_pointage  = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude_pointage = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    distance_bureau    = models.IntegerField(null=True, blank=True)
    dans_zone          = models.BooleanField(default=True)
    created_at         = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pointages'
        ordering = ['-horodatage']

class SeanceTravail(models.Model):
    employe            = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='seances')
    pointage_entree    = models.OneToOneField(Pointage, on_delete=models.CASCADE,  related_name='seance_entree')
    pointage_sortie    = models.OneToOneField(Pointage, on_delete=models.SET_NULL, related_name='seance_sortie', null=True, blank=True)
    date               = models.DateField()
    heure_entree       = models.TimeField()
    heure_sortie       = models.TimeField(null=True, blank=True)
    duree_minutes      = models.IntegerField(null=True, blank=True)
    est_complete       = models.BooleanField(default=False)
    created_at         = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'seances_travail'
        ordering = ['-date', '-heure_entree']

    @property
    def duree_heures(self):
        return round(self.duree_minutes / 60, 2) if self.duree_minutes else None

class CongeAbsence(models.Model):
    TYPE_CHOICES = [
        ('conge_paye',  'Congé payé'),
        ('maladie',     'Maladie'),
        ('sans_solde',  'Sans solde'),
        ('formation',   'Formation'),
        ('autre',       'Autre'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuve',   'Approuvé'),
        ('refuse',     'Refusé'),
    ]

    employe        = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='conges')
    type_absence   = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_debut     = models.DateField()
    date_fin       = models.DateField()
    statut         = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    motif          = models.TextField(blank=True, default='')
    approuve_par   = models.ForeignKey('accounts.Utilisateur', on_delete=models.SET_NULL, null=True, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conges_absences'
