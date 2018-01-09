from flask import Flask, request
from ciscosparkapi import CiscoSparkAPI
import json
import requests

app = Flask(__name__)


BOT_TOKEN = 'OTEwNTA4MGMtYTQ0OS00NjRlLWFlMTgtYWM4YjMxN2Q5NTcyOWE3MWM5YjgtODU5'
SPACE_ID = 'Y2lzY29zcGFyazovL3VzL1JPT00vYTJhZWI5NzAtZTRiNi0xMWU3LWI2MDQtZmRmZDEyNDAyM2E0'

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

        if str(jsonAnswer['data']['personEmail']) != str(botDetails.emails[0]): # If the message is not sent by the bot

            botName = str(botDetails.displayName) # Get bot's display name
            botFirstName = botName.split(None, 1)[0] # Get bot's "first name"

            sparkMessage = api.messages.get(jsonAnswer['data']['id']) # Get message object text from message ID
            sparkMsgText = str(sparkMessage.text) # Get message text
            sparkMsgText = sparkMsgText.split(botFirstName,1)[1] #Remove bot's first name from message
            sparkMsgFiles = str(sparkMessage.files)

            botAnswered = api.messages.create(roomId=SPACE_ID, text=sparkMsgFiles[0])

            # Answering logic
            '''
            if (flagAdd == 1) and (flagEmail == 1):
                participantAdded = api.memberships.create(roomId=SPACE_ID, personEmail=str(emailAddress), isModerator=False)
                textAnswer = 'I have added <@personEmail:' + str(emailAddress) + '> to the space.'
                botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)

            elif (flagRemove == 1) and (flagEmail == 1):
                textAnswer = 'I will do you the honor of removing <@personEmail:' + str(emailAddress) + '> yourself.'
                botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)

            elif flagAdd == 1:
                textAnswer = 'I will need you to type an e-mail address.'
                botAnswered = api.messages.create(roomId=SPACE_ID, text=textAnswer)

            elif flagRemove == 1:
                textAnswer = 'I will do you the honor of removing the participant yourself.'
                botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)

            elif flagHello == 1:
                textAnswer = 'Hello <@personEmail:' + str(jsonAnswer['data']['personEmail']) + '>'
                botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)

            else:
                textAnswer = 'I am sorry but I am not sure that I understand. I am really not that smart. I can only **add** or **remove** a participant from this space.'
                botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)
            '''



            '''
            sparkHeader = {'Authorization': "Bearer " + BOT_TOKEN}
            getResponse = requests.request("GET", "https://api.ciscospark.com/v1/people/me", headers=sparkHeader)
            getResponse.text
            getResponse.content
            '''



    return 'OK'

if __name__ == '__main__':
    app.run()
