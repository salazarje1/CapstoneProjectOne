from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])
    username = StringField('Username', validators=[InputRequired(), Length(max=100)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords do not match.')])
    confirm = PasswordField('Repeat Password', validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class EditForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])
    email = StringField('Email', validators=[InputRequired(), Email()])

class ChangePassword(FlaskForm):
    old_password = PasswordField('Old Password', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords do not match.')])
    confirm = PasswordField('Repeat Password', validators=[InputRequired()])

class HomePageEmailCheck(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])