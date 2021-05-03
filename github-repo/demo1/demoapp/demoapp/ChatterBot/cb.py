# Import "chatbot" from 
# chatterbot package. 
from chatterbot import ChatBot 

# Inorder to train our bot, we have 
# to import a trainer package 
# "ChatterBotCorpusTrainer" 
from chatterbot.trainers import ChatterBotCorpusTrainer 


# Give a name to the chatbot “corona bot” 
# and assign a trainer component. 
chatbot=ChatBot('new_bot') 

# Create a new trainer for the chatbot 
trainer = ChatterBotCorpusTrainer(chatbot) 

# Now let us train our bot with multipple corpus 
trainer.train("chatterbot.corpus.english.greetings", 
			"chatterbot.corpus.english.conversations" ) 

response = chatbot.get_response('What is your Number') 
print(response) 

response = chatbot.get_response('Who are you?') 
print(response) 



'''from chatterbot import ChatBot
chatbot = ChatBot("bot")
from chatterbot.trainers import ListTrainer

conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]
trainer = ListTrainer(chatbot)
trainer.train(conversation)
response = chatbot.get_response("Good morning!")
print(response)'''