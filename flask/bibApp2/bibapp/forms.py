
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, RadioField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Login')
    

        
