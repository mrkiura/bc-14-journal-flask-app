from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.forms import SignUpForm, LoginForm, EditForm
from app.forms import JournalForm, SearchForm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_object('config')

'''Code to initialize the database'''
db = SQLAlchemy(app) # Initiliazation of database
CsrfProtect(app)

'''Code to create a database'''
engine = create_engine('sqlite:///journal.db', echo = True)
Session = sessionmaker(bind=engine)
session = Session()

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

from app import views, models
