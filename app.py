from flask import Flask
from ciscosparkapi import CiscoSparkAPI
import time
app = Flask(__name__)


while True:

    api = CiscoSparkAPI(access_token="OTg5MTk2ODYtYWM1My00YzNlLTgwYTItYzcwOGIzY2YxZDAyZWQxNGI4ODMtMTRm")
    conversations = api.rooms.list(max=(1),sortBy="lastactivity")
    conversations = list(conversations)
    conversations = conversations[0]
    person = api.people.get(personId="{0}".format(conversations.creatorId))
    messages = api.messages.list(roomId="{0}".format(conversations.id))
    message = list(messages)
    last_message = message[0]
    information = api.people.get(personId="{0}".format(conversations.creatorId))
    persons_id = information.orgId
    if last_message.text == "help":
        api.messages.create(toPersonId="{0}".format(conversations.creatorId), text="The commands are as follows: Hello,What is my IDS ")
    if last_message.text == "hello" or last_message.text == "Hello" or last_message.text == "Hi":
        api.messages.create(toPersonId="{0}".format(conversations.creatorId), text="Hello, what can I help you with(Type help for a list of comands)")
    if last_message.text == "What is my ID"or last_message.text == "What is my Id" or last_message.text == "What is my id":
        api.messages.create(toPersonId="{0}".format(conversations.creatorId), text="Your id is:")
        api.messages.create(toPersonId="{0}".format(conversations.creatorId), text="{0}".format(persons_id))
    if last_message.text == "Create room":
        n=0
        api.messages.create(toPersonId="{0}".format(conversations.creatorId),text="What should the Room be called?")

        while n==0 :
            messages = api.messages.list(roomId="{0}".format(conversations.id))
            message = list(messages)
            last_message = message[0]
            n=last_message.text
            print(n)
            time.sleep(500000000)
        print(n)
        api.messages.create(toPersonId="{0}".format(conversations.creatorId,text="{}hjhkjf"))
    time.sleep(1)


@app.route("/")
def hello_world():
    return "---Id"


@app.route("/rooms")
def rooms():
    return rooms


if __name__ == "__main__":
    app.run()
