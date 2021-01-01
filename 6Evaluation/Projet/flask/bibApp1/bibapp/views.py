#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, \
     request, url_for, session


#from .forms import LoginForm
#from .models import connect, User

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
    return "Rien ici encore"

@app.route('/success/<username>')
def sucess(username):
    return "Rien ici encore"


@app.route('/logout')
def logout():
    return "Rien ici encore"    
    

@app.route('/selectEC', methods=('GET', 'POST'))
def selectEC():
    return "Rien ici encore"


@app.route('/selectLabo/')
def selectLabo(labo=None):
    return "Rien ici encore"
    
    
@app.route('/affichEC/')
@app.route('/affichEC/<EC>')
def affichEC(EC=None):
    return "Rien ici encore"

@app.route('/affichLabo/')
@app.route('/affichLabo/<labo>')
def affichLabo(labo=None):
    return "Rien ici encore"

@app.route('/graphLabo/')
@app.route('/graphLabo/<labo>')
def graphLabo(labo=None):
    return "Rien ici encore"



@app.route('/success/<EC>')
def success(EC):
    return "Le choix effectué est " + EC + ".\n"




