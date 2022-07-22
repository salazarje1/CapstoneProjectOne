import os
import re
import psycopg2
from flask import Flask, render_template, redirect, session, flash, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Password, VulnPassword, VulnEmail
from forms import RegisterForm, LoginForm, EditForm, ChangePassword, HomePageEmailCheck
from api import simple_check, email_check, password_check
from database import register_user, update_user, update_password, deleting, adding_resource
from helper import password_setup


app = Flask(__name__, static_url_path='/static')


uri = os.environ.get('DATABASE_URL', "postgresql:///capstone_db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "ABC123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'ThisIsASecret')

API_KEY = os.environ.get('API_KEY')

connect_db(app)

toolbar = DebugToolbarExtension(app)

# Add http methods 

@app.route('/')
def home_page():
    if 'user_id' in session: 
        username = session['user_id']
        return redirect(f'/users/{username}')

    form = HomePageEmailCheck()
    return render_template('index.html', form=form)

@app.route('/simple-check/<email>')
def home_email_check(email):
    resp = simple_check(email)

    if resp.status_code == 200: 
        data = resp.json()
        return jsonify(data)

    elif resp.status_code == 404:
        return jsonify('not breached'), 204

    

# Register Routes
@app.route('/register', methods=["GET", "POST"])
def user_register():
    if 'user_id' in session: 
        return redirect('/')

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            new_user = register_user(
                form.first_name.data,
                form.last_name.data,
                form.username.data,
                form.email.data,
                form.password.data
            )

            session['user_id'] = new_user.username

            flash('Welcome! Successfully created your account')
            return redirect(f'/users/{new_user.username}')
        except:
            db.session.rollback()
            flash('Username in use. Please try a different one.')

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def user_login(): 
    if 'user_id' in session: 
        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user: 
            user = Password.authenticate(username, password)
            if user: 
                flash(f"Welcome back, {user.first_name}!")
                session['user_id'] = user.username
                return redirect(f'/users/{username}')
            else:
                form.username.errors = {'Invalid username/password.'}
        else:
            form.username.errors = {'Invalid username/password.'}

    return render_template('login.html', form=form)

@app.route('/logout', methods=["POST"])
def user_logout():
    session.pop('user_id')
    flash('Successfully logged out.')
    return redirect('/')



# User Routes

@app.route('/users/<username>')
def user_main(username):

    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/login')
    
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user_main.html', user=user)

@app.route('/users/<username>/account')
def user_account(username):

    if 'user_id' not in session:
        flash('Please login first.')
        return redirect('/login')

    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user_account.html', user=user)

@app.route('/users/<username>/edit', methods=["GET", "POST"])
def user_edit(username):
    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/login')

    user = User.query.filter_by(username=username).first_or_404()
    if user.username == session['user_id']:
        form = EditForm(obj=user)

        if form.validate_on_submit():
            update_user(
                user,
                form.first_name.data,
                form.last_name.data,
                form.email.data
            )
            return redirect(f'/users/{user.username}/account')

        return render_template('user_edit.html', user=user, form=form)
    
    return redirect('/login')

@app.route('/users/<username>/change', methods=["GET", "POST"])
def user_change_password(username):
    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/login')

    user = User.query.filter_by(username=username).first_or_404()
    if user.username == session['user_id']:
        form = ChangePassword()

        if form.validate_on_submit():
            update_status = update_password(
                user, 
                form.old_password.data,
                form.password.data
            )
            if update_status: 
                flash('Successfully changed your password.')
                return redirect(f"/users/{user.username}/account")
            else: 
                form.old_password.errors = ['Invalid password/passwords do not match']

        return render_template('user_change_password.html', user=user, form=form)

    return redirect('/')

@app.route('/users/<username>/delete', methods=["POST"])
def user_delete(username):
    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/')

    user = User.query.filter_by(username=username).first_or_404()
    if user.username == session['user_id']:
        deleting(user)
        session.pop('user_id')
        flash('Successfully delete account.')
        return redirect('/')
    else: 
        return redirect('/')



# Emails 
@app.route('/users/<username>/emails', methods=["GET", "POST"])
def adding_emails(username):
    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/')

    user = User.query.filter_by(username=username).first_or_404()

    if request.method == 'POST': 
        if user.username == session['user_id']:
            email = request.form['email']
            adding_resource(user, email, 'email')

            return redirect(f'/users/{user.username}')
        
    return redirect('/')


@app.route('/emails/<int:id>/delete', methods=["POST"])
def delete_emails(id):
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect('/login')

    email = VulnEmail.query.get_or_404(id)
    if email.users.username == session['user_id']:
        deleting(email)
        return redirect(f'/users/{email.users.username}')

    return redirect('/')


@app.route('/emails/<int:id>/check', methods=["GET", "POST"])
def check_email(id):
    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/login')

    email = VulnEmail.query.get_or_404(id)

    [data, status_code] = email_check(email.email)

    if status_code == 200:
        email.breached = True
        db.session.commit()

        return jsonify(data)
    elif status_code == 404:
        email.breached = False
        db.session.commit()

        return jsonify('not breached'), 204



# Passwords

@app.route('/users/<username>/passwords', methods=["GET", "POST"])
def adding_passwords(username):
    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/')

    user = User.query.filter_by(username=username).first_or_404()

    if request.method =='POST':
        if user.username == session['user_id']:
            password = request.form['password']
            adding_resource(user, password, 'password')

            return redirect(f'/users/{user.username}/passwords')

    return render_template('password_check.html', user=user)

@app.route('/passwords/<int:id>/delete', methods=["POST"])
def delete_passwords(id):
    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/login')

    password = VulnPassword.query.get_or_404(id)
    if password.users.username == session['user_id']:
        deleting(password)
        return redirect(f'/users/{password.users.username}/passwords')

    return redirect('/')


@app.route('/passwords/<int:id>/check', methods=["GET", "POST"])
def check_passwords(id):

    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/login')

    password = VulnPassword.query.get_or_404(id)
    [first_part, second_part] = password_setup(password)

    data = password_check(first_part, second_part)

    if data:
        password.vulnerable = True
        db.session.commit()
        return jsonify(data=data)
    
    else: 
        password.vulnerable = False
        db.session.commit()
        return jsonify('safe'), 204




