
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(100), nullable=False)
    dept_id = db.Column(db.String(50), unique=True)
    hod_name = db.Column(db.String(100), unique=True)
    tech_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    tech_phno = db.Column(db.String(20), nullable=False)
    hod_phno = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    faculty = db.relationship("Faculty", backref="department", lazy=True)
    signatures = db.relationship("Signature", backref="department", lazy=True)

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty_name = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    dept_id = db.Column(
        db.Integer,
        db.ForeignKey("department.id"),
        nullable=False
    )

class Signature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(200), nullable=False)
    dept_id = db.Column(
        db.Integer,
        db.ForeignKey("department.id"),
        nullable=False
    )
