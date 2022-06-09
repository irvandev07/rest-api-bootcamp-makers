import base64
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Sychrldi227@localhost:5432/db_course'

user_course = db.Table('user_course',
	db.Column('category_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
	db.Column('instructors_id', db.Integer, db.ForeignKey('instructors.id'), primary_key=True)
)

class Instructors(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	public_id = db.Column(db.String, nullable=False)
	name_instructors = db.Column(db.String(100))
	instructors = db.relationship('Course', backref='instructors', secondary='user_course')

	def __repr__(self):
		return f'<Instructors "{self.name_instructors}">'


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	public_id = db.Column(db.String, nullable=False)
	name_category = db.Column(db.String(100))
	desc = db.Column(db.Text)
	category = db.relationship('Course', backref='category', lazy='dynamic' )

	def __repr__(self):
		return f'<Category "{self.name_category}">'


class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	public_id = db.Column(db.String, nullable=False)
	name_course = db.Column(db.String(100))
	desc = db.Column(db.Text)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
	instructors_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
	instructors_course = db.relationship('Author', backref='book', secondary='user_course')

	def __repr__(self):
		return f'<Book "{self.title}">'

class Enroll(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	public_id = db.Column(db.String, nullable=False)
	date_enroll = db.Column(db.Date)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	is_complete = db.Column(db.Boolean, nullable=False)
	enroll = db.relationship('Course', backref='enroll', lazy=True)
	users = db.relationship('User', backref='users', lazy=True, uselist=False)

	def repr(self):
		return f'Enroll <{self.is_complete}>'

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	public_id = db.Column(db.String, nullable=False)
	name = db.Column(db.String(30), nullable=False)
	username = db.Column(db.String(10), nullable=False, unique=True)
	password = db.Column(db.String(10), nullable=False,unique=True)
	is_admin = db.Column(db.Boolean, default=False)
	# rents = db.relationship('Rent', backref='users', lazy=True)

	def repr(self):
		return f'User <{self.username}>'


db.create_all()
db.session.commit()