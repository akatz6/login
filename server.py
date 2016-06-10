from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
mysql = MySQLConnector(app,'login')
bcrypt = Bcrypt(app)
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods=['POST'])
def new_user():
	query = """INSERT INTO login (first_name, last_name, email, 
		password, created_at, updated_at)VALUES
		(:first_name, :last_name, :email, :password, NOW(), NOW())"""
	password = request.form['password']

	data = {
	'first_name': request.form['first_name'], 
	'last_name':  request.form['last_name'],
	'email': request.form['email'],
	'password': bcrypt.generate_password_hash(password)
	}
	mysql.query_db(query, data)
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password']
	user_query = "SELECT * FROM login WHERE email = :email LIMIT 1"
	query_data = { 'email': email }
	user = mysql.query_db(user_query, query_data) 
	print user
	if bcrypt.check_password_hash(user[0]['password'], password):
		return render_template('login.html')
	else:
		flash("password does not match")
	return render_template('index.html')

app.run(debug=True)