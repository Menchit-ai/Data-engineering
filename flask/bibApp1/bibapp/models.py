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



