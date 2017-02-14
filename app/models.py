from app import db
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import datetime

engine = create_engine('sqlite:///journal.db', echo = True) # create a database when called
Base = declarative_base() # Create only one instance of the base

'''Code to create users table in the database'''
class User(UserMixin, Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    '''
    Instantiate every new Instance
    '''
    def __init__(self, firstname, lastname, username, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.username

    '''Password Hashing'''
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

'''Table to store all created journals'''
class Journal(Base):
    __tablename__ = 'journal'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime)
    body = db.Column(db.String(1500), nullable=False)
    tags = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    jour = db.relationship('User')


    def __init__(self, body, tags, user_id):
        self.body = body
        self.tags = tags
        self.user_id = user_id


    def __repr__(self):
        return '<Journal %r>' % self.body

Base.metadata.create_all(engine)
