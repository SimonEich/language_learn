import tkinter as tk
import random
from .utils import destroy_widgets, add_back_button

def setup_game_screen(gui):
    destroy_widgets(gui.root)
    add_back_button(gui.root, gui.show_start_screen)

    gui.lives = 3
    gui.correct_count = 0
    gui.word_array = gui.data.read_db()
    gui.total_words = len(gui.word_array)

    tk.Label(gui.root, text='Game', font=("Arial", 24, "bold")).place(relx=0.5, y=20, anchor="n")
    gui.lives_label = tk.Label(gui.root, text='❤️❤️❤️', font=("Arial", 20, 'bold'))
    gui.lives_label.place(relx=0.75, y=20, anchor="n")

    gui.correct_label = tk.Label(gui.root, text=f"Correct: 0", font=("Arial", 14, 'bold'))
    gui.correct_label.place(relx=0.25, y=60, anchor='n')

    gui.remaining_label = tk.Label(gui.root, text=f"Remaining: {gui.total_words}", font=("Arial", 14, 'bold'))
    gui.remaining_label.place(relx=0.75, y=60, anchor='n')

    load_new_word(gui)

def load_new_word(gui, after_incorrect=False, idx=None):
    if after_incorrect and idx is not None:
        del gui.word_array[idx]

    if not gui.word_array:
        destroy_widgets(gui.root)
        tk.Label(gui.root, text='You Win!', font=("Arial", 24, 'bold')).place(relx=0.5, y=150, anchor='n')
        return

    destroy_widgets(gui.root)
    add_back_button(gui.root, gui.show_start_screen)

    tk.Label(gui.root, text='Game', font=("Arial", 24, "bold")).place(relx=0.5, y=20, anchor="n")
    gui.lives_label = tk.Label(gui.root, text='❤️' * gui.lives, font=("Arial", 20, 'bold'))
    gui.lives_label.place(relx=0.75, y=20, anchor="n")
    gui.correct_label = tk.Label(gui.root, text=f"Correct: {gui.correct_count}", font=("Arial", 14, 'bold'))
    gui.correct_label.place(relx=0.25, y=60, anchor='n')
    gui.remaining_label = tk.Label(gui.root, text=f"Remaining: {len(gui.word_array)}", font=("Arial", 14, 'bold'))
    gui.remaining_label.place(relx=0.75, y=60, anchor='n')

    random_number_word = random.randrange(0, len(gui.word_array))
    correct_word = gui.word_array[random_number_word]
    word, correct_translation = correct_word[0], correct_word[1]

    other_words = random.sample([w[1] for i, w in enumerate(gui.word_array) if i != random_number_word], min(2, len(gui.word_array) - 1))
    options = other_words + [correct_translation]
    random.shuffle(options)

    tk.Label(gui.root, text=word, font=("Arial", 20, 'bold')).place(relx=0.5, y=120, anchor="n")

    for i, opt in enumerate(options):
        relx = 0.25 + i * 0.25
        is_correct = opt == correct_translation
        btn = tk.Button(gui.root, text=opt, width=12, font=("Arial", 14),
                        command=lambda correct=is_correct, idx=random_number_word: check_word(gui, correct, idx))
        btn.place(relx=relx, y=250, anchor="n")

def check_word(gui, is_correct, index):
    if is_correct:
        del gui.word_array[index]
        gui.correct_count += 1
        load_new_word(gui)
    else:
        gui.lives -= 1
        if gui.lives <= 0:
            game_over(gui, index)
        else:
            show_correct(gui, index)

def show_correct(gui, idx):
    destroy_widgets(gui.root)
    add_back_button(gui.root, gui.show_start_screen)
    tk.Label(gui.root, text='Wrong!', font=("Arial", 24, "bold"), fg="red").place(relx=0.5, y=50, anchor="n")
    tk.Label(gui.root, text=f"{gui.word_array[idx][0]}", font=("Arial", 20, "bold")).place(relx=0.5, y=100, anchor="n")
    tk.Label(gui.root, text=f"Correct answer:\n{gui.word_array[idx][1]}", font=("Arial", 20, "bold")).place(relx=0.5, y=150, anchor="n")

    tk.Button(gui.root, text="Next", width=12, font=("Arial", 14),
              command=lambda: load_new_word(gui, after_incorrect=True, idx=idx)).place(relx=0.5, y=300, anchor="n")

def game_over(gui, index):
    show_correct(gui, index)
    destroy_widgets(gui.root)
    add_back_button(gui.root, gui.show_start_screen)
    tk.Label(gui.root, text='Game Over', font=("Arial", 30, "bold"), fg="red").place(relx=0.5, y=150, anchor="n")
