"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

# Hiding this javascript reference: <script type="text/javascript" src="/static/script.js"></script>
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    if session["logged-in"]:
        if session["logged-in"] == True:
            flash("Welcome back, FRIEND")

    return render_template("homepage.html")

@app.route('/check-login')
def get_login_status():
    """Checks for session information to show logout button"""
    if session.get("logged-in") is True:
        response = {"logged-in": "True"}
    else:
        response = {"logged-in": "False"}
    return jsonify(response)


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register', methods=["GET"])
def registration_form():
    """Allow user to register an account"""

    return render_template("registration.html")


@app.route('/register', methods=["POST"])
def registration_process():
    """Queries database and registers user if email unique"""

    reg_email = request.form.get('email')
    reg_password = request.form.get('password')

    in_db = User.query.filter(User.email == reg_email).first()
    # queries user table for any record with that email; returns None if no record

    if in_db is None:

        user = User(email=reg_email, password=reg_password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')

    else:
        flash("This email is already registered. ):<")

        return render_template("registration.html")


@app.route('/login', methods=['GET'])
def login_form():
    """Allow user to log-in"""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_process():
    """Verifying login data with database"""

    login_email = request.form.get("email")
    login_password = request.form.get("password")

    valid_email = db.session.query(User).filter_by(email=login_email).first()

    if valid_email is None:
        flash("That login is not valid. You should join us, or figure out the right credentials.")
        return redirect("/login")

    else:
        if valid_email.password == login_password:
            session["logged-in"] = True
            return redirect("/")
        else:
            flash("That login is not valid. You should join us, or figure out the right credentials.")
            return redirect("/login")


@app.route('/logout', methods=['POST'])
def logout_form():
    """Allow user to log-out"""

    session["logged-in"] = False
    return redirect('/')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
