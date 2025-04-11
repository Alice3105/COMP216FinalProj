# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 09:28:24 2025

@author: m
"""

import json
import paho.mqtt.client as mqtt



BROKER='test.mosquitto.org'
PORT=1883
TOPIC='group4/smart_home'

def print_data(data):
    print(f"Sensor Reading #{data['id']}")
    print(f"Location: {data['location']}")
    print(f"Time: {data['timestamp']}")
    print(f" Temperature: {data['temperature_c']} °C")
    print("-" * 40)

def on_message(client, userdata, msg):
    try:
        payload_str =  msg.payload.decode('utf-8')
        data = json.loads(payload_str)
        print_data(data)
    except Exception as e :
        print(f"Error processing message: {e}")
        
# Create MQTT client
client = mqtt.Client()

# Assign message handler
client.on_message = on_message

# Connect to broker
client.connect(BROKER, PORT, 60)

# Subscribe to topic
client.subscribe(TOPIC)
print(f"Subscribed to topic: {TOPIC}")

# Start loop
client.loop_forever()  