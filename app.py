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

            if witResp['entities'].get('greetings'):
                greetingsConf = float(witResp['entities']['greetings'][0]['confidence'])
                if greetingsConf > 0.85:
                    flagHello = 1

            if witResp['entities'].get('email'):
                emailConf = float(witResp['entities']['email'][0]['confidence'])
                if emailConf > 0.85:
                    emailAddress = str(witResp['entities']['email'][0]['value'])
                    flagEmail = 1
                    #botAnswer = api.messages.create(roomId=SPACE_ID, text=str(emailAddress))

            if witResp['entities'].get('add_user_intent'):
                addUserConf = float(witResp['entities']['add_user_intent'][0]['confidence'])
                if addUserConf > 0.85:
                    flagAdd = 1
                    

            if witResp['entities'].get('remove_user_intent'):
                removeUserConf = float(witResp['entities']['remove_user_intent'][0]['confidence'])
                if removeUserConf > 0.85:
                    flagRemove = 1

            if (flagAdd == 1) and (flagEmail == 1):
                participantAdded = api.memberships.create(roomId=SPACE_ID, personEmail=str(emailAddress), isModerator=False)
                textAnswer = 'I have added <@personEmail:' + str(emailAddress) + '> to the space.'
                botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)
                flagAdd = 0
                flagEmail = 0

            elif (flagRemove == 1) and (flagEmail == 1):
                textAnswer = 'I will do you the honor of removing <@personEmail:' + str(emailAddress) + '> yourself.'
                botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)
                flagRemove = 0
                flagEmail = 0

            elif (flagAdd == 1) or (flagRemove == 1):
                textAnswer = 'I will need you to type an e-mail address.'
                botAnswered = api.messages.create(roomId=SPACE_ID, text=textAnswer)

            elif flagHello == 1:
                textAnswer = 'Hello <@personEmail:' + str(jsonAnswer['data']['personEmail']) + '>'
                botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)
                flagHello = 0

            else:
                textAnswer = 'I am sorry but I am not sure that I understand. I am really not that smart. I can only **add** or **remove** a participant from this space.'
                botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)




            

            #textAnswer = 'Hello <@personEmail:' + str(jsonAnswer['data']['personEmail']) + '>'

            #tryError = str(type(sparkMessage))

            #botAnswer = api.messages.create(roomId=SPACE_ID, text=sparkMessage)
            #botAnswer2 = api.messages.create(roomId=SPACE_ID, text=tryError)
            #botAnswer2 = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)

    return 'OK'

if __name__ == '__main__':
    app.run()
