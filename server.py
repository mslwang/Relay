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
from logzero import logger as log
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import credentials
from relaybot import RelayBot
import os
import schema as sch
import twitter

app = Flask(__name__, static_folder='build')
connect(credentials.dbUrl)
CORS(app)

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
    log.info(request.values.to_dict())
    from_ = request.values.get('From')
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
            sch.User.objects.raw({'_id': from_}).update({"$set": {"active": mode}})

        else:
            resp.message("Invalid mode type")

    elif cmd == "msg" or cmd == 'message':
        #get user credentials
        log.info(from_) 
        user = sch.User.objects.get({'_id': from_})
        mode = user.active

        if mode == 'messenger':
            login = user.messenger_login
            client = RelayBot(login.email, login.password)
            recipient = body.split(' ', 2)[1]
            user = client.searchForUsers(recipient)[0]
            userId = user.uid
            targetType = ThreadType.USER

            actualMessage = body.split(' ', 2)[2]
            log.info(actualMessage)
            client.send(Message(text=actualMessage), thread_id=userId, thread_type=targetType)

            resp.message("Message Sent")

        elif mode == 'twitter':
            login = user.twitter_login
            api = twitter.Api(
                consumer_key=login.consumer_key,
                consumer_secret=login.consumer_secret,
                access_token_key=login.access_token_key,
                access_token_secret=login.access_token_secret)

            screenName = body.split(' ',2)[1]
            user = api.GetUser(screen_name = screenName)
            twitterid = user.id
            message = body.split(' ', 2)[2]

            api.PostDirectMessage(message, user_id = twitterid)
            resp.message("Message Sent")

    elif cmd == 'tweet':
        user = sch.User.objects.get({'_id': "{}".format(from_)})
        login = user.twitter_login
        api = twitter.Api(
            consumer_key=login.consumer_key,
            consumer_secret=login.consumer_secret,
            access_token_key=login.access_token_key,
            access_token_secret=login.access_token_secret)

        message = body.split(' ', 1)[1]
        api.PostUpdate(message)
        resp.message("Tweet Sent")
    elif cmd == "currentmode":
        resp.message("Currently set on {}".format(mode))
    else:
        resp.message("Invalid Command")

    return str(resp)


@app.route('/signup', methods = ['POST'])
def do_signup():
    data = json.loads(request.data)
    integration = data['integration']
    tel = "+1" + data['tel']
    if integration == "messenger":
        print(data)
        email = data['email']
        password = data['password']
        sch.User(tel, active="messenger", messenger_login=sch.MessengerAccount(email=email, password=password)).save()
    elif integration == "twitter":
        print(data)
        access_token = data['access_token']
        access_secret_token = data['access_secret_token']
        api_key = data['api_key']
        api_secret_key = data['api_secret_key']
        api = twitter.Api(
            consumer_key=api_key,
            consumer_secret=api_secret_key,
            access_token_key=access_token,
            access_token_secret=access_token_secret)
        lastmsgid = api.GetDirectMessages(return_json=True, count = 1).events[0].id
        sch.User(tel, active="twitter", twitter_login=sch.TwitterAccount(access_token=access_token, access_token_secret=access_token_secret, api_key=api_key, api_secret_key=api_secret_key, last_msg = lastmsgid)).save()

    return json.dumps({"status": 200})

@app.route('/exit', methods = ['GET'])
def exit():
    client.logout()

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
