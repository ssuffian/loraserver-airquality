#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sudo apt install nodejs
import paho.mqtt.client as mqtt #pip install paho-mqtt
from datetime import datetime, timedelta
import time

import json
import os
############
from python_cayennelpp.decoder import decode #https://github.com/OlegSomov/Python-CayenneLPP
import subprocess

output_path = '../data_output'
node_path = '../node_for_lora_decrypt'
file_name = 'messages.csv'
def update_json(output_path, file_name, new_message):
    messages = []
    if 'messages.json' in os.listdir(output_path):
        with open('{}/{}'.format(output_path, file_name),'r') as f:
            messages = json.load(f)
        messages.append(new_message)
    else:
        messages = [new_message]
    with open('{}/{}'.format(output_path, file_name),'w') as f:
        json.dump(messages,f, indent=4)

def update_csv(output_path, file_name, new_row):
    with open('{}/{}'.format(output_path, file_name),'a') as f:
        f.write(new_row)
        
def get_output(payload):
    command = 'node {}/payload_decrypt.js --payload {}'.format(node_path, payload)
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
        #update_json(output_path, file_name, output_dict)
        update_csv(output_path, file_name, str(output_dict)+'\n')
########################################
if __name__ == '__main__':
    log_check = datetime.now()
    print("Start {}".format(datetime.now().isoformat()))
    while True:
        current_time = datetime.now()
        time.sleep(1)
        print(current_time)
        print(log_check)
        if current_time > log_check + timedelta(seconds=1):
            log_check = datetime.now()
            print("Update {}".format(datetime.now().isoformat()))

