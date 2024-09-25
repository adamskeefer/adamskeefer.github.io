import os
import tkinter as tk
from tkinter import filedialog
import labeler as labeler
global completion_label
global folder_label

def browse():
    global selected
    selected = filedialog.askdirectory()
    if selected:
        folder_label.config(text="Selected Folder: " + selected)
        run_button.pack()

def run():
    if not selected:
        return

    roll_value = textfield_var.get()
    if not roll_value:
        roll_value = -1
    slider_value = slider.get()
    labeler.label(selected, slider_value, int(roll_value))
    completion_label.config(text="Files Renamed")

  
root = tk.Tk()
root.title("Mr. Fish File Manager")

folder_label = tk.Label(root, text="No folder selected")
folder_label.pack()

completion_label = tk.Label(root, text="")
completion_label.pack()

slider_label = tk.Label(root, text="Threshold (Higher = Faster but less conversions)")
slider_label.pack()

slider = tk.Scale(root, from_=0, to=100, orient="horizontal")
slider.pack()

textfield_var = tk.StringVar()

textfield_label = tk.Label(root, text="Roll (leave blank for auto detection):")
textfield_label.pack()
textfield = tk.Entry(root, textvariable=textfield_var)
textfield.pack()

browse_button = tk.Button(root, text="Browse Folder", command=browse)
browse_button.pack()

run_button = tk.Button(root, text="Run", command=run)

root.mainloop()

selected = None