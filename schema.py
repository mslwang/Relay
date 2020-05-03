from pymongo import MongoClient
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import os
from dotenv import load_dotenv

class Twitter(MongoModel):
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
    phone_number = fields.CharField(primary_key=True, required=True)
    access_token = fields.CharField(required=True)
    access_token_secret = fields.CharField(required=True)
    api_key = fields.CharField(required=True)
    api_secret_key = fields.CharField(required=True)
    active = fields.BooleanField(required=True)
    

class Messenger(MongoModel):
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
    phone_number = fields.CharField(primary_key=True, required=True)
    email = fields.EmailField(required=True)
    password = fields.CharField(required=True)
    active = fields.BooleanField(required=True)

def initial():
    load_dotenv()
    connect(os.getenv("CONNECT"))
    client = MongoClient(os.getenv("CONNECT"))
    return client.Relay

