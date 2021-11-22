from django.http import HttpResponseForbidden
from .models import IPLog
import time

NB_CONNEXION = 15
DELAIS_CONNEXION_SECONDES = 5
TEMPS_BAN_SECONDES = 1 * 60


class DDOS_PROTECTION:
    BAN_IP_LIST = []

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        valide = True
        formulaire = IPLog(adresse_IP=ip, request=req)
        formulaire.save()
        """
        #########################################################
        valide = True

        try:
            ip = request.META.get('HTTP_X_REAL_IP')
            req = request.headers
            #ip = "198.119.191.29"
            objets = IPLog.objects.filter(adresse_IP=ip).order_by('-date')[:NB_CONNEXION-1]
            print(objets)
            if objets:
                debut = objets[len(objets) - 1].date.timestamp()
            else:
                debut = 0

            fin = time.time()
            delais = fin - debut

            print(DDOS_PROTECTION.BAN_IP_LIST, delais)

            is_ban = False
            i = 0
            trouve = False
            while i < len(DDOS_PROTECTION.BAN_IP_LIST) and not trouve:
                if DDOS_PROTECTION.BAN_IP_LIST[i][0] == ip:
                    is_ban = True
                    trouve = True
                else:
                    i += 1
            
            if is_ban:
                if delais >= TEMPS_BAN_SECONDES:
                    del DDOS_PROTECTION.BAN_IP_LIST[i]
                else:
                    valide = False
            else:
                if delais <= DELAIS_CONNEXION_SECONDES:
                    valide = False
                    DDOS_PROTECTION.BAN_IP_LIST.append([ip, time.time()])

            if not valide:
                req = "DOS / DDOS - BLOCKED"

            formulaire = IPLog(adresse_IP=ip, request=req)
            formulaire.save()

            
        except Exception as e:
            print(e)"""

        if valide:
            return response
        else:
            return HttpResponseForbidden()