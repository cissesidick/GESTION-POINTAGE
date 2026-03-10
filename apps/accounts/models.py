from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('admin',   'Administrateur'),
        ('rh',      'Ressources Humaines'),
        ('manager', 'Manager'),
        ('employe', 'Employé'),
    ]
    role    = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employe')
    employe = models.OneToOneField(
        'employes.Employe', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='compte'
    )

    class Meta:
        db_table = 'utilisateurs'

    @property
    def peut_bypasser_geo(self):
        return self.is_superuser or self.role in ('admin', 'rh')
