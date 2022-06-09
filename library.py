import base64
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Sychrldi227@localhost:5432/library' #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://DB_USER:PASSWORD@HOST/DATABASE'


author_book = db.Table('author_book', db.Model.metadata,
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100))
    public_id = db.Column(db.String, nullable=False)
    authors = db.relationship('Book', backref='authors', secondary='author_book')

    def __repr__(self):
        return f'<Author "{self.name}">'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    genre = db.Column(db.String(100))
    desc = db.Column(db.Text)
    public_id = db.Column(db.String, nullable=False)
    books = db.relationship('Book', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category "{self.name}">'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.Text)
    desc = db.Column(db.Text)
    public_id = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    authors_book = db.relationship('Author', backref='book', secondary='author_book')

    def __repr__(self):
        return f'<Book "{self.title}">'

class Rent(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    date_rent = db.Column(db.Date, nullable=False)
    date_return = db.Column(db.Date)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book = db.relationship('Book', backref='rent', lazy=True)
    public_id = db.Column(db.String, nullable=False)
    # users = db.relationship('User', backref='users', lazy=True, uselist=False)

    def repr(self):
        return f'Rent <{self.date_rent}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False,unique=True)
    public_id = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # rents = db.relationship('Rent', backref='users', lazy=True)

    def repr(self):
        return f'User <{self.username}>'


# db.create_all()
# db.session.commit()

@app.route('/')
def home():
	return {
		'message': 'Welcome Library'
	}

#---------------------AUTH
# @app.route('/auth')
def author_user(auth):
	decode_var = request.headers.get('Authorization')
	c = base64.b64decode(auth[6:])
	e = c.decode("ascii")
	lis = e.split(':')
	username = lis[0]
	passw = lis [1]
	user = User.query.filter_by(username=username).filter_by(password=passw).first()
	# pas = User.query.filter_by(password=passw).first()

	if not user:
		return 'Please check your login details and try again.'
	elif not user.is_admin :
		return False
	elif user.is_admin is True:
		return True

def auth_admin(auth):
    # decode_var = request.headers.get('Authorization')
	c = base64.b64decode(auth[6:])
	e = c.decode("ascii")
	lis = e.split(':')
	username = lis[0]
	passw = lis [1]

	return [username, passw]

# #---------------------------------CATEGORY

@app.route('/category/')
def get_category():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow is False or allow is True:
		return jsonify([
			{
				'id': category.public_id, 
				'genre': category.genre, 
				'desc': category.desc,
			} for category in Category.query.all()
		]),200
	elif allow == 'Please check your login details and try again.':
		return allow

@app.route('/category/<id>/')
def get_category_id(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == False or allow == True:
		print(id)
		category = Category.query.filter_by(public_id=id).first_or_404()
		return {
			'success': 'Data load successfully',
			'id': category.public_id, 'genre': category.genre, 
			'desc': category.desc
		}, 201
	elif allow == 'Please check your login details and try again.':
		return allow

@app.route('/category/', methods=['POST'])
def create_category():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True:
		data = request.get_json()
		if not 'genre' in data:
			return jsonify({
				'error': 'Bad Request',
				'message': 'Genre not given'
			}), 400
		if len(data['genre']) < 4 :
			return jsonify({
				'error': 'Bad Request',
				'message': 'Genre must be contain minimum of 4 letters'
			}), 400
		u = Category(
				genre=data['genre'], 
				desc=data['desc'],
				public_id=str(uuid.uuid4())
			)
		db.session.add(u)
		db.session.commit()
		return {
			'success': 'Data added successfully',
			'id': u.public_id, 'genre': u.genre, 
			'desc': u.desc 
		}, 201
	elif allow == False:
		return "Youre not admin! please check and try again."
	elif allow == 'Please check your login details and try again.':
		return allow

@app.route('/category/<id>/', methods=['PUT'])
def update_category(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True:
		data = request.get_json()
		if 'genre' not in data:
			return {
				'error': 'Bad Request',
				'message': 'id field needs to be present'
			}, 400
		category = Category.query.filter_by(public_id=id).first_or_404()
		# category.public_id=data['name']
		category.genre=data.get('name', category.genre)
		db.session.commit()
		return jsonify({
			'success': 'Data update successfully',
			'genre': category.genre,
			'desc': category.desc
		}),204
	elif allow == False:
		return "Youre not admin! please check and try again."
	elif allow == 'Please check your login details and try again.':
		return allow

@app.route('/category/<id>/', methods=['DELETE'] )
def delete_category(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True:
		category = Category.query.filter_by(public_id=id).first_or_404()
		db.session.delete(category)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		},200
	elif allow == False:
		return "Youre not admin! please check and try again."
	elif allow == 'Please check your login details and try again.':
		return allow
# #---------------------------------BOOK

@app.route('/book/')
def get_book():
	return jsonify([
		{ 
			'id': book.public_id, 
			'title': book.title,
			'quantity' : book.quantity,
			'category': {
				'genre': book.category.genre,
			},
			'author' : [
				x.name
				for x in book.authors
			]
		} for book in Book.query.all()
	]),200

@app.route('/book/<id>')
def get_book_id(id):
	book = Book.query.filter_by(public_id=id).first_or_404()
	return jsonify([
		{ 
			'id': book.public_id, 
			'title': book.title,
			'quantity' : book.quantity,
			'category': {
				'genre': book.category.genre,
			},
			'author' : [
				x.name
				for x in book.authors
			]
		},200
	])

@app.route('/author-book' , methods=['POST'])
def create_author_book():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True:
		data = request.get_json()
		books = Book.query.filter_by(id=data['book_id']).first_or_404()
		author = Author.query.filter_by(id=data['author_id']).first_or_404()
		books.authors_book.append(author)
		db.session.add(books)
		db.session.commit()
		return {
			"message" : "success"
		},201
	elif allow == False:
		return "Youre not admin! please check and try again."
	elif allow == 'Please check your login details and try again.':
		return allow
# @app.route('/books-genre', methods=['POST'])
# def get_romance():
#     data = request.get_json()
#     categories = Category.query.filter_by(genre=data['genre']).first_or_404()
#     b = []
#     for x in categories.book:
#         b.append(x.title)
#     return {
#         'genre': categories.genre, 'books': b
#     }

@app.route('/book/', methods=['POST'])
def create_book():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True:
		data = request.get_json()
		if not 'title' in data:
			return jsonify({
				'error': 'Bad Request',
				'message': 'title not given'
			}), 400
		if len(data['title']) < 4 :
			return jsonify({
				'error': 'Bad Request',
				'message': 'title must be contain minimum of 4 letters'
			}), 400
		category= Category.query.filter_by(genre=data['genre']).first()
		if not category:
			return {
				'error': 'Bad request',
				'message': 'Invalid genre'
			}
		book = Book(
				title=data['title'], 
				desc=data['desc'],
				quantity=data['quantity'],
				category_id = category.id,
				public_id=str(uuid.uuid4())
			)
		db.session.add(book)
		db.session.commit()
		return {
			'id': book.public_id, 
			'title': book.title,
			'quantity': book.quantity,
			'desc': book.desc,
			'category': {
				'genre': book.category.genre,
				'desc': book.category.desc
			}
		}, 201
	elif allow == False:
		return "Youre not admin! please check and try again."
	elif allow == 'Please check your login details and try again.':
		return allow

@app.route('/book/<id>/', methods=['PUT'])
def update_book(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True:
		data = request.get_json()
		print(data)
		if not 'title' in data :
			return {
				'error': 'Bad Request',
				'message': 'title or completed fields need to be present'
			}, 400
		book = Book.query.filter_by(public_id=id).first_or_404()
		book.title=data.get('title', book.title)
		db.session.commit()
		return {
			'id': book.public_id, 
			'title': book.title, 
			# 'desc': book.desc,
			'category': {
				'genre': book.category.genre,
				'desc': book.category.desc,
				'public_id': book.category.public_id,
			} 
		}, 201
	elif allow == False:
		return "Youre not admin! please check and try again."
	elif allow == 'Please check your login details and try again.':
		return allow

@app.route('/book/<id>/', methods=['DELETE'] )
def delete_todo(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True:
		book = Book.query.filter_by(public_id=id).first_or_404()
		db.session.delete(book)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		},200
	elif allow == False:
		return "Youre not admin! please check and try again."
	elif allow == 'Please check your login details and try again.':
		return allow

# #----------------------------------AUTHOR

@app.route('/author/')
def get_author():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True or allow == False:
		return jsonify([
			{
				'id': author.public_id, 
				'name': author.name, 
				'book' : [
					x.title
					for x in author.book
				],
			} for author in Author.query.all()
		]),200
	return {
		'message' : 'invalid username or password'
	}
		
@app.route('/author/<id>/')
def get_author_id(id):
	print(id)
	author = Author.query.filter_by(public_id=id).first_or_404()
	return {
		'id': author.public_id, 'name': author.name, 
		},200

@app.route('/author/', methods=['POST'])
def create_author():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True:
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
		a = Author(
				name=data['name'], 
				public_id=str(uuid.uuid4())
			)
		db.session.add(a)
		db.session.commit()
		return {
			'id': a.public_id, 'name': a.name,
		}, 201
	elif allow == False:
		return "Youre not admin! please check and try again."
	elif allow == 'Please check your login details and try again.':
		return allow

@app.route('/author/<id>/', methods=['PUT'])
def update_author(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True:
		data = request.get_json()
		if 'name' not in data:
			return {
				'error': 'Bad Request',
				'message': 'id field needs to be present'
			}, 400
		author = Author.query.filter_by(public_id=id).first_or_404()
		author.name=data['name']
		db.session.commit()
		return jsonify({
			'id': author.public_id,
			'name': author.name
			})
	elif allow == False:
		return "Youre not admin! please check and try again."
	elif allow == 'Please check your login details and try again.':
		return allow

@app.route('/author/<id>/', methods=['DELETE'] )
def delete_author(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True:
		author = Author.query.filter_by(public_id=id).first_or_404()
		db.session.delete(author)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		}
	elif allow == False:
		return "Youre not admin! please check and try again."
	elif allow == 'Please check your login details and try again.':
		return allow

#------------------------------USER

@app.route('/users/')
def get_users():
	return jsonify([
	{
		'id': user.public_id, 'name': user.name, 'username': user.username,
		'password' : user.password, 'is admin': user.is_admin
	} for user in User.query.all()
	]),200
		
@app.route('/users/<id>/')
def get_user(id):
	print(id)
	user = User.query.filter_by(public_id=id).first_or_404()
	return {
		'id': user.public_id, 'name': user.name, 'username': user.username,
		'password' : user.password, 'is admin': user.is_admin
		},200

@app.route('/add-users/', methods=['POST'])
def create_user():
	data = request.get_json()
	if not 'name' in data or not 'username' in data:
		return jsonify({
			'error': 'Bad Request',
			' message': 'Name or Username not given'
		}), 400
	if len(data['name']) < 4 or len(data['username']) < 5:
		return jsonify({
			'error': 'Bad Request',
			'message': 'Name and Username must be contain minimum of 4 letters'
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
		'id': user.public_id, 'name': user.name, 'username': user.username,
		'password' : user.password, 'is admin': user.is_admin
	}, 201

@app.route('/users/<id>/', methods=['PUT'])
def update_user(id):
	data = request.get_json()
	if 'public_id' not in data:
		return {
			'error': 'Bad Request',
			'message': 'id field needs to be present'
		}, 400
	user = User.query.filter_by(public_id=id).first_or_404()
	user.public_id=data['public_id']
	if 'is admin' in data:
		user.is_admin=data['admin']
	db.session.commit()
	return jsonify({
		'id': user.public_id, 'name': user.name, 'username': user.username,
		'password' : user.password, 'is admin': user.is_admin
		}),204

@app.route('/users/<id>/', methods=['DELETE'] )
def delete_user(id):
	user = User.query.filter_by(public_id=id).first_or_404()
	db.session.delete(user)
	db.session.commit()
	return {
		'success': 'Data deleted successfully'
	},200

#------------------------------------ RENT
@app.route('/rent/')
def get_rent():
    return jsonify([
		{
			'id': rent.public_id,
			'date rent': rent.date_rent,
			'date return': rent.date_return,
			'user_id' : rent.user_id,
			'book_id' : {
				"id" : rent.book.public_id,
				"title" : rent.book.title,
				"desc" : rent.book.desc
			},
			'admin_id': rent.admin_id
		} for rent in Rent.query.all()
	]),200

@app.route('/rent/<id>')
def get_rent_id(id):
	print(id)
	rent = Rent.query.filter_by(public_id=id).first_or_404()
	return jsonify([
		{
			'id': rent.public_id,
			'date rent': rent.date_rent,
			'date return': rent.date_return,
			'user_id' : rent.user_id,
			'book_id' : {
				"id" : rent.book.public_id,
				"title" : rent.book.title,
				"desc" : rent.book.desc
			},
			'admin_id': rent.admin_id
		}
	]),200

@app.route('/rent/', methods=['POST'])
def create_rent():
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True:
		data = request.get_json()
		user = User.query.filter_by(username=data['username']).first()
		if not 'username':
			return jsonify({
				'error': 'Bad Request',
				' message': 'Username not given'
			}), 400
		for x in data['title']:
			book = Book.query.filter_by(title=x).first()
			if book.quantity == 0:
				return jsonify ({
                    'message': 'Book not available'
                }), 400

		for x in data['title']:
			book = Book.query.filter_by(title=x).first()
			if not book:
				return jsonify({
					'error': 'Bad Request',
					' message': 'Title not given'
				}), 400

			admin = auth_admin(decode_var)[0]
			admin_ = User.query.filter_by(username=admin).first()
			rent = Rent(
					date_rent=data['date_rent'], 
					date_return=data['date_return'],
					book_id=book.id,
					user_id=user.id,
					admin_id=admin_.id,
					public_id=str(uuid.uuid4())
				)
			book.quantity -= 1
			db.session.add(rent)
		db.session.commit()
		return {
			"message" :  "success"
			# 'id': rent.public_id,
			# 'date rent': rent.date_rent,
			# 'date return': rent.date_return,
			# 'user_id' :rent.rent.user_id,
			# 'book_id' : rent.book.title,
			# 'admin_id': rent.is_admin
		}, 201
	else:
		return {
            'message': 'Access denied'
        }, 401

@app.route('/rent/<id>',  methods=['PUT'])
def update_rent(id):
    decode_var = request.headers.get('Authorization')
    allow = author_user(decode_var)
    if allow == True :
        data = request.get_json()
        rent = Rent.query.filter_by(public_id=id).first_or_404()
        book = Book.query.filter_by(id=rent.book_id).first_or_404()
        rent.date_return = data['date_return']
        book.quantity += 1
        db.session.commit()
        return {
            'message': 'success'
        }
    else:
        return {
            'message': 'Access denied'
        }, 401

@app.route('/rent/<id>/', methods=['DELETE'] )
def delete_rent(id):
	decode_var = request.headers.get('Authorization')
	allow = author_user(decode_var)
	if allow == True:
		rent = Rent.query.filter_by(public_id=id).first_or_404()
		db.session.delete(rent)
		db.session.commit()
		return {
			'success': 'Data deleted successfully'
		}
	elif allow == False:
		return "Youre not admin! please check and try again."
	elif allow == 'Please check your login details and try again.':
		return allow