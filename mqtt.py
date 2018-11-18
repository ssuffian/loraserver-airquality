#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sudo apt install nodejs
import paho.mqtt.client as mqtt #pip install paho-mqtt
from datetime import datetime
import time

import json
import os
############
from python_cayennelpp.decoder import decode #https://github.com/OlegSomov/Python-CayenneLPP
import subprocess

path_name = '.'
file_name = 'messages.csv'
def update_json(path_name, file_name, new_message):
    messages = []
    if 'messages.json' in os.listdir(path_name):
        with open('{}/{}'.format(path_name, file_name),'r') as f:
            messages = json.load(f)
        messages.append(new_message)
    else:
        messages = [new_message]
    with open('{}/{}'.format(path_name, file_name),'w') as f:
        json.dump(messages,f, indent=4)

def update_csv(path_name, file_name, new_row):
    with open('{}/{}'.format(path_name, file_name),'a') as f:
        f.write(new_row)
        
def get_output(payload):
    command = 'node payload_decrypt.js --payload {}'.format(payload)
    node = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)                                                                                                           
    out, err = node.communicate() 
    return out

def decode_payload(out):
    return decode(out.strip().decode('utf-8'))

def get_value_or_none(output, channel):
    list_or_empty = [o['value'] for o in channel if o['channel']==channel]
    return ('' if channel == [] else channel[0])


def on_message(client, userdata, message):
    payload = eval(message.payload.decode("utf-8"))
    if 'phyPayload' in payload:
        phy_payload = payload['phyPayload']
        print(datetime.now()) 
        print(phy_payload)
        output = get_output(phy_payload)
        print(output)
        output = decode_payload(output)
        output_dict = {'{}_{}'.format(row['name'],row['channel']):row['value'] for row in output}
        output_dict['datetime'] = datetime.now().isoformat()
        #update_json(path_name, file_name, output_dict)
        update_csv(path_name, file_name, str(output_dict)+'\n')
########################################
if __name__ == '__main__':
    broker_address="localhost"
    print("creating new instance")
    client = mqtt.Client("P1",clean_session=False) #create new instance
    client.on_message=on_message #attach function to callback
    print("connecting to broker")
    client.connect(broker_address) #connect to broker
    client.loop_start() #start the loop
    topic = 'gateway/c0ee40ffff2939d7/rx'
    print("Subscribing to topic",topic)
    client.subscribe(topic)
    while True:
        time.sleep(1)
    client.loop_stop() #stop the loop

