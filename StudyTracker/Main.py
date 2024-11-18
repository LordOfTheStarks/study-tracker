# File: main.py

import tkinter as tk
from tkinter import messagebox
from ui_components import SubjectWindow

class StudyTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Tracker")
        self.subjects = []  # List of subjects

        self.create_main_ui()

    def create_main_ui(self):
        """Create main window UI."""
        tk.Label(self.root, text="Study Tracker", font=("Arial", 20)).pack(pady=10)

        self.subject_list_frame = tk.Frame(self.root)
        self.subject_list_frame.pack(pady=10)

        add_subject_btn = tk.Button(self.root, text="+ Add Subject", font=("Arial", 14),
                                    command=self.add_subject)
        add_subject_btn.pack(pady=10)

    def add_subject(self):
        """Add a new subject."""
        new_subject_name = tk.simpledialog.askstring("New Subject", "Enter Subject Name:")
        if new_subject_name:
            self.subjects.append(new_subject_name)
            self.refresh_subject_list()

    def open_subject_window(self, subject_name):
        """Open subject-specific window."""
        SubjectWindow(self.root, subject_name)

    def refresh_subject_list(self):
        """Refresh the subject list."""
        for widget in self.subject_list_frame.winfo_children():
            widget.destroy()  # Clear old widgets

        for subject in self.subjects:
            subject_button = tk.Button(self.subject_list_frame, text=subject, font=("Arial", 14),
                                        command=lambda s=subject: self.open_subject_window(s))
            subject_button.pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudyTrackerApp(root)
    root.mainloop()
