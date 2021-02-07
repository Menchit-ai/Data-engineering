from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class MySelectMenu(FlaskForm):
  
    mySelect = SelectField('selectFieldName', 
                choices=[], 
                    id = 'selectMenu')
    research = StringField('Research', validators=[DataRequired()])
    submit = SubmitField('Go')
      
    def __init__(self, choices=None, selectFieldName="", **kwargs):
        super().__init__(**kwargs)
        if choices is None:
            choices=[('1', 'un'), ('2', 'deux')]
        self['mySelect'].label = selectFieldName    
        self['mySelect'].choices = choices

class GraphsMenu(FlaskForm):
  
    mySelect = SelectField('selectFieldName', 
                choices=[], 
                    id = 'selectMenu')
    #radio = RadioField('Options pour le graphe :', choices=[('Max','Récurrence'), ('Mean','Moyenne')], default='Max') 
    submit = SubmitField('Go')
      
    def __init__(self, choices=None, selectFieldName="", **kwargs):
        super().__init__(**kwargs)
        if choices is None:
            choices=[('1', 'un'), ('2', 'deux')]
        self['mySelect'].label = selectFieldName    
        self['mySelect'].choices = choices