from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from twilio import twiml


app = Flask(__name__)

@app.route('/send', methods = ['POST'])


#User receives messages from social media
@app.route('/receive', methods = ['POST'])
