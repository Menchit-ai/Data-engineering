
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Go')
    
class MySelectMenu(FlaskForm):
  
    mySelect = SelectField('selectFieldName', 
                choices=[], 
                    id = 'selectMenu')
    submit = SubmitField('Go')
      
    def __init__(self, choices=None, selectFieldName="", **kwargs):
        super().__init__(**kwargs)
        if choices is None:
            choices=[('1', 'un'), ('2', 'deux')]
        self['mySelect'].label = selectFieldName    
        self['mySelect'].choices = choices   


        
