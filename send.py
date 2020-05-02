import requests
import json
import os
import sys
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from twilio import twiml
from flask import Flask, request
from fbchat import Client
from fbchat.models import *
import getpass

app = Flask(__name__)

client = Client('kelvin.zhang@uwaterloo.ca', getpass.getpass())

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
            returnMessage += "{}: {}\n".format(user.name, user.uid)

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


@app.route('/exit', methods = ['GET'])
def exit():
    client.logout()

if __name__ == "__main__":
    app.run(threaded=True, port=5000)

        


    
