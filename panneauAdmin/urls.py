from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("connexion/", views.connexion),
    path("accueil/", views.accueil),
    path("tables/", views.tables),
    path("utilisateurs/", views.utilisateurs),
    path("table/<str:nom_table>", views.afficher_table),
    path("table/<str:nom_table>/<str:id_enregistrement>", views.afficher_enregistrement),
    path("utilisateurs/", views.utilisateurs),
    path("api/<str:fonction>", views.api),
    path("serveur/", views.serveur),
]