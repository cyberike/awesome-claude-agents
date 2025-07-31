import tkinter as tk
from tkinter import ttk

class EmbeddedUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Embedded UI")
        self.geometry("800x480")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Create and configure widgets for the embedded UI
        label = ttk.Label(self, text="Welcome to the Embedded UI")
        label.pack(pady=20)
        
        button = ttk.Button(self, text="Click Me", command=self.button_clicked)
        button.pack(pady=10)
    
    def button_clicked(self):
        print("Button clicked!")

if __name__ == "__main__":
    app = EmbeddedUI()
    app.mainloop()
