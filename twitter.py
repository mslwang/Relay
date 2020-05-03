import twitter

# Recipient username goes here
twitter_handle = ''

# User API keys (fetched from database)
consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''

#Fetch message content from the POST request
message = ''

api = twitter.Api(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token_key,
    access_token_secret=access_token_secret)

#CODE TO POST A TWEET
api.PostUpdate(message)

#CODE TO SEE NEW TWEETS
api.PostDirectMessage(message, screen_name=twitter_handle)

#CODE TO SEE 5 DIRECT MESSAGES. Can be modified to make it since x message or y total messages
api.GetDirectMessages(since_id=None, count=5)
