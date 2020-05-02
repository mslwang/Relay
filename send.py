import requests
import json
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from twilio import twiml
from flask import Flask, request
load_dotenv()

app = Flask(__name__)

#user is sending something
@app.route('/send', methods = ['POST'])
def incoming_sms():
    #Get the message
    body = request.values.get('Body', None);
    resp = MessagingResponse();
    if(!isValid(body)):
        resp.message("Invalid Command")
    else:
        resp.message("Your command has been received")
        actualMessage = body.split(' ', 2)[2]
        #TODO: SEND THE ACTUAL MESSAGE

    return str(resp)
        


#Check if a message is a valid command
def isValid(msg):
    #Array of words
    allWords = msg.split(' ')
    if len(allWords < 3):
        return False
    elif allWords[0].lower() != "relay":
        return False
    elif !isNetwork(allWords[1]):
        return False
    else return True

#If msg is a valid social network
def isNetwork(msg):
    #Our only valid social network rn
    if msg.lower() == 'messenger':
        return True;
    #We add more social networks here later
    else return False;
    
    
    
