import requests
import json
import time
import os
import sys
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from twilio import twiml
from flask import Flask, request
from flask_cors import CORS
from fbchat import Client
from fbchat.models import *
import getpass
from pymongo import MongoClient
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import os
from dotenv import load_dotenv

app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app)
mongoClient = MongoClient('localhost', 27017)

client = Client('kelvin.zhang@uwaterloo.ca', getpass.getpass())

@app.route('/')
def index():
    return app.send_static_file('index.html')

#user is sending something
@app.route('/sms', methods = ['POST'])
def incoming_sms():
    #Get the message
    body = request.values.get('Body', None)
    resp = MessagingResponse()

    cmds = {
        "getfriends": "",
        "msg {name} {msg}": "send message to friend",
        "getactivechats": "print a list of active chats"
    }

    cmd = body.split(' ', 2)[0].lower()

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


@app.route('/signup', methods = ['POST'])
def do_signup():
    data = json.loads(request.data)
    integration = data['integration']
    tel = data['tel']
    email = data['email']
    password = data['password']

    # store this in mongo
    print("{}, {}, {}, {}".format(integration, tel, email, password))
    return json.dumps({"status": 200})


@app.route('/exit', methods = ['GET'])
def exit():
    client.logout()

if __name__ == "__main__":
    app.run(threaded=True, port=5000)

        


    
