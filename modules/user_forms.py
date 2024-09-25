from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, RadioField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(message="You must have a username")
    ])

    password = PasswordField(validators=[
        InputRequired(message="You must have a password")
    ])


class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(message="A username is required")
    ])
    password = PasswordField(validators=[
        InputRequired(message="A password is required")
    ])
    password_repeat = PasswordField(validators=[
        InputRequired(message="You must put the same password again")
    ])

class LogoutForm(FlaskForm):
    do_logout = RadioField(choices=[
        
    ])