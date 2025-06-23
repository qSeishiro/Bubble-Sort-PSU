import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import random
import time
import base64
import json
import urllib.request
import urllib.error
import re
import io

arr = []
time_spent = 0.0
repeat_sort = False


def download_from_github():
    # Запрашиваем URL у пользователя
    url = simpledialog.askstring("GitHub", "Введите raw-URL файла с GitHub:")
    if not url:
        return

    try:
        # Преобразуем обычную ссылку GitHub в raw-ссылку
        if "github.com" in url and "/blob/" in url:
            url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        
        # Убедимся, что это raw-ссылка
        if not url.startswith("https://raw.githubusercontent.com/"):
            messagebox.showwarning("Предупреждение", 
                                 "Используйте raw-ссылку GitHub\n"
                                 "Пример: https://raw.githubusercontent.com/user/repo/main/file.txt")
            return

        # Создаем запрос
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "PythonApp"}
        )
        
        # Отправляем запрос
        with urllib.request.urlopen(req) as response:
            content = response.read().decode("utf-8")
            
            # Обрабатываем содержимое файла
            lines = content.splitlines()
            if len(lines) < 2:
                raise ValueError("Некорректный формат файла")
            
            size = int(lines[0])
            arr_loaded = list(map(int, lines[1].split()))
            
            if size != len(arr_loaded):
                messagebox.showwarning("Предупреждение", 
                                      f"Размер в файле ({size}) не соответствует количеству элементов ({len(arr_loaded)})")
            
            global arr, repeat_sort
            arr = arr_loaded
            repeat_sort = False
            update_array_display()
            messagebox.showinfo("Успех", "Массив успешно загружен с GitHub!")
    
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        messagebox.showerror("Ошибка", f"HTTP ошибка {e.code}: {error_msg}")
    except ValueError as e:
        # Покажем первые 100 символов содержимого для отладки
        debug_content = content[:100] + ("..." if len(content) > 100 else "")
        messagebox.showerror("Ошибка", 
                           f"Ошибка формата файла:\n{str(e)}\n\n"
                           f"Первые 100 символов содержимого:\n{debug_content}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл с GitHub:\n{str(e)}")

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
        min_val = int(entry_min.get())
        max_val = int(entry_max.get())
        
        if size <= 0:
            raise ValueError("Размер должен быть положительным числом")
        if min_val > max_val:
            min_val, max_val = max_val, min_val  # Автокоррекция диапазона
        
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        update_array_display()
        repeat_sort = False
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Некорректные значения:\n{str(e)}")

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
    global arr, repeat_sort
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not filename:
        return
    try:
        with open(filename, "r", encoding="utf-8") as f:
            size = int(f.readline())
            arr = list(map(int, f.read().split()))
        update_array_display()
        repeat_sort = False
        messagebox.showinfo("Успех", "Массив успешно загружен!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось прочитать файл:\n{e}")

def load_array_from_url():
    global arr, repeat_sort
    url = simpledialog.askstring("Загрузка по URL", "Введите URL файла:")
    if not url:
        return
    
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8').strip()
        
        lines = content.split('\n')
        
        # Более гибкая обработка формата файла
        if len(lines) > 1:
            # Формат: первая строка - размер, вторая - числа
            try:
                size = int(lines[0])
                arr = list(map(int, lines[1].split()))
            except:
                # Попробуем прочитать все числа из всего файла
                arr = []
                for line in lines:
                    arr.extend(map(int, line.split()))
        else:
            # Весь файл - одна строка с числами
            arr = list(map(int, lines[0].split()))
        
        update_array_display()
        repeat_sort = False
        messagebox.showinfo("Успех", f"Успешно загружено {len(arr)} элементов по URL!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при загрузке файла:\n{str(e)}")

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

# Создаем фрейм для элементов управления
control_frame = tk.Frame(frame_top)
control_frame.pack(fill=tk.X, pady=5)

# Размер массива
tk.Label(control_frame, text="Размер массива:").grid(row=0, column=0, padx=5, sticky="e")
entry_size = tk.Entry(control_frame, width=7)
entry_size.grid(row=0, column=1, padx=5)
entry_size.insert(0, "10")  # Значение по умолчанию

# Диапазон значений
tk.Label(control_frame, text="Диапазон от:").grid(row=0, column=2, padx=5, sticky="e")
entry_min = tk.Entry(control_frame, width=7)
entry_min.grid(row=0, column=3, padx=5)
entry_min.insert(0, "0")  # Значение по умолчанию

tk.Label(control_frame, text="до:").grid(row=0, column=4, padx=5, sticky="w")
entry_max = tk.Entry(control_frame, width=7)
entry_max.grid(row=0, column=5, padx=5)
entry_max.insert(0, "100")  # Значение по умолчанию

# Кнопка генерации
tk.Button(control_frame, text="Сгенерировать", command=generate_array).grid(row=0, column=6, padx=10)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

# Создаем сетку кнопок
tk.Button(frame_buttons, text="Сортировать", width=15, command=bubble_sort).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Сохранить в файл", width=15, command=save_array).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_buttons, text="Загрузить из файла", width=15, command=load_array).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_buttons, text="Загрузить по URL", width=15, command=load_array_from_url).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame_buttons, text="Загрузить с GitHub", width=15, command=download_from_github).grid(row=0, column=2, padx=5, pady=5)
tk.Button(frame_buttons, text="Время сортировки", width=15, command=show_time).grid(row=1, column=2, padx=5, pady=5)

frame_array = tk.LabelFrame(root, text="Массив", padx=10, pady=10)
frame_array.pack(fill="both", expand=True, padx=10, pady=10)

# Добавляем скроллбар для массива
scrollbar = tk.Scrollbar(frame_array)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_array = tk.Text(frame_array, height=15, wrap=tk.NONE, yscrollcommand=scrollbar.set)
text_array.pack(fill="both", expand=True)

scrollbar.config(command=text_array.yview)

update_array_display()

root.mainloop()
