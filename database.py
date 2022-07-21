from models import db, User, Password, VulnEmail, VulnPassword

def register_user(first, last, username, email, password):
        first_name = first
        last_name = last
        username = username
        email = email
        password = password

        new_user = User.register(username, first_name, last_name, email)
        db.session.add(new_user)
        db.session.commit()

        password = Password.register(new_user.id, password)
        db.session.add(password)
        db.session.commit()

        return new_user

def update_user(user, first, last, email):
        user.first_name = first
        user.last_name = last
        user.email = email

        db.session.commit()

def update_password(user, old, new):
        old_password = old
        new_password = new

        user = Password.authenticate(user.username, old_password)
        if user: 
                user.passwd[0].password = Password.new_password(new_password)
                db.session.commit()
                return True
        else: 
                return False

def deleting(resource):
        db.session.delete(resource)
        db.session.commit()


# Emails and Passwords
def adding_resource(user, resource, resource_id):
        id = user.id

        if resource_id == 'email':
                new_resource = VulnEmail(userId=id, email=resource)
        elif resource_id == 'password':
                new_resource = VulnPassword(userId=id, password=resource)

        db.session.add(new_resource)
        db.session.commit()

