import tkinter as tk
from tkinter import ttk
import threading, time
import random

class LineChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Line Chart")
        self.root.geometry("800x600")
        
        # Y-axis maximum value
        self.y_max = 50
        
        # Data for the line chart (initial random data)
        self.data = [random.randint(5, 40) for _ in range(10)]
        
        # Chart dimensions and padding
        self.chart_width = 700
        self.chart_height = 400
        self.padding_left = 50
        self.padding_right = 50
        self.padding_top = 50
        self.padding_bottom = 50
        
        # Create frames
        self.input_frame = ttk.Frame(root, padding="10")
        self.input_frame.pack(fill=tk.X)
        
        self.chart_frame = ttk.Frame(root)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the canvas for the chart
        self.canvas = tk.Canvas(self.chart_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw the initial chart
        self.draw_chart()
        
        # Bind resize event
        self.canvas.bind("<Configure>", self.on_resize)

   
        t = threading.Thread(
            target = self.add_new_value,
            name = "thread",
            daemon = True
        )

        t.start()
    
    def on_resize(self, event):
        # Update canvas dimensions when window is resized
        self.chart_width = event.width - self.padding_left - self.padding_right
        self.chart_height = event.height - self.padding_top - self.padding_bottom
        self.draw_chart()
    
    def draw_chart(self):
        self.canvas.delete("all")
        self.draw_axis()
        self.draw_data()
        self.draw_grid()
        self.canvas.create_text(self.canvas.winfo_width() // 2, 20, 
                                text="Temperature Chart", 
                                font=("Arial", 14, "bold"))
    
    def draw_axis(self):
        # Draw X-axis
        self.canvas.create_line(
            self.padding_left, self.canvas.winfo_height() - self.padding_bottom,
            self.padding_left + self.chart_width, self.canvas.winfo_height() - self.padding_bottom,
            width=2
        )
        
        # Draw Y-axis
        self.canvas.create_line(
            self.padding_left, self.canvas.winfo_height() - self.padding_bottom,
            self.padding_left, self.padding_top,
            width=2
        )
        
        # Draw X-axis labels
        x_interval = self.chart_width / (len(self.data) - 1) if len(self.data) > 1 else self.chart_width
        for i in range(len(self.data)):
            x = self.padding_left + i * x_interval
            # X-axis tick
            self.canvas.create_line(
                x, self.canvas.winfo_height() - self.padding_bottom,
                x, self.canvas.winfo_height() - self.padding_bottom + 5,
                width=1
            )
            # X-axis label
            self.canvas.create_text(
                x, self.canvas.winfo_height() - self.padding_bottom + 20,
                text=str(i + 1)
            )
        
        # Draw Y-axis labels - adjusted for max 50
        y_step = 10 
        for i in range(0, self.y_max + 1, y_step):
            y = self.canvas.winfo_height() - self.padding_bottom - (i / self.y_max * self.chart_height)
            # Y-axis tick
            self.canvas.create_line(
                self.padding_left, y,
                self.padding_left - 5, y,
                width=1
            )
            # Y-axis label
            self.canvas.create_text(
                self.padding_left - 25, y,
                text=str(i)
            )
        
        # Axis labels
        self.canvas.create_text(
            self.padding_left + self.chart_width // 2, 
            self.canvas.winfo_height() - 15,
            text="Data Points"
        )
        self.canvas.create_text(
            15, 
            self.padding_top + self.chart_height // 2,
            text="Temperature (C)",
            angle=90
        )
    
    def draw_grid(self):
        # Draw horizontal grid lines 
        y_step = 10 
        for i in range(0, self.y_max + 1, y_step):
            y = self.canvas.winfo_height() - self.padding_bottom - (i / self.y_max * self.chart_height)
            self.canvas.create_line(
                self.padding_left, y,
                self.padding_left + self.chart_width, y,
                width=1, dash=(4, 4), fill="#CCCCCC"
            )
        
        # Draw vertical grid lines
        x_interval = self.chart_width / (len(self.data) - 1) if len(self.data) > 1 else self.chart_width
        for i in range(len(self.data)):
            x = self.padding_left + i * x_interval
            self.canvas.create_line(
                x, self.canvas.winfo_height() - self.padding_bottom,
                x, self.padding_top,
                width=1, dash=(4, 4), fill="#CCCCCC"
            )
    
    def draw_data(self):
        if not self.data:
            return
            
        # Calculate coordinates for each data point
        x_interval = self.chart_width / (len(self.data) - 1) if len(self.data) > 1 else self.chart_width
        points = []
        
        for i, value in enumerate(self.data):
            normalized_value = max(0, min(50, value))
            
            # Calculate position
            x = self.padding_left + i * x_interval
            y = self.canvas.winfo_height() - self.padding_bottom - (normalized_value / self.y_max * self.chart_height)
            
            points.append((x, y))
            
            # Draw point
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="#3498db", outline="#2980b9")
            
            # Draw value text above point
            self.canvas.create_text(x, y-15, text=str(value))
        
        # Draw lines between points
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, width=2, fill="#3498db")
    
    def add_new_value(self):
        while True:
            new_value = random.randint(5, 50)
            del self.data[0]
            self.data.append(new_value)
            self.draw_chart()

            time.sleep(0.5)
if __name__ == "__main__":
    root = tk.Tk()
    app = LineChartApp(root)
    root.mainloop()