"""
GUI application for a Spanish-English vocabulary trainer using Tkinter.
Features:
- Game mode with multiple choice translation
- Training mode with self-assessment
- Word management (add, view, edit, delete)
"""

from tkinter import *
from tkinter import filedialog, ttk
import tkinter as tk

from .game_screen import setup_game_screen
from .training_screen import training_screen
from .add_screen import addData_screen
from .text_screen import text_screen

from .utils import destroy_widgets, add_back_button

class Gui:
    """
    Main GUI class for the vocabulary training application.
    
    Attributes:
        data: An object that handles data operations (e.g., database access).
        root: The main Tkinter window.
    """
    def __init__(self, data):
        """
        Initialize the GUI, set up initial state, and create the root window.
        
        Args:
            data: A data handler object with methods like read_db(), insert_word(), etc.
        """
        self.data = data
        self.root = tk.Tk()
        self.root.geometry("600x400")
        self.root.title("El espanol")

        self.word_var = StringVar()
        self.lives = 3
        self.word_array = []
        self.lives_label = None
        self.correct_count = 0
        self.total_words = 0
        self.correct_label = None
        self.remaining_label = None

        self.show_start_screen()
        
    def show_start_screen(self) -> None:
        """Display the start screen with navigation buttons."""
        destroy_widgets(self.root)
        
        
        label = tk.Label(self.root, text='Start', font=("Arial", 24, "bold"))
        label.place(relx=0.25, y=10, anchor="n")

        start_button = Button(self.root, text='Start Game', width=12, font=("Arial", 14), command=lambda: setup_game_screen(self))
        start_button.place(relx=0.25, y=80, anchor="n")

        training_button = Button(self.root, text='Training', width=12, font=("Arial", 14), command=lambda: training_screen(self))
        training_button.place(relx=0.25, y=120, anchor="n")

        add_button = Button(self.root, text='Add Words', width=12, font=("Arial", 14), command=lambda: addData_screen(self))
        add_button.place(relx=0.75, y=80, anchor="n")
        
        text_button = Button(self.root, text='Translate Text', width=12, font=("Arial", 14), command=lambda: text_screen(self))
        text_button.place(relx=0.75, y=120, anchor="n")
        

