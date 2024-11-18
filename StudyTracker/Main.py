import tkinter as tk
from tkinter import messagebox
class StudyTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Tracker")
        self.subjects = [] #List of subjects

        self.create_main_ui()

    def create_main_ui(self):
        """Create main window UI."""
        tk.Label(self.root, text = "Study Tracker", font = ("Arial", 20)).pack(pady = 10)

        self.subject_list_frame = tk.Frame(self.root)
        self.subject_list_frame.pack(pady=10)

        add_subject_btn = tk.Button(self.root, text="+ Add Subject", font=("Arial", 14),
                                    command=self.add_subject)
        add_subject_btn.pack(pady=10)