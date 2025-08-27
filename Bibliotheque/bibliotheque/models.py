from django.db import models

# Create your models here.
class Auteur(models.Model):
    nom = models.CharField(max_length=150)
    date_naissance = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nom

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    date_sortie = models.DateField(null=True, blank=True)
    auteur = models.ForeignKey(Auteur, related_name='livres', on_delete=models.CASCADE)

    def __str__(self):
        return self.titre