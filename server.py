import requests
import json
import time
import os
import sys
import atexit
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
import threading
from activetwitter import checkDMs

app = Flask(__name__, static_folder='build')
messenger_instances = dict()
twitter_instances = dict()
threads = []

connect(credentials.dbUrl)
CORS(app)

def listen(client):
    log.info("spawning new thread")
    client.listen()

def newMessengerInstance(phoneNum, email, password):
    client = RelayBot(phoneNum, email, password)
    log.info("adding {}, {}, {}".format(phoneNum, email, password))
    th = threading.Thread(target=listen, args=(client,))
    threads.append(th)
    th.start()
    messenger_instances[phoneNum] = client
    if not client.isLoggedIn():
        raise Exception
    return client

def newTwitterInstance(phoneNum, consumer_key, consumer_secret, access_token_key, access_token_secret):
    log.info("adding {}, {}, {}, {}, {}".format(phoneNum, consumer_key, consumer_secret, access_token_key, access_token_secret))
    client = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret)
    twitter_instances[phoneNum] = client
    if not client.VerifyCredentials():
        raise Exception
    return client

# when we start, populate instances
users = list(sch.User.objects.all())
for user in users:
    active = user.active
    if active == "messenger":
        login = user.messenger_login
        phoneNum = user.phone_number 
        try:
            newMessengerInstance(phoneNum, login.email, login.password)
        except Exception:
            pass
    elif active == "twitter":
        login = user.twitter_login
        try:
            newTwitterInstance(
                phoneNum,
                consumer_key=login.api_key,
                consumer_secret=login.api_secret_key,
                access_token_key=login.access_token,
                access_token_secret=login.access_token_secret)
        except Exception:
            pass

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
            client = None
            if from_ in messenger_instances:
                client = messenger_instances[from_]
            else:
                login = user.messenger_login
                client = newMessengerInstance(user.phone_number, user.email, user.password)  
            if not client or not client.isLoggedIn():
                resp.message("Failed to log in, please update credentials")
                return str(resp)

            recipient = body.split(' ', 2)[1]
            user = client.searchForUsers(recipient)[0]
            userId = user.uid
            targetType = ThreadType.USER

            actualMessage = body.split(' ', 2)[2]
            log.info(actualMessage)
            client.send(Message(text=actualMessage), thread_id=userId, thread_type=targetType)

            resp.message("Message Sent")

        elif mode == 'twitter':
            client = None
            if from_ in twitter_instances:
                client = twitter_instances[from_]
            else:
                login = user.twitter_login
                client = newTwitterInstance(
                    user.phone_number,
                    consumer_key=login.api_key,
                    consumer_secret=login.api_secret_key,
                    access_token_key=login.access_token,
                    access_token_secret=login.access_token_secret)
            if not client or not client.VerifyCredentials():
                resp.message("Failed to log in, please update credentials")
                return str(resp)

            screenName = body.split(' ',2)[1]
            user = client.GetUser(screen_name = screenName)
            twitterid = user.id
            message = body.split(' ', 2)[2]

            client.PostDirectMessage(message, user_id = twitterid)
            resp.message("Message Sent")

    elif cmd == 'tweet':
        user = sch.User.objects.get({'_id': "{}".format(from_)})
        login = user.twitter_login
        client = None
        if from_ in twitter_instances:
            client = twitter_instances[from_]
        else:
            login = user.twitter_login
            client = newTwitterInstance(
                user.phone_number,
                consumer_key=login.api_key,
                consumer_secret=login.api_secret_key,
                access_token_key=login.access_token,
                access_token_secret=login.access_token_secret)
        if not client or not client.VerifyCredentials():
            resp.message("Failed to log in, please update credentials")
            return str(resp)

        message = body.split(' ', 1)[1]
        client.PostUpdate(message)
        resp.message("Tweet Sent")

    elif cmd == "currentmode":
        user = sch.User.objects.get({'_id': from_})
        mode = user.active
        
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
        try:
            newMessengerInstance(tel, email, password)
        except Exception:
            log.info("whoops")
            pass
    elif integration == "twitter":
        print(data)
        access_token = data['access_token']
        access_token_secret = data['access_secret_token']
        api_key = data['api_key']
        api_secret_key = data['api_secret_key']
        client = None
        try:
            client = newTwitterInstance(
                tel,
                consumer_key=api_key,
                consumer_secret=api_secret_key,
                access_token_key=access_token,
                access_token_secret=access_secret_token)
            lastmsgid = client.GetDirectMessages(return_json=True, count = 1).events[0].id
        except Exception:
            pass
        lastmsgid = 100
        sch.User(tel, active="twitter", twitter_login=sch.TwitterAccount(access_token=access_token, access_token_secret=access_token_secret, api_key=api_key, api_secret_key=api_secret_key, last_msg = lastmsgid)).save()

    return json.dumps({"status": 200})

@app.route('/exit', methods = ['GET'])
def exit():
    client.logout()

def close_running_threads():
    for thread in threads:
        thread.join()
    print("Merging threads")

atexit.register(close_running_threads)

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
