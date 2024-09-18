import os
import tkinter as tk
from tkinter import filedialog
import labeler
global completion_label
global folder_label

def browse():
    global selected
    selected = filedialog.askdirectory()
    if selected:
        folder_label.config(text="Selected Folder: " + selected)

def run():
    if not selected:
        return

    labeler.label(selected)
    completion_label.config(text="Files Renamed")

    
root = tk.Tk()
root.title("Folder Selection and Run")

folder_label = tk.Label(root, text="No folder selected")
folder_label.pack()

completion_label = tk.Label(root, text="")
completion_label.pack()

browse_button = tk.Button(root, text="Browse Folder", command=browse)
browse_button.pack()

run_button = tk.Button(root, text="Run", command=run)
run_button.pack()

root.mainloop()

selected = None