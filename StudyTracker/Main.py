import tkinter as tk
from tkinter import ttk
from datetime import datetime
from data_manager import DataManager
from progress_calc import ProgressCalculator
from subject_window import SubjectWindow
from add_dialog import AddDialog


class StudyTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tracker Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Center the window
        self.center_window()

        self.data_manager = DataManager()
        self.progress_calculator = ProgressCalculator(self.data_manager)

        self.setup_ui()

    def setup_ui(self):
        # Main container with sidebar
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar = ttk.Frame(self.main_container, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.setup_sidebar()

        # Content area
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Clock in the center
        self.clock_label = ttk.Label(self.content_frame, font=("Helvetica", 48), anchor="center")
        self.clock_label.pack(pady=20)
        self.update_clock()

        # Study tracker content
        self.study_tracker_frame = ttk.Frame(self.content_frame)
        self.study_tracker_frame.pack(fill="both", expand=True)
        self.setup_study_tracker()

    def setup_sidebar(self):
        # Sidebar header
        ttk.Label(
            self.sidebar,
            text="Trackers",
            font=("Helvetica", 14, "bold"),
            anchor="center"
        ).pack(pady=20)

        # Buttons for trackers
        study_tracker_btn = ttk.Button(
            self.sidebar,
            text="Study Tracker",
            command=self.show_study_tracker
        )
        study_tracker_btn.pack(fill="x", padx=10, pady=5)

        # Add more tracker buttons as needed
        other_tracker_btn = ttk.Button(
            self.sidebar,
            text="Other Tracker",
            command=lambda: print("Other Tracker (Placeholder)")  # Replace with actual functionality
        )
        other_tracker_btn.pack(fill="x", padx=10, pady=5)

    def update_clock(self):
        if self.clock_label.winfo_exists():
            now = datetime.now().strftime("%H:%M:%S")
            self.clock_label.config(text=now)
            self.root.after(1000, self.update_clock)

    def setup_study_tracker(self):
        # Main study tracker content
        self.create_subject_list()
        self.create_add_button()

    def show_study_tracker(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Recreate clock label
        self.clock_label = ttk.Label(self.content_frame, font=("Helvetica", 48), anchor="center")
        self.clock_label.pack(pady=20)
        self.update_clock()

        # Rebuild the study tracker UI
        self.study_tracker_frame = ttk.Frame(self.content_frame)
        self.study_tracker_frame.pack(fill="both", expand=True)
        self.setup_study_tracker()

    def create_subject_list(self):
        # Clear existing widgets
        for widget in self.study_tracker_frame.winfo_children():
            widget.destroy()

        # Subjects list with scrollbar
        self.canvas = tk.Canvas(self.study_tracker_frame, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(self.study_tracker_frame, orient="vertical", command=self.canvas.yview)
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

    def create_subject_button(self, subject):
        frame = ttk.Frame(self.scrollable_frame)
        frame.pack(fill="x", padx=5, pady=5)

        completion = self.progress_calculator.calculate_subject_completion(subject)

        button = ttk.Button(
            frame,
            text=f"{subject} ({completion}% Complete)",
            command=lambda s=subject: self.open_subject_window(s)
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
            self.study_tracker_frame,
            text="+ Add Subject",
            command=self.add_subject
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
        # Clear main menu
        for widget in self.root.winfo_children():
            widget.destroy()

        # Open subject window
        SubjectWindow(self.root, subject, self.data_manager, self.progress_calculator, self.return_to_main_menu)

    def return_to_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = StudyTrackerApp(root)
    root.mainloop()
