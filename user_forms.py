from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, RadioField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Regexp

class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(message="You must have a username"),
        Regexp("r'^[\w.@+-]+$'", message="Provide a username without whitespaces.")
    ])

    password = PasswordField(validators=[
        InputRequired(message="You must have a password"),
        Regexp("r'^[\w.@+-]+$'", message="Provide a password without whitespaces.")
    ])


class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(message="A username is required"),
        Regexp("r'^[\w.@+-]+$'", message="Provide a username without whitespaces.")
    ])
    password = PasswordField(validators=[
        InputRequired(message="A password is required"),
        EqualTo("password_repeat", message="Passwords must match"),
        Regexp("r'^[\w.@+-]+$'", message="Provide a password without whitespaces.")
    ])
    password_repeat = PasswordField()

class LogoutForm(FlaskForm):
    user_logout = RadioField('logout',
                             choices=[(True, 'Yes, log me out.'), (False, 'Return to homepage.')],
                             validators=[InputRequired("Please choose.")
    ])
