from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from elasticsearch import Elasticsearch
import pandas as pd
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)
db = SQLAlchemy(app)
es = Elasticsearch([{"host": "host.docker.internal", "port": 9200}])
fich = pd.read_json("./json/data.json")
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
