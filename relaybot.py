from fbchat import Client
from fbchat.models import *
from datetime import datetime

from twilio.rest import Client as twilClient
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from twilio import twiml

import credientials
import getpass

sms = twilClient(credentials.twil_account_id, credentials.twil_auth_token)

class RelayBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        # TODO: store in dict for faster lookup
        user = client.fetchUserInfo(author_id)[author_id]

        message = "{}: {}".format(user.name, message_object.text) 
        
        sms.messages.create \
        (
            body = message,
            from_ = credentials.twil_number,
            to = phoneNumber
        )
