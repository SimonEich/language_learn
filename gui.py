import random
from tkinter import *
from tkinter import filedialog, ttk
import tkinter as tk
from read_file import ReadFile  # Make sure this file/module exists and works

class Gui:
    def __init__(self, data):
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

        self._create_gui()

    def _create_gui(self) -> None:
        self.show_start_screen()

    def _destroy_widgets(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def _backButton(self) -> None:
        back_button = Button(self.root, text='Back', width=12, font=('Arial', 14), command=self.show_start_screen)
        back_button.place(relx=0.15, y=20, anchor='n')

    def show_start_screen(self) -> None:
        self._destroy_widgets()

        label = tk.Label(self.root, text='Start', font=("Arial", 24, "bold"))
        label.place(relx=0.25, y=10, anchor="n")

        start_button = Button(self.root, text='Start Game', width=12, font=("Arial", 14), command=self.game_screen)
        start_button.place(relx=0.25, y=80, anchor="n")

        train_button = Button(self.root, text='Training', width=12, font=("Arial", 14), command=self.training_screen)
        train_button.place(relx=0.25, y=120, anchor="n")

        add_button = Button(self.root, text='Add Words', width=12, font=("Arial", 14), command=self.addData_screen)
        add_button.place(relx=0.75, y=80, anchor="n")

    def game_screen(self):
        self._destroy_widgets()
        self._backButton()
        self.lives = 3
        self.correct_count = 0
        self.word_array = self.data.read_db()
        self.total_words = len(self.word_array)

        tk.Label(self.root, text='Game', font=("Arial", 24, "bold")).place(relx=0.5, y=20, anchor="n")

        self.lives_label = tk.Label(self.root, text='❤️❤️❤️', font=("Arial", 20, 'bold'))
        self.lives_label.place(relx=0.75, y=20, anchor="n")

        self.correct_label = tk.Label(self.root, text=f"Correct: 0", font=("Arial", 14, 'bold'))
        self.correct_label.place(relx=0.25, y=60, anchor='n')

        self.remaining_label = tk.Label(self.root, text=f"Remaining: {self.total_words}", font=("Arial", 14, 'bold'))
        self.remaining_label.place(relx=0.75, y=60, anchor='n')

        self.load_new_word()

    def load_new_word(self, after_incorrect=False, idx=None):
        self._destroy_widgets()
        self._backButton()

        tk.Label(self.root, text='Game', font=("Arial", 24, "bold")).place(relx=0.5, y=20, anchor="n")

        self.lives_label = tk.Label(self.root, text='❤️' * self.lives, font=("Arial", 20, 'bold'))
        self.lives_label.place(relx=0.75, y=20, anchor="n")

        self.correct_label = tk.Label(self.root, text=f"Correct: {self.correct_count}", font=("Arial", 14, 'bold'))
        self.correct_label.place(relx=0.25, y=60, anchor='n')

        self.remaining_label = tk.Label(self.root, text=f"Remaining: {len(self.word_array)}", font=("Arial", 14, 'bold'))
        self.remaining_label.place(relx=0.75, y=60, anchor='n')

        if after_incorrect and idx is not None:
            del self.word_array[idx]

        if not self.word_array:
            tk.Label(self.root, text='You Win!', font=("Arial", 24, 'bold')).place(relx=0.5, y=150, anchor='n')
            return

        db_length = len(self.word_array)
        random_number_word = random.randrange(0, db_length)
        correct_word = self.word_array[random_number_word]
        word, correct_translation = correct_word[0], correct_word[1]

        other_words = random.sample(
            [w[1] for i, w in enumerate(self.word_array) if i != random_number_word], min(2, db_length - 1)
        )
        options = other_words + [correct_translation]
        random.shuffle(options)

        tk.Label(self.root, text=word, font=("Arial", 20, 'bold')).place(relx=0.5, y=120, anchor="n")

        for i, opt in enumerate(options):
            relx = 0.25 + i * 0.25
            is_correct = opt == correct_translation
            btn = Button(self.root, text=opt, width=12, font=("Arial", 14),
                         command=lambda correct=is_correct, idx=random_number_word: self.check_word(correct, idx))
            btn.place(relx=relx, y=250, anchor="n")

            
    def show_correct(self, idx) -> None:
        self._destroy_widgets()
        self._backButton()

        tk.Label(self.root, text='Wrong!', font=("Arial", 24, "bold"), fg="red").place(relx=0.5, y=50, anchor="n")
        tk.Label(self.root, text=f"{self.word_array[idx][0]}", font=("Arial", 20, "bold")).place(relx=0.5, y=100, anchor="n")

        tk.Label(self.root, text=f"Correct answer:\n{self.word_array[idx][1]}", font=("Arial", 20, "bold")).place(relx=0.5, y=150, anchor="n")

        next_button = Button(self.root, text="Next", width=12, font=("Arial", 14), command=lambda: self.load_new_word(after_incorrect=True, idx=idx))
        next_button.place(relx=0.5, y=300, anchor="n")

    
    def check_word(self, is_correct, index):
        if is_correct:
            del self.word_array[index]
            self.correct_count += 1
            self.load_new_word()
        else:
            self.lives -= 1
            if self.lives <= 0:
                self.show_correct(index)
                self._destroy_widgets()
                self._backButton()
                tk.Label(self.root, text='Game Over', font=("Arial", 30, "bold"), fg="red").place(relx=0.5, y=150, anchor="n")
            else:
                self.show_correct(index)

    def training_screen(self) -> None:
        self._destroy_widgets()
        self._backButton()
        
        
        training_words = self.data.get_training_words()
        index = random.randrange(0, len(training_words))
        print(training_words)
        training_word = training_words[index][0]
        training_word_translation = training_words[index][1]


        tk.Label(self.root, text='Training', font=('Arial', 18, 'bold')).place(relx=0.5, y=20, anchor='n')
        tk.Label(self.root, text='new Words: 0', font=("Arial", 14, 'bold')).place(relx=0.75, y=20, anchor='n')
        tk.Label(self.root, text=training_word_translation, font=("Arial", 24, 'bold')).place(relx=0.5, y=100, anchor='n')

        training_check_button = Button(self.root, text="Translate", width=12, font=("Arial", 14), command=lambda: self.training_check_screen(training_word, training_word_translation))
        training_check_button.place(relx=0.5, y=300, anchor="n")        
        
    def training_check_screen(self, training_word, training_word_translation) -> None:
        self._destroy_widgets()
        self._backButton()
        
        
        tk.Label(self.root, text='Training', font=('Arial', 18, 'bold')).place(relx=0.5, y=20, anchor='n')
        tk.Label(self.root, text='new Words: 0', font=("Arial", 14, 'bold')).place(relx=0.75, y=20, anchor='n')
        tk.Label(self.root, text=training_word_translation, font=("Arial", 24, 'bold')).place(relx=0.5, y=100, anchor='n')
        
        tk.Label(self.root, text=training_word, font=('Araial', 24, 'bold')).place(relx=0.5, y= 200, anchor='n')
        
        training_right_button = Button(self.root, text="Right", width=12, font=("Arial", 14), command=lambda: self.training_right_wrong(word_right=True, training_word=training_word))
        training_right_button.place(relx=0.75, y=300, anchor="n")
        
        training_wrong_button = Button(self.root, text="Wrong", width=12, font=("Arial", 14), command=lambda: self.training_right_wrong(word_right=False, training_word=training_word))
        training_wrong_button.place(relx=0.25, y=300, anchor="n")
        
    def training_right_wrong(self, word_right, training_word)->None:
        if word_right == True:
            print()
            self.data.increase_count(training_word) 
            self.training_screen()
        else: 
            self.training_screen()
        
        
        
        
        
        

    def addData_screen(self) -> None:
        self._destroy_widgets()
        self._backButton()

        tk.Label(self.root, text='Add Data', font=('Arial', 24, 'bold')).place(relx=0.5, y=20, anchor='n')

        self.spanish_field = Entry(self.root, font=("Arial", 14), width=20)
        self.spanish_field.place(relx=0.2, y=100, anchor="n")

        self.english_field = Entry(self.root, font=("Arial", 14), width=20)
        self.english_field.place(relx=0.50, y=100, anchor="n")

        add_command = lambda: (
            self.data.insert_word(self.spanish_field.get(), self.english_field.get()),
            self.spanish_field.delete(0, tk.END),
            self.english_field.delete(0, tk.END)
        )

        Button(self.root, text='Add Data', width=12, font=("Arial", 14), command=add_command).place(relx=0.8, y=100, anchor="n")
        self.root.bind('<Return>', lambda event: add_command())

        Button(self.root, text='Add words by file', width=12, font=("Arial", 14), command=self.choose_file).place(relx=0.5, y=200, anchor="n")
        Button(self.root, text='See words', width=12, font=("Arial", 14), command=self.list_screen).place(relx=0.5, y=250, anchor="n")

    def list_screen(self) -> None:
        self._destroy_widgets()
        self._backButton()

        def resetCount_reload():
            self.data.reset_count_db()
            self.list_screen()

        tk.Label(self.root, text='All Words', font=('Arial', 24, 'bold')).place(relx=0.5, y=20, anchor='n')


        reset_button = Button(self.root, text="Reset count", width=12, font=("Arial", 14), command=lambda: resetCount_reload())
        reset_button.place(relx=0.85, y=20, anchor="n")
        # Updated Treeview with "Count" column
        tree = ttk.Treeview(
            self.root,
            columns=("Number", "Spanish", "English", "Count", "Delete", "Edit"),
            show="headings",
            height=15
        )
        tree.place(relx=0.5, y=100, anchor="n")

        # Define headings
        tree.heading("Number", text="No.")
        tree.heading("Spanish", text="Spanish")
        tree.heading("English", text="English")
        tree.heading("Count", text="Count")
        tree.heading("Delete", text="Delete")
        tree.heading("Edit", text="Edit")

        # Define column width
        tree.column("Number", width=50, anchor="center")
        tree.column("Spanish", width=150)
        tree.column("English", width=150)
        tree.column("Count", width=40, anchor="center")  # Width 20 as you requested
        tree.column("Delete", width=60, anchor="center")
        tree.column("Edit", width=60, anchor="center")

        # Read all words and insert into tree
        all_words = self.data.read_db()

        for idx, (word, translation, count) in enumerate(all_words, 1):
            tree.insert("", "end", values=(idx, word, translation, count, "❌", "⚙️"))

        # Add vertical scrollbar
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=tree.yview)
        scrollbar.place(relx=1, y=100, anchor='n', height=300)
        tree.config(yscrollcommand=scrollbar.set)

        # Handle delete/edit clicks
        tree.bind("<Button-1>", lambda event: self.handle_tree_click(event, tree))

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=(("Text and CSV files", "*.txt *.csv"),)
        )
        if file_path:
            self.data.insert_from_file(file_path)
            print("Selected file:", file_path)

    def show_all_words(self) -> None:
        self._destroy_widgets()
        self._backButton()
        tk.Label(self.root, text='All Words', font=('Arial', 24, 'bold')).place(relx=0.5, y=20, anchor='n')
        words_listbox = tk.Listbox(self.root, font=("Arial", 14), width=40, height=15)
        words_listbox.place(relx=0.5, y=100, anchor='n')

    def edit_screen(self, edit_word: list) -> None:
        self._destroy_widgets()
        self._backButton()

        tk.Label(self.root, text='Edit Word', font=('Arial', 24, 'bold')).place(relx=0.5, y=20, anchor='n')

        spanish_entry = Entry(self.root, font=("Arial", 14), width=20)
        spanish_entry.place(relx=0.3, y=100, anchor="n")
        spanish_entry.insert(0, edit_word[0])

        english_entry = Entry(self.root, font=("Arial", 14), width=20)
        english_entry.place(relx=0.7, y=100, anchor="n")
        english_entry.insert(0, edit_word[1])

        def save_edit():
            new_spanish = spanish_entry.get()
            new_english = english_entry.get()
            self.data.update_word(edit_word[0], new_spanish, new_english)
            self.list_screen()

        save_edit_button = Button(self.root, text='Save', width=12, font=('Arial', 14), command=save_edit)
        save_edit_button.place(relx=0.5, y=200, anchor='n')

# You can start the GUI like this:
# if __name__ == "__main__":
#     data = ReadFile("your_database_path_or_handler_here")
#     gui = Gui(data)
#     gui.root.mainloop()
