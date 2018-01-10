from flask import Flask, request
from ciscosparkapi import CiscoSparkAPI
import json
import requests
import csv

app = Flask(__name__)


BOT_TOKEN = 'NWI0ZmVhZjktM2ZlMy00YWQ1LTgyYjYtMzEyZWQ2NGVhMTg0MWRmMTc0OWUtYWEy'
SPACE_ID = 'Y2lzY29zcGFyazovL3VzL1JPT00vNzUzY2ZkYTAtZjVkNS0xMWU3LTgyZTUtMmRmOGYwZGY4ZWQw'

api = CiscoSparkAPI(access_token=BOT_TOKEN)


@app.route('/')
def hello():
    return 'Hello World!'

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

            #botAnswered = api.messages.create(roomId=SPACE_ID, text=sparkMsgFileUrl)

            if not sparkMessage.files:
                textAnswer = 'Hello <@personEmail:' + str(jsonAnswer['data']['personEmail']) + '>, you can send me a CSV file including a list of e-mail addresses and I will add them to this space.'
                botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)

            else:
                sparkMsgFileUrl = str(sparkMessage.files[0])

                sparkHeader = {'Authorization': "Bearer " + BOT_TOKEN}
                i = 0 #Index to skip title row in the CSV file

                with requests.Session() as s:
                    getResponse = s.get(sparkMsgFileUrl, headers=sparkHeader)

                    if str(getResponse.headers['Content-Type']) == 'text/csv':
                        decodedContent = getResponse.content.decode('utf-8')
                        csvFile = csv.reader(decodedContent.splitlines(), delimiter=';')
                        listEmails = list(csvFile)
                        for row in listEmails:
                            if i != 0:
                                participantAdded = api.memberships.create(roomId=SPACE_ID, personEmail=str(row[2]), isModerator=False)
                            i += 1

                    else:
                        textAnswer = 'Sorry, I only understand **CSV** files.'
                        botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)


    return 'OK'

if __name__ == '__main__':
    app.run()
