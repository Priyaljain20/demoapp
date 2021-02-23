from flask import jsonify, request, session
from app import db

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer 
from datetime import datetime

class Chatbot:
    # def __init__(self):   
    #     self.chatbot = ChatBot('new_bot')
    #     trainer = ChatterBotCorpusTrainer(self.chatbot) 
    #     trainer.train("chatterbot.corpus.english.greetings", 
	# 		"chatterbot.corpus.english.conversations" ) 

    def response(self):
        #initializing bot
        chatbot = ChatBot('new_bot')

        #getting message request
        msg=request.form.get("message")
        response = str(chatbot.get_response(msg))
        
        # getting user id from session
        user_id=session['user']['_id']

        #checks if the chat exist in data base, if not it creats a new one else it will update old chat
        if db.chats.find_one({"user_id":user_id}):
            if db.chats.update_many({"user_id":user_id},
                {"$set":{
                    "user_id":user_id,
                    str(datetime.now()).replace("."," ")+"@user":msg,
                    str(datetime.now()).replace("."," ")+"@bot":response
                }}
            ):
                print ("chat added")
            else:
                print("chat not added")
                return jsonify({"error":"chat not added"}),400
        else:   
            if db.chats.insert_one({
                    "user_id":user_id,
                    str(datetime.now()).replace("."," ")+"@user":msg,
                    str(datetime.now()).replace("."," ")+"@bot":response
                }):
                print("new conversation created in database for the user")
            else:
                print("error inserting data")
                return jsonify({"error":"chat not added"}),400

        return jsonify({"bot":chatbot.name,"reply":response}),200