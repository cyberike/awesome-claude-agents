import tkinter as tk
from tkinter import ttk

class EmbeddedUI:
    def __init__(self, master):
        self.master = master
        master.title("Embedded UI")

        self.label = ttk.Label(master, text="Welcome to the Embedded UI")
        self.label.pack()

        self.button = ttk.Button(master, text="Click Me", command=self.button_click)
        self.button.pack()

    def button_click(self):
        self.label.config(text="Button clicked!")

root = tk.Tk()
ui = EmbeddedUI(root)
root.mainloop()
