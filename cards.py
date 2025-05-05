from tkinter import *
import tkinter as tk

class Card:
    def __init__(self)->None:
        
        self._create_gui()
        
        
    def _create_gui(self)->None:
     
        self.root = Tk()  # Initialize the main window
        self.label = Label(self.root, text='Hello World')
        button = tk.Button(self.root, text='Button', command=forward)
        button.pack()
        self.label.pack()
        
    def print(self)->None:
        print('got it!')
        
def forward():
    print('forward')