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
    if not session.get('user_id'):
            return redirect('/login')
    return render_template("newMainPage.html")

@app.route('/register', methods=["GET", "POST"])
# Registers a new user
def register():
    # Configures SQLite database
    db=sqlite3.connect("donations")
    c=db.cursor()
    
    # Forgets any existing userID
    session.clear()

    form = RegistrationForm(request.form)
    
    try:
        form = RegistrationForm(request.form)
        if (request.method == 'POST' and form.validate()):
            username=form.name.data
            password=form.password.data

            script="INSERT INTO users (user_name, password) VALUES (?, ?)"
            values=(username, password)
            # Insert user info into database
            c.execute(script, values)
            db.commit()
            return redirect('/login')
        return render_template('registerNew.html', form=form)

    except Exception as e:
        print("register info ERROR : " , str(e))
        return "register info ERROR : " + str(e)


@app.route('/login', methods=["GET", "POST"])
# Logs the user in
def login():

    # Configures SQLite database
    db=sqlite3.connect("donations")
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
        df=pd.DataFrame(c.fetchall(), columns=['user_id', 'user_name', 'password', 'user_score'])

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
                session["user_id"]= (user_data[0], user_data[1])
                # Redirect user to home page
                return redirect("/")
    
    return render_template("loginNew.html", form=form, error=error)

@app.route("/logout")
# Logs the user out
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/donor", methods=["GET", "POST"])
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



@app.route("/receiver_form", methods=["GET", "POST"])
# View for receiver to fill out form
def receiver_form():
    # if not session.get('user_id'):
    #         return redirect('/login')
    # Opens up the form for the user to use
    if request.method == "GET":
        return render_template('formAdmin.html', name = session.get('user_id')[1])
    if request.method == "POST":
        db=sqlite3.connect("donations")
        c=db.cursor()

        form = request.form

        script='''INSERT INTO donations 
                (object, cause, user_id, donation_scores, x, y) 
                    VALUES 
                    (?, ?, ?, ?, ?, ?)'''
        values=(form['object'], form['cause'], session.get('user_id')[0], form['donation_scores'], None, None)
        # Insert donation info into database
        c.execute(script, values)
        db.commit() 

        script2='''SELECT * FROM donations WHERE object = ? AND 
                    user_id = ?'''
        values2 = (form['object'], session.get('user_id')[0])
        c.execute(script2, values2)
        donation_line=c.fetchall()
        session["donation_id"] = donation_line[0][0]
        return redirect("/receiver_map")


@app.route("/receiver_submit", methods=["GET", "POST"])
def receiver_submit():
    if request.method == "POST":
        return None


@app.route("/receiver_map", methods=["GET", "POST"])
# Map view for receiver to ping location
def receiver_map():
    form = request.form
    if request.method == "POST":
        # Only add to database if user confirms
        if form.get("confirmation"):
            print(form)
            # Parse location data
            latitude = form.get("latitude")
            longitude = form.get("longitude")

            user_id = session.get('user_id')[0]

            # Stores the user's geolocation into database
            db = sqlite3.connect("donations")

            db.execute(f'''
                    UPDATE donations
                    SET 
                        x = {latitude},
                        y = {longitude}
                    WHERE
                        user_id = {user_id}
                    ''')
            
            db.commit()

            # Returns render template of end page after storing data
            return render_template("confirmation.html")
        

    # Renders the empty map image if method = GET
    return render_template("receiver_map.html", form=form)

if __name__=="__main__":
    app.run()

