from django.db import models

# Create your models here.
class PhotoAccueil(models.Model):
    nom = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()

    def __str__(self):
        return self.nom

class PhotoCliches(models.Model):
    nom = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()

    def __str__(self):
        return self.nom

class TypeCategorie(models.Model):
    nom = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class PhotoCategories(models.Model):
    nom = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    categorie =  models.ForeignKey(TypeCategorie, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

class APropos(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.titre