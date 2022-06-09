import base64
from crypt import methods
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Sychrldi227@localhost:5432/ecourse'

user_course = db.Table('user_course',
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
	category = db.relationship('Course', backref='category', lazy='dynamic')

	def __repr__(self):
		return f'<Category "{self.name}">'

class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	public_id = db.Column(db.String, nullable=False)
	name_course = db.Column(db.String(100))
	desc = db.Column(db.Text)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
	instructors_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
	courses_enroll = db.relationship('Enroll', backref='courses_enroll' , lazy=True)

	def __repr__(self):
		return f'<Course "{self.name}">'

class Enroll(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	public_id = db.Column(db.String, nullable=False)
	date_enroll = db.Column(db.Date)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	is_complete = db.Column(db.Boolean, nullable=False)
	# users = db.relationship('User', backref='users')

	def __repr__(self):
		return f'<Enroll "{self.is_complete}">'

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, index=True)
	public_id = db.Column(db.String, nullable=False)
	name = db.Column(db.String(30), nullable=False)
	username = db.Column(db.String(10), nullable=False, unique=True)
	password = db.Column(db.String(10), nullable=False,unique=True)
	is_admin = db.Column(db.Boolean, default=False)
	user_enroll = db.relationship('Enroll', backref='user_enroll')

	def repr(self):
		return f'User <{self.username}>'


# db.create_all()
# db.session.commit()

@app.route('/auth')
def author_user(auth):
	decode_var = request.headers.get('Authorization')
	c = base64.b64decode(auth[6:])
	e = c.decode("ascii")
	lis = e.split(':')
	username = lis[0]
	passw = lis [1]
	user = User.query.filter_by(username=username).filter_by(password=passw).first()
	# pas = User.query.filter_by(password=passw).first()

	# return [username, passw]
	if not user:
		return 'Please check login detail'
	elif user:
		return [username, passw]
	
	# if not user:
	# 	return 'Please check your login details and try again.'
	# elif not user.is_admin :
	# 	return False
	# elif user.is_admin is True:
	# 	return True

#------------------------------USERS

@app.route('/users/')
def get_users():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	# return str(user)
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user:
		# return "auth"
		return jsonify([
			{
				'id': user.public_id, 'name': user.name, 'username': user.username, 'is admin': user.is_admin
			} for user in User.query.all()
		]), 200

@app.route('/users/<id>/')
def get_user(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user:
		print(id)
		user = User.query.filter_by(public_id=id).first_or_404()
		return {
			'id': user.public_id, 'name': user.name, 'username': user.username, 'is admin': user.is_admin
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
			is_admin=data.get('is admin', False),
			public_id=str(uuid.uuid4())
		)
	db.session.add(user)
	db.session.commit()
	return {
		'id': user.public_id, 'name': user.name, 'username': user.username, 'is admin': user.is_admin
	}, 201

@app.route('/users/<id>/', methods=['PUT'])
def update_user(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user:
		data = request.get_json()
		if 'name' not in data:
			return {
				'error': 'Bad Request',
				'message': 'Name field needs to be present'
			}, 400
		user = User.query.filter_by(public_id=id).filter_by(username=allow).first_or_404()
		if not user:
			return {'message' : 'Please check login detail!'}
		user.name=data['name']
		user.username=data['username']
		user.password=data['password']
		if 'name' in data:
			user.name=data['name']
		if 'username' in data:
			user.username=data['username']
		if 'password' in data:
			user.password=data['password']
		db.session.commit()
		return jsonify({
			'id': user.public_id, 'name': user.name, 'username': user.username, 'password': user.password,
		}),200

#--------------------------------------- INSTRUCTORS

@app.route('/instructors/')
def get_instructors():
	decode_var = request.headers.get('Authorization')
	username = author_user(decode_var)[0]
	user = User.query.filter_by(username=username).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user:
		return jsonify([
			{
				'id': ins.public_id, 'name': ins.name_instructors
				} for ins in Instructors.query.all()
		])


@app.route('/instructors/<id>/')
def get_instructors_id(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user:
		print(id)
		ins = Instructors.query.filter_by(public_id=id).first_or_404()
		return {
			'id': ins.public_id, 'name': ins.name_instructors, 
		}, 201

@app.route('/instructors/', methods=['POST'])
def create_instructors():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user.is_admin is True:
		data = request.get_json()
		if not 'name_instructors' in data :
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name or username or password not given'
			}), 400
		if len(data['name_instructors']) < 4 :
			return jsonify({
				'error': 'Bad Request',
				'message': 'Name must be contain minimum of 4 letters'
			}), 400
		ins = Instructors(
				name_instructors=data['name_instructors'],
				public_id=str(uuid.uuid4())
			)
		db.session.add(ins)
		db.session.commit()
		return {
			'id': ins.public_id, 'name': ins.name_instructors
		}, 201
	elif user.is_admin is False:
		return {'message' : 'Your not admin'}

#-------------------------------- CATEGORY

@app.route('/category/')
def get_category():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user:
		return jsonify([
			{
				'id': category.public_id, 
				'name': category.name_category, 
				'desc': category.desc,
			} for category in Category.query.all()
		]),200

@app.route('/category/<id>/')
def get_category_id(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user:
		print(id)
		category = Category.query.filter_by(public_id=id).first_or_404()
		return {
			'id': category.public_id, 'name': category.name_category, 
			'desc': category.desc
		}, 201

@app.route('/category/', methods=['POST'])
def create_category():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user.is_admin is True:
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
				name_category=data['name_category'], 
				desc=data['desc'],
				public_id=str(uuid.uuid4())
			)
		db.session.add(c)
		db.session.commit()
		return {
			'id': c.public_id, 'name': c.name_category, 
			'desc': c.desc 
		}, 201
	elif user.is_admin is False:
		return {
			'message' : 'Your not admin!'
			}


#------------------------------COURSE

@app.route('/course/')
def get_course():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user:
		return jsonify([
			{
				'id': course.public_id, 
				'name': course.name_course, 
				'desc': course.desc,
				'category' : course.category.name_category,
				'instructors' : course.instructors.name_instructors
				# 'category' : {
				# 	'id' : course.category.public_id,
				# 	'name' : course.category.name_category,
				# 	'desc' : course.category.desc
				# },
				# 'instructors' : {
				# 	'id' : course.instructors.public_id,
				# 	'name' : course.instructors.name_instructors
			# }
			} for course in Course.query.all()
		]),200


@app.route('/course/<id>/')
def get_course_id(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user:
		print(id)
		course = Course.query.filter_by(public_id=id).first_or_404()
		return {
			'id': course.public_id, 
			'name': course.name_course, 
			'desc': course.desc,
		}, 201

@app.route('/course/', methods=['POST'])
def create_course():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user.is_admin is True :
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

	elif user.is_admin is False:
		return {
			'message' : 'Your not admin'
		}

@app.route('/course/<id>',  methods=['PUT'])
def update_course(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user.is_admin is True :
		data = request.get_json()
		course = Course.query.filter_by(public_id=id).first_or_404()
		cat = Category.query.filter_by(name_category=data['name_category']).first_or_404()
		course.name_course = data['name_course']
		course.category_id = cat.id
		db.session.commit()
		return {
			'message': 'success'
		}
	elif user.is_admin is False:
		return {
			'message' : 'Your not admin! please check again.'
		},401
	else:
		return {
			'message' : 'UNAUTOHORIZED'
		},401

#------------------------------------ENROLL

@app.route('/enroll/')
def get_enroll():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user:
		return jsonify([
			{
				'id': enroll.public_id, 
				'date enroll': enroll.date_enroll, 
				'name course': enroll.courses_enroll.name_course,
				'is complete' : enroll.is_complete
			} for enroll in Enroll.query.all()
		]),200

@app.route('/enroll/', methods=['POST'])
def user_enroll():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401
	elif user.is_admin is False:
		data = request.get_json()
		user = User.query.filter_by(username=data['username']).first()
		if not user:
			return jsonify({
				'error': 'Bad Request',
				'message': 'User not exits'
			}), 400
		enroll = Enroll.query.filter_by(user_id=user.id).filter_by(is_complete=False).count()
		if enroll == 3:
			return {
				'message' : 'your not complete 3 courses'
			}
		course = Course.query.filter_by(name_course=data['name_course']).first()
		if not course:
			return {
				'error': 'Bad request',
				'message': 'Invalid Course'
			}
		nroll = Enroll(
				date_enroll=data['date_enroll'],
				course_id=course.id,
				user_id = user.id,
				is_complete = data.get('is complete', False),
				public_id=str(uuid.uuid4())
			)
		db.session.add(nroll)
		db.session.commit()
		return {
			'id': nroll.public_id, 
			'date_enroll' : nroll.date_enroll,
			'course_id' : nroll.user_id, 
			'user_id' : nroll.user_id,
			'is_complete' : nroll.is_complete, 
		}, 201
	else:
		return {
			'message' : 'UNAUTOHORIZED'
		},401

@app.route('/enroll/<id>',  methods=['PUT'])
def update_enroll(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401

	elif user:
		enroll = Enroll.query.filter_by(course_id=id).filter_by(user_id=user.id).first_or_404()
		if enroll.is_complete == True:
			return {'message' : 'Enroll is complete'}
		elif enroll.is_complete == False:
			enroll.is_complete = True
			db.session.commit()
			return {
				'message': 'success'
			}
	else:
		return {
			'message' : 'UNAUTOHORIZED'
		},401

@app.route('/enroll/<id>/', methods=['DELETE'] )
def delete_author(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)[0]
	user = User.query.filter_by(username=allow).first()
	if not user:
		return {
			'message' : 'Please check your login details and try again.'
		}, 401

	elif user:
		enroll = Enroll.query.filter_by(public_id=id).filter_by(user_id=user.id).first_or_404()
		db.session.delete(enroll)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		}
