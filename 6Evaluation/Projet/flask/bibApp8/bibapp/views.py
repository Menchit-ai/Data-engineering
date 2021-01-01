#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, \
     request, url_for, session
from flask_login import LoginManager, logout_user, login_required, \
       login_user, current_user, UserMixin

from .forms import LoginForm, MySelectMenu, MyLaboMenu
from .models import connect, User, ESIEEAuthor, Labo, Publis

from . import app, login_manager 


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
@app.route('/index')
def rien():
    return render_template('index.html')
    

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if connect(form.login.data, form.password.data):
            u = User(42, form.login.data)
            login_user(u, remember=form.remember_me.data)
            session['user_id']=u.get_id()
            print("current_user", current_user)            
            return redirect('/success/'+form.login.data)
    return render_template('login.html', form=form)


@app.route('/success/<username>')
@login_required
def sucess(username):
    print("current_user", current_user)
    return "Salut " + username + ".\nTu es arrivé jusque là. "



@app.route('/logout')
@login_required
def logout():
    print("current_user", current_user)
    session.clear()
    logout_user()
    return "you are logged out"
    
    

@app.route('/selectEC', methods=('GET', 'POST'))
@login_required
def selectEC():
    print("current_user", current_user)
    ListeAuthors = [(au.nom,au.nom) for au in ESIEEAuthor.query.all()]
    ListeAuthors.sort()
    form = MySelectMenu(choices=ListeAuthors, selectFieldName="Choix d'un auteur")
    if form.validate_on_submit():
        return redirect('/affichEC/'+form.mySelect.data)
    return render_template('menu.html', form=form, title="SelectEC")

@app.route('/selectLabo', methods=('GET', 'POST'))    
@login_required
def selectlabo():
    ListeLabos = [(labo.labname, labo.labname) for labo in Labo.query.all()]
    form = MyLaboMenu(choices=ListeLabos, selectFieldName="Choix d'un laboratoire")
    if form.validate_on_submit():
        if form.radio.data=='no':
            return redirect('/affichLabo/'+form.mySelect.data)
        else:
            return redirect('/graphLabo/'+form.mySelect.data)
    return render_template('menu_radio.html', form=form, title="SelectLabo")    

@app.route('/affichEC/')
@app.route('/affichEC/<EC>')
def affichEC(EC=None):
    if EC is None:
        flash("pas d'auteur spécifié")
        return redirect('/')
    auteur = ESIEEAuthor.query.filter(ESIEEAuthor.nom==EC).first()
    allPubs = auteur.publis
    return render_template('affichPublis.html', listePublis=allPubs, Qui=auteur.prenom + " " + auteur.nom)    

@app.route('/affichLabo/')
@app.route('/affichLabo/<labo>')
def affichLabo(labo=None):
    if labo is None:
        flash("pas de labo spécifié")
        return redirect('/')
    allPubs = Publis.query.join(Publis.Author).join(ESIEEAuthor.labo).filter(Labo.labname==labo).all() 
    return render_template('affichPublis.html', listePublis=allPubs, Qui=labo)    


@app.route('/graphLabo/<labo>')
def graphLabo(labo):
    from datetime import date
    import pandas as pd
    allPubs = Publis.query.join(Publis.Author).join(ESIEEAuthor.labo).filter(Labo.labname==labo).all() 
    monthsDict = {'January': 1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 
                  'September':9, 'October':10, 'November':11, 'December':12 , None:1}
    listDates = [date(pub.Year, monthsDict[pub.Month], 1) for pub in allPubs]
    dateIndex = pd.date_range('2015-01-01', periods=72, freq='MS').to_native_types()
    tab = pd.DataFrame(index=dateIndex, columns=['vals'])
    tab['vals'] = 0
    for d in listDates:
        tab.loc[str(d), 'vals'] = tab.loc[str(d), 'vals']+1

    pd.options.plotting.backend = "pandas_bokeh"
    w = tab.plot(kind='bar',vertical_xlabel=True, return_html=True, show_figure=False)
    
    return render_template('graphPublis.html', graph=w, Qui=labo) 


@app.route('/success/<EC>')
def success(lang):
    return "Le choix effectué est " + EC + ".\n"




