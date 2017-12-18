from flask import Flask, request
from ciscosparkapi import CiscoSparkAPI
from wit import Wit
import json

app = Flask(__name__)


BOT_TOKEN = 'ZjBhYWVlYWUtYTY4NC00MTFiLThhOGItODEzOGYzZDYyNzJiYzJjNGVhNjAtZWM2'
SPACE_ID = 'Y2lzY29zcGFyazovL3VzL1JPT00vYWQ3ODExMDAtZTNmMS0xMWU3LTllYTUtNjFmNzA3MjJlYjkz'
WIT_TOKEN = 'NXZNQT2BEKTEYCT2NHATEDVIKB3HAZTU'

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
            sparkMessage = str(sparkMessage.text) # Get message text
            sparkMessage = sparkMessage.split(botFirstName,1)[1] #Remove bot's first name from message

            witClient = Wit(access_token=WIT_TOKEN) # Create Wit session
            witResp = witClient.message(sparkMessage) # Answer from Wit after sending message in Spark

            
            if witResp['entities'].get('email'):
                emailAddress = str(witResp['entities']['email'][0]['value'])
                emailConf = float(witResp['entities']['email'][0]['confidence'])
                if emailConf > 0.85:
                    botAnswer = api.messages.create(roomId=SPACE_ID, text=str(emailAddress))
                #participantAdded = api.memberships.create(roomId=SPACE_ID, personEmail=str(emailAddress), isModerator=False)

            if witResp['entities'].get('add_user_intent'):
                addUserConf = str(witResp['entities']['add_user_intent'][0]['confidence'])

            if witResp['entities'].get('greetings'):
                greetingsConf = str(witResp['entities']['greetings'][0]['confidence'])
            

            #textAnswer = 'Hello <@personEmail:' + str(jsonAnswer['data']['personEmail']) + '>'

            #tryError = str(type(sparkMessage))

            #botAnswer = api.messages.create(roomId=SPACE_ID, text=sparkMessage)
            #botAnswer2 = api.messages.create(roomId=SPACE_ID, text=tryError)
            #botAnswer2 = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)

if __name__ == '__main__':
    app.run()
