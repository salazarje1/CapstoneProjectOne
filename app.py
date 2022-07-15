from flask import Flask, render_template, redirect, session, flash, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests
from hashlib import sha1
from models import db, connect_db, User, Password, VulnPassword, VulnEmail
from forms import RegisterForm, LoginForm, EditForm, ChangePassword, HomePageEmailCheck
from secrets import API_KEY, SECRET_KEY


app = Flask(__name__, static_url_path='/static')

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "ABC123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = SECRET_KEY

connect_db(app)

toolbar = DebugToolbarExtension(app)




@app.route('/')
def home_page():
    if 'user_id' in session: 
        username = session['user_id']
        return redirect(f'/users/{username}')

    form = HomePageEmailCheck()
    return render_template('index.html', form=form)

@app.route('/simple-check/<email>')
def home_email_check(email):
    resp = requests.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
        headers={
            'hibp-api-key': API_KEY
        }
    )

    if resp.status_code == 200: 
        data = resp.json()

        return jsonify(data)
    elif resp.status_code == 404:

        return jsonify('not breached'), 204

    


@app.route('/register', methods=["GET", "POST"])
def user_register():
    if 'user_id' in session: 
        return redirect('/')

    form = RegisterForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        new_user = User.register(username, first_name, last_name, email)
        db.session.add(new_user)
        db.session.commit()

        password = Password.register(new_user.id, password)
        db.session.add(password)
        db.session.commit()

        session['user_id'] = new_user.username

        flash('Welcome! Successfully created your account')
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def user_login(): 
    if 'user_id' in session: 
        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Password.authenticate(username, password)
        if user: 
            flash(f"Welcome back, {user.first_name}!")
            session['user_id'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = {'Invalid username/password.'}

    return render_template('login.html', form=form)

@app.route('/logout', methods=["POST"])
def user_logout():
    session.pop('user_id')
    flash('Succefully logged out.')
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
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data

            db.session.commit()
            return redirect(f'/users/{user.username}/account')

        return render_template('user_edit.html', user=user, form=form)
    
    return redirect('/')

@app.route('/users/<username>/change', methods=["GET", "POST"])
def user_change_password(username):
    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/login')

    user = User.query.filter_by(username=username).first_or_404()
    if user.username == session['user_id']:
        form = ChangePassword()

        if form.validate_on_submit():
            old_password = form.old_password.data
            new_password = form.password.data

            user = Password.authenticate(user.username, old_password)
            if user: 
                user.passwd[0].password = Password.new_password(new_password)
                db.session.commit()

                flash('Successfully changed your password.')
                return redirect(f"/users/{user.username}/account")
            else: 
                form.old_password.errors = ['Invalid password/passwords dont match']

        return render_template('user_change_password.html', user=user, form=form)

    return redirect('/')

@app.route('/users/<username>/delete', methods=["POST"])
def user_delete(username):
    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/')

    user = User.query.filter_by(username=username).first_or_404()
    if user.username == session['user_id']:
        db.session.delete(user)
        db.session.commit()
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
            id = user.id
            email = request.form['email']

            new_email = VulnEmail(userId=id, email=email)
            db.session.add(new_email)
            db.session.commit()

            return redirect(f'/users/{user.username}')
        
    return redirect('/')


@app.route('/emails/<int:id>/delete', methods=["POST"])
def delete_emails(id):
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect('/login')

    email = VulnEmail.query.get_or_404(id)
    if email.users.username == session['user_id']:
        db.session.delete(email)
        db.session.commit()

        return redirect(f'/users/{email.users.username}')

    return redirect('/')


@app.route('/emails/<int:id>/check', methods=["GET", "POST"])
def check_email(id):
    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/login')

    email = VulnEmail.query.get_or_404(id)

    resp = requests.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{email.email}', 
        params={
            'truncateResponse':'false'
        },
        headers={
            'hibp-api-key':API_KEY
        }
    )

    if resp.status_code == 200: 
        data = resp.json()
        email.breached = True
        db.session.commit()

        return jsonify(data)
    elif resp.status_code == 404:
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
            id = user.id
            password = request.form['password']

            new_password = VulnPassword(userId=id, password=password)
            db.session.add(new_password)
            db.session.commit()

            return redirect(f'/users/{user.username}/passwords')

    return render_template('password_check.html', user=user)

@app.route('/passwords/<int:id>/delete', methods=["POST"])
def delete_passwords(id):
    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/login')

    password = VulnPassword.query.get_or_404(id)
    if password.users.username == session['user_id']:
        db.session.delete(password)
        db.session.commit()

        return redirect(f'/users/{password.users.username}/passwords')

    return redirect('/')


@app.route('/passwords/<int:id>/check', methods=["GET", "POST"])
def check_passwords(id):

    if 'user_id' not in session: 
        flash('Please login first.')
        return redirect('/login')

    password = VulnPassword.query.get_or_404(id)
    passwd = password.password.encode()
    hashed_pass_obj = sha1(passwd)
    hashed_pass = hashed_pass_obj.hexdigest()

    first_part = hashed_pass[:5]
    second_part = hashed_pass[5:].upper()

    resp = requests.get(f'https://api.pwnedpasswords.com/range/{first_part}')

    data = resp.text
    data = data.splitlines()

    for d in data: 
        [hash, count] = d.split(':')
        if str(second_part) == hash: 
            password.vulnerable = True
            db.session.commit()
            return jsonify(data=count)


    print('===================')
    print('Checked safe')
    password.vulnerable = False
    db.session.commit()
    return jsonify('safe'), 204




