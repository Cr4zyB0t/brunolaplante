from django.shortcuts import render, redirect
from .models import PhotoAccueil, PhotoCategories, PhotoCliches, TypeCategorie, APropos
# Create your views here.
def index(request):
    images = PhotoAccueil.objects.all()
    donnees = {"images" : images}
    return render(request, "home/index.html", donnees)

def cliches(request):
    images = PhotoCliches.objects.all()
    donnees = {"images" : images}
    return render(request, "home/cliches.html", donnees)

def apropos(request):   
    articles = APropos.objects.all()
    donnees = {"articles": articles}
    return render(request, "home/apropos.html", donnees)

def categories(request):
    liste_categories = TypeCategorie.objects.all()
    
    return redirect(f"../categorie/{str(liste_categories[0]).lower()}")

def categorie(request, nom_categorie):
    categories = TypeCategorie.objects.all()
    liste_photo = []
    trouve = False

    for categorie in categories:
        if categorie.nom.lower() == nom_categorie.lower():
            photos = PhotoCategories.objects.filter(categorie=categorie)
            
            liste_photo = photos
            trouve = True

    if not trouve:
        return redirect("/")
    
    donnees = {"categories" : categories, "selected" : categorie, "photos" : liste_photo}
    return render(request, "home/categories.html", donnees)