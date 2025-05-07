from .utils import destroy_widgets, add_back_button
from tkinter import *

import re

#from transformers import MarianMTModel, MarianTokenizer

# Load MarianMT model
src_lang = "es"
tgt_lang = "en"
model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
#tokenizer = MarianTokenizer.from_pretrained(model_name)
#model = MarianMTModel.from_pretrained(model_name)

def text_screen(self):
    # GUI
    root = Tk()
    root.title("Offline Translator")
    root.geometry("800x600")

    Label(root, text="Enter text:", font=("Arial", 14)).pack(pady=(30, 10))

    root.text_field = Text(root, font=("Arial", 14), wrap=WORD, height=6)
    root.text_field.pack(padx=20, pady=10, fill=BOTH, expand=False, ipady=100)

    convert_text_button = Button(
        root,
        text='Convert',
        width=12,
        font=("Arial", 14),
        command=lambda: text_translate_screen(root)
    )
    convert_text_button.pack(pady=80)

    self.root = root
    root.mainloop()

def text_translate_screen(root):
    text = root.text_field.get("1.0", END).strip()  # Get all the text from the Text widget
    sentences = re.split(r'(?<=[.!?]) +', text.strip())  # Split text into sentences

    # Clear any existing widgets (if needed)
    for widget in root.winfo_children():
        widget.destroy()

    # Show the label
    Label(root, text="Click a sentence to print it:", font=("Arial", 14)).pack(pady=10)

    # Create a Text widget to display the sentences
    text_widget = Text(root, wrap=WORD, font=("Arial", 20))
    text_widget.pack(expand=True, fill=BOTH, padx=10, pady=10)

    # Insert and tag each sentence
    for i, sentence in enumerate(sentences):
        tag = f"sentence_{i}"
        text_widget.insert(END, sentence + " ", tag)

        # Bind each sentence to a click event that prints it
        def bind_sentence(s):
            return lambda e: print(s)

        text_widget.tag_bind(tag, "<Button-1>", bind_sentence(sentence))

    # Add a back button to return to the previous screen
    back_button = Button(root, text="Back", font=("Arial", 14), command=lambda: go_back(root))
    back_button.pack(pady=10)


def go_back(root):
    # Close the current window (destroy the root window)
    root.destroy()

    # Recreate the initial window (text screen)
    text_screen(None)
