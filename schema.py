from pymongo import MongoClient
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import os
from dotenv import load_dotenv


class Account(EmbeddedMongoModel):
    """
    Schema for account information

    Properties:

    integration -- integration
                type: String
                options: MESSENGER

    username -- username
                type: String

    utype -- type of the username
             type: String
             options: USERNAME, EMAIL

    password -- password(not hashed)
                type: String
    """
    integration = fields.CharField(required=True, choices=['messenger'])
    username = fields.CharField(required=True)
    utype = fields.CharField(required=True, choices=['username', 'email'])
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
    email= fields.EmailField(required=True)
    accounts = fields.EmbeddedDocumentListField(Account)

def initial():
    load_dotenv()
    connect(os.getenv("CONNECT"))
    client = MongoClient(os.getenv("CONNECT"))
    print("Done")
    return client.Relay

