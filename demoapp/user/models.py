from flask import Flask, jsonify, request, session, redirect
import uuid
from app import db
from app import neo4jSession
import datetime

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
        print("*****************************************************",request)
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
    
    def get_managers(self):
        all_managers=list(db.users.find({},{"name":True,"_id":True}))
        if all_managers:
            return jsonify(all_managers), 200
        return jsonify({"error":"error in finding manager"}), 400

    def set_manager(self):
        manager_id=request.form.get("managers")
        if manager_id=='none':
            return jsonify("select valid manager"), 400
        db.users.update({'_id':session['user']['_id']},{'$set':{'manager_id':manager_id}})
        session['user']['manager_id']=manager_id
        print(session,"sessssssssssssssssionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        return jsonify({"added manager id":manager_id}), 200

    def get_manager_and_reportee(self):
        employeeID=request.form.get('get_manager_and_reportee')
        get_manager_query='MATCH (n:user{_id:"'+ employeeID+'"})-->(m) RETURN n,m'
        get_reportee_query='MATCH (n:user{_id:"'+ employeeID +'"})<--(m) RETURN n,m'
        resp={}
        resp['manager']=[{"name":x['m']['name'],"ID":x['m']['_id']} for x in neo4jSession.run(get_manager_query)]
        resp['reportee']=[{"name":x['m']['name'],"ID":x['m']['_id']} for x in neo4jSession.run(get_reportee_query)]
        return jsonify(resp),200
        
    def get_group_chats_list(self):     
        resp=list(db.group_chat.find({},{
            "_id":0
            }))
        if resp:
            #print(resp)
            return jsonify(resp), 200
        return jsonify({"status":"not able to load chat from database"}), 400


    def add_group_chat_message(self,email,message):
        if db.group_chat.insert({
            "email":email,
            "message":message,
            "timestamp":datetime.datetime.now()
        }):
            return jsonify({"email":email,
            "message":message,
            "timestamp":datetime.datetime.now()}), 200
        return jsonify({"status":"not able to add chat into database"}), 400


    def get_all_user_email_and_id(self):
        all_emails,all_ids=[],[]
        for x in db.users.find({},{"_id":1,"email":1}):
            all_ids.append(x["_id"])
            all_emails.append(x["email"])
        return all_emails,all_ids
    

    def get_last_email_sent_time(self,all_emails,all_ids):
        last_email_sent_time_list=[]
        for _id,email in zip(all_ids,all_emails):
            x = db.last_email_sent_time.find_one({"user_id":_id})
            if x :
                last_email_sent_time_list.append(x['time'])
            else :
                time="NA"
                db.last_email_sent_time.insert_one({
                    "user_id":_id,
                    "email":email,
                    "time":time
                })
                last_email_sent_time_list.append(time)
        return last_email_sent_time_list
    

    def update_last_email_sent_time(self,all_emails,all_ids,updated_time_list):
        for _id,time in zip(all_ids,updated_time_list):
            db.last_email_sent_time.update({'user_id':_id},{'$set':{'time':time}})
        

    def get_last_one_hour_msg(self):
        
        return list(db.group_chat.find({"timestamp":{"$gte": datetime.datetime.now()-datetime.timedelta(hours = 1) }},{"_id":0}))