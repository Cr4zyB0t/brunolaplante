from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="accueil.urls"),
    path('cliches/', views.cliches),
    path('categories/', views.categories),
    path("categorie/<str:nom_categorie>", views.categorie),
    path('apropos/', views.apropos),
]