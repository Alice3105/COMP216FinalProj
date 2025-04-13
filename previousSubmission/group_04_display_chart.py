import tkinter as tk
from tkinter import ttk, messagebox
import random

class HistoricalDataApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # 1) Create a fixed list of 20 values (random values between 0 and 50)
        self.data = [random.randint(0, 50) for _ in range(20)]
        
        # Keep track of the current "start index" to draw
        self.current_start_index = 0

        self.initUI()
    
    def initUI(self):
        self.master.title("Historical Data")
        self.pack(fill=tk.BOTH, expand=True)

        # Top frame for controls
        top_frame = ttk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Label "Data range:", Entry, and "Go" Button
        self.label_prompt = ttk.Label(top_frame, text="Data range (from 0 to 14):")
        self.label_prompt.pack(side=tk.LEFT, padx=(0,5))

        self.entry_range = ttk.Entry(top_frame, width=5)
        self.entry_range.insert(0, "0")  # default start index
        self.entry_range.pack(side=tk.LEFT, padx=(0,5))

        self.btn_go = ttk.Button(top_frame, text="Go", command=self.on_go_clicked)
        self.btn_go.pack(side=tk.LEFT)

        # Label showing the current slice "Data range: X-Y"
        self.label_current_range = ttk.Label(self, text="Data range: 0-5")
        self.label_current_range.pack(side=tk.TOP, pady=5)

        # Canvas for drawing bars & connecting line
        self.canvas = tk.Canvas(self, width=500, height=300, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Bind <Configure> so we re-draw whenever the canvas size changes
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # Draw the initial range (0-5)
        self.current_start_index = 0
        self.draw_range(self.current_start_index)

    def on_canvas_resize(self, event):
        """
        Called whenever the canvas is resized.
        Redraws the current slice of data so it fills the new canvas size.
        """
        self.draw_range(self.current_start_index)

    def on_go_clicked(self):
        """
        Reads the start index from the Entry widget and draws the 6-value range.
        If the user enters a value outside the allowed range, a popup message
        informs them of the allowed range and reminds them that the sensor maximum is 50.
        """
        try:
            start_index = int(self.entry_range.get())
        except ValueError:
            messagebox.showerror("Invalid Input", 
                                 "Please enter a valid integer. Allowed sensor range is 0 to 50.")
            return

        # The allowed start index is from 0 to len(self.data)-6
        max_start_index = len(self.data) - 6

        if start_index < 0:
            messagebox.showerror("Out of Range", 
                                 f"Start index cannot be negative.\nAllowed range: 0 to {max_start_index}\nSensor max limit is 50.")
            start_index = 0
        elif start_index > max_start_index:
            messagebox.showerror("Out of Range", 
                                 f"Start index cannot exceed {max_start_index} because the program uses a fixed list of 20 values and displays 6 consecutive values at a time.\nAllowed range: 0 to {max_start_index}\nSensor max limit is 50.")
            start_index = max_start_index

        self.current_start_index = start_index
        self.draw_range(start_index)

    def draw_range(self, start_index):
        """
        Draws 6 bars plus a connecting line for data[start_index : start_index+6].
        """
        self.canvas.delete("all")  # Clear previous drawing

        # Extract 6 consecutive values from the fixed list
        slice_of_values = self.data[start_index : start_index + 6]

        # Update the label "Data range: X-Y"
        self.label_current_range.config(
            text=f"Data range: {start_index}-{start_index + 5}"
        )

        # Get the actual canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Define padding so bars aren’t at the extreme edges
        left_padding   = 40
        right_padding  = 20
        top_padding    = 20
        bottom_padding = 40

        # Compute the drawable area dimensions
        drawable_width  = canvas_width  - (left_padding + right_padding)
        drawable_height = canvas_height - (top_padding + bottom_padding)

        # Assume the sensor’s maximum possible value is 50
        max_value = 50

        # We'll draw 6 bars
        num_bars = 6
        bar_spacing = 10

        # Prevent negative width in case the window is very small
        if drawable_width < 0:
            drawable_width = 0

        bar_width = (drawable_width - bar_spacing * (num_bars - 1)) / num_bars if num_bars > 0 else 0

        points_for_line = []  # To store top center points for the connecting line

        for i, val in enumerate(slice_of_values):
            # Scale bar height relative to max_value
            scaled_height = (val / max_value) * drawable_height if max_value else 0

            # Calculate the x positions for each bar
            x1 = left_padding + i * (bar_width + bar_spacing)
            x2 = x1 + bar_width

            # Bottom and top positions of the bar
            y2 = canvas_height - bottom_padding
            y1 = y2 - scaled_height

            # Draw the bar as a rectangle
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="lightgreen", outline="black"
            )

            # Compute the top center for the line
            bar_top_center_x = (x1 + x2) / 2
            bar_top_center_y = y1
            points_for_line.append((bar_top_center_x, bar_top_center_y))

            # Display the value above the bar
            self.canvas.create_text(
                bar_top_center_x, y1 - 10,
                text=str(val), fill="red",
                font=("Arial", 10, "bold")
            )

        # Draw a connecting line between the top centers of each bar
        for i in range(len(points_for_line) - 1):
            x1, y1 = points_for_line[i]
            x2, y2 = points_for_line[i + 1]
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="red", width=2
            )

def main():
    root = tk.Tk()
    app = HistoricalDataApp(master=root)
    # Set an initial window size (user can resize later)
    root.geometry("600x400")
    root.mainloop()

if __name__ == "__main__":
    main()
