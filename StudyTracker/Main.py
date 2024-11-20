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
            foreground="#ecf0f1",
            background="#2c3e50"
        ).pack(pady=20)

        # Configure sidebar style
        style = ttk.Style()
        style.configure(
            "Sidebar.TFrame",
            background="#2c3e50"
        )
        style.configure(
            "Sidebar.TButton",
            padding=10,
            font=("Helvetica", 11, "bold"),
            background="#2c3e50",
            foreground="#000000"
        )
        style.configure(
            "Sidebar.TLabel",
            background="#2c3e50",
            foreground="#ecf0f1",
            font=("Helvetica", 14, "bold")
        )

        # Apply the sidebar frame style
        self.sidebar.configure(style="Sidebar.TFrame")

        # Buttons for trackers
        study_tracker_btn = ttk.Button(
            self.sidebar,
            text="Study Tracker",
            command=self.show_study_tracker,
            style="Sidebar.TButton"
        )
        study_tracker_btn.pack(fill="x", padx=10, pady=5)

        # Other tracker button
        other_tracker_btn = ttk.Button(
            self.sidebar,
            text="Other Tracker",
            command=lambda: print("Other Tracker (Placeholder)"),
            style="Sidebar.TButton"
        )
        other_tracker_btn.pack(fill="x", padx=10, pady=5)

        # Optional: Configure sidebar background
        self.sidebar.configure(style="Sidebar.TFrame")

    def update_clock(self):
        if self.clock_label.winfo_exists():
            now = datetime.now().strftime("%H:%M:%S")
            self.clock_label.config(text=now)
            self.root.after(1000, self.update_clock)

    def setup_study_tracker(self):
        # Create a frame for the list
        self.list_frame = ttk.Frame(self.study_tracker_frame)
        self.list_frame.pack(fill="both", expand=True)

        # Create subject list in the list frame
        self.create_subject_list()

        # Create add button frame
        self.button_frame = ttk.Frame(self.study_tracker_frame)
        self.button_frame.pack(side="bottom", fill="x")

        # Create add button in the button frame
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
        # Clear existing widgets in list frame only
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        # Create outer frame to manage boundaries
        self.outer_frame = ttk.Frame(self.list_frame)
        self.outer_frame.pack(fill="both", expand=True)

        # Subjects list with scrollbar
        self.canvas = tk.Canvas(self.outer_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.outer_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configure scrolling behavior
        def _on_frame_configure(event):
            # Update the scrollregion to match the frame's actual size
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            # Get the visible height of the canvas
            visible_height = self.canvas.winfo_height()
            # Get the total height of the content
            total_height = self.scrollable_frame.winfo_reqheight()

            if total_height > visible_height:
                # Only show scrollbar when content exceeds visible area
                scrollbar.pack(side="right", fill="y")
                self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
            else:
                # Hide scrollbar when all content is visible
                scrollbar.pack_forget()
                self.canvas.unbind_all("<MouseWheel>")

        def _on_mousewheel(event):
            # Get current scroll position
            current_pos = self.canvas.yview()

            # Calculate scroll direction
            if event.delta > 0:  # Scrolling up
                if current_pos[0] <= 0:  # At the top
                    return
            else:  # Scrolling down
                if current_pos[1] >= 1:  # At the bottom
                    return

            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_canvas_configure(event):
            # Update the width of the scrollable frame when canvas is resized
            self.canvas.itemconfig(canvas_window, width=event.width)

        # Bind configuration events
        self.scrollable_frame.bind("<Configure>", _on_frame_configure)
        self.canvas.bind("<Configure>", _on_canvas_configure)

        # Create the window for the scrollable frame
        canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            tags="self.scrollable_frame"
        )

        # Configure canvas and scrollbar
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create subject buttons
        data = self.data_manager.load_data()
        for subject in data:
            self.create_subject_button(subject)

    def create_subject_button(self, subject):
        frame = ttk.Frame(self.scrollable_frame)
        frame.pack(fill="x", padx=5, pady=5)

        completion = self.progress_calculator.calculate_subject_completion(subject)

        # Create a frame for the button and delete button
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", expand=True)

        button = ttk.Button(
            button_frame,
            text=f"{subject} ({completion}% Complete)",
            command=lambda s=subject: self.open_subject_window(s),
            style="Subject.TButton"  # Added style for consistency
        )
        button.pack(side="left", fill="x", expand=True)

        delete_btn = ttk.Button(
            button_frame,
            text="×",
            command=lambda s=subject: self.delete_subject(s),
            width=3,
            style="Delete.TButton"  # Added style for consistency
        )
        delete_btn.pack(side="right", padx=(5, 0))

    def create_add_button(self):
        add_button = ttk.Button(
            self.button_frame,
            text="+ Add Subject",
            command=self.add_subject
        )
        add_button.pack(pady=20)

    def add_subject(self):
        AddDialog("Add Subject", "Enter subject name:", self.add_subject_callback)

    def add_subject_callback(self, subject_name):
        if not subject_name:
            return

        data = self.data_manager.load_data()
        if subject_name not in data:
            data[subject_name] = {"topics": {}}
            self.data_manager.save_data(data)
            self.create_subject_list()  # This now only updates the list, not the button

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