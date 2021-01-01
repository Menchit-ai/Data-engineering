#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, \
     request, url_for, session
from flask_login import LoginManager, logout_user, login_required, \
       login_user, current_user, UserMixin

from .forms import LoginForm, MySelectMenu
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
    form = MySelectMenu(choices=ListeLabos, selectFieldName="Choix d'un laboratoire")
    if form.validate_on_submit():
         return redirect('/affichLabo/'+form.mySelect.data)       
    return render_template('menu.html', form=form, title="SelectLabo")    

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





@app.route('/success/<EC>')
def success(lang):
    return "Le choix effectué est " + EC + ".\n"




