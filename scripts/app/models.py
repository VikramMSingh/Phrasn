from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import *


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    name = db.Column(db.String(100))
    language = db.Column(db.String(48))
    standard = db.Column(db.String(5))
    questions = db.relationship('ChatHistory', backref='user', lazy=True)
    token_usage = db.relationship('UserTokenUsage', backref='user', lazy='dynamic')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subname = db.Column(db.String(100), nullable=False)
    standard = db.Column(db.String(5), nullable=False)


class UserTokenUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, default=datetime.utcnow().date)
    tokens_used = db.Column(db.Integer, default=0)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
