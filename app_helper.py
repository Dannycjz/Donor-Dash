from functools import wraps
from flask import g, redirect, session
from wtforms import Form, BooleanField, StringField, PasswordField, validators

# Login required Decorator
# From http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# Form class
# From https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/
class RegistrationForm(Form):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

# Form class
# From https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/
class LoginForm(Form):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()
    ])