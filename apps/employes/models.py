from django.db import models

class Departement(models.Model):
    nom         = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'departements'
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Employe(models.Model):
    STATUT_CHOICES = [
        ('actif',   'Actif'),
        ('inactif', 'Inactif'),
        ('conge',   'En congé'),
    ]

    matricule      = models.CharField(max_length=20, unique=True)
    nom            = models.CharField(max_length=100)
    prenom         = models.CharField(max_length=100)
    email          = models.EmailField(unique=True)
    telephone      = models.CharField(max_length=20, blank=True, default='')
    poste          = models.CharField(max_length=100)
    departement    = models.ForeignKey(
        Departement, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='employes'
    )
    date_embauche  = models.DateField(null=True, blank=True, auto_now_add=True)
    statut         = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    heures_contrat = models.DecimalField(max_digits=4, decimal_places=1, default=8.0)
    photo_url      = models.URLField(blank=True, default='')
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employes'
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matricule})"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
