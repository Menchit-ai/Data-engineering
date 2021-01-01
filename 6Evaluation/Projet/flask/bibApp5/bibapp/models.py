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
    db.Column('publis', db.Integer, db.ForeignKey('publis.id')),
    db.Column('labos', db.Integer, db.ForeignKey('labos.id'))                             
)



class Labo(db.Model):
    __tablename__ = 'labos'
    id = db.Column(db.Integer, primary_key=True)
    labname = db.Column(db.String(64), index=True)
    membres = db.relationship('ESIEEAuthor', backref='labo', lazy='dynamic') # crée un lien avec un attribut "author" pour chacun des posts
    publis = db.relationship(
        "Publis",
        secondary=association_table,
        back_populates="labos")    

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
    publis = db.relationship(
        "Publis",
        secondary=association_table,
        back_populates="Author")
    labo_id = db.Column(db.Integer, db.ForeignKey('labos.id'))

    def __repr__(self):
        return '<Author {}>'.format(self.nom)


class Publis(Base):
    __tablename__ = 'publis'
    id = db.Column(db.Integer, primary_key=True)
    #id = db.Column(db.String(64), primary_key=True)
    BibliographyType = db.Column(db.String(64))
    authors = db.Column(db.String(128))
    ISBN = db.Column(db.String(64))
    Identifier = db.Column(db.String(64))
    Title = db.Column(db.String(64))
    Journal = db.Column(db.String(64))
    Volume = db.Column(db.String(64))
    Number = db.Column(db.String(64))
    Month = db.Column(db.String(64))
    Pages = db.Column(db.String(64))
    Year = db.Column(db.Integer)
    Address = db.Column(db.String(64))
    Note = db.Column(db.String(64))
    URL = db.Column(db.String(64))
    Booktitle = db.Column(db.String(64))
    Chapter = db.Column(db.String(64))
    Edition = db.Column(db.String(64))
    Series = db.Column(db.String(64))
    Editor = db.Column(db.String(64))
    Publisher = db.Column(db.String(64))
    ReportType = db.Column(db.String(64))
    Howpublished = db.Column(db.String(64))
    Institution = db.Column(db.String(64))
    Organizations = db.Column(db.String(64))
    School = db.Column(db.String(64))
    Annote = db.Column(db.String(64))
    Custom1 = db.Column(db.String(64))
    Custom2 = db.Column(db.String(64))
    Custom3 = db.Column(db.String(64))
    Custom4 = db.Column(db.String(64))
    Custom5 = db.Column(db.String(64))
    Author = db.relationship(
        "ESIEEAuthor",
        secondary=association_table,
        back_populates="publis")
    labos = db.relationship(
        "Labo",
        secondary=association_table,
        back_populates="publis")    

    def __repr__(self):
        return '<Publis {}>'.format(self.Identifier)    

"""
'BibliographyType', 'ISBN', 'Identifier', 'Author', 'Title', 'Journal',
       'Volume', 'Number', 'Month', 'Pages', 'Year', 'Address', 'Note', 'URL',
       'Booktitle', 'Chapter', 'Edition', 'Series', 'Editor', 'Publisher',
       'ReportType', 'Howpublished', 'Institution', 'Organizations', 'School',
       'Annote', 'Custom1', 'Custom2', 'Custom3', 'Custom4', 'Custom5'
"""
        
#db.create_all() # Création des tables    
