from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
mysql = MySQLConnector(app,'wall')
bcrypt = Bcrypt(app)

def allMessages():
	return """SELECT u.first_name, u.last_name, u.updated_at, m.message, 
	 m.m_id
	FROM  messages m
	JOIN users u ON u.u_id = m.user_id
	ORDER BY m.m_id DESC"""

def allComments():
	return """SELECT u.first_name, u.last_name,c.updated_at, 
	c.comment, c.message_id
	FROM comments c
	JOIN users u on u.u_id = c.user_id
	ORDER BY c.updated_at"""

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods=['POST'])
def new_user():
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']
	password = request.form['password']
	valid = True

	if len(first_name) < 1:
		valid = False
		flash("Please enter first name", "error")

	if len(last_name) < 1:
		valid = False
		flash("Please enter last name", "error")

	if len(email) < 1:
		valid = False
		flash("Please enter email", "error")
	elif not EMAIL_REGEX.match(request.form['email']):
		valid = False
		("Invalid Email Address!", "error")

	if len(password) < 1:
		valid = False
		flash("Please enter password", "error")

	if valid:
		query = """INSERT INTO users (first_name, last_name, email, 
			password, created_at, updated_at)VALUES
		(:first_name, :last_name, :email, :password, NOW(), NOW())"""	
		data = {
		'first_name': first_name, 
		'last_name':  last_name,
		'email': email,
		'password': bcrypt.generate_password_hash(password)
		}
		mysql.query_db(query, data)
		flash("Data entered, please log in", "error")
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	valid = True
	email = request.form['email']
	password = request.form['password']

	if len(email) < 1:
		valid = False
		flash("Please enter email", "success")
	elif not EMAIL_REGEX.match(request.form['email']):
		valid = False
		("Invalid Email Address!", "success")

	if len(password) < 1:
		valid = False
		flash("Please enter password", "success")

	if valid:
		user_query = """SELECT * 
		FROM users
		WHERE email = :email"""
		query_data = { 'email': email }
		user = mysql.query_db(user_query, query_data) 
		session['user'] = user
		user_query = allMessages()
		
		messages = mysql.query_db(user_query, "")
		user_query = allComments()
		comments = mysql.query_db(user_query, "")
		try:
			print password
			print user[0]['password']
			bcrypt.check_password_hash(user[0]['password'], password)
			print password
			return render_template('wall.html', users = user, messages = messages, 
				comments = comments)
		except:
			flash("password does not match", "success")
	return render_template('index.html')



@app.route('/messages', methods=['POST'])
def messages():
	valid = True
	message = request.form['message']
	user = session['user']
	user_id = user[0]['u_id']
	print user_id

	query = """SELECT * FROM messages 
	WHERE user_id =:user_id and message =:message"""
	data = { 
	'user_id': user_id, 
	'message' : message
	}
	exists = mysql.query_db(query, data)

	if len(message) > 0 and len(exists) < 1:
		user_query = "SELECT u_id FROM users WHERE email = :email LIMIT 1"
		query_data = { 'email': user[0]['email'] }
		user1 = mysql.query_db(user_query, query_data)
		user_id = user1[0]['u_id']
		query = """INSERT INTO messages (user_id, message, created_at, updated_at)
		VALUES
		(:user_id, :message, NOW(), NOW())"""
		data = {
		'user_id': user_id, 
		'message':  message,
		} 
		mysql.query_db(query, data)
	user_query = allMessages()
	messages = mysql.query_db(user_query, "")
	user_query = allComments()
	comments = mysql.query_db(user_query, "")
	return render_template('wall.html',users = user, messages = messages, 
		comments = comments)


@app.route('/comments/<message_id>', methods=['POST'])
def comments(message_id):
	user = session['user']
	comment = request.form['comment']
	user_id = user[0]['u_id']
	message_id = message_id
	
	query = """SELECT * FROM comments 
	WHERE message_id = :message_id and user_id =:user_id and comment =:comment"""
	data = { 
	'message_id' : message_id,
	'user_id': user_id, 
	'comment' : comment
	}
	exists = mysql.query_db(query, data)

	if len(comment) > 0 and len(exists) < 1:
		query = """INSERT INTO comments (message_id, user_id, comment, created_at,
		updated_at) VALUES
		(:message_id, :user_id, :comment, NOW(), NOW())"""
		data = { 
		'message_id' : message_id,
		'user_id': user_id, 
		'comment' : comment
		}
		mysql.query_db(query, data)
		print "Why am I in here"
	user_query = allMessages()
	messages = mysql.query_db(user_query, "")
	user_query = allComments()
	comments = mysql.query_db(user_query, "")
	return render_template('wall.html',users = user, messages = messages,
		comments = comments)

@app.route('/logoff')
def logff():
	return render_template('index.html')

app.run(debug=True)
