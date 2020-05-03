#every x seconds, scan the list of active twitter users 
# and if there are any changes from before, message the user with the new changes
import json
import twitter
from pymongo import MongoClient
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import credentials 

connect(credentials.dbUrl)
client = MongoClient(credentials.dbUrl).Relay.users


#infinite loop baby
#while True: 

active_users = client.find({"active":'twitter'})
print(active_users)

#for user in active_users:
    # User API keys (fetched from database)
consumer_key = credentials.consumer_key
consumer_secret = credentials.consumer_secret
access_token_key = credentials.access_token_key
access_token_secret = credentials.access_token_secret

api = twitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token_key,
    access_token_secret=access_token_secret)




#CODE TO SEE 5 DIRECT MESSAGES. Can be modified to make it since x message or y total messages
last_message = json.loads(api.GetDirectMessages(return_json=True, count = 1))