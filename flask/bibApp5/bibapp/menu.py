from flask_wtf import Form
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class MyForm(Form):
   

    lang = SelectField(u'Programming Language', 
                choices=[], 
                    id = 'selectmenu')
    submit = SubmitField('Go')
    
    
    def __init__(self, choices=None, **kwargs):
        super().__init__(**kwargs)
        if choices is None:
            choices=[('1', 'un'), ('2', 'deux')]
        self['lang'].choices = choices   

    
from flask import Flask, flash, redirect, render_template, \
     request, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/menu', methods=('GET', 'POST'))
def menu():
    choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
    form = MyForm(choices)
    if form.validate_on_submit():
        return redirect('/success/'+form.lang.data)
    return render_template('menu.html', form=form)

@app.route('/success/<lang>')
def success(lang):
    return "Le choix effectué est " + lang + ".\n"


if __name__=='__main__':
    app.run(debug=True, port=2747)
