from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import fields, MongoModel, EmbeddedMongoModel

class Account(EmbeddedMongoModel):
    """
    Schema for account information

    Properties:

    platform -- platform
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
    platform = fields.CharField(choices=('MESSENGER'), required=True)
    username = fields.CharField(required=True)
    utype = fields.CharField(choices=('USERNAME', 'EMAIL'), required=True)
    password = fields.CharField(required=True)

class User(MongoModel):
    """
    Schema for a user

    Properties:

    email -- note: will represent unique id
            type: String
             
    
    first_name -- First name
                    type: String

    last_name --  Last name
                type: String

    accounts -- List of accounts
                type: List(Account)
    """
    email = fields.EmailField(primary_key=True, required=True)
    first_name = fields.CharField(required=True)
    last_name = fields.CharField(required=True)
    accounts = fields.EmbeddedDocumentListField(Account)
