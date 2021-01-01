#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, \
     request, url_for
from flask_login import LoginManager, logout_user, login_required, \
       login_user, current_user, UserMixin

from .forms import LoginForm
from .models import connect, User

from . import app, login_manager 


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
def rien():
    return "Rien ici... <a href='/login'> voir là </a> "

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if connect(form.login.data, form.password.data):
            u = User(42, form.login.data)
            login_user(u, remember=form.remember_me.data)
            return redirect('/success/'+form.login.data)
    return render_template('login.html', form=form)

@login_required
@app.route('/success/<username>')
def sucess(username):
    return "Salut " + username + ".\nTu es arrivé jusque là. "


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return "you are logged out"
    
    
@login_required
@app.route('/selectEC', methods=('GET', 'POST'))

def menu():
    ListeAuthors = [(au.nom,au.nom) for au in ESIEEAuthor.query.all()]
    choices=ListeAuthors
    form = MySelectMenu(choices=choices, selectFieldName="Choix d'un auteur")
    if form.validate_on_submit():
        return redirect('/success/'+form.mySelect.data)
    return render_template('menu.html', form=form)

@app.route('/success/<EC>')
def success(lang):
    return "Le choix effectué est " + EC + ".\n"




