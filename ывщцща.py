import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.file_name = "trainings.json"
        self.data = self.load_data()

        # Интерфейс ввода
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(fill="x")

        tk.Label(frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.date_entry = tk.Entry(frame)
        self.date_entry.grid(row=0, column=1)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))

        tk.Label(frame, text="Тип:").grid(row=0, column=2)
        self.type_entry = tk.Entry(frame)
        self.type_entry.grid(row=0, column=3)

        tk.Label(frame, text="Мин:").grid(row=0, column=4)
        self.dur_entry = tk.Entry(frame, width=10)
        self.dur_entry.grid(row=0, column=5)

        tk.Button(frame, text="Добавить", command=self.add_training).grid(row=0, column=6, padx=5)

        # Фильтры
        filter_frame = tk.Frame(root, padx=10)
        filter_frame.pack(fill="x")

        tk.Label(filter_frame, text="Фильтр тип:").pack(side="left")
        self.filter_type = tk.Entry(filter_frame, width=15)
        self.filter_type.pack(side="left", padx=5)
        self.filter_type.bind("<KeyRelease>", lambda e: self.update_table())

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Date", "Type", "Duration"), show="headings")
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Type", text="Тип тренировки")
        self.tree.heading("Duration", text="Длительность (мин)")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.update_table()

    def validate(self, date_str, duration_str):
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            if int(duration_str) <= 0: raise ValueError
            return True
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте формат даты (ДД.ММ.ГГГГ) и длительность (>0)")
            return False

    def add_training(self):
        d, t, dur = self.date_entry.get(), self.type_entry.get(), self.dur_entry.get()
        if self.validate(d, dur):
            self.data.append({"date": d, "type": t, "duration": dur})
            self.save_data()
            self.update_table()
            self.type_entry.delete(0, tk.END)
            self.dur_entry.delete(0, tk.END)

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        search = self.filter_type.get().lower()
        for item in self.data:
            if search in item["type"].lower():
                self.tree.insert("", "end", values=(item["date"], item["type"], item["duration"]))

    def save_data(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as f:
                return json.load(f)
        return []


if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
