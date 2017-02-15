from flask import render_template, flash
from flask_login import (current_user, logout_user)
from functools import wraps
from flask import g, request, redirect, url_for
from app import SignUpForm, LoginForm, JournalForm, EditForm, SearchForm
from .models import User, Journal
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

'''View all journal entries code'''
@app.route("/viewentries/<id>", methods=['GET'])
@app.route("/viewentries/", methods=['GET'])
@login_required
def viewentries(id=None):
    if id is not None:
        entry_rows = session.query(Journal).filter(Journal.id==id)
    else:
        entry_rows = session.query(Journal).filter_by(user_id=current_user_id)
    entries = []
    for entry in entry_rows:
        entries.append({
            "id": entry.id,
            "body": entry.body,
            "tags": entry.tags
        })
    return render_template('viewentries.html', entries=entries)

'''Code to add a new journal entry to database'''
@app.route("/newjournal", methods=['POST', 'GET'])
@login_required
def newjournal():
    form = JournalForm(request.form)
    if request.method == 'POST' and form.validate():
        new = Journal(form.body.data, form.tags.data, current_user_id)
        print ("User id: "+ str(current_user_id))
        session.add(new)
        session.commit()
        flash('Your Journal has been Created')
        return redirect("/viewentries")
    else:
        flash_errors(form)
    return render_template('newjournal.html', form = form)

@app.route('/search/', methods=['GET'])
@login_required
def search():
    form = SearchForm(request.form)
    return render_template('search.html', form = form)

@app.route('/edit')
@login_required
def edit():
    form = EditForm(request.form)
    return render_template('edit.html', form = form)

