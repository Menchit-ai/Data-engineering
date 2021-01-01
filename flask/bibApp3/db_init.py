#!/usr/bin/env python3


from bibapp import db
from bibapp.models import ESIEEAuthor, Labo


import pandas as pd

# ================ Labos =============
labnames = ['LIGM', 'ESYCOM', 'LISIS', 'IRG', 'ESIEE']
labDict = {}
for lab in labnames:
    l = Labo(labname=lab)
    labDict[lab] = l 
    db.session.add(l)
    db.session.commit()

#================= Auteurs ============


Tab = pd.read_excel("listeBiblio.xls")



for idx in Tab.index:
    try:
        deb = int(Tab.loc[idx, 'Début'])
    except:
        deb=0
    try:
        fin = int(Tab.loc[idx, 'Fin'])
    except:
        fin=2999    
        
    auteur = ESIEEAuthor(
        nom=Tab.loc[idx, 'Nom'],
        prenom=Tab.loc[idx, 'Prenom'],
        labo=labDict.get(Tab.loc[idx, 'Labo'], labDict['ESIEE']),
        HAL=Tab.loc[idx, 'HAL'],
        debut_activite=deb,
        fin_activite=fin
    )
    db.session.add(auteur)
    db.session.commit()


