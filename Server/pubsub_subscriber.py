# Created by Omer Shwartz (www.omershwartz.com)
#
# This script uses service credentials to subscribe to a topic of the Pub/Sub broker residing in
# Google Cloud.
# Using this code a server can receive messages from the device.
#
# This file may contain portions of cloudiot_mqtt_example.py licensed to Google
# under the Apache License, Version 2.0. The original version can be found in
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/iot/api-client/mqtt_example/cloudiot_mqtt_example.py
#
############################################################

import time
import os


#our imports start:
import base64
import math
import random, string
import json
import face_recognition
import threading
from set_device_configuration import sendConfigurationToclient
import threading
from queue import *
#our importss end^

from google.cloud import pubsub
from oauth2client.service_account import ServiceAccountCredentials


topic_name = 'imagestopic'  # Enter your topic name here
project_id = 'iot-project1-189016'  # Enter your project ID here
subscription_name = 'subscriptionnametmp'  # Can be whatever, but must be unique (for the topic?)
service_account_json = 'iot-project1-485dd52bafd4.json' # Location of the server service account credential file


def on_message(message):
	"""Called when a message is received"""
	print('Received message: {}'.format(message))
	#our code start:
	check_incoming_message(message)
	#our code end^

	message.ack()



# Ugly hack to get the API to use the correct account file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_json

# Create a pubsub subscriber
subscriber = pubsub.SubscriberClient()

topic = 'projects/{project_id}/topics/{topic}'.format(
    project_id=project_id,
    topic=topic_name,
)

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=project_id,
    sub=subscription_name,
)

# Try to delete the subscription before creating it again
try:
    subscriber.delete_subscription(subscription_name)
except: # broad except because who knows what google will return
    # Do nothing if fails
    None

# Create subscription
subscription = subscriber.create_subscription(subscription_name, topic)

# Subscribe to subscription
print "Subscribing"
subscriber.subscribe(subscription_name, callback=on_message)


#################################################################
#			Our Code Start				#
#################################################################
#get an image from  a device via mqtt isawsomeone
RequestType = {"TEXT": 0, "IMAGE_TO_RECOGNIZE": 1, "IMAGE_TO_ADD": 2}
responesQueue = Queue()

global sendResponseEvt

def sendResponesWork():
	global sendResponseEvt
	sendResponseEvt = False
	while True:
		if sendResponseEvt == True:
			payload = responesQueue.get()
			sendConfigurationToclient(payload)
			responesQueue.task_done()
			time.sleep(1) #the difference between two configurations has to be at list 1 sec
			sendResponseEvt = False

#responseSenderThread = threading.Thread(target=sendResponesWork, args=())
#responseSenderThread.start()

global CurrMsg
CurrMsg = ""

def check_incoming_message(message):
	global CurrMsg
	messagedata = message.data
	messagedatadict = json.loads(messagedata)
	if messagedatadict['data'] != "done":
		CurrMsg = CurrMsg + messagedatadict['data']
	else:
		print "done"
		messagedatadict['data'] = CurrMsg
		CurrMsg = ""
		print str(len(messagedatadict['data'])) + " " + messagedatadict['imagename']
		messagereqtpe = messagedatadict['reqtype']
		if(messagereqtpe == RequestType['TEXT']):
			pass
		elif (messagereqtpe == RequestType['IMAGE_TO_RECOGNIZE']):
			#threading.Thread(target=recognizeImageAndPutResInQueue, args=(messagedatadict,)).start()
			recognizeImageAndPutResInQueue(messagedatadict)

		elif (messagereqtpe == RequestType['IMAGE_TO_ADD']):
			saveimage(messagedatadict, "Registered Users")
	
def recognizeImageAndPutResInQueue(messagedatadict):
	global sendResponseEvt
	saveimage(messagedatadict, "Unknown Person")
		
	imagename = messagedatadict['imagename']
	imageid = messagedatadict['pic_id']
	isExists = isPersonExists(messagedatadict, "Unknown Person/" + imagename,"Registered Users")	
	
	payload = "image: " + imagename + " | isExists: " + str(isExists) + " | id: " + imageid
	responesQueue.put(payload)
	sendResponseEvt = True
	threading.Thread(target=sendConfigurationToclient, args=(payload,)).start()		

def isPersonExists(messagedatadict, pathToImage, pathToRegisteredUsers):
	picture_of_me = face_recognition.load_image_file(pathToImage)
	if len(face_recognition.face_encodings(picture_of_me)) > 0:
		my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

		# my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!
		listnameofimages = os.listdir(pathToRegisteredUsers)
		isFaceExistInRegisteredUsers = False
		for imagename in listnameofimages:
			unknown_picture = face_recognition.load_image_file(pathToRegisteredUsers + "/" + imagename)
			unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

			# Now we can see the two face encodings are of the same person with `compare_faces`!

			results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

			if results[0] == True:
				print("Image: " + imagename + "- has the same person!")
				return True
			else:
				print("Image: " + imagename + " - isn't the same person...")


def saveimage(messagedatadict, pathToFolder):
	
	if not os.path.exists(pathToFolder):
		os.makedirs(pathToFolder)

	image_64_decode = base64.b64decode(messagedatadict['data']) 
	saveInFolder(image_64_decode, pathToFolder, messagedatadict['imagename'])


def saveInFolder(image_64_decode, pathToFolder, imageName):
	image_result = open(pathToFolder + '/' + imageName, 'wb') # create a writable image and write the decoding result
	image_result.write(image_64_decode)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#			Our Code End				#
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



# Keep the main thread alive
while True:
    time.sleep(1000)
