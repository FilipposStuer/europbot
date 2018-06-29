from flask import Flask
from ciscosparkapi import CiscoSparkAPI

api = CiscoSparkAPI(access_token="NmQ2ZDE2MDQtMzljNC00Njg1LWI2YTYtZDMxMWU0YThlYmNmNDg3MzUyY2UtNTVl")
person = api.people.get(personId="Y2lzY29zcGFyazovL3VzL1BFT1BMRS9kMDMwYThlYy0zZGE0LTRiMDUtOGQ2OS0yMzIyY2EzZDZhOGE")
print(person.id)

messages = api.messages.list(roomId="Y2lzY29zcGFyazovL3VzL1JPT00vMjQ3ZWZiMmUtODhjZS0zOTgyLWEzZWQtMzQyZTliNzRhNzYx", )
message = list(messages)

# testing
last_message = message[0]
print(last_message.text)

information = api.people.get(personId="Y2lzY29zcGFyazovL3VzL1BFT1BMRS9kMDMwYThlYy0zZGE0LTRiMDUtOGQ2OS0yMzIyY2EzZDZhOGE")
persons_id = information.orgId
print(persons_id)
# the bots responses
if last_message.text == ("What is my ID"):
    api.messages.create(toPersonEmail="filippos.stuer@gmail.com", text="Your id is:")
    api.messages.create(toPersonEmail="filippos.stuer@gmail.com",text="{0}".format(persons_id))
if last_message.text == ("hello") or last_message.text == ("Hello"):
    api.messages.create(toPersonEmail="filippos.stuer@gmail.com", text="Hello, what can I help you with")


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "---Id:{}".format(person.id)


@app.route("/rooms")
def rooms():
    return rooms


if __name__ == "__main__":
    app.run()
