import tkinter as tk
from tkinter import messagebox

def show_prompt():
    # Create root window but hide it
    root = tk.Tk()
    root.withdraw()

    # Show a message box with an OK button
    messagebox.showinfo("( ͡◉◞ ͜ʖ◟ ͡◉) Grow a Garden!!", " "*35 + "\nHi\n" + " "*35)

show_prompt()
