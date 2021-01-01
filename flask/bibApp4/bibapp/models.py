from flask_login import UserMixin

#

from . import db 

def connect(accountName,password):
    if (accountName=="user") & (password=="password"):
      return True
    return False
##
class User(db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())

    def __init__(self, id, username=''):
        self.username = username
        self.id = id
        
    def get_id(self):         
        return str(self.id)
    def get_role(self):
        return 2
    def get_name(self):
        return self.username    
    @property
    def is_active(self):
        return True
        
    @property
    def is_anonymous(self):
        return False


    @property
    def is_authenticated(self):
        return True                    
        
###        



#https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
#from sqlalchemy import Table, Column, Integer, ForeignKey
#from sqlalchemy.orm import relationship
#from sqlalchemy.ext.declarative import declarative_base

Base = db.Model 


association_table = db.Table('association', Base.metadata,
    db.Column('auteurs', db.Integer, db.ForeignKey('authors.id')),
    db.Column('labos', db.Integer, db.ForeignKey('labos.id'))                             
)



class Labo(db.Model):
    __tablename__ = 'labos'
    id = db.Column(db.Integer, primary_key=True)
    labname = db.Column(db.String(64), index=True)
    membres = db.relationship('ESIEEAuthor', backref='labo', lazy='dynamic') 

    def __repr__(self):
        return '<Lab {}>'.format(self.labname)

class ESIEEAuthor(Base):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64))
    prenom = db.Column(db.String(64))
    HAL = db.Column(db.String(64))
    debut_activite = db.Column(db.Integer)
    fin_activite = db.Column(db.Integer)
    labo_id = db.Column(db.Integer, db.ForeignKey('labos.id'))

    def __repr__(self):
        return '<Author {}>'.format(self.nom)

