'''
Create the forms that will be used for registration, login in, creating journals,
editing journals and searching for a journal
'''
from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField,Form
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired

'''Login Form'''
class LoginForm(Form):
    email = StringField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(message='Must provide a password.')])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Submit')

'''Signup Form'''
class SignUpForm(Form):
    firstname = StringField('firstname', [validators.Length(min=2, max=20)])
    lastname = StringField('lastname', [validators.Length(min=2, max=20)])
    username = StringField('Username', [validators.Length(min=2, max=25)])
    email = StringField('Email Address', [validators.Length(min=2, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

'''Journal Form'''
class JournalForm(Form):
    body = PageDownField('Body', [validators.Length(min=1, max=1500)])
    tags = StringField('Tags', [validators.Length(min=1, max=20)])

'''Search Form'''
class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField("Submit")

'''Edit Form'''
class EditForm(Form):
    body = PageDownField('Body', [validators.Length(min=1, max=1500)])
    tags = StringField('Tags', [validators.Length(min=1, max=20)])
