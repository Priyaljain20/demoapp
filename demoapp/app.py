from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo

app=Flask(__name__)
app.secret_key=b'\xa1c*\x10<\xbb&\x17\xee\xcd\x0c\x81\xd2\xe0\xfdk'

#Database
client =pymongo.MongoClient('localhost',27017)
db=client.user_login_system

#decoratars
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect('/')
	return wrap

# importing user routes present in ChatterBot/routes.py file
from user import routes

# importing chat routes present in ChatterBot/routes.py file
from ChatterBot import routes

# home is login and signin page
@app.route("/")
def home():
	return render_template('home.html')

# dashboard is where user chat and can logout
@app.route("/dashboard/")
@login_required
def dashboard():
	return render_template('dashboard.html')
