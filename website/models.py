from sqlalchemy.types import BOOLEAN, Boolean
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150),unique=True)
    author = db.Column(db.String(150))
    realese_date = db.Column(db.DateTime(timezone=True))
    gener = db.Column(db.String(150))
    is_available = db.Column(db.Boolean , default=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean,default=False)
    notes = db.relationship('Book')
