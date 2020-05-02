#from fbchat import Client as fbClient
#from fbchat.models import *

from flask import Flask, request
from twilio.rest import Client as twilClient
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from twilio import twiml

import twilio_creds as twil_creds

#User receives messages from social media
@app.route('/receive', methods = ['POST'])
def handler():

    #Placeholders
    to = '+14167069819'
    body = 'placeholder'

    client = twilClient(twil_creds.twil_account_id, twil_creds.twil_auth_token)

    message = client.messages \
        .create (
            body=body,
            from_=twil_creds.twil_number,
            to=to
        )

    print(message.sid)