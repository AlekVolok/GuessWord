import os
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from random import shuffle
import random

MAX_ROWS = 10

def check_pair(left_word, right_word):
    """Проверяет, соответствует ли пара словам из словаря."""
    if pairs.get(left_word) == right_word:
        # Если правильная пара, подсвечиваем зеленым
        left_buttons[left_word].config(bg="green", state=tk.DISABLED)
        right_buttons[right_word].config(bg="green", state=tk.DISABLED)
        
        # Проверяем, все ли пары найдены
        if all(btn.cget("bg") == "green" for btn in left_buttons.values()) and \
           all(btn.cget("bg") == "green" for btn in right_buttons.values()):
            messagebox.showinfo("Поздравляем!", "Вы угадали все пары!")
    else:
        # Если неправильная пара, подсвечиваем красным на короткое время
        left_buttons[left_word].config(bg="red")
        right_buttons[right_word].config(bg="red")
        root.after(1000, lambda: [left_buttons[left_word].config(bg="white"), right_buttons[right_word].config(bg="white")])

def on_left_click(word):
    global selected_left, selected_right
    if selected_right:
        check_pair(word, selected_right)
        selected_left = None
        selected_right = None
    else:
        selected_left = word

def on_right_click(word):
    global selected_left, selected_right
    if selected_left:
        check_pair(selected_left, word)
        selected_left = None
        selected_right = None
    else:
        selected_right = word

def load_words():
    global pairs
    topic = combo.get()
    
    with open(f"words_database/{topic}.json", "r", encoding="utf-8") as file:
        pairs = json.load(file)

    for btn in left_buttons.values():
        btn.destroy()
    
    for btn in right_buttons.values():
        btn.destroy()

    left_buttons.clear()
    right_buttons.clear()
    
    # Выберите случайные пары слов из словаря
    selected_pairs = random.sample(list(pairs.items()), min(MAX_ROWS, len(pairs)))

    # Разделим ключи и значения
    selected_left_words = [pair[0] for pair in selected_pairs]
    selected_right_words = [pair[1] for pair in selected_pairs]

    # Перемешиваем слова для правого столбца
    shuffle(selected_right_words)
    
    # Находим максимальное слово для установки ширины кнопки
    max_length = max(max(len(word) for word in selected_left_words), max(len(word) for word in selected_right_words)) + 2
    
    for word in selected_left_words:
        btn = tk.Button(left_frame, text=word, width=max_length, command=lambda w=word: on_left_click(w))
        btn.pack(pady=10)
        left_buttons[word] = btn

    for word in selected_right_words:
        btn = tk.Button(right_frame, text=word, width=max_length, command=lambda w=word: on_right_click(w))
        btn.pack(pady=10)
        right_buttons[word] = btn

# Получите список тематических названий из имен файлов в папке 'words_database'
topics = [filename.replace(".json", "") for filename in os.listdir("words_database") if filename.endswith(".json")]

root = tk.Tk()
root.title("Игра угадай пару")

# Фрейм для выпадающего списка и кнопки перезагрузки
frame = tk.Frame(root)
frame.pack(pady=20)

# Создайте выпадающий список и добавьте его во фрейм
global combo
combo = ttk.Combobox(frame, values=topics)
combo.grid(row=0, column=0, padx=10)
if topics:
    combo.set(topics[0])

combo.bind("<<ComboboxSelected>>", lambda event: load_words())

# Добавьте кнопку перезагрузки рядом с выпадающим списком
reload_button = tk.Button(frame, text="Reload", command=load_words)
reload_button.grid(row=0, column=1)


selected_left = None
selected_right = None
left_buttons = {}
right_buttons = {}

# Создаем два столбца (Frame'ы) для кнопок
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=20, pady=20)
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=20, pady=20)

selected_left = None
selected_right = None
left_buttons = {}
right_buttons = {}

load_words()  # Перенесите эту функцию здесь, после инициализации всех переменных.

root.mainloop()
