<<<<<<< HEAD
from pymongo import MongoClient
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import os
from dotenv import load_dotenv

=======
from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import fields, MongoModel, EmbeddedMongoModel
>>>>>>> 3d8b1fc91641b33a82b075711b03d9653a60b259

class Account(EmbeddedMongoModel):
    """
    Schema for account information

    Properties:

<<<<<<< HEAD
    integration -- integration
=======
    platform -- platform
>>>>>>> 3d8b1fc91641b33a82b075711b03d9653a60b259
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
<<<<<<< HEAD
    integration = fields.CharField(required=True, choices=['messenger'])
    username = fields.CharField(required=True)
    utype = fields.CharField(required=True, choices=['username', 'email'])
=======
    platform = fields.CharField(choices=('MESSENGER'), required=True)
    username = fields.CharField(required=True)
    utype = fields.CharField(choices=('USERNAME', 'EMAIL'), required=True)
>>>>>>> 3d8b1fc91641b33a82b075711b03d9653a60b259
    password = fields.CharField(required=True)

class User(MongoModel):
    """
    Schema for a user

    Properties:

<<<<<<< HEAD
    phone_number -- note: will represent unique id
            type: String
             
    email -- email
             type: Email
=======
    email -- note: will represent unique id
            type: String
             
>>>>>>> 3d8b1fc91641b33a82b075711b03d9653a60b259
    
    first_name -- First name
                    type: String

    last_name --  Last name
                type: String

    accounts -- List of accounts
                type: List(Account)
    """
<<<<<<< HEAD
    phone_number = fields.CharField(primary_key=True, required=True)
    email= fields.EmailField(required=True)
    first_name = fields.CharField(required=True)
    last_name = fields.CharField(required=True)
    accounts = fields.EmbeddedDocumentListField(Account)

def initial():
    load_dotenv()
    connect(os.getenv("CONNECT"))
    client = MongoClient(os.getenv("CONNECT"))
    print("Done")
    return client.Relay

=======
    email = fields.EmailField(primary_key=True, required=True)
    first_name = fields.CharField(required=True)
    last_name = fields.CharField(required=True)
    accounts = fields.EmbeddedDocumentListField(Account)
>>>>>>> 3d8b1fc91641b33a82b075711b03d9653a60b259
