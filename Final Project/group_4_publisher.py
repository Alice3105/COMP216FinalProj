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
        self.publisher_id = publisher_id # Unique ID for each publisher
        self.start_id = 100 + (publisher_id * 1000)  # Unique ID range for each publisher
        self.client = mqtt.Client(2, f"publisher_{publisher_id}") # 2 is the protocol version and f"publisher_{publisher_id}" is the client ID
        self.client.connect(BROKER, PORT, 60) # Connect to the broker   
        self.sensor = Sensor() # Create a sensor object
        self.interval = interval  # Seconds between publications
        self.running = True # Flag to indicate if the publisher is running
        self.location = location  # Fixed location or None for random
        
    def create_data(self): # Create data to be published
        raw_data = self.sensor.generate_data()  # Fixed typo: generate_date -> generate_data
        
        temp_data = raw_data.pop(0) if raw_data else self.sensor.generate_data()[0] # Pop the first element from raw_data or generate new data
        
        # Use fixed location or random choice
        if self.location:
            room_data = self.location # Use fixed location
        else:
            room_data = random.choice(['Kitchen', 'Living Room', 'Bedroom', 'Bathroom']) # Use random choice
            
        payload = {
            'id': self.start_id, # Unique ID for each data point
            'publisher': self.publisher_id, # Unique ID for each publisher
            'location': room_data, # Fixed location or random choice
            'timestamp': time.asctime(), # Current timestamp
            'temperature_c': int(round(temp_data, 0)), # Round temperature to nearest integer
        }
        self.start_id += 1 # Increment the start ID for the next data point
        return payload
    
    def run(self): # Run the publisher
        try: 
            while self.running: # While the publisher is running
                data = self.create_data() # Create data to be published
                payload = json.dumps(data) # Convert data to JSON format
                self.client.publish(TOPIC, payload) # Publish the data to the topic
                print(f"Publisher {self.publisher_id} - Published to {TOPIC}: {payload}") # Print the data that was published
                time.sleep(self.interval) # Wait for the interval before publishing again
        
        except Exception as e: # Handle any exceptions that occur
            print(f"Publisher {self.publisher_id} error: {e}") # Print the error message
        
        self.client.disconnect() # Disconnect from the broker
        print(f"Publisher {self.publisher_id} disconnected from broker.") # Print the message that the publisher disconnected from the broker
    
    def stop(self): # Stop the publisher
        self.running = False # Set the running flag to False

def main(): # Main function to create and start multiple publishers 
    # Create multiple publishers
    publishers = [] # List to store the publishers
    
    # Create publishers with different configurations
    publishers.append(Publisher(1, interval=2, location="Kitchen")) # Create a publisher with a specific interval and location
    publishers.append(Publisher(2, interval=3, location="Living Room")) # Create a publisher with a specific interval and location
    publishers.append(Publisher(3, interval=5)) # Create a publisher with a specific interval
    
    # Start all publishers
    for pub in publishers:
        pub.start() # Start the publisher
        print(f"Started publisher {pub.publisher_id}") # Print the message that the publisher was started
    
    try:
        # Keep the main thread alive
        while True: 
            time.sleep(1) # Wait for 1 second
    
    except KeyboardInterrupt:
        print("Publishers stopped by user.") # Print the message that the publishers were stopped by the user
        
        # Stop all publishers
        for pub in publishers: 
            pub.stop() # Stop the publisher
        
        # Wait for all publishers to finish
        for pub in publishers:
            pub.join() # Wait for the publisher to finish
            
    print("All publishers disconnected.") # Print the message that all publishers were disconnected from the broker 

if __name__ == "__main__":
    main()
    