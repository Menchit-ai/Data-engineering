#
from flask import Flask
from flask_bootstrap import Bootstrap

#from config import Config # si la config est définie dans config.py
# Base de données
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# LoginManager
from flask_login import LoginManager

# Création app
app = Flask(__name__)
#app.config['SECRET_KEY'] = 'you-will-never-guess'

Bootstrap(app)

## Configuration
#app.config.from_object(Config) # Si objet Config dans config.py 
app.config.from_object('config') # nom du fichier de config

login_manager = LoginManager() 

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#from app import routes, models 
from bibapp import login

