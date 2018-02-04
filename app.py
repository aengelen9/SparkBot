from flask import Flask, request
from ciscosparkapi import CiscoSparkAPI
import json
import requests
import csv

app = Flask(__name__)


#BOT_TOKEN = 'OTc5OGY3YjEtM2I4OC00ZjhiLTg5YjMtYzU1NTdkOGM4NTViMTg0ZDYxYzMtOTRm'
BOT_TOKEN = 'OTc5OGY3YjEtM2I4OC00ZjhiLTg5YjMtYzU1NTdkOGM4NTViMTg0ZDYxYzMtOTRm'
MY_TOKEN = 'Zjk5ODUzN2QtN2FlOS00ODQ0LWI0NTgtOWQ3MjY5MmU5ZmQ0NGZhNDY4ZTEtNTli'
SPACE_ID = 'Y2lzY29zcGFyazovL3VzL1JPT00vZjUwNjZjZTAtZjYxMy0xMWU3LTkyYTgtYjNiNGFhZDUxNzIy'
BROKERBOT_ID = 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS8zMWJlZTdjZi1mNTlmLTRlYjgtYmY5Ny1jZjkxOWYxMjRhZDY'
EVENT_ID = 'JDJhJDEwJEFkZ1pQcks5Vkc0cUduNnUwaEoucGVMYmZRa3N3WFc2czYveEFoTXV0eEVwT0lmLkxGbIIO'



import requests

URL = 'https://api.ciscospark.com/v1/messages'
ACCESS_TOKEN = '<your_access_token>'
ROOM_ID = '<room_id>'
MESSAGE_TEXT = '<message_text>'

headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN,
           'Content-type': 'application/json;charset=utf-8'}
post_data = {'roomId': ROOM_ID,
             'text': MESSAGE_TEXT}
response = requests.post(URL, json=post_data, headers=headers)
if response.status_code == 200:
    # Great your message was posted!
    message_id = response.json['id']
    message_text = response.json['text']
    print("New message created, with ID:", message_id)
    print(message_text)
else:
    # Oops something went wrong...  Better do something about it.
    print(response.status_code, response.text)

api = CiscoSparkAPI(access_token=BOT_TOKEN)


def setSparkHeader():
    sparkHeader = {'Authorization': "Bearer " + MY_TOKEN}
    return sparkHeader
    

def postSparkMessage(personId, message):
    message = {"toPersonId":personId,"text":message}
    url = "https://api.ciscospark.com/v1/messages"
    sparkHeader = setSparkHeader()
    postResponse = requests.request("POST", url, data=message, headers=sparkHeader)
    print("POST message: ", postResponse.json())


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
            sparkMsgText = sparkMsgText.split(botFirstName,1)[1] # Remove bot's first name from message

            # Say hello if the message doesn't contain a file
            if not sparkMessage.files:
                textAnswer = 'Hello <@personEmail:' + str(jsonAnswer['data']['personEmail']) + '>, you can send me a CSV file including a list of e-mail addresses and I will assign them a pod.'
                botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)

            # If the message comes with a file
            else:
                sparkMsgFileUrl = str(sparkMessage.files[0]) # Get the URL of the first file

                sparkHeader = {'Authorization': "Bearer " + BOT_TOKEN}
                i = 0 # Index to skip title row in the CSV file

                with requests.Session() as s: # Creating a session to allow several HTTP messages with one TCP connection
                    getResponse = s.get(sparkMsgFileUrl, headers=sparkHeader) # Get file

                    # If the file extension is CSV
                    if str(getResponse.headers['Content-Type']) == 'text/csv':
                        decodedContent = getResponse.content.decode('utf-8')
                        csvFile = csv.reader(decodedContent.splitlines(), delimiter=',')
                        listEmails = list(csvFile)
                        for row in listEmails: # Creating one list for each line in the file
                            if i != 0:
                                #participantAdded = api.memberships.create(roomId=SPACE_ID, personEmail=str(row[5]), isModerator=False) # Add participant from e-mail field
                                botAnswered = api.messages.create(roomId=SPACE_ID, text=str(row[4]))
                            i += 1
                        msgString = 'events set ' + EVENT_ID
                        brokerBotMsg = postSparkMessage(BROKERBOT_ID, msgString)


                    # If the attached file is not a CSV
                    else:
                        textAnswer = 'Sorry, I only understand **CSV** files.'
                        botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)


    return 'OK'

if __name__ == '__main__':
    app.run()
