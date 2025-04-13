# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 08:57:16 2025

@author: m
"""
import random
import time

start_id=111

def create_data():
    global start_id
    payload = {
        'id': start_id,
        'room': random.choice(['Kitchen', 'Living Room', 'Bedroom', 'Bathroom']),
        'timestamp': time.asctime(),
        'motion_detected': random.choice([True, False]),
        'light_level_lux': round(random.uniform(100, 800), 2),  # in lux
        'temperature_c': round(random.uniform(18, 25), 1),       # in Celsius
        'humidity_percent': round(random.uniform(30, 60), 1)     # in %
    }
    start_id+=1
    return payload



def print_data(data):
    print(f"Sensor Reading #{data['id']}")
    print(f"Room: {data['room']}")
    print(f"Time: {data['timestamp']}")
    print(f"Motion detected: {'Yes' if data['motion_detected'] else 'No'}")
    print(f"Light level: {data['light_level_lux']} lux")
    print(f" Temperature: {data['temperature_c']} °C")
    print(f" Humidity: {data['humidity_percent']} %")
    print("-" * 40)
    