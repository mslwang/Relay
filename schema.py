from pymongo import MongoClient
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import credentials  

class TwitterAccount(MongoModel):
    """
    Schema for a twitter user

    Properties:

    phone_number -- note: will represent unique id
            type: String
             
    access_token -- access token
             type: String

    access_token_secret -- access token secret
                            type: String

    api_key -- api key
                type: String
    
    api_secret_key -- api secret key
                      type: String
    """
    access_token = fields.CharField(required=True)
    access_token_secret = fields.CharField(required=True)
    api_key = fields.CharField(required=True)
    api_secret_key = fields.CharField(required=True)
    last_msg = fields.BigIntegerField(required=False)

class MessengerAccount(MongoModel):
    """
    Schema for a messenger user

    Properties:

    phone_number -- note: will represent unique id
                    type: String
             
    email -- email
             type: Email

    password -- password
                type: String
    """
    email = fields.EmailField(required=True)
    password = fields.CharField(required=True)

class User(MongoModel):
    """
    Schema for a user
    Properties:
    phone_number -- note: will represent unique id
            type: String
             
    email -- email
             type: Email
    accounts -- List of accounts
                type: List(Account)
    """
    phone_number = fields.CharField(primary_key=True, required=True)
    active = fields.CharField(required=True)
    twitter_login = fields.EmbeddedDocumentField('TwitterAccount')
    messenger_login = fields.EmbeddedDocumentField('MessengerAccount')
