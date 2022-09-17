from flask import Flask, render_template, request, session, redirect, flash
import sys
from app_helper import login_required
from flask_session import Session
import sqlite3
from tempfile import mkdtemp
from sqlite3 import Error
import pandas as pd
from wtforms import Form, BooleanField, StringField, PasswordField, validators

from app_helper import login_required, RegistrationForm, LoginForm

app=Flask(__name__)

# Configure session to use filesystem 
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
# Registers a new user
def register():
    # Configures SQLite database
    db=sqlite3.connect("chess")
    c=db.cursor()
    
    # Forgets any existing userID
    session.clear()

    form = RegistrationForm(request.form)
    
    # User reached route via POST
    if request.method=="POST" and form.validate():

        username=form.username.data
        password=form.password.data

        script="INSERT INTO users (user_name, password) VALUES (?, ?)"
        values=(username, password)
        # Insert user info into database
        c.execute(script, values)
        db.commit()

        # Redirect the user back to the homepage
        return redirect('/')
    # User reached route via GET
    else:
        return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
# Logs the user in
def login():

    # Configures SQLite database
    db=sqlite3.connect("chess")
    c=db.cursor()
    
    # Forget any current user_id
    session.clear()
    
    form = LoginForm(request.form)
    error = None

    # User reached route via POST
    if request.method=="POST":

        password=form.password.data

        # Query database for username
        script="SELECT * FROM users WHERE user_name=?"
        username=form.username.data
        c.execute(script, [username])

        # Loads SQLite object into a dataframe
        df=pd.DataFrame(c.fetchall(), columns=['user_id', 'user_name', 'password'])

        if len(df)==0:
            error = 'Invalid username'
        else:
            # Remember which user has logged in
            user_data=df.loc[df['user_name']==username].values[0]

            # Ensure username exists and password is correct 
            if user_data[2]!=password:
                error = 'Invalid password'
            else:
                flash('You were successfully logged in')
                session["user_id"]=user_data[0]
                # Redirect user to home page
                return redirect("/")
    
    return render_template("login.html", form=form, error=error)

@app.route("/logout")
# Logs the user out
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/donor")
# Donor view
def donor():
    # Pull receiver data from database
    db = sqlite3.connect("donations")
    cursor = db.cursor()

    cursor.execute('''
                SELECT * FROM donations
                ''')
    
    df=pd.DataFrame(cursor.fetchall(), columns=['donation_id', 
                                                'object', 
                                                'cause', 
                                                'user_id', 
                                                'donation_scores', 
                                                'x', 
                                                'y'])

    # Render map + Receiver pings

    # Show info once ping is clicked

    return render_template("donor_map.html")

@app.route("/receiver_form", methods=["GET"])
# View for receiver to fill out form
def receiver_form():
    # Opens up the form for the user to use
    if request.method == "GET":
        return render_template('formAdmin.html')


@app.route("/receiver_submit", methods=["POST"])
def receiver_submit():
    if request.method == "POST":
        return None


@app.route("/receiver_map")
# Map view for receiver to ping location
def receiver_map():
    # Renders the empty map image

    # Stores the user's geolocation into database

    # Returns render template of end page after storing data
    return None

if __name__=="__main__":
    app.run()

