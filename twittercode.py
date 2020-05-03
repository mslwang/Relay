import twitter

# Recipient username goes here
twitter_handle = ''
#Recipient id goes here
twitter_id = 0

# User API keys (fetched from database)
consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''

#Fetch message content from the POST request
message = ""

api = twitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token_key,
    access_token_secret=access_token_secret)

#CODE TO POST A TWEET
api.PostUpdate(message)

#CODE TO SEND MESSAGE
print(api.PostDirectMessage(message, user_id=1256753829057462273, return_json=True))
