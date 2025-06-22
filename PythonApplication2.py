import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import random
import time

arr = []
time_spent = 0.0
repeat_sort = False

def bubble_sort():
    global repeat_sort, time_spent  
    if repeat_sort:
        messagebox.showinfo("Повтор", "Массив уже отсортирован")  
        return
    
    if not arr:
        messagebox.showwarning("Ошибка", "Сначала создайте массив!")
        return
    
    start = time.time()
    for i in range(len(arr) - 1):
        swapped = False
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    end = time.time()
    time_spent = end - start
    update_array_display()
    repeat_sort = True
    messagebox.showinfo("Успех", f"Массив отсортирован за {time_spent:.20f} сек.")

def generate_array():
    global arr, repeat_sort 
    try:
        size = int(entry_size.get())
        if size <= 0:
            raise ValueError
        arr = [random.randint(0, 1000000) for _ in range(size)]
        update_array_display()
        repeat_sort = False 
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректный размер массива!")

def save_array():
    if not arr:
        messagebox.showwarning("Ошибка", "Сначала создайте массив!")
        return
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt")])
    if not filename:
        return
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{len(arr)}\n")
            f.write(" ".join(map(str, arr)))
        messagebox.showinfo("Успех", "Массив успешно записан!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

def load_array():
    global arr
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not filename:
        return
    try:
        with open(filename, "r", encoding="utf-8") as f:
            size = int(f.readline())
            arr = list(map(int, f.read().split()))
        update_array_display()
        messagebox.showinfo("Успех", "Массив успешно загружен!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось прочитать файл:\n{e}")

def update_array_display():
    text_array.delete("1.0", tk.END)
    if not arr:
        text_array.insert(tk.END, "[пусто]")
    else:
        text_array.insert(tk.END, "\n".join(f"{i+1}) {val}" for i, val in enumerate(arr)))

def show_time():
    if time_spent == 0.0:
        messagebox.showinfo("Время сортировки", "Сначала отсортируйте массив!")
    else:
        messagebox.showinfo("Время сортировки", f"{time_spent:.6f} сек.")

root = tk.Tk()
root.title("Сортировка пузырьком")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Размер массива:").pack(side=tk.LEFT)
entry_size = tk.Entry(frame_top, width=10)
entry_size.pack(side=tk.LEFT, padx=5)
tk.Button(frame_top, text="Сгенерировать", command=generate_array).pack(side=tk.LEFT)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Сортировать", width=15, command=bubble_sort).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Сохранить в файл", width=15, command=save_array).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_buttons, text="Загрузить из файла", width=15, command=load_array).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Время сортировки", width=15, command=show_time).grid(row=1, column=1, padx=5, pady=5)

frame_array = tk.LabelFrame(root, text="Массив", padx=10, pady=10)
frame_array.pack(fill="both", expand=True, padx=10, pady=10)

text_array = tk.Text(frame_array, height=15, wrap=tk.NONE)
text_array.pack(fill="both", expand=True)

update_array_display()

root.mainloop()
