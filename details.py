
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# database table
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    dept = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phno2 = db.Column(db.String(15), nullable=False)
    phno1 = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(200), nullable=False)

