import TKinterModernThemes as TKMT
import tkinter as tk
from tkinter import filedialog, messagebox
import random
import time


class App(TKMT.ThemedTKinterFrame):
    def generate_array(self):
        try:
            size = int(self.size_var.get())
            if size <= 0:
                raise ValueError
            self.arr = [random.randint(0, 1000000) for _ in range(size)]
            self.repeat_sort = False
            self.update_array_display()
            self.time_spent = 0.0
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный размер массива!")

    def bubble_sort(self):
        if self.repeat_sort:
            messagebox.showinfo("Повтор", "Массив уже отсортирован")
            return

        if not self.arr:
            messagebox.showwarning("Ошибка", "Сначала создайте массив!")
            return

        start = time.time()
        for i in range(len(self.arr) - 1):
            swapped = False
            for j in range(len(self.arr) - i - 1):
                if self.arr[j] > self.arr[j + 1]:
                    self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]
                    swapped = True
            if not swapped:
                break
        end = time.time()

        self.time_spent = end - start
        self.repeat_sort = True
        self.update_array_display()
        messagebox.showinfo("Успех", f"Массив отсортирован за {self.time_spent:.20f} сек.")

    def save_array(self):
        if not self.arr:
            messagebox.showwarning("Ошибка", "Сначала создайте массив!")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not filename:
            return
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"{len(self.arr)}\n")
                f.write(" ".join(map(str, self.arr)))
            messagebox.showinfo("Успех", "Массив успешно записан!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

    def load_array(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not filename:
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                size = int(f.readline())
                self.arr = list(map(int, f.read().split()))
            self.repeat_sort = False
            self.update_array_display()
            messagebox.showinfo("Успех", "Массив успешно загружен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл:\n{e}")

    def update_array_display(self):
        self.text_array.delete("1.0", tk.END)
        if not self.arr:
            self.text_array.insert(tk.END, "[пусто]")
        else:
            self.text_array.insert(tk.END, "\n".join(f"{i + 1}) {val}" for i, val in enumerate(self.arr)))

    def show_time(self):
        if self.time_spent == 0.0:
            messagebox.showinfo("Время сортировки", "Сначала отсортируйте массив!")
        else:
            messagebox.showinfo("Время сортировки", f"{self.time_spent:.6f} сек.")

    def __init__(self):
        super().__init__("Сортировка пузырьком", theme="sun-valley", mode="dark")

        self.arr = []
        self.time_spent = 0.0
        self.repeat_sort = False
        self.size_var = tk.StringVar()

        self.input_frame = self.addFrame("Ввод массива")
        self.input_frame.Label("Размер массива:")
        self.input_frame.Entry(textvariable=self.size_var)
        self.input_frame.Button("Сгенерировать", self.generate_array)

        self.buttons_frame = self.addLabelFrame("Управление")
        self.buttons_frame.Button("Сортировать", self.bubble_sort, row=0, col=0)
        self.buttons_frame.Button("Сохранить в файл", self.save_array, row=0, col=1)
        self.buttons_frame.Button("Загрузить из файла", self.load_array, row=0, col=2)
        self.buttons_frame.Button("Время сортировки", self.show_time, row=0, col=3)

        self.root.resizable(False, False)

        self.array_frame = self.addLabelFrame("Массив")
        self.text_array = tk.Text(self.array_frame.master, height=15)
        self.text_array.pack(fill="both", expand=True, padx=5, pady=5)

        self.update_array_display()
        self.run()




if __name__ == "__main__":
    App()
