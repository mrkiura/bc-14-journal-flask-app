from flask import render_template, flash
from flask_login import (current_user, logout_user)
from functools import wraps
from flask import g, request, redirect, url_for
from app import SignUpForm, LoginForm
from .models import User
from app import app, session,lm

current_user_id = -1

@lm.user_loader
def user_loader(user_id):
    return session.query(User).get(user_id)

@app.before_request
def before_request():
    g.user = current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

'''Home page is basically the signup page. This is code implementation for signup'''
@app.route("/")
def index():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.firstname.data, form.lastname.data, form.username.data, form.email.data,
                    form.password.data)
        session.add(user)
        session.commit()
        flash('Welcome to The Journal App, Create you first Journal')
        return redirect(url_for('login'))
    else:
        flash_errors(form)
    return render_template('signup.html', form=form)
    return render_template('signup.html')

'''Flashing form errors'''
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


'''Authenticate users, then log them in, or redirect to sign up page'''
@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        if form.email.data == form.email.data:
            return redirect(url_for('viewentries'))
    else:
        flash_errors(form)
        print("If you have no account, sign up")
    return render_template('login.html', form=form)

'''Implementation for logging users out'''
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return render_template("index.html")


'''Register a new user, add his info to database'''
@app.route("/signup", methods=['POST', 'GET'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.firstname.data, form.lastname.data, form.username.data, form.email.data,
                    form.password.data)
        session.add(user)
        session.commit()
        flash('Welcome to The Journal App, Create you first Journal')
        return redirect(url_for('login'))
    else:
        flash_errors(form)
    return render_template('signup.html', form=form)
