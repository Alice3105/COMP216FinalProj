# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 09:20:53 2025

@author: m
"""

import json
import time
import random
import paho.mqtt.client as mqtt
import threading
from group_4_lab6_data_generator import Sensor

BROKER='test.mosquitto.org'
PORT=1883
TOPIC='group4/smart_home'

class Publisher(threading.Thread):
    def __init__(self, publisher_id, interval=3, location=None):
        threading.Thread.__init__(self)
        self.publisher_id = publisher_id
        self.start_id = 100 + (publisher_id * 1000)  # Unique ID range for each publisher
        self.client = mqtt.Client(2, f"publisher_{publisher_id}")
        self.client.connect(BROKER, PORT, 60)
        self.sensor = Sensor()
        self.interval = interval  # Seconds between publications
        self.running = True
        self.location = location  # Fixed location or None for random
        
    def create_data(self):
        raw_data = self.sensor.generate_data()  # Fixed typo: generate_date -> generate_data
        
        temp_data = raw_data.pop(0) if raw_data else self.sensor.generate_data()[0]
        
        # Use fixed location or random choice
        if self.location:
            room_data = self.location
        else:
            room_data = random.choice(['Kitchen', 'Living Room', 'Bedroom', 'Bathroom'])
            
        payload = {
            'id': self.start_id,
            'publisher': self.publisher_id,
            'location': room_data,
            'timestamp': time.asctime(),
            'temperature_c': int(round(temp_data, 0)), 
        }
        self.start_id += 1
        return payload
    
    def run(self):
        try:
            while self.running:
                data = self.create_data()
                payload = json.dumps(data)
                self.client.publish(TOPIC, payload)
                print(f"Publisher {self.publisher_id} - Published to {TOPIC}: {payload}")
                time.sleep(self.interval)
        
        except Exception as e:
            print(f"Publisher {self.publisher_id} error: {e}")
        
        self.client.disconnect()
        print(f"Publisher {self.publisher_id} disconnected from broker.")
    
    def stop(self):
        self.running = False

def main():
    # Create multiple publishers
    publishers = []
    
    # Create publishers with different configurations
    publishers.append(Publisher(1, interval=2, location="Kitchen"))
    publishers.append(Publisher(2, interval=3, location="Living Room"))
    publishers.append(Publisher(3, interval=5))  # Random locations
    
    # Start all publishers
    for pub in publishers:
        pub.start()
        print(f"Started publisher {pub.publisher_id}")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Publishers stopped by user.")
        # Stop all publishers
        for pub in publishers:
            pub.stop()
        
        # Wait for all publishers to finish
        for pub in publishers:
            pub.join()
            
    print("All publishers disconnected.")

if __name__ == "__main__":
    main()
    