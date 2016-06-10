from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
mysql = MySQLConnector(app,'login')
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods=['POST'])
def new_user():
	query = """INSERT INTO login (first_name, last_name, email, 
		password, created_at, updated_at)VALUES
		(:first_name, :last_name, :email, :password, NOW(), NOW())"""
	data = {
	'first_name': request.form['first_name'], 
	'last_name':  request.form['last_name'],
	'email': request.form['email'],
	'password': request.form['password']
	}
	print date
	mysql.query_db(query, data)
	return render_template('index.html')

# @app.route('/friends/<id>/edit', methods=['POST'])
# def edit(id):

# 	query = "SELECT * FROM friends where id = :id"
# 	data = {
# 	'id':id
# 	}
# 	result = mysql.query_db(query, data)
# 	print result
# 	return render_template('update.html', friend = result)


# @app.route('/friends/<id>/test', methods=['POST'])
# def update(id):
# 	query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation WHERE id = :id"
# 	data = {
# 	'first_name': request.form['first_name'],
# 	'last_name':  request.form['last_name'],
# 	'occupation': request.form['occupation'],
# 	'id': id
# 	}
# 	mysql.query_db(query, data)
# 	return redirect('/')

# @app.route('/friends/<id>/delete', methods=['POST'])
# def destroy(id):
# 	query = "DELETE FROM friends WHERE id = :id"
# 	data = {'id': id}
# 	mysql.query_db(query, data)
# 	return redirect('/')

app.run(debug=True)