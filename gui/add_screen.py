from tkinter import *
from tkinter import filedialog, ttk
import tkinter as tk

from .utils import destroy_widgets, add_back_button


def addData_screen(app) -> None:
    destroy_widgets(app.root)
    add_back_button(app.root, app.show_start_screen)
    tk.Label(app.root, text='Add Data', font=('Arial', 24, 'bold')).place(relx=0.5, y=20, anchor='n')
    app.spanish_field = Entry(app.root, font=("Arial", 14), width=20)
    app.spanish_field.place(relx=0.2, y=100, anchor="n")
    app.english_field = Entry(app.root, font=("Arial", 14), width=20)
    app.english_field.place(relx=0.50, y=100, anchor="n")

    def add_command():
        app.data.insert_word(app.spanish_field.get(), app.english_field.get())
        app.spanish_field.delete(0, tk.END)
        app.english_field.delete(0, tk.END)

    Button(app.root, text='Add Data', width=12, font=("Arial", 14), command=add_command).place(relx=0.8, y=100, anchor="n")
    app.root.bind('<Return>', lambda event: add_command())
    Button(app.root, text='Add words by file', width=12, font=("Arial", 14), command=lambda: choose_file(app)).place(relx=0.5, y=200, anchor="n")
    Button(app.root, text='See words', width=12, font=("Arial", 14), command=lambda: list_screen(app)).place(relx=0.5, y=250, anchor="n")


def list_screen(app) -> None:
    destroy_widgets(app.root)
    add_back_button(app.root, app.show_start_screen)

    def resetCount_reload():
        app.data.reset_count_db()
        list_screen(app)

    tk.Label(app.root, text='All Words', font=('Arial', 24, 'bold')).place(relx=0.5, y=20, anchor='n')
    Button(app.root, text="Reset count", width=12, font=("Arial", 14), command=resetCount_reload).place(relx=0.85, y=20, anchor="n")

    tree = ttk.Treeview(
        app.root,
        columns=("Number", "Spanish", "English", "Count", "Delete", "Edit"),
        show="headings",
        height=15
    )
    tree.place(relx=0.5, y=100, anchor="n")

    for col in ("Number", "Spanish", "English", "Count", "Delete", "Edit"):
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    all_words = app.data.read_db()
    for idx, (word, translation, count) in enumerate(all_words, 1):
        tree.insert("", "end", values=(idx, word, translation, count, "❌", "⚙️"))

    scrollbar = tk.Scrollbar(app.root, orient="vertical", command=tree.yview)
    scrollbar.place(relx=1, y=100, anchor='n', height=300)
    tree.config(yscrollcommand=scrollbar.set)

    tree.bind("<Button-1>", lambda event: handle_tree_click(event, tree, app))


def handle_tree_click(event, tree, app):
    region = tree.identify("region", event.x, event.y)
    if region != "cell":
        return

    row_id = tree.identify_row(event.y)
    column = tree.identify_column(event.x)

    if not row_id:
        return

    selected_item = tree.item(row_id)["values"]
    if not selected_item:
        return

    spanish = selected_item[1]
    english = selected_item[2]

    if column == "#5":  # Delete
        app.data.delete_word(spanish)
        list_screen(app)
    elif column == "#6":  # Edit
        edit_screen(app, [spanish, english])


def choose_file(app):
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(("Text and CSV files", "*.txt *.csv"),)
    )
    if file_path:
        app.data.insert_from_file(file_path)
        print("Selected file:", file_path)


def show_all_words(app) -> None:
    destroy_widgets(app.root)
    add_back_button(app.root, app.show_start_screen)
    tk.Label(app.root, text='All Words', font=('Arial', 24, 'bold')).place(relx=0.5, y=20, anchor='n')
    words_listbox = tk.Listbox(app.root, font=("Arial", 14), width=40, height=15)
    words_listbox.place(relx=0.5, y=100, anchor='n')

    words = app.data.read_db()
    for spanish, english, _ in words:
        words_listbox.insert(tk.END, f"{spanish} - {english}")


def edit_screen(app, edit_word: list) -> None:
    destroy_widgets(app.root)
    add_back_button(app.root, app.show_start_screen)
    tk.Label(app.root, text='Edit Word', font=('Arial', 24, 'bold')).place(relx=0.5, y=20, anchor='n')
    spanish_entry = Entry(app.root, font=("Arial", 14), width=20)
    spanish_entry.place(relx=0.3, y=100, anchor="n")
    spanish_entry.insert(0, edit_word[0])
    english_entry = Entry(app.root, font=("Arial", 14), width=20)
    english_entry.place(relx=0.7, y=100, anchor="n")
    english_entry.insert(0, edit_word[1])

    def save_edit():
        new_spanish = spanish_entry.get()
        new_english = english_entry.get()
        app.data.update_word(edit_word[0], new_spanish, new_english)
        list_screen(app)

    Button(app.root, text='Save', width=12, font=("Arial", 14), command=save_edit).place(relx=0.5, y=200, anchor='n')
