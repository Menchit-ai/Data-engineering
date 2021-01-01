#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, \
     request, url_for, session
from flask_login import LoginManager, logout_user, login_required, \
       login_user, current_user, UserMixin

from .forms import LoginForm, MySelectMenu
from .models import connect, User, ESIEEAuthor, Labo

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
    return "Rien ici encore"


@app.route('/selectLabo/')
def selectLabo(labo=None):
    return "Rien ici encore"
    
    
@app.route('/affichEC/')
@app.route('/affichEC/<EC>')
def affichEC(EC=None):
    if EC is None:
        flash("pas d'auteur spécifié")
        return redirect('/')
    auteur = ESIEEAuthor.query.filter(ESIEEAuthor.nom==EC).first()        
    return render_template('affichQui.html', Qui=auteur.prenom + " " + auteur.nom)    

@app.route('/affichLabo/')
@app.route('/affichLabo/<labo>')
def affichLabo(labo=None):
    return "Rien ici encore"

@app.route('/graphLabo/')
@app.route('/graphLabo/<labo>')
def graphLabo(labo=None):
    return "Rien ici encore"



@app.route('/success/<EC>')
def success(lang):
    return "Le choix effectué est " + EC + ".\n"




