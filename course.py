import base64
from unicodedata import category
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Sychrldi227@localhost:5432/ecourse'

enroll = db.Table('enroll',
	db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Instructors(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	public_id = db.Column(db.String, nullable=False)
	name_instructors = db.Column(db.String(100))
	instructors = db.relationship('Course', backref='instructors')

	def __repr__(self):
		return f'<Instructors "{self.name}">'


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	public_id = db.Column(db.String, nullable=False)
	name_category = db.Column(db.String(100))
	desc = db.Column(db.Text)
	# categories = db.relationship('Course', backref='categories')

	def __repr__(self):
		return f'<Category "{self.name}">'


class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	public_id = db.Column(db.String, nullable=False)
	name_course = db.Column(db.String(100))
	desc = db.Column(db.Text)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
	instructors_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
	# courseuser = db.relationship('User', backref='courseuser')

	def __repr__(self):
		return f'<Course "{self.name}">'


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	public_id = db.Column(db.String, nullable=False)
	name = db.Column(db.String(30), nullable=False)
	username = db.Column(db.String(10), nullable=False, unique=True)
	password = db.Column(db.String(10), nullable=False,unique=True)
	# users = db.relationship('Course', backref='users')

	def repr(self):
		return f'User <{self.username}>'


# db.create_all()
# db.session.commit()

#------------------------------USERS

@app.route('/users/')
def get_users():
	return jsonify([
		{
			'id': user.public_id, 'name': user.name, 'username': user.username
			} for user in User.query.all()
	])

@app.route('/users/<id>/')
def get_user(id):
	print(id)
	user = User.query.filter_by(public_id=id).first_or_404()
	return {
		'id': user.public_id, 'name': user.name, 'username': user.username
		}

@app.route('/users/', methods=['POST'])
def create_user():
	data = request.get_json()
	if not 'name' in data or not 'username' in data or not 'password' in data:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Name or username or password not given'
		}), 400
	if len(data['username']) < 4 or len(data['password']) < 6:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Username must be contain minimum of 4 letters and Password must be contain minimum of 6 letters'
		}), 400
	user = User(
			name=data['name'], 
			username=data['username'],
			password=data['password'],
			public_id=str(uuid.uuid4())
		)
	db.session.add(user)
	db.session.commit()
	return {
		'id': user.public_id, 'name': user.name, 'username': user.username
	}, 201

@app.route('/users/<id>/', methods=['PUT'])
def update_user(id):
	data = request.get_json()
	if 'name' not in data:
		return {
			'error': 'Bad Request',
			'message': 'Name field needs to be present'
		}, 400
	user = User.query.filter_by(public_id=id).first_or_404()
	user.name=data['name']
	if 'name' in data:
		user.name=data['name']
	db.session.commit()
	return jsonify({
		'id': user.public_id, 'name': user.name,
	}),200

#--------------------------------------- INSTRUCTORS
@app.route('/instructors/')
def get_instructors():
	return jsonify([
		{
			'id': ins.public_id, 'name': ins.name
			} for ins in Instructors.query.all()
	])

@app.route('/instructors/<id>/')
def get_instructors_id(id):
		print(id)
		ins = Instructors.query.filter_by(public_id=id).first_or_404()
		return {
			'id': ins.public_id, 'name': ins.name, 
		}, 201

@app.route('/instructors/', methods=['POST'])
def create_instructors():
	data = request.get_json()
	if not 'name' in data :
		return jsonify({
			'error': 'Bad Request',
			'message': 'Name or username or password not given'
		}), 400
	if len(data['name']) < 4 :
		return jsonify({
			'error': 'Bad Request',
			'message': 'Name must be contain minimum of 4 letters'
		}), 400
	ins = Instructors(
			name=data['name'],
			public_id=str(uuid.uuid4())
		)
	db.session.add(ins)
	db.session.commit()
	return {
		'id': ins.public_id, 'name': ins.name
	}, 201

#-------------------------------- CATEGORY

@app.route('/category/')
def get_category():
		return jsonify([
			{
				'id': category.public_id, 
				'name': category.name, 
				'desc': category.desc,
			} for category in Category.query.all()
		]),200

@app.route('/category/<id>/')
def get_category_id(id):
		print(id)
		category = Category.query.filter_by(public_id=id).first_or_404()
		return {
			'id': category.public_id, 'name': category.name, 
			'desc': category.desc
		}, 201

@app.route('/category/', methods=['POST'])
def create_category():
		data = request.get_json()
		if not 'name' in data:
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name not given'
			}), 400
		if len(data['name']) < 4 :
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name must be contain minimum of 4 letters'
			}), 400
		c = Category(
				name=data['name'], 
				desc=data['desc'],
				public_id=str(uuid.uuid4())
			)
		db.session.add(c)
		db.session.commit()
		return {
			'id': c.public_id, 'name': c.name, 
			'desc': c.desc 
		}, 201


#------------------------------COURSE

@app.route('/course/')
def get_course():
		return jsonify([
			{
				'id': category.public_id, 
				'name': category.name, 
				'desc': category.desc,
			} for category in Course.query.all()
		]),200

@app.route('/course/<id>/')
def get_course_id(id):
		print(id)
		category = Category.query.filter_by(public_id=id).first_or_404()
		return {
			'id': category.public_id, 'name': category.name, 
			'desc': category.desc
		}, 201

@app.route('/course/', methods=['POST'])
def create_course():
		data = request.get_json()
		if not 'name_course' in data:
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name Course not given'
			}), 400
		if len(data['name_course']) < 4 :
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name Course must be contain minimum of 4 letters'
			}), 400

		category = Category.query.filter_by(name_category=data['name_category']).first()
		if not category:
			return {
				'error': 'Bad request',
				'message': 'Invalid Name Category'
			}
		ins = Instructors.query.filter_by(name_instructors=data['name_instructors']).first()
		if not ins:
			return {
				'error': 'Bad request',
				'message': 'Invalid Name Instructors'
			}
		cou = Course(
				name_course=data['name_course'], 
				desc=data['desc'],
				category_id=category.id,
				instructors_id = ins.id,
				public_id=str(uuid.uuid4())
			)
		db.session.add(cou)
		db.session.commit()
		return {
			'id': cou.public_id, 
			'name_course': cou.name_course, 
			'instructors_id' : cou.instructors_id, 
			'category_id' : cou.category_id, 
			'desc': cou.desc 
		}, 201
