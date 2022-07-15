from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.init_app(app)
    db.app = app



class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    passwd = db.relationship('Password', backref='users', passive_deletes=True)

    vulnpassword = db.relationship('VulnPassword', backref='users', passive_deletes=True)

    vulnemail = db.relationship('VulnEmail', backref='users', passive_deletes=True)

    @classmethod
    def register(cls, username, first_name, last_name, email):

        return cls(username=username, first_name=first_name, last_name=last_name, email=email)


class Password(db.Model):

    __tablename__ = 'passwords'

    id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, userId, password):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(id=userId, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        passwd = user.passwd[0].password
        
        if user and bcrypt.check_password_hash(passwd, password):
            return user
        else:
            return False

    @classmethod
    def new_password(cls, password):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return hashed_utf8


class VulnEmail(db.Model):

    __tablename__ = 'vulnemails'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False)
    breached = db.Column(db.Text, nullable=False, default='pending')
    userId = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)

    vulnemailinfo = db.relationship('VulnEmailInfo', backref='vulnemails', passive_deletes=True)


class VulnEmailInfo(db.Model):

    __tablename__ = 'vulnemailinfos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vulnEmailId = db.Column(db.Integer, db.ForeignKey('vulnemails.id', ondelete='cascade'), nullable=False)
    vulnInfo = db.Column(db.Text, nullable=False, default='Not Found')

class VulnPassword(db.Model):
    
    __tablename__ = 'vulnpasswords'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.Text, nullable=False)
    vulnerable = db.Column(db.Text, nullable=False, default="pending")
    userId = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
