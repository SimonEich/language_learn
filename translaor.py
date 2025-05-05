from tkinter import *
from transformers import MarianMTModel, MarianTokenizer

# Load MarianMT model
src_lang = "es"
tgt_lang = "en"
model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_text():
    text = input_field.get("1.0", END)
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    output = tokenizer.decode(translated[0], skip_special_tokens=True)
    output_field.delete("1.0", END)
    output_field.insert(END, output)

# GUI
root = Tk()
root.title("Offline Translator")
root.geometry("2000x3000")

Label(root, text="Enter text:").pack()
input_field = Text(root, height=5)
input_field.pack()

Button(root, text="Translate", command=translate_text).pack()

Label(root, text="Translation:").pack()
output_field = Text(root, height=5)
output_field.pack()

root.mainloop()

