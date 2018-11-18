#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt #pip install paho-mqtt

if __name__ == '__main__':
    broker_address="localhost"
    print("creating new instance")
    client = mqtt.Client("P1",clean_session=False) #create new instance
    print("connecting to broker")
    client.connect(broker_address) #connect to broker
    topic = 'gateway/c0ee40ffff2939d7/rx'
    print("Subscribing to topic",topic)
    client.publish(topic, 'TEST')

