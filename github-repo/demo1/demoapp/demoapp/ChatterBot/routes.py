from flask import Flask 
from app import app
from ChatterBot.models import Chatbot

@app.route('/ChatterBot/get_response',methods=['POST'])
def getresponse():
    return Chatbot().response()
