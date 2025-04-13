# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 20:49:42 2025

@author: m
"""

# Importing necessary modules
import tkinter as tk
from tkinter import ttk, Canvas, Frame, BOTH
class BarDisplay(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.value = 0
        self.initUI()

    def initUI(self):
        self.master.title('Bar Display')
        self.pack(fill=BOTH, expand=1)

        # Canvas for the bar
        self.canvas = Canvas(self, width=300, height=100)
        self.canvas.pack()

        # Entry and Button to change the value
        self.entry = ttk.Entry(self)
        self.entry.pack()
        self.button = ttk.Button(self, text='Update Value', command=self.update_bar)
        self.button.pack()

        # Display description text
        self.desc_label = ttk.Label(self, text='Units: Celsius\nLow: 0, Normal: 20-25, High: 30')
        self.desc_label.pack()

        self.draw_bar()

    def draw_bar(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(10, 40, 10 + (self.value * 2), 60, fill='lightgreen')
        self.canvas.create_text(150, 20, text=str(self.value), font=('Helvetica', 20))

    def update_bar(self):
        try:
            self.value = int(self.entry.get())
            if 0 <= self.value <= 100:
                self.draw_bar()
            else:
                print("Please enter a value between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")         
            


if __name__ == '__main__':
  
    root2 = tk.Tk()
    app2 = BarDisplay(master=root2)
    root2.geometry('400x200')
    root2.mainloop()
