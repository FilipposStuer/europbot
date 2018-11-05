from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from flask import Flask, request
import json
from ciscosparkapi import CiscoSparkAPI
import time
import re
pattern = re.compile("([cC]reate room[\s]{0,1})(?s)([\s\w]*$)")
add_p = re.compile("([aA]dd a person to a team[\s])(?s)(([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4}))[\s]([\w]*$)")
app = Flask(__name__)
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))


@app.route("/hello")
def hello_world():
    return "Hello"


# Receive POST from Webex Teams Space
@app.route('/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        api = CiscoSparkAPI(access_token="ZmZjODhhNWUtOGIxZi00Y2NlLTk1MDYtNzBkMDhlYjdmMmUyNzQ3MWZiMzUtYzFj")
        conversations = api.rooms.list(max=1, sortBy="lastactivity")
        conversations = list(conversations)
        conversations = conversations[0]
        creator_id = conversations.creatorId
        jsonAnswer = json.loads(request.data)
        last_message=api.messages.get(messageId="{0}".format(jsonAnswer["data"]["id"]))
        match = re.search(pattern, last_message.text)
        match_add=re.search(add_p, last_message.text)
        if str(jsonAnswer["data"]["personEmail"]) != "europaUn@webex.bot":
            if last_message.text == "Delete current event":
                now = datetime.datetime.utcnow().isoformat() + 'Z'
                future = datetime.datetime.utcnow() + datetime.timedelta(seconds=1)
                now_1 = future.isoformat() + 'Z'


                print("The next meeting")
                events_result = service.events().list(calendarId='primary',timeMin=now, timeMax=now_1, singleEvents=True,
                                                      orderBy='startTime', maxResults=1).execute()
                events = events_result.get('items', [])

                if not events:
                    api.messages.create(toPersonId="{}".format(creator_id), text="No events planned")
                else:
                    for event in events:
                        start = event['start'].get('dateTime', event['start'].get('date'))
                        print(event)
                        message_string = start
                        api.messages.create(toPersonId="{}".format(creator_id),text="{0}".format(message_string))
                        print (events)
                        api.messages.create(toPersonId="{}".format(creator_id),text="Are you sure you want to delete that event")
                        time.sleep(10)
                        api = CiscoSparkAPI(access_token="ZmZjODhhNWUtOGIxZi00Y2NlLTk1MDYtNzBkMDhlYjdmMmUyNzQ3MWZiMzUtYzFj")
                        conversations = api.rooms.list(max=1, sortBy="lastactivity")
                        conversations = list(conversations)
                        conversations = conversations[0]
                        creator_id = conversations.creatorId

                        if last_message.text == "Yes":
                            service.events().delete(calendarId="primary",eventId="{0}".format(event.id)).execute()

                            api.messages.create(toPersonId="{}".format(creator_id),text="OK")

            elif last_message.text == "Goodbye" or last_message.text == "goodbye":
                api.messages.create(toPersonId="{}".format(creator_id), text="Thank you come again")

            elif match_add:

                api.memberships.create(roomId="{}".format(match_add.group(2)), personEmail="{}".format(match_add.group(7)))

            elif last_message.text == "Help" or last_message.text == "help":
                api.messages.create(toPersonId="{0}".format(creator_id),
                                    text="The commands are as follows: Hello , What is my ID, Create room and Add a person to a room")
            elif last_message.text == "hello" or last_message.text == "Hello" or last_message.text == "Hi":
                api.messages.create(toPersonId="{0}".format(creator_id),
                                    text="Hello, what can I help you with(Type help for a list of comands)")
            elif last_message.text == "What is my ID" or last_message.text == "What is my Id" or last_message.text == "What is my id" or last_message.text == "what is my id" or last_message.text == "What is my ID" or last_message.text == "what is my Id" or last_message.text == "what is my ID":
                api.messages.create(toPersonId="{0}".format(creator_id), text="Your id is:")
                api.messages.create(toPersonId="{0}".format(creator_id), text="{0}".format(creator_id))
            elif match:
                room_id = api.rooms.create(title="{0}".format(match.group(2)), teamId=None)
                api.messages.create(toPersonId="{}".format(creator_id), text="The rooms Id is:{}".format(room_id.id))
                api.memberships.create(roomId="{0}".format(room_id.id), personId="{0}".format(creator_id))
            else:
                api.messages.create(toPersonId="{0}".format(creator_id), text="Type help")
    return "Ok"


if __name__ == "__main__":
    app.run(port=5000,debug=False)
