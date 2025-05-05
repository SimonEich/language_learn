import tkinter as tk
import random

from tkinter import *

from .utils import destroy_widgets, add_back_button
 
def training_screen(self) -> None:
    """Display the training screen with a randomly selected word."""
    destroy_widgets(self.root)
    add_back_button(self.root, self.show_start_screen)
    training_words = self.data.get_training_words()
    index = random.randrange(0, len(training_words))
    training_word = training_words[index][0]
    training_word_translation = training_words[index][1]
    tk.Label(self.root, text='Training', font=('Arial', 18, 'bold')).place(relx=0.5, y=20, anchor='n')
    tk.Label(self.root, text='new Words: 0', font=("Arial", 14, 'bold')).place(relx=0.75, y=20, anchor='n')
    tk.Label(self.root, text=training_word_translation, font=("Arial", 24, 'bold')).place(relx=0.5, y=100, anchor='n')
    training_check_button = Button(self.root, text="Translate", width=12, font=("Arial", 14), command=lambda: training_check_screen(self, training_word, training_word_translation))
    training_check_button.place(relx=0.5, y=300, anchor="n")   
    
         
def training_check_screen(self, training_word, training_word_translation) -> None:
    """
    Show the correct answer for a training word and let the user mark it correct/incorrect.
    
    Args:
        training_word (str): The Spanish word.
        training_word_translation (str): Its English translation.
    """
    destroy_widgets(self.root)
    add_back_button(self.root, self.show_start_screen)
    tk.Label(self.root, text='Training', font=('Arial', 18, 'bold')).place(relx=0.5, y=20, anchor='n')
    tk.Label(self.root, text='new Words: 0', font=("Arial", 14, 'bold')).place(relx=0.75, y=20, anchor='n')
    tk.Label(self.root, text=training_word_translation, font=("Arial", 24, 'bold')).place(relx=0.5, y=100, anchor='n')
    tk.Label(self.root, text=training_word, font=('Arial', 24, 'bold')).place(relx=0.5, y=200, anchor='n')
    Button(self.root, text="Right", width=12, font=("Arial", 14), command=lambda: training_right_wrong(self, True, training_word)).place(relx=0.75, y=300, anchor="n")
    Button(self.root, text="Wrong", width=12, font=("Arial", 14), command=lambda: training_right_wrong(self, False, training_word)).place(relx=0.25, y=300, anchor="n")
    
    
def training_right_wrong(self, word_right, training_word) -> None:
    """
    Update the word count if answered correctly and show the next word.
    
    Args:
        word_right (bool): Whether the user knew the word.
        training_word (str): The word in question.
    """
    if word_right:
        self.data.increase_count(training_word)
    training_screen(self)