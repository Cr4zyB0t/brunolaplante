from django.shortcuts import render, redirect, HttpResponse
from . import forms
import psutil
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
import sys, inspect
from django.forms import ModelForm
sys.path.append("../")
import home, todo
from home.models import *
import ddos_protection
from ddos_protection.models import *
from django.conf import settings
from django.db.models import Count
import itertools
import json
import time
import threading
import os
from subprocess import Popen, PIPE, STDOUT

PAGE_ADMIN = settings.ADMIN_PAGE
PAGE_CAFE = False
CLASSES = inspect.getmembers(home.models, inspect.isclass)
CLASSES.append(inspect.getmembers(ddos_protection.models, inspect.isclass)[0])
FORMULAIRES = []

CONSOLE_SERVEUR = ""


CLASSE_BASE = """class {NOM}Form(ModelForm):
    class Meta:
        model = {NOM}
        fields = '__all__'
FORMULAIRES.append({NOM}Form)"""

for classe in CLASSES:
    chaine = CLASSE_BASE.replace("{NOM}", classe[0])
    exec(chaine)

THREAD_RUNNING = False

# Create your views here.
def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("accueil/")
    else:
        return redirect("connexion/")


    #return render(request, "panneauAdmin/connexion.html", formulaire)
    #return redirect("connexion/")

def connexion(request):
    formulaire = {"page_admin": PAGE_ADMIN, "form" : forms.ConnexionForm()}

    utilisateur = request.user
    if utilisateur.is_authenticated:
        form = None
        return redirect("/")
    else:
        form = forms.ConnexionForm(request.POST or None)
    
    if not utilisateur.is_authenticated and form.is_valid():
        pseudo = form.cleaned_data.get("pseudo")
        mot_de_passe = form.cleaned_data.get("mot_de_passe")
        user = authenticate(request, username=pseudo, password=mot_de_passe)
        print(pseudo, mot_de_passe)
        print(user)
        if user != None:
            login(request, user)
            return redirect("../accueil/")
        else:

            #attempt = request.session["attempt"] or 0
            #request.session["attempt"] = attempt + 1
            #return redirect("/invalid-password")
            request.session["invalid_user"] = 1
            #return render(request, "accounts/invalid-login.html", {"form" : form})

    return render(request, "panneauAdmin/connexion.html", formulaire)

# TODO : optimiser si possible 
def accueil(request):
    user = request.user
    if user.is_superuser:
        disque = psutil.disk_usage('/')
        total = round(disque.total / (2**30), 2)
        utilise = round(disque.used / (2**30), 2)
        restant = round(disque.free / (2**30), 2)

        ram = psutil.virtual_memory()
        ram_total = round(ram.total / (2**30), 2)
        ram_utilise = round(ram.used / (2**30), 2)
        ram_restant = round(ram.free / (2**30) + ram.cached / (2**30), 2)
        
        cpu_utilise = psutil.cpu_percent(0.1)
        tableau = []

        for c in CLASSES:
            if c[0].lower() == "iplog":
                classe = c[1]

                qs = classe.objects.values('date').values('date')
                grouped = itertools.groupby(qs, lambda d: d.get('date').strftime('%d'))

                tableau = [[day, len(list(this_day))] for day, this_day in grouped]
                tableau.reverse()
                tableau = tableau[:7]
                tableau.reverse()
                tableau.insert(0, ["Date", ""])


        donnees = {"page_admin": PAGE_ADMIN,
        "selected" : "dashboard", 
        "espace_utilise" : utilise,
        "espace_total" : total,
        "espace_restant" : restant,
        "ram_total": ram_total,
        "ram_utilise" : ram_utilise,
        "ram_restant" : ram_restant,
        "cpu_utilise" : cpu_utilise,
        "tableau_requetes" : tableau} 
        return render(request, "panneauAdmin/accueil.html", donnees)

    else:
        return redirect("/")

# TODO : optimiser
def tables(request):
    user = request.user
    exclude_list = ["__", 
    "DoesNotExist", 
    "MultipleObjectsReturned", 
    "get_next_by_", 
    "get_previous_by_", 
    "objects", 
    "_meta", 
    "id"]

    if user.is_superuser:
        tables = []
        items = admin.site._registry
        for item in items:
            if item.__name__ != "Group" and item.__name__ != "User":
                temp = {"titre" : item.__name__}
                cles = ["id"]
                dictionnaire = item.__dict__.keys()
                
                for element in dictionnaire:
                    trouve = False
                    for chaine in exclude_list:
                        if chaine in element:
                            trouve = True
                            break
                    if not trouve:
                        cles.append(element)
                temp["colonnes"] = cles
                lignes = []
                objets = item.objects.all().order_by('-id')[:5] # TODO : aller chercher les X derniers éléments
                objets = reversed(objets)

                for objet in objets:
                    temp2 = []
                    for colonne in cles:
                        texte = str(objet.__dict__.get(colonne))
                        if len(texte) > 15:
                            texte = f"{texte[0:12]}..."
                        temp2.append(texte)
                    lignes.append(temp2)
                
                temp["lignes"] = lignes

                #print(item.__name__, item.objects.all())
                tables.append(temp)
        donnees = {"page_admin": PAGE_ADMIN,
        "selected" : "tables", 
        "tables" : tables}
        
        return render(request, "panneauAdmin/tables.html", donnees)
    else:
        return redirect("/")

# TODO : optimiser
def utilisateurs(request):
    user = request.user
    exclude_list = ["__", 
    "DoesNotExist", 
    "MultipleObjectsReturned", 
    "get_next_by_", 
    "get_previous_by_", 
    "objects", 
    "_meta", 
    "_state",
    "password",
    "id"]

    if user.is_superuser:
        tables = []
        item = get_user_model()
        print(item.__dict__.keys())
        if item.__name__ == "User":
            temp = {"titre" : "Utilisateurs"}
            cles = ["id"]
            dictionnaire = item.objects.all()[0].__dict__.keys()
            
            for element in dictionnaire:
                trouve = False
                for chaine in exclude_list:
                    if chaine in element:
                        trouve = True
                        break
                if not trouve:
                    cles.append(element)
            temp["colonnes"] = cles
            print(cles)
            lignes = []
            objets = item.objects.all().order_by('-id')
            print(objets)
            objets = reversed(objets)

            for objet in objets:
                temp2 = []
                for colonne in cles:
                    texte = str(objet.__dict__.get(colonne))
                    if len(texte) > 15:
                        texte = f"{texte[0:12]}..."
                    temp2.append(texte)
                lignes.append(temp2)
            
            temp["lignes"] = lignes

            #print(item.__name__, item.objects.all())
            tables.append(temp)
        donnees = {"page_admin": PAGE_ADMIN,
        "selected" : "utilisateurs", 
        "tables" : tables}
        
        return render(request, "panneauAdmin/utilisateurs.html", donnees)
    else:
        return redirect("/")

# TODO : optimiser
def afficher_table(request, nom_table):
    user = request.user
    exclude_list = ["__", 
    "DoesNotExist", 
    "MultipleObjectsReturned", 
    "get_next_by_", 
    "get_previous_by_", 
    "objects", 
    "_meta", 
    "id"]
    temp = {}
    form = None
    form_suppr = None

    if user.is_superuser:
        items = admin.site._registry
        for item in items:
            if item.__name__.lower() == nom_table.lower():
                
                trouve = False
                i = 0
                while i < len(CLASSES) and not trouve:
                    if item.__name__.lower() == CLASSES[i][0].lower():
                        form = FORMULAIRES[i]()
                        trouve = True
                    else:
                        i += 1
                
                if request.method == "POST":
                    formulaire_sauvegarde = FORMULAIRES[i](request.POST, request.FILES)
                    formulaire_supprimer = forms.SupprimerIDForm(request.POST)

                    if formulaire_sauvegarde.is_valid():
                        formulaire_sauvegarde.save()
                    elif formulaire_supprimer.is_valid():
                        liste_identifiants = formulaire_supprimer.cleaned_data.get("liste_identifiants").replace(" ", '')
                        classe = CLASSES[i][1]
                        #print(classe.objects.all())
                        try:
                            if liste_identifiants.lower() == "all":
                                pass # TODO : faire l'option tout
                            else:
                                if ',' in liste_identifiants:
                                    for obj in liste_identifiants.split(","):
                                        if "-" in obj:
                                            elements_separes = obj.split("-")
                                            premier_element = int(elements_separes[0])
                                            deuxieme_element = int(elements_separes[1])

                                            while premier_element <= deuxieme_element:
                                                try:
                                                    objet = classe.objects.get(id=premier_element)
                                                    objet.delete()
                                                except:
                                                    pass
                                                premier_element += 1
                                        else:
                                            element = int(obj)
                                            try:
                                                objet = classe.objects.get(id=element)
                                                objet.delete()
                                            except:
                                                pass
                                else:
                                    if "-" in liste_identifiants:
                                        elements_separes = liste_identifiants.split("-")
                                        premier_element = int(elements_separes[0])
                                        deuxieme_element = int(elements_separes[1])

                                        while premier_element <= deuxieme_element:
                                            try:
                                                objet = classe.objects.get(id=premier_element)
                                                objet.delete()
                                            except:
                                                pass
                                            premier_element += 1
                                    else:
                                        element = int(liste_identifiants)
                                        try:
                                            objet = classe.objects.get(id=element)
                                            objet.delete()
                                        except:
                                            pass

                        except Exception as e:
                            print(e)
                form_suppr = forms.SupprimerIDForm()
                temp = {"titre" : item.__name__}
                cles = ["id"]
                dictionnaire = item.__dict__.keys()
                
                for element in dictionnaire:
                    trouve = False
                    for chaine in exclude_list:
                        if chaine in element:
                            trouve = True
                            break
                    if not trouve:
                        cles.append(element)
                temp["colonnes"] = cles
                lignes = []
                objets = item.objects.all().order_by('-id')[:100]

                for objet in objets:
                    temp2 = []
                    for colonne in cles:
                        texte = str(objet.__dict__.get(colonne))
                        if len(texte) > 15:
                            texte = f"{texte[0:12]}..."
                        temp2.append(texte)
                    lignes.append(temp2)
                
                temp["lignes"] = lignes

                #print(item.__name__, item.objects.all())
        if not temp:
            return redirect("../tables")

        donnees = {"page_admin": PAGE_ADMIN,
        "selected" : "tables", 
        "table" : temp, 
        "form" : form, 
        "form_supprimer" : form_suppr}
        
        return render(request, "panneauAdmin/table.html", donnees)
    else:
        return redirect("/")

def afficher_enregistrement(request, nom_table, id_enregistrement):
    
    user = request.user
    exclude_list = ["__", 
    "DoesNotExist", 
    "MultipleObjectsReturned", 
    "get_next_by_", 
    "get_previous_by_", 
    "objects", 
    "_meta", 
    "id"]

    form = None

    if user.is_superuser:
        items = admin.site._registry
        for item in items:
            if item.__name__.lower() == nom_table.lower():
                
                trouve = False
                i = 0
                while i < len(CLASSES) and not trouve:
                    if item.__name__.lower() == CLASSES[i][0].lower():
                        form = FORMULAIRES[i]()
                        trouve = True
                    else:
                        i += 1
                
                if request.method == "POST":
                    if trouve:
                        objet = CLASSES[i][1].objects.get(id=id_enregistrement)
                        formulaire_sauvegarde = FORMULAIRES[i](request.POST, request.FILES, instance=objet)


                    if formulaire_sauvegarde.is_valid():
                        formulaire_sauvegarde.save()
                        return redirect(f"../{CLASSES[i][0]}")

                else:
                    if trouve:
                        objet = CLASSES[i][1].objects.get(id=id_enregistrement)
                        form = FORMULAIRES[i](instance=objet)


                #print(item.__name__, item.objects.all())
        #if not form:
         #   return redirect("../tables")

        donnees = {"page_admin": PAGE_ADMIN,
        "selected" : "tables", 
        "form" : form, 
        "nom_table": nom_table}

        return render(request, "panneauAdmin/enregistrement.html", donnees)
    else:
        return redirect("/")

def executer_comamnde(commande, delais = 0):
    global THREAD_RUNNING, CONSOLE_SERVEUR
    time.sleep(delais)
    p = Popen(commande, stdout = PIPE, stderr = STDOUT, shell = True)
    
    for ligne in p.stdout:
        ligne = ligne.decode().replace("\n", '')
        print(ligne)
        CONSOLE_SERVEUR += ligne + "<br>"; 

    THREAD_RUNNING = False

def api(request, fonction):
    global THREAD_RUNNING, CONSOLE_SERVEUR
    user = request.user

    if user.is_superuser:
        return_content = {}

        if fonction == "all":
            disque = psutil.disk_usage('/')
            disqueTotal = round(disque.total / (2**30), 2)
            disqueUtilise = round(disque.used / (2**30), 2)
            disqueRestant = round(disque.free / (2**30), 2)

            ram = psutil.virtual_memory()
            ram_total = round(ram.total / (2**30), 2)
            ram_utilise = round(ram.used / (2**30), 2)
            ram_restant = round(ram.free / (2**30) + ram.cached / (2**30), 2)
            
            return_content = {
                "cpu" : psutil.cpu_percent(2),
                "ramUtilise" : ram_utilise,
                "ramRestant" : ram_restant,
                "ramTotal" : ram_total,
                "disqueUtilise" : disqueUtilise,
                "disqueRestant" : disqueRestant,
                "disqueTotal" : disqueTotal,

            }
            if THREAD_RUNNING:
                return_content["etat_serveur"] = "maj"
            else:
                return_content["etat_serveur"] = "ok"
            
        elif fonction == "update":
            if not THREAD_RUNNING:
                print("update")
                command = ""
                arch = os.popen("command -v pacman").read()
                debian = os.popen("command -v apt").read()
                #fedora = os.popen("command -v dnf").read()

                if arch != "":
                    command = "sudo pacman -Syyu --noconfirm"
                elif debian != "":
                    command = "sudo apt update -y && sudo apt upgrade -y && sudo apt dist-upgrade -y && sudo apt autoremove -y"
                else:
                    command = "sudo dnf upgrade -y"
                th = threading.Thread(target=executer_comamnde, args=(command, ))
                th.start()
                THREAD_RUNNING = True
            

        elif fonction == "reboot":
            if not THREAD_RUNNING:
                print("reboot")
            
                command = "sudo reboot"
                th = threading.Thread(target=executer_comamnde, args=(command, ))
                th.start()
                THREAD_RUNNING = True
        
        elif fonction == "console":
            return_content["consoleServeur"] =  CONSOLE_SERVEUR
            
        elif fonction == "clear":
            CONSOLE_SERVEUR = ""
            return_content["consoleServeur"] =  CONSOLE_SERVEUR

        return HttpResponse(json.dumps(return_content), content_type="application/json")

def serveur(request):
    user = request.user

    if user.is_superuser:
        formCommande = forms.CommandeForm()
        donnees = {"formCommande" : formCommande,
        "selected" : "serveur",
        "page_admin" : PAGE_ADMIN}
        return render(request, "panneauAdmin/serveur.html", donnees)

def activer_cafe(request):
    global PAGE_CAFE

    utilisateur = request.user

    if utilisateur.is_superuser:
        PAGE_CAFE = not PAGE_CAFE
        return redirect(f"/{PAGE_ADMIN}")