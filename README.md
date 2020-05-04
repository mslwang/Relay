# Relay: Keeping you Connected


# For Developers
* Run `npm install` to install Node dependencies
* Run `pip install -r requirements.txt` to install Python dependencies
* `python server.py` starts the Flask server
* `npm run start` starts the React server


* Don't forget to install python-twitter instead of twitter for the flask dependencies

**Important note**: After installing python-twitter, locate the api.py file (it should tell you where this is being downloaded to as you install python-twitter). Then find the GetDirectMessage function and locate the following code snippet:

``` python
"""
Returns:
    A sequence of twitter.DirectMessage instances
"""
url = '%s/direct_messages.json' % self.base_url
parameters = {
    'full_text': bool(full_text),
    'include_entities': bool(include_entities),
```
Replace the default url with:

``` python
url = '%s/direct_messages/events/list.json' % self.base_url
```
And then you should be good to go!

# Functionality

## Front-End Website: Register Social Meda Integrations
Visit Relayme.online to register for relay and connect your social media accounts to your phone number

## SMS Number: +1 (587) 806-3827
Text *+1 (587) 806-3827* to relay your online social media via SMS. All commands are case insensitive, messages are not


To Switch between Messenger & Twitter:

- "Switch {platform name}" to change platforms
- "Currentmode" to display the currently selected platform


For Messenger:
- "message {recipient name} {message body}" to send a DM
- Notifications for incoming DMs will be sent automatically when Messenger is selected


For Twitter:
- "message {recipient name} {message body}" to send a DM
- Notifications for incoming DMs will be sent automatically when Messenger is selected
- "tweet {tweet message}" to post a tweet

