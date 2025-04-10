import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
import random
import paho.mqtt.client as mqtt
from group_4_lab6_data_generator import Sensor

# MQTT Configuration
BROKER = 'test.mosquitto.org'
PORT = 1883
TOPIC = 'group4/smart_home'

class SmartHomePublisherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home Data Publisher")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Initialize raw temp data
        self.sensor = Sensor()
        self.raw_data = self.sensor.generate_data()
        
        # Initialize MQTT client
        self.client = mqtt.Client()
        self.client.connect(BROKER, PORT, 60)
    
        self.start_id = 111
        
        # Data points list
        self.data_points = []
        
        # Create GUI elements
        self.create_widgets()
        
        # Start displaying temperature in status
        self.display_temperature()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Smart Home Sensor Data", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Temperature input
        temp_frame = ttk.Frame(main_frame)
        temp_frame.pack(fill=tk.X, pady=5)
        
        temp_label = ttk.Label(temp_frame, text="Temperature (°C):", width=15)
        temp_label.pack(side=tk.LEFT)
        
        self.temp_var = tk.StringVar()
        self.temp_entry = ttk.Entry(temp_frame, textvariable=self.temp_var)
        self.temp_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Location input
        location_frame = ttk.Frame(main_frame)
        location_frame.pack(fill=tk.X, pady=5)
        
        location_label = ttk.Label(location_frame, text="Location:", width=15)
        location_label.pack(side=tk.LEFT)
        
        self.location_var = tk.StringVar()
        self.location_combo = ttk.Combobox(location_frame, textvariable=self.location_var)
        self.location_combo['values'] = ('Kitchen', 'Living Room', 'Bedroom', 'Bathroom')
        self.location_combo.current(0)
        self.location_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add instruction label
        location_help = ttk.Label(location_frame, text="(type or select)", font=("Arial", 8))
        location_help.pack(side=tk.RIGHT, padx=5)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Generate button
        self.gen_button = ttk.Button(button_frame, text="Generate Temp", command=self.add_data_point)
        self.gen_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Temperature Data")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a Text widget for the status with scrollbar
        self.status_text = tk.Text(status_frame, height=20, width=40, wrap=tk.WORD)
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
        
        # Set background color the same as parent
        self.status_text.configure(background=self.root.cget('bg'), relief=tk.FLAT)
        self.status_text.configure(state=tk.DISABLED)  # Make read-only
    
    def generate_temperature(self):
        # Use the sensor to generate temperature data
        if not self.raw_data:
                self.raw_data = self.sensor.generate_data()
        temp_data = self.raw_data.pop(0)
        return int(round(temp_data, 0))
    
    def add_data_point(self):
        # Check if manual temperature is entered
        try:
            if self.temp_var.get():
                temperature = float(self.temp_var.get())
            else:
                temperature = self.generate_temperature()
        except ValueError:
            messagebox.showerror("Input Error", "Temperature must be a number")
            return
        
        # Get location
        location = self.location_var.get()
        if not location:
            messagebox.showerror("Input Error", "Location cannot be empty")
            return
        
        # Create a data point and add it to the beginning of the list
        data_point = {
            'location': location,
            'temperature_c': temperature,
            'timestamp': time.asctime(),
            'source': 'manual'
        }
        
        # Add to the beginning of the list
        self.data_points.insert(0, data_point)
        
        # Update display
        self.update_status_display()
        
        # Clear temperature field
        self.temp_var.set("")
    
    def display_temperature(self):
        # Generate a new data point
        temp = self.generate_temperature()
        location = self.location_var.get() or "Default"
        data_point = {
            'location': location,
            'temperature_c': temp,
            'timestamp': time.asctime(),
            'source': 'auto'
        }
            
        # Add to the end of the list (lower priority)
        self.data_points.append(data_point)
        
        time.sleep(5)
        
        # Publish the data
        try:
            payload = {
                'id': self.start_id,
                'location': data_point['location'],
                'timestamp': time.asctime(),  
                'temperature_c': int(round(data_point['temperature_c'], 0)),
            }
                
            self.start_id += 1
                
            json_payload = json.dumps(payload)
            self.client.publish(TOPIC, json_payload)
                
            data_point['published_at'] = time.asctime()
            self.update_status_display()
                
            print(f"Published to {TOPIC}: {json_payload}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to publish data: {str(e)}")
        
        # Schedule next update (every 5 seconds)
        self.root.after(5000, self.display_temperature)
    
    def update_status_display(self):
        # Enable text widget for editing
        self.status_text.configure(state=tk.NORMAL)
        
        # Clear current content
        self.status_text.delete(1.0, tk.END)
        
        # Add each data point to the display
        for i, point in enumerate(self.data_points): 
            source_marker = " (manual)" if point['source'] == 'manual' else ""
            line = f"{i+1}. {point['location']}: {point['temperature_c']}°C - {point['timestamp']}{source_marker}\n"
            # Make manual entries bold
            if point['source'] == 'manual':
                self.status_text.insert(tk.END, line, 'bold')
            else:
                self.status_text.insert(tk.END, line)
        
        self.status_text.tag_configure('bold', font=('Arial', 10, 'bold'))

        self.status_text.configure(state=tk.DISABLED)
    
    def on_closing(self):
        self.client.disconnect()
        print("Disconnected from broker.")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomePublisherGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop() 