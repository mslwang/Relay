from fbchat import Client
from fbchat.models import *
import getpass

print("Please enter your password:")
client = Client('kelvin.zhang@uwaterloo.ca', getpass.getpass())

print("Logged with id: {}".format(client.uid))

cmds = {
        "getfriends": "",
        "msg {name} {msg}": "send message to friend",
        "getactivechats": "print a list of active chats"
    }
print("Please enter a command. Type help for list of commands")
prompt = "Enter a command: "
cmd = str(raw_input(prompt)) 

ids = dict()

while cmd: 
    if cmd == "help":
        print("----- HELP ------")
        for key, val in cmds.items():
            print("{}: {}".format(key, val))
        print("-----------------")
    elif cmd == "getactivechats":
        users = client.fetchAllUsers()
        for user in users:
            print("{}: {}".format(user.name, user.uid))
    elif cmd.startswith("msg"):
        args = cmd.split(" ")
        if len(args) < 3:
            print("Invalid arguments")
            continue
        name = args[1]
        message = args[2]
        user = client.searchForUsers(name)[0]
        userId = user.uid
        targetType = ThreadType.USER
        
        client.send(Message(text=message), thread_id=userId, thread_type=targetType)
    cmd = str(raw_input(prompt))

client.logout()
