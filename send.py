import requests
import json
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from twilio import twiml
from flask import Flask, request
from fbchat import Client
from fbchat.models import *
import getpass
from messenger import RelayBot


app = Flask(__name__)
client = RelayBot('kelvin.zhang@uwaterloo.ca', getpass.getpass())

#user is sending something
@app.route('/', methods = ['POST'])
def incoming_sms():
    #Get the message
    body = request.values.get('Body', None).lower()
    resp = MessagingResponse()

    cmds = {
        "getfriends": "",
        "msg {name} {msg}": "send message to friend",
        "getactivechats": "print a list of active chats"
    }

    cmd = body.split(' ', 2)[0]

    if cmd == "getactivechats":
        users = client.fetchAllUsers()
        returnMessage = ''
        for user in users:
            returnMessage += "{}: {}".format(user.name, user.uid)

        resp.message(returnMessage)
        
    elif cmd == "msg" or cmd == 'message':
        recipient = body.split(' ', 2)[1]
        user = client.searchForUsers(recipient)

        actualMessage = body.split(' ', 3)[2]
        userId = user.uid
        targetType = ThreadType.USER
        
        client.send(Message(text=actualMessage), thread_id=userId, thread_type=targetType)

        resp.message("Message Sent")
    
    else:
        resp.message("Invalid Command")


client.logout()



        

'''
#Check if a message is a valid command
def isValid(msg):
    #Array of words
    allWords = msg.split(' ')
    if len(allWords) < 2:
        return False
    elif not isNetwork(allWords[1]):
        return False
    else:
        return True

#If msg is a valid social network
def isNetwork(msg):
    #Our only valid social network rn
    if msg.lower() == 'messenger':
        return True
    #We add more social networks here later
    else:
        return False
'''

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
    
