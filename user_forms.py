from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, RadioField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Regexp

class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(message="You must have a username"),
    ])
    password = PasswordField(validators=[
        InputRequired(message="You must have a password"),
    ])


class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(message="A username is required"),
    ])
    password = PasswordField(validators=[
        InputRequired(message="A password is required"),
        EqualTo("password_repeat", message="Passwords must match"),
    ])
    password_repeat = PasswordField()

class LogoutForm(FlaskForm):
    user_logout = RadioField('logout',
                             choices=[(True, 'Yes, log me out.'), (False, 'Return to homepage.')],
                             validators=[InputRequired("Please choose.")
    ])
