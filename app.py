from flask import Flask, request
from ciscosparkapi import CiscoSparkAPI
import json

app = Flask(__name__)


BOT_TOKEN = 'ZjBhYWVlYWUtYTY4NC00MTFiLThhOGItODEzOGYzZDYyNzJiYzJjNGVhNjAtZWM2'
SPACE_ID = 'Y2lzY29zcGFyazovL3VzL1JPT00vYWQ3ODExMDAtZTNmMS0xMWU3LTllYTUtNjFmNzA3MjJlYjkz'

api = CiscoSparkAPI(access_token=BOT_TOKEN)


@app.route('/')
def hello():
    return "Hello World!"

# Receive POST from Spark Space
@app.route('/sparkhook', methods=['POST'])
def sparkhook():

    if request.method == 'POST':

        jsonAnswer = json.loads(request.data) # Format data from POST into JSON

        botDetails = api.people.me() # Get details of the bot from its token

        if str(jsonAnswer["data"]["personEmail"]) != str(botDetails.emails[0]): # If the message is not sent by the bot

            botName = str(botDetails.displayName)
            botFirstName = botName.split(None, 1)[0]

            sparkMessage = str(api.messages.get(jsonAnswer["data"]["id"]))
            sparkMessage = sparkMessage.split(botFirstName,1)[1] #Remove bot's first name from message

            botAnswer = api.messages.create(roomId=SPACE_ID, text='Hello Sir')

if __name__ == '__main__':
    app.run()
