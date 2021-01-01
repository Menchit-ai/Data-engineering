#
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

Bootstrap(app)

login_manager = LoginManager() 

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
