from flask import Flask, request
from ciscosparkapi import CiscoSparkAPI
import json
import requests
import csv
import base64
import re

import io
#import pytesseract
from PIL import Image
# Imports the Google Cloud client library
#from google.cloud import vision
#from google.cloud.vision import types

app = Flask(__name__)

#export GOOGLE_APPLICATION_CREDENTIALS="./cloudvisionkeyfile.json"
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./cloudvisionkeyfile.json"


#BOT_TOKEN = 'OTc5OGY3YjEtM2I4OC00ZjhiLTg5YjMtYzU1NTdkOGM4NTViMTg0ZDYxYzMtOTRm'
BOT_TOKEN = 'OTc5OGY3YjEtM2I4OC00ZjhiLTg5YjMtYzU1NTdkOGM4NTViMTg0ZDYxYzMtOTRm'
MY_TOKEN = 'Zjk5ODUzN2QtN2FlOS00ODQ0LWI0NTgtOWQ3MjY5MmU5ZmQ0NGZhNDY4ZTEtNTli'
SPACE_ID = 'Y2lzY29zcGFyazovL3VzL1JPT00vZjUwNjZjZTAtZjYxMy0xMWU3LTkyYTgtYjNiNGFhZDUxNzIy'
BROKERBOT_ID = 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS8zMWJlZTdjZi1mNTlmLTRlYjgtYmY5Ny1jZjkxOWYxMjRhZDY'
#EVENT_ID = 'JDJhJDEwJEFkZ1pQcks5Vkc0cUduNnUwaEoucGVMYmZRa3N3WFc2czYveEFoTXV0eEVwT0lmLkxGbIIO'
EVENT_ID = 'JDJhJDEwJEhlTHg5U3JRRFIzNXFWZWVZUjk2UU84VGZLZktBTjQ1Nk0zN3BVamNSbkV5NmhWVjN2MFcu4'
GOOGLE_TOKEN = 'AIzaSyB2pRywaLOUcO2ddwlTNJAUmanxByZvvKc'

api = CiscoSparkAPI(access_token=BOT_TOKEN)

# Instantiates a client
#client = vision.ImageAnnotatorClient()


def setSparkHeader():
    sparkHeader = {'Authorization': "Bearer " + MY_TOKEN}
    return sparkHeader
    

def postSparkMessage(personId, message):
    message = {"toPersonId":personId,"text":message}
    url = "https://api.ciscospark.com/v1/messages"
    sparkHeader = setSparkHeader()
    postResponse = requests.request("POST", url, data=message, headers=sparkHeader)
    print("POST message: ", postResponse.json())

def postGoogleOCR(image):
    #queryString = {"key":GOOGLE_TOKEN}
    headers = {
        'Content-Type': "application/json"
    }
    data = {
        "requests":[
            {
                "image":{
                    "content":image
                },
                "features":[
                    {
                        "type":"TEXT_DETECTION"
                    }
                ]
            }
        ]
    }
    url = "https://vision.googleapis.com/v1/images:annotate?key="+ GOOGLE_TOKEN
    #postResponse = requests.request("POST", url, data=data, headers=headers, params=queryString)
    postResponse = requests.request("POST", url, data=json.dumps(data), headers=headers)
    postResponse = json.loads(postResponse.content)
    return postResponse


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
                textAnswer = 'Hello <@personEmail:' + str(jsonAnswer['data']['personEmail']) + '>, you can send me a picture of a MAC address.'
                botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)

            # If the message comes with a file
            else:
                sparkMsgFileUrl = str(sparkMessage.files[0]) # Get the URL of the first file

                sparkHeader = {'Authorization': "Bearer " + BOT_TOKEN}

                with requests.Session() as s: # Creating a session to allow several HTTP messages with one TCP connection
                    getResponse = s.get(sparkMsgFileUrl, headers=sparkHeader) # Get file

                    # If the file extension is CSV
                    if str(getResponse.headers['Content-Type']) == 'image/jpeg':
                        #decodedContent = getResponse.content.decode('utf-8')
                        #csvFile = csv.reader(decodedContent.splitlines(), delimiter=',')
                        #listEmails = list(csvFile)
                        #img = Image.open(io.BytesIO(getResponse.content))
                        encodedImg = base64.b64encode(getResponse.content)
                        encodedImgUtf8 = encodedImg.decode('utf-8')

                        imgText = postGoogleOCR(encodedImgUtf8)
                        imgText = imgText['responses'][0]['textAnnotations'][0]['description']

                        p = re.compile('([0-9A-F]{2}[:-]){5}([0-9A-F]{2})|([0-9A-F]{12})', re.IGNORECASE)

                        macAddr = re.findall(p, imgText)




                        # print( type(img) ) # <class 'PIL.JpegImagePlugin.JpegImageFile'>
                        #imgText = pytesseract.image_to_string(img)
                         
                        #image = types.Image(content=img)

                        #response = client.text_detection(image=image)
                        #text = response.text_annotations


                       
                        botAnswered = api.messages.create(roomId=SPACE_ID, text=str(macAddr))
                                


                    # If the attached file is not a CSV
                    #else:
                    #    textAnswer = 'Sorry, I only understand **CSV** files.'
                    #    botAnswered = api.messages.create(roomId=SPACE_ID, markdown=textAnswer)


    return 'OK'

if __name__ == '__main__':
    app.run()
