#!/usr/bin/env python3


from bibapp import db
from bibapp.models import ESIEEAuthor, Labo, Publis


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

# ============== Publis ===============
def splitAuthors(authors):
    l = authors.split(';')
    w = [x.split(',')[0].strip() for x in l]
    if '&' in l[-1]:
        w.append(l[-1].split('&')[1].split(',')[0].strip())
    return w

import pandas as pd

listColumns = ['BibliographyType', 'ISBN', 'Identifier', 'Author', 'Title', 'Journal',
       'Volume', 'Number', 'Month', 'Pages', 'Year', 'Address', 'Note', 'URL',
       'Booktitle', 'Chapter', 'Edition', 'Series', 'Editor', 'Publisher',
       'ReportType', 'Howpublished', 'Institution', 'Organizations', 'School',
       'Annote', 'Custom1', 'Custom2', 'Custom3', 'Custom4', 'Custom5'],

authorsDict = {u.nom.lower():u for u in ESIEEAuthor.query.all()}

for csvfile in ['2015-16.csv', '2016-17.csv','2017-18.csv', '2018-19.csv', '2019-20.csv', '2020-21.csv']:
    
    Tab = pd.read_csv("csv/"+csvfile, sep=",", header=0, escapechar="\\", error_bad_lines=False)

    for idx in Tab.index:           
        if not Publis.query.filter(Publis.Identifier==Tab.loc[idx, 'Identifier']).first(): #Test si pas déjà dans la base       
            authors = splitAuthors(Tab.loc[idx, 'Author'])
            listAuthors = []
            for author in authors:
                if author.lower() in authorsDict.keys():
                    listAuthors.append(authorsDict[author.lower()])

            publi = Publis()
                #id = Tab.loc[idx, 'Identifier']) 
            for attribut in dir(publi): 
                if not attribut.startswith('_') :
                    try:
                        if not attribut=='Year': 
                            setattr(publi, attribut, Tab.loc[idx, attribut])
                    except:
                        pass
            publi.Author = listAuthors 
            publi.Year = int(Tab.loc[idx,'Year'])
            publi.authors = Tab.loc[idx, 'Author']
            db.session.add(publi)
            db.session.commit()
