#routes related to user eg. signup login
from flask import Flask,request,session,make_response,jsonify
from app import app
from user.models import User
from sendEmail.send_email import notify_message_to_given_email_list
from threading import Thread
import datetime

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

@app.route('/user/get_managers')
def get_managers():
    return User().get_managers()

@app.route('/user/set_manager',methods=['POST'])
def set_manager():
    response=User().set_manager()[0]
    response.headers.add('Access-Control-Allow-Headers',
                         "Origin, X-Requested-With, Content-Type, Accept, x-auth")
    return response

@app.route('/user/get_manager_and_reportee',methods=['POST'])
def get_manager_and_reportee():
    return User().get_manager_and_reportee()

@app.route("/user/get_group_chats_list")
def get_group_chats_list():
	return User().get_group_chats_list()

@app.route("/user/add_group_chat_message",methods=['POST'])
def add_group_chat_message():
    x=User().add_group_chat_message(session["user"]["email"],request.form.get("group_chat_message"))
    email_list, id_list = User().get_all_user_email_and_id()
    email_list.remove(session['user']['email'])
    id_list.remove(session['user']['_id'])
    last_email_sent_time_list = User().get_last_email_sent_time(all_emails=email_list,all_ids=id_list)
    #notify_message_to_given_email_list(session['user']['email'],email_list,request.form.get('group_chat_message'))

    thread = Thread(
        target=lambda user_id, user_email, user_message, email_list, id_list, last_email_sent_time_list : 
            User().update_last_email_sent_time(email_list,id_list,notify_message_to_given_email_list(user_id, user_email, user_message, email_list, id_list, last_email_sent_time_list)), 
        args=(session['user']['_id'],session['user']['email'],request.form.get('group_chat_message'),email_list,id_list,last_email_sent_time_list)
    )
    thread.start()

    return x


@app.route("/user/receive_response_from_email",methods=['post'])
def receive_response_from_email():
    print(request.headers,request.args)
    email_list,id_list=User().get_all_user_email_and_id()
    print(email_list ,'------', request.args["email"])
    print(request.args['time'],type(request.args['time']))
    if not request.args["email"] in email_list or datetime.datetime.now()-datetime.datetime.strptime(request.args["time"], '%Y-%m-%d %H:%M:%S.%f')>=datetime.timedelta(minutes=5):
        response = make_response(
        jsonify(
            {"status": "failure"}
        ),
        400,
        )
    else:
        email_list.remove(request.args["email"])
        id_list.remove(request.args["_id"])
        last_email_sent_time_list = User().get_last_email_sent_time(all_emails=email_list,all_ids=id_list)
        response = make_response(
        jsonify(
            {"status": "sucess",
            "user":request.args["email"],
            "message":request.values['message_from_email']}
        ),
        200,
        )
        
        thread = Thread(
            target=lambda  user_id, user_email, user_message, email_list, id_list, last_email_sent_time_list : 
                User().update_last_email_sent_time(email_list,id_list,notify_message_to_given_email_list(user_id, user_email, user_message, email_list, id_list, last_email_sent_time_list)),
            args=(request.args["_id"],request.args["email"],request.values['message_from_email'],email_list,id_list,last_email_sent_time_list)
        )
        User().add_group_chat_message(request.args["email"],request.values['message_from_email'])
        thread.start()
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Credentials"]="true"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["AMP-Access-Control-Allow-Source-Origin"] = request.args["__amp_source_origin"]
    response.headers["Access-Control-Expose-Headers"] = "AMP-Access-Control-Allow-Source-Origin"
    return response


@app.route("/user/get_last_one_hour_msg")
def get_last_one_hour_msg():
    email_list,id_list=User().get_all_user_email_and_id()
    if not request.args["email"] in email_list:
        response = make_response(
        jsonify(
            {"status": "failure"}
        ),
        400,
        )
    else:
        response = make_response(
        jsonify(
            {"items":User().get_last_one_hour_msg()}
        ),
        200,
        )
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Credentials"]="true"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["AMP-Access-Control-Allow-Source-Origin"] = request.args["__amp_source_origin"]
    response.headers["Access-Control-Expose-Headers"] = "AMP-Access-Control-Allow-Source-Origin"
    return response

