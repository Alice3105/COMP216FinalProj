# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 09:20:53 2025

@author: m
"""

import json
import time
import paho.mqtt.client as mqtt
from group_4_util import create_data

BROKER='test.mosquitto.org'
PORT=1883
TOPIC='group4/smart_home'

client =mqtt.Client()

client.connect(BROKER,PORT,60)

try:
    for _ in range(5):
        data = create_data()
        payload = json.dumps(data)
        client.publish(TOPIC, payload)
        print(f"Published to {'TOPIC'}: {'payload'}")
        time.sleep(3)
except KeyboardInterrupt:
    print("Publisher stopped by user.")
    
    
client.disconnect()
print("Disconnected from broker.")
    