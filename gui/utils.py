import tkinter as tk

def destroy_widgets(root):
    for widget in root.winfo_children():
        widget.destroy()

def add_back_button(root, callback):
    tk.Button(root, text='Back', width=12, font=('Arial', 14), command=callback).place(relx=0.15, y=20, anchor='n')
