#routes related to user eg. signup login
from flask import Flask
from app import app
from user.models import User

#routes the request to User().signup() function
@app.route('/user/signup',methods=['POST'])
def signup():
    return User().signup()

#routes the request to User().login() function
@app.route('/user/login',methods=['POST'])
def login():
    return User().login()

#routes the request to User().signout() function
@app.route('/user/signout')
def signout():
    return User().signout()

