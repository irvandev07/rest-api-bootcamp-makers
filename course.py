import base64
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Sychrldi227@localhost:5432/ecourse'


class Instructors(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    public_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String(100))
    # authors = db.relationship('Book', backref='authors', secondary='author_book')

    def __repr__(self):
        return f'<Author "{self.name}">'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    public_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String(100))
    desc = db.Column(db.Text)
    # books = db.relationship('Book', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category "{self.name}">'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    public_id = db.Column(db.String, nullable=False)
    name = db.Column(db.Text)
    desc = db.Column(db.Text)

    def __repr__(self):
        return f'<Book "{self.title}">'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    public_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False,unique=True)

    def repr(self):
        return f'User <{self.username}>'


db.create_all()
db.session.commit()