# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 13:55:45 2025

@author: m
"""

import matplotlib.pyplot as plt
import random

# Sensor measures temperature of the pavement throughout the day
class Sensor:
    def __init__(self):
        self.high_value = 40
        self.low_value = 15

        self.base = 0.5
        self.delta = 0.02
        self.min = 0.0
        self.max = 1.0
        self.cycle = random.randint(50, 100)

    def generator(self) -> float:
        self.cycle -= 1
        if self.cycle == 0:
            self.cycle = random.randint(50, 100)
            self.delta *= -1

        self.base += self.delta
        self.base = max(self.min, min(self.max, self.base))
        return self.base
    
    def generator_2(self) -> float:
        return random.uniform(0.3, 0.7)
    
    def generator_3(self) -> float:
        value = random.gauss(0.5, 0.1)
        return max(0.0, min(1.0, value))

    def generator_4(self) -> float:
        if self.base <= self.min or self.base >= self.max:
            self.delta *= -1
        self.base += self.delta
        return max(0.0, min(1.0, self.base))
    
    def generate_date(self) -> list[float]:
        sensor = Sensor()

        gen2_data = [sensor.generator_2() for _ in range(50)]
        gen2_value = [(value * (sensor.high_value - sensor.low_value)) + sensor.low_value for value in gen2_data]

        gen3_data = [sensor.generator_3() for _ in range(500)]
        gen3_value = [(value * (sensor.high_value - sensor.low_value)) + sensor.low_value for value in gen3_data]

        gen4_data = [sensor.generator_4() for _ in range(100)]
        gen4_value = [(value * (sensor.high_value - sensor.low_value)) + sensor.low_value for value in gen4_data]

        plot_data = (
            gen3_value[0:150] + gen2_value[0:25] + gen4_value[0:50] +
            gen3_value[151:350] + gen2_value[26:50] + gen4_value[51:100] +
            gen3_value[351:500]
        )
        
        return plot_data
    
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
