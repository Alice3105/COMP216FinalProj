import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
import paho.mqtt.client as mqtt
import threading
import queue
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# MQTT Configuration
BROKER = 'test.mosquitto.org'
PORT = 1883
TOPIC = 'group4/smart_home'

# Configuration
MAX_POINTS = 50  # Maximum number of points to display on chart
EXPECTED_INTERVAL = 5  # Expected time between data points (seconds)
TEMPERATURE_MIN = -30  # Minimum valid temperature
TEMPERATURE_MAX = 50  # Maximum valid temperature


class TemperatureChart:
    def __init__(self, frame):
        self.frame = frame
        
        # Create matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize data
        self.timestamps = []
        self.temperatures = []
        self.locations = {}  # Dictionary to track different locations
        self.missed_points = []  # Track timestamps of missed transmissions
        
        # Configure plot
        self.ax.set_title('Smart Home Temperature Data')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Temperature (°C)')
        self.ax.grid(True)
        
        # Set y-axis limits
        self.ax.set_ylim(TEMPERATURE_MIN - 5, TEMPERATURE_MAX + 5)
        
        # Plot lines (empty initially)
        self.line, = self.ax.plot([], [], 'b-', label='Temperature')
        self.error_points, = self.ax.plot([], [], 'ro', label='Out of Range')
        self.missed_markers, = self.ax.plot([], [], 'yx', markersize=10, label='Missed Data')
        self.manual_points, = self.ax.plot([], [], 'gs', markersize=8, label='Manual Entry')
        
        # Legend
        self.ax.legend(loc='upper right')
        
        # Tight layout
        self.fig.tight_layout()
    
    def update_chart(self, data_points):
        # Clear existing data
        self.timestamps = []
        self.temperatures = []
        self.error_timestamps = []
        self.error_temps = []
        self.manual_timestamps = []
        self.manual_temps = []
        
        # Process data points
        for point in data_points:
            self.timestamps.append(point.get('index', 0))
            temp = point.get('temperature_c', 0)
            self.temperatures.append(temp)
            
            # Check for out-of-range temperatures
            if temp < TEMPERATURE_MIN or temp > TEMPERATURE_MAX:
                self.error_timestamps.append(point.get('index', 0))
                self.error_temps.append(temp)
            
            # Check for manual entries
            if point.get('source') == 'manual':
                self.manual_timestamps.append(point.get('index', 0))
                self.manual_temps.append(temp)
        
        # Update plot data
        self.line.set_data(self.timestamps, self.temperatures)
        self.error_points.set_data(self.error_timestamps, self.error_temps)
        self.missed_markers.set_data(self.missed_points, [TEMPERATURE_MIN-3] * len(self.missed_points))
        self.manual_points.set_data(self.manual_timestamps, self.manual_temps)
        
        # Adjust x-axis limits if we have data
        if self.timestamps:
            x_min = max(0, min(self.timestamps))
            x_max = max(self.timestamps) + 1
            self.ax.set_xlim(x_min, x_max)
        
        # Redraw the canvas
        self.canvas.draw()


class SmartHomeSubscriberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home Data Subscriber")
        self.root.geometry("800x600")
        
        # Queue for processing messages between MQTT thread and GUI
        self.message_queue = queue.Queue()
        
        # Data points storage
        self.data_points = []
        self.data_index = 0
        self.last_id = None
        self.last_timestamp = None
        
        # Stats counters
        self.total_messages = 0
        self.missed_messages = 0
        self.out_of_range_values = 0
        
        # Create GUI elements
        self.create_widgets()
        
        # MQTT Client setup
        self.setup_mqtt_client()
        
        # Start processing messages from queue
        self.process_message_queue()
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Smart Home Sensor Data Subscriber", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Connection Status")
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_var = tk.StringVar(value="Disconnected")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, font=("Arial", 10, "bold"))
        status_label.pack(pady=5)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics")
        stats_frame.pack(fill=tk.X, pady=5)
        
        # Grid for statistics
        self.total_var = tk.StringVar(value="Total Messages: 0")
        self.missed_var = tk.StringVar(value="Missed Messages: 0")
        self.range_var = tk.StringVar(value="Out of Range Values: 0")
        
        ttk.Label(stats_frame, textvariable=self.total_var).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(stats_frame, textvariable=self.missed_var).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ttk.Label(stats_frame, textvariable=self.range_var).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        # Create tabbed interface
        self.tabs = ttk.Notebook(main_frame)
        self.tabs.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Chart Tab
        chart_tab = ttk.Frame(self.tabs)
        self.tabs.add(chart_tab, text="Temperature Chart")
        
        # Create the chart
        self.chart = TemperatureChart(chart_tab)
        
        # Data Tab
        data_tab = ttk.Frame(self.tabs)
        self.tabs.add(data_tab, text="Data Log")
        
        # Create text widget with scrollbar for data display
        self.data_text = tk.Text(data_tab, height=20, width=70, wrap=tk.WORD)
        self.data_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(data_tab, command=self.data_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.data_text.config(yscrollcommand=scrollbar.set)
        self.data_text.configure(state=tk.DISABLED)  # Make read-only
    
    def setup_mqtt_client(self):
        # Create MQTT client
        self.client = mqtt.Client()
        
        # Set callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        try:
            # Connect to broker
            self.client.connect(BROKER, PORT, 60)
            self.status_var.set(f"Connected to {BROKER}")
            
            # Start MQTT client in a separate thread
            self.client_thread = threading.Thread(target=self.client.loop_forever)
            self.client_thread.daemon = True
            self.client_thread.start()
        except Exception as e:
            self.status_var.set(f"Connection failed: {str(e)}")
            messagebox.showerror("Connection Error", f"Failed to connect to MQTT broker: {str(e)}")
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.status_var.set(f"Connected to {BROKER}, Subscribed to {TOPIC}")
            # Subscribe to topic
            client.subscribe(TOPIC)
        else:
            error_messages = {
                1: "Incorrect protocol version",
                2: "Invalid client identifier",
                3: "Server unavailable",
                4: "Bad username or password",
                5: "Not authorized"
            }
            error = error_messages.get(rc, f"Unknown error ({rc})")
            self.status_var.set(f"Connection failed: {error}")
    
    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.status_var.set("Unexpectedly disconnected")
        else:
            self.status_var.set("Disconnected")
    
    def on_message(self, client, userdata, msg):
        try:
            # Decode payload
            payload_str = msg.payload.decode('utf-8')
            data = json.loads(payload_str)
            
            # Put in queue for GUI thread to process
            self.message_queue.put(data)
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def process_message_queue(self):
        try:
            # Check for new messages
            while not self.message_queue.empty():
                data = self.message_queue.get_nowait()
                self.process_data(data)
        except Exception as e:
            print(f"Error processing message queue: {e}")
        
        # Schedule next check
        self.root.after(100, self.process_message_queue)
    
    def process_data(self, data):
        # Update counters
        self.total_messages += 1
        
        # Check for message ID gaps
        current_id = data.get('id', 0)
        if self.last_id is not None:
            # Check for missing messages
            expected_id = self.last_id + 1
            if current_id > expected_id:
                missing_count = current_id - expected_id
                self.missed_messages += missing_count
                print(f"Detected {missing_count} missing message(s) between ID {self.last_id} and {current_id}")
                
                # Add markers for missed data points in the chart
                for i in range(missing_count):
                    self.chart.missed_points.append(self.data_index + i)
        
        # Update last ID
        self.last_id = current_id
        
        # Check for out-of-range temperature
        temperature = data.get('temperature_c', 0)
        is_out_of_range = temperature < TEMPERATURE_MIN or temperature > TEMPERATURE_MAX
        
        if is_out_of_range:
            self.out_of_range_values += 1
            print(f"Out of range temperature: {temperature}°C")
        
        # Add data point with additional metadata
        data_point = {
            **data,  # Include all original data
            'index': self.data_index,
            'received_at': time.asctime(),
            'out_of_range': is_out_of_range
        }
        
        # Add to data points
        self.data_points.append(data_point)
        if len(self.data_points) > MAX_POINTS:
            self.data_points.pop(0)
        
        # Increment data index
        self.data_index += 1
        
        # Update statistics
        self.update_statistics()
        
        # Update data display
        self.update_data_display(data_point)
        
        # Update chart
        self.chart.update_chart(self.data_points)
    
    def update_statistics(self):
        self.total_var.set(f"Total Messages: {self.total_messages}")
        self.missed_var.set(f"Missed Messages: {self.missed_messages}")
        self.range_var.set(f"Out of Range Values: {self.out_of_range_values}")
    
    def update_data_display(self, data_point):
        # Enable text widget for editing
        self.data_text.configure(state=tk.NORMAL)
        
        # Format data point as text
        formatted_text = f"--- Sensor Reading #{data_point['id']} ---\n"
        formatted_text += f"Location: {data_point.get('location', 'Unknown')}\n"
        formatted_text += f"Temperature: {data_point.get('temperature_c', 0)}°C"
        
        # Add warning if out of range
        if data_point.get('out_of_range', False):
            formatted_text += " [OUT OF RANGE]"
            
        formatted_text += f"\nTimestamp: {data_point.get('timestamp', 'Unknown')}\n"
        formatted_text += f"Received at: {data_point.get('received_at', 'Unknown')}\n"
        
        # Add source information (manual or auto)
        if 'source' in data_point:
            formatted_text += f"Source: {data_point['source'].upper()}\n"
            
        if 'thread' in data_point:
            formatted_text += f"Publisher thread: {data_point['thread']}\n"
            
        formatted_text += "-----------------------------------\n\n"
        
        # Insert at the beginning of the text widget
        self.data_text.insert("1.0", formatted_text)
        
        # Set tag for out of range values or manual entries
        if data_point.get('out_of_range', False):
            # Calculate line count
            line_count = formatted_text.count('\n')
            self.data_text.tag_add("warning", "1.0", f"{line_count}.0")
            self.data_text.tag_configure("warning", background="#CA5600")
        elif data_point.get('source') == 'manual':
            # Highlight manual entries
            line_count = formatted_text.count('\n')
            self.data_text.tag_add("manual", "1.0", f"{line_count}.0")
            self.data_text.tag_configure("manual", background="#0062C4")
        
        # Limit text length
        all_text = self.data_text.get("1.0", tk.END)
        if len(all_text) > 10000:  # Limit to about 10KB
            self.data_text.delete("100.0", tk.END)
        
        self.data_text.configure(state=tk.DISABLED)
    
    def on_closing(self):
        if self.client:
            self.client.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeSubscriberGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop() 