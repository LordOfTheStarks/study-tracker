import tkinter as tk
from tkinter import ttk


class AddDialog:
    def __init__(self, title, prompt, callback):
        self.dialog = tk.Toplevel()
        self.dialog.title(title)
        self.dialog.geometry("300x150")

        ttk.Label(self.dialog, text=prompt).pack(pady=20)

        self.entry = ttk.Entry(self.dialog)
        self.entry.pack(pady=10)

        ttk.Button(self.dialog, text="Save", command=lambda: self.save(callback)).pack(pady=10)

    def save(self, callback):
        value = self.entry.get().strip()
        callback(value)
        self.dialog.destroy()