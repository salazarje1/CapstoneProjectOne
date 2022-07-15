from models import db, connect_db, User, Password, VulnPassword
from app import app


# Create all tables
db.drop_all()
db.create_all()