# Created by Omer Shwartz (www.omershwartz.com)
#
# This script uses service credentials to modify device configuration over REST API of Google Cloud.
# Using this code a server can change the configuration of the device.
#
# This file may contain portions of cloudiot_mqtt_example.py licensed to Google
# under the Apache License, Version 2.0. The original version can be found in
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/iot/api-client/mqtt_example/cloudiot_mqtt_example.py
#
############################################################

import base64
import datetime
import json

import googleapiclient
import jwt
import requests
from google.oauth2 import service_account
from googleapiclient import discovery

service_account_json = 'iot-project1-485dd52bafd4.json' # Location of the server service account credential file
device_id = 'my-ubunto-device'  # Enter your Device ID here
project_id = 'iot-project1-189016'  # Enter your project ID here
registry_id = 'registery1'  # Enter your Registry ID here


# Unless you know what you are doing, the following values should not be changed
cloud_region = 'us-central1'
###

device_name = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
    project_id, cloud_region, registry_id, device_id)


def get_client():
    """Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(
        discovery_api, api_version)

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials)


                      
def sendConfigurationToclient(configuration_payload):
	body = {"versionToUpdate": "0", "binaryData": base64.urlsafe_b64encode(configuration_payload)}
	print get_client().projects().locations().registries().devices().modifyCloudToDeviceConfig(name=device_name,body=body).execute()


