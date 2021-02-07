from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, es, fich
from app.forms import LoginForm, RegistrationForm, MySelectMenu, GraphsMenu
from app.models import User

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#####################

def create_figure(label): #Fonction pour faire trois différents types de graphe avec les données
    size = 20

    labels = label.split()

    if labels[0] == "max" :

        size = labels[2]

        QUERY = {
            "aggs": {
            "count_gender": {
            "terms": {
                "field": str(labels[1]),
                "size": size,
                "order": {
                "_count": "desc"
                }
            }
                }
            }
        }

        result = es.search(index="stacks", body=QUERY)
        df = pd.DataFrame(result["aggregations"]["count_gender"]["buckets"])

        df.set_index('key', inplace = True)

        #fig = plt.figure()
        #ax = fig.add_subplot(111)
        #tags = list(df['key'])
        #numbers = list(df['doc_count'])
        #ax.bar(tags,numbers)
        #ax.set_xticks(np.arange(len(tags)))
        #ax.set_xticklabels(tags, rotation = 45, zorder=100)

        pd.options.plotting.backend = "pandas_bokeh"

        fig = df.plot(kind='bar', xlabel=str(labels[1].split(".")[0]), ylabel='Nombre de posts', vertical_xlabel=True, return_html=True, show_figure=False)

        return fig

    elif labels[0] == 'look' :

        size = labels[3]

        QUERY = {
            "query": {
                "match_all": {}
            },
            "sort" : [
                { labels[1] : {"order" : "desc"}}
            ]
        }

        result = es.search(index="stacks", body=QUERY, size=size)

        titles = []

        for hit in result['hits']['hits']:
            print(hit)
            titre = str("{" + labels[2] + "}").format(**hit['_source'])
            view = str("{" + labels[1] + "}").format(**hit['_source'])

            #words = titre.split()
            #titre = words[0:5]

            if titre not in titles :
                titles.append([titre[0:25], int(view)])
            #ids.append(hit['_source'])

        df = pd.DataFrame(titles, columns = [str(labels[2]), 'vues'])
        df.set_index(str(labels[2]), inplace = True)

        pd.options.plotting.backend = "pandas_bokeh"

        fig = df.plot(kind='bar', xlabel=str(labels[2]), ylabel=str(labels[1]), vertical_xlabel=True, return_html=True, show_figure=False)

        return fig

    elif labels[0] == 'date' :

        dates = fich['date']
        hours = pd.Series([date.hour for date in dates])
        total = hours.value_counts().sort_index()

        pd.options.plotting.backend = "pandas_bokeh"

        fig = total.plot(kind='line', xlabel='Heure', ylabel='Nombre de posts', vertical_xlabel=True, return_html=True, show_figure=False)

        return fig



    else :

        size = labels[2]

        QUERY = {
            "aggs": {
                "count_gender": {
                    "terms": {
                        "field": "tags.keyword",
                        "size": size,
                        "order": {
                            "_count": "desc"
                        }
                    },
                    "aggs": {
                        "average":{
                            "avg" : {
                                "field" : str(labels[1])
                            }
                        }
                    }
                }
            }
        }

        result = es.search(index="stacks", body=QUERY)
        df = pd.DataFrame(result["aggregations"]["count_gender"]["buckets"])
        df = df.drop('doc_count', axis=1)

        a = list(df['average'])
        lis = []
        for elm in range(len(a)) :
            lis.append(int(a[elm]['value']))

        df['average'] = lis

        df.set_index('key', inplace = True)

        pd.options.plotting.backend = "pandas_bokeh"

        fig = df.plot(kind='bar', xlabel='Tags', ylabel=str(labels[1]), vertical_xlabel=True, return_html=True, show_figure=False)

        return fig

####################

@app.route('/')
@app.route('/index') #Page de bienvenue avec plusieurs liens à d'autres pages
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST']) #Pour se connecter à un compte, mais c'est inutile sur l'appli
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout') #Pour se déconnecter
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST']) #Pour créer un compte
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/search', methods=('GET', 'POST')) #Pour faire une recherche en fonction d'une caractéristique
#@login_required
def search():
    print("current_user", current_user)
    result = es.search(index="stacks", body={"query": {"match_all": {}}}, size=10)
    var = list(result['hits']['hits'][0]['_source'].keys()) #On prend toutes les variables de la base de données
    var.sort()
    form = MySelectMenu(choices=var, selectFieldName="Choix d'une variable") #Form retournant le choix de la variable et le mot recherché
    if form.validate_on_submit():
        return redirect('/result/'+ form.mySelect.data + '/' + form.research.data)
    return render_template('menu.html', form=form, title="Search")

@app.route('/result/')
@app.route('/result/<tag>/<research>') #Résultat de la recherche en fonction de la variable et du mot tapé
def searchresult(tag=None, research=None):
    if tag is None:
        flash("pas de label spécifié")
        return redirect('/')
    QUERY = {
      "query": {
        "term": {
          str(tag): str(research)
        }
      }
    }
    result = es.search(index="stacks", body=QUERY, size=200) #Query qui cherche les mentions de la recherche sur la variable
    #On prend les 200 premiers résultats

    ids = []
    titles = []
    no = False
    if len(result['hits']['hits']) != 0 :
        for hit in result['hits']['hits']:
            titre = "{title}".format(**hit['_source'])
            if titre not in titles : #Il peut apparaître des topics doublons qu'on ne prend pas
                titles.append(titre)
                print(titre)
                ids.append(hit['_source'])

    if len(ids) == 0 :
        no = True #Si on n'a pas de résultat, on affiche qu'il n'y a aucun résultat

    return render_template('result.html', results = ids, condition = no)

@app.route('/graphs', methods=('GET', 'POST')) #Menu pour le choix des graphes
#@login_required
def graphs():
    print("current_user", current_user)
    #result = es.search(index="stacks", body={"query": {"match_all": {}}}, size=10)
    #var = list(result['hits']['hits'][0]['_source'].keys())
    #var.sort()
    var = [('max author.keyword 20', 'Auteur avec le plus de posts'), ('max tags.keyword 20', 'Tags apparaissant le plus de fois'), ('look views title 50', 'Topics les plus fréquentés')
    , ('mean views 20','Moyenne des vues en fonction des tags populaires'), ('date',"Moyenne d'activité du site")] #Cinq graphes disponibles

    graphTitles = ['Auteur avec le plus de posts', 'Tags apparaissant le plus de fois', 'Topics les plus fréquentés', 'Moyenne des vues en fonction des tags populaires', "Moyenne d'activité du site"]

    form = GraphsMenu(choices=var, selectFieldName="Choix pour le tracé du graphe")
    if form.validate_on_submit():
        name = "Graphe"
        for i in range(len(var)) :
            if form.mySelect.data in var[i] : #Pour avoir le titre du graphe
                name = graphTitles[i]
        return redirect('/graphresult/'+ form.mySelect.data + '/' + name)
    return render_template('graphmenu.html', form=form, title="Graphs")

@app.route('/graphresult/<label>/<name>')
def plotgraph(label=None, name=None):
    fig = create_figure(label) #Fonction traçant le graphe choisi
    return render_template('graphresult.html', graph=fig, name=name)