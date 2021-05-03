from flask import Flask, render_template, session, redirect,request
from functools import wraps
import pymongo
from neo4j import GraphDatabase

app=Flask(__name__)
app.secret_key=b'\xa1c*\x10<\xbb&\x17\xee\xcd\x0c\x81\xd2\xe0\xfdk'

# MongoDB Database
client =pymongo.MongoClient('localhost',27017)
db=client.user_login_system


# GraphDB Database
neo4jSession=None
'''
uri="bolt://localhost:7687"
user="neo4j"
pwd="priyal"
graphDatabase="neo4j"
driver= GraphDatabase.driver(uri, auth=(user, pwd))
if graphDatabase is not None:
    neo4jSession = driver.session(database=graphDatabase)  
else:
    neo4jSession = driver.session() 
'''

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
	print(request.host_url)
	return render_template('dashboard.html')

@app.route("/user/<id>")
@login_required
def user_profile(id=None):
	print(session,"-------------------------------------")
	return render_template('profile.html',id=id)

@app.route("/user/group_chat")
@login_required
def group_chat():
	return render_template('group_chat.html')
