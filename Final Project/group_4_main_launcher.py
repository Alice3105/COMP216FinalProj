import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import threading
import time

class IoTSystemLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home IoT System Launcher")
        self.root.geometry("900x500")
        
        # Store running processes
        self.publisher_processes = []
        self.subscriber_processes = []
        
        # Create widgets
        self.create_widgets()
        
        # Monitor running processes
        self.start_process_monitor()
    
    def create_widgets(self):
        # Title
        title_label = ttk.Label(self.root, text="Smart Home IoT System Launcher", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Create tabbed interface
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Publisher tab
        publisher_tab = ttk.Frame(self.tabs)
        self.tabs.add(publisher_tab, text="Publishers")
        self.create_publisher_tab(publisher_tab)
        
        # Create Subscriber tab
        subscriber_tab = ttk.Frame(self.tabs)
        self.tabs.add(subscriber_tab, text="Subscribers")
        self.create_subscriber_tab(subscriber_tab)
        
        # Status bar
        self.status_var = tk.StringVar(value="System ready")
        status_label = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_publisher_tab(self, parent):
        # Controls frame
        controls_frame = ttk.LabelFrame(parent, text="Publisher Controls")
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Button to launch GUI publisher
        gui_pub_button = ttk.Button(
            controls_frame, 
            text="Launch Publisher GUI", 
            command=lambda: self.launch_process("group_4_publisher_gui.py")
        )
        gui_pub_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Button to launch multiple publishers
        multi_pub_button = ttk.Button(
            controls_frame, 
            text="Launch Multiple Publishers", 
            command=lambda: self.launch_process("group_4_publisher.py")
        )
        multi_pub_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Button to stop all publishers
        stop_pub_button = ttk.Button(
            controls_frame, 
            text="Stop All Publishers", 
            command=self.stop_all_publishers
        )
        stop_pub_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Publisher process list
        list_frame = ttk.LabelFrame(parent, text="Running Publishers")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Listbox com scrollbar vertical e horizontal
        pub_scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        pub_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        pub_scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        pub_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.pub_listbox = tk.Listbox(list_frame, height=10, xscrollcommand=pub_scrollbar_x.set, yscrollcommand=pub_scrollbar_y.set)
        self.pub_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        pub_scrollbar_y.config(command=self.pub_listbox.yview)
        pub_scrollbar_x.config(command=self.pub_listbox.xview)
    
    def create_subscriber_tab(self, parent):
        # Controls frame
        controls_frame = ttk.LabelFrame(parent, text="Subscriber Controls")
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Button to launch single subscriber
        single_sub_button = ttk.Button(
            controls_frame, 
            text="Launch Subscriber GUI Automatically", 
            command=lambda: self.launch_process("group_4_subscriber_gui.py", is_publisher=False)
        )
        single_sub_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Button to launch multi-subscriber manager
        multi_sub_button = ttk.Button(
            controls_frame, 
            text="Launch Multi-Subscriber Manually", 
            command=lambda: self.launch_process("group_4_multi_subscriber.py", is_publisher=False)
        )
        multi_sub_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Button to stop all subscribers
        stop_sub_button = ttk.Button(
            controls_frame, 
            text="Stop All Subscribers", 
            command=self.stop_all_subscribers
        )
        stop_sub_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Subscriber process list
        list_frame = ttk.LabelFrame(parent, text="Running Subscribers")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Listbox com scrollbar vertical e horizontal
        sub_scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        sub_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        sub_scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        sub_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.sub_listbox = tk.Listbox(list_frame, height=10, xscrollcommand=sub_scrollbar_x.set, yscrollcommand=sub_scrollbar_y.set)
        self.sub_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        sub_scrollbar_y.config(command=self.sub_listbox.yview)
        sub_scrollbar_x.config(command=self.sub_listbox.xview)
    
    def launch_process(self, script_name, is_publisher=True):
        try:
            # Find the script
            if not os.path.exists(script_name):
                script_path = os.path.join("Final Project", script_name)
                if not os.path.exists(script_path):
                    self.status_var.set(f"Error: Could not find {script_name}")
                    return
                script_name = script_path
            
            # Launch the process
            process = subprocess.Popen([sys.executable, script_name])
            
            # Store the process
            if is_publisher:
                process_id = len(self.publisher_processes) + 1
                self.publisher_processes.append((process, script_name, process_id))
                
                # Create a more descriptive label based on the script name
                if "publisher_gui.py" in script_name:
                    description = f"Publisher GUI (PID: {process.pid}) - Manual and auto data generation"
                elif "publisher.py" in script_name:
                    # This creates multiple publishers with predefined locations
                    description = f"Multiple Publishers (PID: {process.pid}):\n"
                    description += "  • Publisher 1 (Kitchen) - 2s interval\n"
                    description += "  • Publisher 2 (Living Room) - 3s interval\n"
                    description += "  • Publisher 3 (Random location) - 5s interval"
                else:
                    description = f"{script_name} (PID: {process.pid})"
                
                self.pub_listbox.insert(tk.END, description)
                self.status_var.set(f"Launched publisher: {os.path.basename(script_name)}")
            else:
                process_id = len(self.subscriber_processes) + 1
                self.subscriber_processes.append((process, script_name, process_id))
                
                # Create a more descriptive label for subscribers
                if "subscriber_gui.py" in script_name:
                    description = f"Subscriber GUI (PID: {process.pid}) - Topic: group4/smart_home"
                elif "multi_subscriber.py" in script_name:
                    description = f"Multi-Subscriber Manager (PID: {process.pid})"
                else:
                    description = f"{script_name} (PID: {process.pid})"
                
                self.sub_listbox.insert(tk.END, description)
                self.status_var.set(f"Launched subscriber: {os.path.basename(script_name)}")
            
        except Exception as e:
            self.status_var.set(f"Error launching process: {str(e)}")
    
    def stop_all_publishers(self):
        for process, _, _ in self.publisher_processes:
            try:
                process.terminate()
            except:
                pass
        
        self.publisher_processes = []
        self.pub_listbox.delete(0, tk.END)
        self.status_var.set("All publishers stopped")
    
    def stop_all_subscribers(self):
        for process, _, _ in self.subscriber_processes:
            try:
                process.terminate()
            except:
                pass
        
        self.subscriber_processes = []
        self.sub_listbox.delete(0, tk.END)
        self.status_var.set("All subscribers stopped")
    
    def start_process_monitor(self):
        """Start a thread to monitor running processes and update the UI"""
        def monitor_processes():
            while True:
                # Check publisher processes
                for i, (process, script_name, process_id) in enumerate(self.publisher_processes[:]):
                    if process.poll() is not None:  # Process has ended
                        self.root.after(0, lambda i=i: self.update_process_status(i, True))
                
                # Check subscriber processes
                for i, (process, script_name, process_id) in enumerate(self.subscriber_processes[:]):
                    if process.poll() is not None:  # Process has ended
                        self.root.after(0, lambda i=i: self.update_process_status(i, False))
                
                time.sleep(1)
        
        monitor_thread = threading.Thread(target=monitor_processes, daemon=True)
        monitor_thread.start()
    
    def update_process_status(self, index, is_publisher):
        try:
            if is_publisher:
                if index < len(self.publisher_processes):
                    # Get the text of the item
                    item_text = self.pub_listbox.get(index)
                    if "Multiple Publishers" in item_text:
                        new_text = "Multiple Publishers (Exited)"
                    elif "Publisher GUI" in item_text:
                        new_text = "Publisher GUI (Exited)"
                    else:
                        _, script_name, _ = self.publisher_processes[index]
                        new_text = f"{script_name} (Exited)"
                    
                    self.pub_listbox.delete(index)
                    self.pub_listbox.insert(index, new_text)
            else:
                if index < len(self.subscriber_processes):
                    # Get the text of the item
                    item_text = self.sub_listbox.get(index)
                    if "Subscriber GUI" in item_text:
                        new_text = "Subscriber GUI (Exited)"
                    elif "Multi-Subscriber Manager" in item_text:
                        new_text = "Multi-Subscriber Manager (Exited)"
                    else:
                        _, script_name, _ = self.subscriber_processes[index]
                        new_text = f"{script_name} (Exited)"
                    
                    self.sub_listbox.delete(index)
                    self.sub_listbox.insert(index, new_text)
        except Exception as e:
            print(f"Error updating process status: {e}")
    
    def on_closing(self):
        # Stop all processes
        self.stop_all_publishers()
        self.stop_all_subscribers()
        
        # Close the window
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = IoTSystemLauncher(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop() 