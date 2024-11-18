import tkinter as tk
from tkinter import ttk
from data_manager import DataManager
from progress_calc import ProgressCalculator
from subject_window import SubjectWindow
from add_dialog import AddDialog


class StudyTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Progress Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.data_manager = DataManager()
        self.progress_calculator = ProgressCalculator(self.data_manager)

        self.setup_ui()

    def setup_ui(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Style configuration
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", padding=10)

        self.create_subject_list()
        self.create_add_button()

    def create_subject_list(self):
        # Clear existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Subjects list with scrollbar
        self.canvas = tk.Canvas(self.main_frame, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Create subject buttons
        data = self.data_manager.load_data()
        for subject in data:
            self.create_subject_button(subject)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.create_add_button()

    def create_subject_button(self, subject):
        frame = ttk.Frame(self.scrollable_frame)
        frame.pack(fill="x", padx=5, pady=5)

        completion = self.progress_calculator.calculate_subject_completion(subject)

        button = ttk.Button(
            frame,
            text=f"{subject} ({completion}% Complete)",
            command=lambda s=subject: self.open_subject_window(s),
            style="Custom.TButton"
        )
        button.pack(side="left", fill="x", expand=True)

        delete_btn = ttk.Button(
            frame,
            text="×",
            command=lambda s=subject: self.delete_subject(s),
            width=3
        )
        delete_btn.pack(side="right")

    def create_add_button(self):
        add_button = ttk.Button(
            self.main_frame,
            text="+",
            command=self.add_subject,
            style="Custom.TButton"
        )
        add_button.pack(side="bottom", pady=20)

    def add_subject(self):
        AddDialog("Add Subject", "Enter subject name:", self.add_subject_callback)

    def add_subject_callback(self, subject_name):
        if not subject_name:
            return

        data = self.data_manager.load_data()
        if subject_name not in data:
            data[subject_name] = {"topics": {}}
            self.data_manager.save_data(data)
            self.create_subject_list()

    def delete_subject(self, subject):
        data = self.data_manager.load_data()
        del data[subject]
        self.data_manager.save_data(data)
        self.create_subject_list()

    def open_subject_window(self, subject):
        SubjectWindow(self.root, subject, self.data_manager, self.progress_calculator)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudyTrackerApp(root)
    root.mainloop()