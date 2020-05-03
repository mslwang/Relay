import requests
from flask import Flask, request, send_from_directory
import time
import json
from flask_cors import CORS
import schema as sch

app = Flask(__name__)
CORS(app)

# sample API that gets time, replace with the following API calls:
#   * add new user to mongo
#   * create an endpoint which twilio will call (integrate send.py) 
@app.route('/signup', methods = ['POST'])
def do_signup():
    data = json.loads(request.data)
    integration = data['integration']
    tel = data['tel']
    email = data['email']
    password = data['password']

    # store this in mongo
    sch.User(tel, email=email, accounts=[sch.Account(integration=integration, username=email, utype="email", password=password)]).save()
    print("{}, {}, {}, {}".format(integration, tel, email, password))
    return json.dumps({"status": 200})

if __name__ == "__main__":
    sch.initial()
    app.run(threaded=True, port=5000)
