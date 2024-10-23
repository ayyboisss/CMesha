from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, RadioField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Regexp

class LoginForm(FlaskForm):
    """
    Login Form utilizing flask-WTF. Has 2 fields, 'username' and 'password'.
    All fields have validator 'InputRequired'.
    """
    username = StringField(validators=[
        InputRequired(message="You must have a username"),
    ])
    password = PasswordField(validators=[
        InputRequired(message="You must have a password"),
    ])
    label = "Login"


class RegisterForm(FlaskForm):
    """
    Register Form utilizing flask-wtf. Has 3 fields, 'username', 'password' and 'password_repeat'.
    'username' and 'password' fields have InputRequired as validators, password has validator 'EqualTo' requiring the data
    to match with 'password_repeat'.
    """
    username = StringField(validators=[
        InputRequired(message="A username is required"),
    ])
    password = PasswordField(validators=[
        InputRequired(message="A password is required"),
        EqualTo("password_repeat", message="Passwords must match"),
    ])
    password_repeat = PasswordField()
    label= "Register"

class LogoutForm(FlaskForm):
    """
    Logout Form utilizing flask-wtf. Has 1 field, 'user_logout'. This is a radio field
    with 2 choices, 'Yes, log me out.' and 'Return to homepage'. Has validator InputRequired.
    """
    user_logout = RadioField('logout',
                             choices=[(True, 'Yes, log me out.'), (False, 'Return to homepage.')],
                             validators=[InputRequired("Please choose.")])
    label="Logout"
