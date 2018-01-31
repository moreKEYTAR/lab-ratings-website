"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


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

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register', methods=["GET"])
def registration_form():
    """Allow user to make an account login."""

    return render_template("registration.html")


@app.route('/register', methods=["POST"])
def registration_process():
    """Allow user to make an account login."""

    reg_email = request.form.get('email')
    reg_password = request.form.get('password')

    is_valid = User.query.filter(User.email == reg_email).first()
    # queries user table for any record with that email; returns None if no record

    if not is_valid:
        # already there, so they can't register, so try another email or recover password
        # some type of flash message
        print "idiot"
    else:
        user = User(email=reg_email, password=reg_password)
        db.session.add(user)
        db.session.commit()

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
