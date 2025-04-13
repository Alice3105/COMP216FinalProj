import tkinter as tk
import subprocess
import sys
import os
import threading
import time

class MultiSubscriberManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home Multi-Subscriber Manager")
        self.root.geometry("500x400")
        
        self.subscribers = []
        self.processes = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Smart Home Multi-Subscriber Manager", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Frame for controls
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(fill=tk.X)
        
        # Button to launch new subscriber
        launch_button = tk.Button(control_frame, text="Launch New Subscriber", command=self.launch_subscriber)
        launch_button.pack(side=tk.LEFT, padx=5)
        
        # Button to stop all subscribers
        stop_all_button = tk.Button(control_frame, text="Stop All Subscribers", command=self.stop_all_subscribers)
        stop_all_button.pack(side=tk.LEFT, padx=5)
        
        # Frame for subscriber list
        list_frame = tk.LabelFrame(self.root, text="Active Subscribers", padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Listbox for subscribers with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.subscriber_listbox = tk.Listbox(list_frame, height=10, width=60)
        self.subscriber_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.subscriber_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.subscriber_listbox.yview)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to launch subscribers")
        status_label = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def launch_subscriber(self):
        try:
            # Get the script path
            subscriber_script = "group_4_subscriber_gui.py"
            
            # Check if the script exists
            if not os.path.exists(subscriber_script):
                subscriber_script = os.path.join("Final Project", "group_4_subscriber_gui.py")
                if not os.path.exists(subscriber_script):
                    self.status_var.set(f"Error: Could not find {subscriber_script}")
                    return
            
            # Launch the subscriber process
            process = subprocess.Popen([sys.executable, subscriber_script])
            
            # Record the process
            subscriber_id = len(self.processes) + 1
            self.processes.append(process)
            
            # Update listbox
            self.subscriber_listbox.insert(tk.END, f"Subscriber #{subscriber_id} - PID: {process.pid}")
            
            # Update status
            self.status_var.set(f"Launched Subscriber #{subscriber_id}")
            
            # Start a monitoring thread
            monitor_thread = threading.Thread(
                target=self.monitor_process,
                args=(process, subscriber_id),
                daemon=True
            )
            monitor_thread.start()
            
        except Exception as e:
            self.status_var.set(f"Error launching subscriber: {str(e)}")
    
    def monitor_process(self, process, subscriber_id):
        """Monitor a subscriber process and update the list when it exits"""
        process.wait()
        
        # Update the listbox from the main thread
        self.root.after(0, lambda: self.update_subscriber_status(subscriber_id, "Exited"))
    
    def update_subscriber_status(self, subscriber_id, status):
        # Find the listbox item
        for i in range(self.subscriber_listbox.size()):
            if f"Subscriber #{subscriber_id}" in self.subscriber_listbox.get(i):
                self.subscriber_listbox.delete(i)
                self.subscriber_listbox.insert(i, f"Subscriber #{subscriber_id} - {status}")
                break
    
    def stop_all_subscribers(self):
        """Stop all running subscriber processes"""
        for process in self.processes:
            try:
                process.terminate()
            except:
                pass
        
        # Clear the processes list
        self.processes = []
        
        # Update the listbox
        self.subscriber_listbox.delete(0, tk.END)
        
        # Update status
        self.status_var.set("All subscribers stopped")
    
    def on_closing(self):
        """Clean up when the window is closing"""
        self.stop_all_subscribers()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiSubscriberManager(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop() 