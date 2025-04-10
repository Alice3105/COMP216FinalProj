# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 09:20:53 2025

@author: m
"""

import json
import time
import random
import paho.mqtt.client as mqtt
from group_4_lab6_data_generator import Sensor

BROKER='test.mosquitto.org'
PORT=1883
TOPIC='group4/smart_home'
start_id=111
client =mqtt.Client()
sensor = Sensor()

client.connect(BROKER,PORT,60)

def create_data():
    raw_data = sensor.generate_date()
    
    temp_data = raw_data.pop(0) if raw_data else sensor.generate_date()[0]
    room_data = random.choice(['Kitchen', 'Living Room', 'Bedroom', 'Bathroom'])
        
    global start_id
    payload = {
        'id': start_id,
        'room': room_data,
        'timestamp': time.asctime(),
        'temperature_c': int(round(temp_data , 0)), 
    }
    start_id+=1
    return payload

try:
    while True:
        data = create_data()
        payload = json.dumps(data)
        client.publish(TOPIC, payload)
        print(f"Published to {TOPIC}: {payload}")
        time.sleep(3)
    
except KeyboardInterrupt:
    print("Publisher stopped by user.")
    
    
client.disconnect()
print("Disconnected from broker.")
    