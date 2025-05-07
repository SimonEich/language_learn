from .utils import destroy_widgets, add_back_button
from tkinter import *
from transformers import MarianMTModel, MarianTokenizer
import re

# Load MarianMT model
src_lang = "es"
tgt_lang = "en"
model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

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
    text = root.text_field.get("1.0", END).strip()
    sentences = re.split(r'(?<=[.!?]) +', text.strip())

    # Clear all widgets on screen
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text="Click a sentence to translate it:", font=("Arial", 14)).pack(pady=10)

    text_widget = Text(root, wrap=WORD, font=("Arial", 20), height=10)
    text_widget.pack(padx=10, pady=10, fill=X)
    
    
    # Create a label for translation output with line wrapping
    label = Label(root, text="", font=('Arial', 20), wraplength=700, justify=LEFT)
    label.pack(pady=20, padx=20)



    # Pass label as an argument when binding sentences
    for i, sentence in enumerate(sentences):
        tag = f"sentence_{i}"
        text_widget.insert(END, sentence + " ", tag)

        # Fix late binding issue by defining the function inside the loop
        def make_callback(s):
            return lambda e: translate_text(s, label)

        text_widget.tag_bind(tag, "<Button-1>", make_callback(sentence))

def translate_text(s, label):
    inputs = tokenizer(s, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    output = tokenizer.decode(translated[0], skip_special_tokens=True)

    # Update the label with the translated text
    label.config(text=output)

