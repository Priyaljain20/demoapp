from flask import Flask, jsonify, request, session, redirect
import uuid
from app import db

class User:

    #starts session if logged in or signed in
    def startSession(self,user):
        del user['password']
        session['logged_in']=True
        session['user']=user
        return jsonify(user), 200

    #process signin request
    def signup(self):
        print("hiiiii models ",request.form)

        user={
            "_id":uuid.uuid4().hex,
            "name":request.form.get('name'),
            "email":request.form.get('email'),
            "password":request.form.get('password')
        }

        if db.users.find_one({"email":user["email"]}):
         return jsonify({"error":"Email address address already exist"}),400
        
        if db.users.insert_one(user):
            #return jsonify(user), 200
            #starts session
            return self.startSession(user)
        
        return jsonify({"error":"signup failed"}), 400
    
    #process login request
    def login(self):
        user={
            "email":request.form.get('email'),
            "password":request.form.get('password')
        }
        x=db.users.find_one({"email":user["email"]})
        if x:
            if user['password']==x['password']:
                #starts session
                return self.startSession(x)
            else:
                return jsonify({"error":"password wrong"}) ,400
        else:
            return jsonify({"error":"email not registered"}), 400

        return jsonify({"error":"login failed"}), 400
    
    #process logout request
    def signout(self):
        session.clear()
        return redirect('/') 