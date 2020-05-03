import requests
import json
import time
import os
import sys
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from twilio import twiml
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from fbchat import Client
from fbchat.models import *
import getpass
from pymongo import MongoClient
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import os
from dotenv import load_dotenv
import schema as sch
import twitter

load_dotenv()
app = Flask(__name__, static_folder='build')
CORS(app)
mongoClient = MongoClient('localhost', 27017)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

#user is sending something
@app.route('/sms', methods = ['POST'])
def incoming_sms():
    #Get the message
    body = request.values.get('Body', None)
    from_ = request.values.get('from')
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

    elif cmd == "switch":
        mode = body.split(' ', 2)[1].lower()

        modes = ['messenger', 'twitter']

        if mode in modes:
            resp.message("Mode switched to {}".format(mode))

        else:
            resp.message("Invalid mode type")

    elif cmd == "msg" or cmd == 'message':

        #get user credentials
        valid_accounts = sch.User.objects.get({'_id': "{}".format(from_)}).accounts

        if mode in valid_accounts.integration:
            if mode == 'messenger':
                #client.logout()
                login = valid_accounts[mode]
                client = Client(login.email, login.password)
                recipient = body.split(' ', 2)[1]
                user = client.searchForUsers(recipient)[0]
                userId = user.uid

                actualMessage = body.split(' ', 2)[2]
                client.send(Message(text=actualMessage), thread_id=userId, thread_type=targetType)

                resp.message("Message Sent")

            elif mode == 'twitter':
                consumer_key = ''
                consumer_secret = ''
                access_token_key = ''
                access_token_secret = ''

                api = twitter.Api(
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token_key=access_token_key,
                    access_token_secret=access_token_secret)

                screenName = body.split(' ',2)[1]
                user = api.getUser(screen_name = screenName)
                twitterid = user.id
                message = body.split(' ', 2)[2]

                api.PostDirectMessage(message, user_id = twitterid)
                resp.message("Message Sent")
    
    elif cmd == 'tweet':
        if mode == 'twitter':
            valid_accounts = sch.User.objects.get({'_id': "{}".format(from_)}).accounts
            
            if mode in valid_accounts.integration:
                consumer_key = ''
                consumer_secret = ''
                access_token_key = ''
                access_token_secret = ''

                api = twitter.Api(
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token_key=access_token_key,
                    access_token_secret=access_token_secret)

                message = body.split(' ', 1)[1]

                api.PostUpdate(message)
                resp.message("Tweet Sent")
        
        else:
            resp.message('{} does not exist for {}'.format(cmd, mode))
        
    elif cmd == "currentmode"
        resp.message("Currently set on {}".format(mode))

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
    sch.User(tel, email=email, accounts=[sch.Account(integration=integration, username=email, utype="email", password=password)]).save()
    #print("{}, {}, {}, {}".format(integration, tel, email, password))
    return json.dumps({"status": 200})

@app.route('/exit', methods = ['GET'])
def exit():
    client.logout()

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
