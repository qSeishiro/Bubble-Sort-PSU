import TKinterModernThemes as TKMT
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import random
import time
import urllib.request
import urllib.error
import base64
import json


class App(TKMT.ThemedTKinterFrame):
    def generate_array(self):
        try:
            size = int(self.size_var.get())
            min_val = int(self.min_var.get())
            max_val = int(self.max_var.get())
            if size <= 0:
                raise ValueError("Размер должен быть положительным")
            if min_val > max_val:
                min_val, max_val = max_val, min_val
            self.arr = [random.randint(min_val, max_val) for _ in range(size)]
            self.repeat_sort = False
            self.update_array_display()
            self.time_spent = 0.0
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения!")



    def load_array_from_url(self):
        url = simpledialog.askstring("Загрузка по URL", "Введите URL файла:")
        if not url:
            return
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read().decode('utf-8').strip()
            lines = content.split('\n')
            if len(lines) > 1:
                try:
                    size = int(lines[0])
                    self.arr = list(map(int, lines[1].split()))
                except:
                    self.arr = []
                    for line in lines:
                        self.arr.extend(map(int, line.split()))
            else:
                self.arr = list(map(int, lines[0].split()))
            self.update_array_display()
            self.repeat_sort = False
            messagebox.showinfo("Успех", f"Успешно загружено {len(self.arr)} элементов по URL!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке файла:\n{str(e)}")



    def upload_to_github(self):
        if not self.arr:
            messagebox.showwarning("Ошибка", "Сначала создайте массив!")
            return
        token = simpledialog.askstring("GitHub Token", "Введите ваш GitHub Personal Access Token:", show='*')
        if not token:
            return
        try:
            check_req = urllib.request.Request(
                "https://api.github.com/user",
                headers={"Authorization": f"token {token}", "User-Agent": "PythonApp"}
            )
            with urllib.request.urlopen(check_req) as response:
                user_data = json.loads(response.read().decode())
                scopes = response.headers.get('X-OAuth-Scopes', '')
                if 'repo' not in scopes:
                    messagebox.showerror("Ошибка прав", "Токен не имеет права 'repo'!")
                    return
        except urllib.error.HTTPError as e:
            error_msg = e.read().decode()
            messagebox.showerror("Ошибка токена", f"Ошибка проверки токена ({e.code}):\n{error_msg}")
            return
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось проверить токен: {str(e)}")
            return

        repo_owner = simpledialog.askstring("Репозиторий", "Владелец репозитория:")
        if not repo_owner:
            return
        repo_name = simpledialog.askstring("Репозиторий", "Имя репозитория:")
        if not repo_name:
            return
        try:
            repo_req = urllib.request.Request(
                f"https://api.github.com/repos/{repo_owner}/{repo_name}",
                headers={"Authorization": f"token {token}", "User-Agent": "PythonApp"}
            )
            with urllib.request.urlopen(repo_req) as response:
                repo_data = json.loads(response.read().decode())
                permissions = repo_data.get('permissions', {})
                if not permissions.get('push', False):
                    messagebox.showerror("Ошибка доступа", "Нет прав на запись в этот репозиторий!")
                    return
        except urllib.error.HTTPError as e:
            if e.code == 404:
                messagebox.showerror("Ошибка", "Репозиторий не найден!")
            else:
                messagebox.showerror("Ошибка", f"HTTP ошибка {e.code}")
            return

        file_path = simpledialog.askstring("Файл", "Путь к файлу в репозитории:", initialvalue="array.txt")
        if not file_path:
            return
        commit_message = simpledialog.askstring("Коммит", "Сообщение коммита:", initialvalue="Обновление массива")
        if not commit_message:
            return

        try:
            content = f"{len(self.arr)}\n" + " ".join(map(str, self.arr))
            content_bytes = content.encode("utf-8")
            content_base64 = base64.b64encode(content_bytes).decode("utf-8")
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
            data = {
                "message": commit_message,
                "content": content_base64,
                "branch": "main"
            }
            sha = None
            try:
                req = urllib.request.Request(
                    url,
                    headers={"Authorization": f"token {token}", "User-Agent": "PythonApp"}
                )
                with urllib.request.urlopen(req) as response:
                    existing_data = json.loads(response.read().decode())
                    sha = existing_data.get("sha")
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    error_msg = e.read().decode()
                    messagebox.showerror("Ошибка", f"Ошибка проверки файла ({e.code}):\n{error_msg}")
                    return
            if sha:
                data["sha"] = sha
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={"Authorization": f"token {token}", "User-Agent": "PythonApp", "Content-Type": "application/json"},
                method="PUT"
            )
            with urllib.request.urlopen(req) as response:
                if response.status in (200, 201):
                    messagebox.showinfo("Успех", "Файл успешно загружен на GitHub!")
                else:
                    messagebox.showerror("Ошибка", "Ошибка при загрузке файла")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл на GitHub:\n{str(e)}")



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
        self.time_spent = (end - start)*1000
        self.repeat_sort = True
        self.update_array_display()
        messagebox.showinfo("Успех", f"Массив отсортирован за {self.time_spent:.3f} мс.")



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
            messagebox.showinfo("Время сортировки", f"{self.time_spent:.3f} мс.")




    def __init__(self):
        super().__init__("Сортировка пузырьком", theme="sun-valley", mode="dark")
        self.arr = []
        self.time_spent = 0.0
        self.repeat_sort = False

        self.size_var = tk.StringVar()
        self.min_var = tk.StringVar(value="0")
        self.max_var = tk.StringVar(value="1000000")

        self.input_frame = self.addFrame("Ввод массива")
        self.input_frame.Label("Размер массива:", row=0, col=0)
        self.input_frame.Entry(textvariable=self.size_var, row=1, col=0)
        self.input_frame.Label("Минимум:", row=0, col=1)
        self.input_frame.Entry(textvariable=self.min_var, row=1, col=1)
        self.input_frame.Label("Максимум:", row=0, col=2)
        self.input_frame.Entry(textvariable=self.max_var, row=1, col=2)
        self.input_frame.Button("Сгенерировать", self.generate_array, row=2, col=0, colspan=3)
        self.input_frame.gridkwargs = {"padx": 10, "pady": 10, "sticky": "ew"}
        self.input_frame.master.grid_columnconfigure(0, weight=1)
    

        self.buttons_frame = self.addLabelFrame("Управление")
        self.buttons_frame.Button("Сортировать", self.bubble_sort, row=0, col=0)
        self.buttons_frame.Button("Сохранить", self.save_array, row=0, col=1)
        self.buttons_frame.Button("Загрузить", self.load_array, row=0, col=2)
        self.buttons_frame.Button("Из URL", self.load_array_from_url, row=0, col=3)
        self.buttons_frame.Button("На GitHub", self.upload_to_github, row=0, col=4)
        self.buttons_frame.Button("Время", self.show_time, row=0, col=5)

        self.root.resizable(False, False)

        self.array_frame = self.addLabelFrame("Массив")
        scrollbar = tk.Scrollbar(self.array_frame.master, bg="#1e1e1e", troughcolor="#2c2c2c", activebackground="#3a3a3a", highlightbackground="#1e1e1e")
        scrollbar.pack(side="right", fill="y")

        self.text_array = tk.Text(self.array_frame.master, height=15, yscrollcommand=scrollbar.set)
        self.text_array.pack(fill="both", expand=True, padx=5, pady=5)

        scrollbar.config(command=self.text_array.yview)

        self.update_array_display()
        self.run()





if __name__ == "__main__":
    App()
