# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 13:55:45 2025

@author: m
"""

import matplotlib.pyplot as plt
import random

# Sensor measures temperature of the pavement throughout the day
class Sensor: # Sensor class to generate data   
    def __init__(self):
        self.high_value = 35 # High value for the sensor
        self.low_value = 16 # Low value for the sensor

        self.base = 0.5 # Base value for the sensor
        self.delta = 0.02 # Delta value for the sensor
        self.min = 0.0 # Minimum value for the sensor
        self.max = 1.0 # Maximum value for the sensor
        self.cycle = random.randint(50, 100) # Random cycle value for the sensor

    def generator(self) -> float: # Generator function to generate data 
        self.cycle -= 1 # Decrement the cycle value
        if self.cycle == 0: # If the cycle value is 0
            self.cycle = random.randint(50, 100) # Random cycle value for the sensor
            self.delta *= -1 # Change the direction of the delta value

        self.base += self.delta # Increment the base value
        self.base = max(self.min, min(self.max, self.base)) # Ensure the base value is within the minimum and maximum values
        return self.base 
    
    def generator_2(self) -> float: # Generator function to generate data 
        return random.uniform(0.3, 0.7) # Random uniform value for the sensor
    
    def generator_3(self) -> float:
        value = random.gauss(0.5, 0.1) # Random gaussian value for the sensor
        return max(0.0, min(1.0, value)) # Ensure the value is within the minimum and maximum values

    def generator_4(self) -> float: # Generator function to generate data
        if self.base <= self.min or self.base >= self.max: # If the base value is less than the minimum or greater than the maximum
            self.delta *= -1 # Change the direction of the delta value
        self.base += self.delta # Increment the base value
        return max(0.0, min(1.0, self.base)) # Ensure the value is within the minimum and maximum values
    
    def generate_data(self) -> list[float]: # Generate data for the sensor
        sensor = Sensor() # Create a sensor object  

        gen2_data = [sensor.generator_2() for _ in range(50)] # Generate data for the sensor
        gen2_value = [(value * (sensor.high_value - sensor.low_value)) + sensor.low_value for value in gen2_data] # Convert the data to the high and low values

        gen3_data = [sensor.generator_3() for _ in range(500)] # Generate data for the sensor
        gen3_value = [(value * (sensor.high_value - sensor.low_value)) + sensor.low_value for value in gen3_data] # Convert the data to the high and low values

        gen4_data = [sensor.generator_4() for _ in range(100)] # Generate data for the sensor
        gen4_value = [(value * (sensor.high_value - sensor.low_value)) + sensor.low_value for value in gen4_data] # Convert the data to the high and low values 

        plot_data = ( # Combine the data for the sensor
            gen3_value[0:150] + gen2_value[0:25] + gen4_value[0:50] + # First 150 data points from gen3, 25 data points from gen2, and 50 data points from gen4 
            gen3_value[151:350] + gen2_value[26:50] + gen4_value[51:100] + # Next 200 data points from gen3, 24 data points from gen2, and 49 data points from gen4
            gen3_value[351:500] # Last 150 data points from gen3
        )
        
        return plot_data # Return the combined data
    
# if __name__ == "__main__":
#     sensor = Sensor()

#     gen2_data = [sensor.generator_2() for _ in range(50)]
#     gen2_value = [(value * (sensor.high_value - sensor.low_value)) + sensor.low_value for value in gen2_data]

#     gen3_data = [sensor.generator_3() for _ in range(500)]
#     gen3_value = [(value * (sensor.high_value - sensor.low_value)) + sensor.low_value for value in gen3_data]

#     gen4_data = [sensor.generator_4() for _ in range(100)]
#     gen4_value = [(value * (sensor.high_value - sensor.low_value)) + sensor.low_value for value in gen4_data]

#     plot_data = (
#         gen3_value[0:150] + gen2_value[0:25] + gen4_value[0:50] +
#         gen3_value[151:350] + gen2_value[26:50] + gen4_value[51:100] +
#         gen3_value[351:500]
#     )
    
#     plt.figure(figsize=(10, 5))
#     plt.plot(plot_data, 'g', alpha=0.7)
#     plt.title('Pavement Temperature Data')
#     plt.ylabel('Temperature (°C)')
#     plt.xlabel('Time')
#     plt.grid(True)
#     plt.show()
