# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 08:57:16 2025

@author: m
"""
import random
import time

start_id=111

# def create_data():
#     global start_id
#     payload = {
#         'id': start_id,
#         'room': random.choice(['Kitchen', 'Living Room', 'Bedroom', 'Bathroom']),
#         'timestamp': time.asctime(),
#         'temperature_c': round(random.uniform(18, 25), 1), 
#     }
#     start_id+=1
#     return payload



def print_data(data):
    print(f"Sensor Reading #{data['id']}")
    print(f"Location: {data['location']}")
    print(f"Time: {data['timestamp']}")
    print(f" Temperature: {data['temperature_c']} °C")
    print("-" * 40)
    