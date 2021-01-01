import os
basedir  = os.getcwd()
basedir = basedir[0] if isinstance(basedir, list) else basedir

"""class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
"""    
    
# global configs
basedir = os.path.abspath(os.path.dirname(__file__))


# database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True


# login token
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


# global constants
FILES = basedir + '/files'
APPDIR = basedir + '/bibapp'

