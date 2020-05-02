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



app = Flask(__name__)

class RelayBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        #self.markAsRead(thread_id)
        # TODO: store in dict for faster lookup
        user = client.fetchUserInfo(author_id)[author_id]
        message = "{}: {}".format(user.name, message_object.text) 
        
        sms.messages.create \
        (
            body = message,
            from_ = twil_creds.twil_number,
            to = phoneNumber
        )

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
        user = client.searchForUsers(recipient)[0]
        userId = user.uid

        actualMessage = body.split(' ', 2)[2]
        targetType = ThreadType.USER
        
        client.send(Message(text=actualMessage), thread_id=userId, thread_type=targetType)

        resp.message("Message Sent")
    
    else:
        resp.message("Invalid Command")

    return str(resp)


if __name__ == "__main__":
    app.run(threaded=True, port=5000)

        

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


    
