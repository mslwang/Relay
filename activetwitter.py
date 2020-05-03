#every x seconds, scan the list of active twitter users
# and if there are any changes from before, message the user with the new changes
import json
import twitter
from pymongo import MongoClient
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import credentials
import schema as sch
from twilio.rest import Client as twilClient
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse
from twilio import twiml
from logzero import logger as log

connect(credentials.dbUrl)
client = MongoClient(credentials.dbUrl).Relay.user

#infinite loop baby
#while True:
active_users = client.find({"active":'twitter'})
log.info(active_users)

for user in active_users:
    # User API keys (fetched from database)
    consumer_key = credentials.consumer_key #user.api_key
    consumer_secret = credentials.consumer_secret #user.api_secret_key
    access_token_key = credentials.access_token_key #user.access_token
    access_token_secret = credentials.access_token_secret #user.access_secret_key
    lastmsgid = user['twitter_login']['last_msg']

    log.info(lastmsgid)

    api = twitter.Api(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret)

    account_sid = credentials.twil_account_id
    auth_token = credentials.twil_auth_token
    twilioClient = twilClient(account_sid, auth_token)

    newmsgid = api.GetDirectMessages(return_json=True, count = 1)['events'][0]['id']
    log.info(newmsgid)

    if(newmsgid != lastmsgid):
        #TODO SEND SMS WITH:
        #This is a JSON with all the messages since the lastmsg
        newMessages = api.GetDirectMessages(return_json=True, since_id=lastmsgid)

        recipient = user['_id']
        log.info(recipient)

        sch.User.objects.raw({'_id': '{}'.format(recipient)}).update({"$set": {"twitter_login.last_msg": '{}'.format(newmsgid)}})

        for msg in newMessages['events']:
            #Message body
            actualContent = msg['message_create']['message_data']['text']
            #Sender name
            user = api.GetUser(user_id = msg['message_create']['sender_id'])
            name = user.name

            message = twilioClient.messages.create(
                body=actualContent + " was sent from " + name,
                from_ = credentials.twil_number,
                to = recipient
            )
