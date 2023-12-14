from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo


#UTENTE
class RegistrazioneForm(FlaskForm):
    nome = StringField('nome', validators=[InputRequired(), Length(min=2, max=50)])
    cognome = StringField('cognome', validators=[InputRequired(), Length(min=2, max=50)])
    email = StringField('email', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired()])
    confermaPassword = PasswordField('confermaPassword', validators=[InputRequired(), EqualTo('password')])

    

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    submit = SubmitField('invia')


