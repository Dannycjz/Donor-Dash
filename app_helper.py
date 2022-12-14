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
    name = StringField('Name', [validators.InputRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder": "Name", "class": "form-control"})
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6),
        validators.EqualTo('confirm', message='Passwords must match')
    ], render_kw={"placeholder": "Password", "class": "form-control"})
    confirm = PasswordField('Retype password', [validators.InputRequired()], render_kw={"placeholder": "Retype Password", "class": "form-control"})

# Form class
# From https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/
class LoginForm(Form):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()
    ])