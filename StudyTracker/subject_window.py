# subject_window.py
import tkinter as tk
from tkinter import ttk
from progress_circle import ProgressCircle
from topic_frame import TopicFrame
from add_dialog import AddDialog


class ModernScrollFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg='#ffffff', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind('<Configure>', self.on_canvas_configure)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.bind_mouse_scroll()

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def bind_mouse_scroll(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class ModernSidebar(ttk.Frame):
    def __init__(self, parent, current_subject, data_manager, callback):
        super().__init__(parent)
        self.data_manager = data_manager
        self.callback = callback
        self.current_subject = current_subject

        style = ttk.Style()
        style.configure("Sidebar.TFrame", background="#2c3e50")
        self.configure(style="Sidebar.TFrame")

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ttk.Label(
            self,
            text="Subjects",
            font=("Helvetica", 12, "bold"),
            foreground="#ecf0f1",
            background="#2c3e50"
        )
        header.pack(pady=20, padx=10)

        # Subjects list
        subjects = self.data_manager.load_data().keys()
        for subject in subjects:
            self.create_subject_button(subject)

    def create_subject_button(self, subject):
        is_current = subject == self.current_subject
        bg_color = "#34495e" if is_current else "#2c3e50"

        button_frame = tk.Frame(self, bg=bg_color)
        button_frame.pack(fill="x", pady=2)

        button = tk.Label(
            button_frame,
            text=subject,
            bg=bg_color,
            fg="#ecf0f1",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        button.pack(fill="x")

        # Hover effects
        def on_enter(e):
            if not is_current:
                button_frame.configure(bg="#34495e")
                button.configure(bg="#34495e")

        def on_leave(e):
            if not is_current:
                button_frame.configure(bg="#2c3e50")
                button.configure(bg="#2c3e50")

        def on_click(e):
            if not is_current:
                self.callback(subject)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<Button-1>", on_click)
        button_frame.bind("<Button-1>", on_click)


class SubjectWindow:
    def __init__(self, parent, subject, data_manager, progress_calculator):
        self.window = tk.Toplevel(parent)
        self.window.title(f"{subject} - Topics")
        self.window.geometry("1200x800")
        self.window.configure(bg="#ffffff")

        self.subject = subject
        self.data_manager = data_manager
        self.progress_calculator = progress_calculator

        # Configure styles
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()

        # Configure modern button style
        style.configure(
            "Modern.TButton",
            padding=10,
            background="#3498db",
            foreground="#ffffff",
            font=("Helvetica", 10)
        )

        # Configure frame style
        style.configure(
            "Modern.TFrame",
            background="#ffffff"
        )

        # Configure labelframe style
        style.configure(
            "Modern.TLabelframe",
            background="#ffffff",
            padding=10
        )
        style.configure(
            "Modern.TLabelframe.Label",
            font=("Helvetica", 11, "bold"),
            foreground="#2c3e50",
            background="#ffffff"
        )

    def setup_ui(self):
        # Main container with sidebar
        self.main_container = ttk.Frame(self.window, style="Modern.TFrame")
        self.main_container.pack(fill="both", expand=True)

        # Create and pack sidebar
        self.sidebar = ModernSidebar(
            self.main_container,
            self.subject,
            self.data_manager,
            self.switch_subject
        )
        self.sidebar.pack(side="left", fill="y")

        # Content area
        self.content_frame = ttk.Frame(self.main_container, style="Modern.TFrame")
        self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Progress circle area
        self.canvas = tk.Canvas(
            self.content_frame,
            width=200,
            height=200,
            bg="#ffffff",
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        self.progress_circle = ProgressCircle(self.canvas)
        self.update_progress()

        # Scrollable topics area
        self.scroll_frame = ModernScrollFrame(self.content_frame)
        self.scroll_frame.pack(fill="both", expand=True, pady=20)

        self.topics_frame = self.scroll_frame.scrollable_frame
        self.display_topics()

        # Add topic button at the bottom
        self.create_add_topic_button()

    def switch_subject(self, new_subject):
        self.window.destroy()
        SubjectWindow(
            self.window.master,
            new_subject,
            self.data_manager,
            self.progress_calculator
        )

    def update_progress(self):
        percentage = self.progress_calculator.calculate_subject_completion(self.subject)
        self.progress_circle.draw(percentage)

    def display_topics(self):
        data = self.data_manager.load_data()
        for topic_name, topic_data in data[self.subject]["topics"].items():
            TopicFrame(
                self.topics_frame,
                self.subject,
                topic_name,
                topic_data,
                self.data_manager,
                self.progress_calculator,
                self.update_progress
            )

    def create_add_topic_button(self):
        add_topic_btn = ttk.Button(
            self.content_frame,
            text="+ Add Topic",
            command=self.add_topic,
            style="Modern.TButton"
        )
        add_topic_btn.pack(pady=20)

    def add_topic(self):
        AddDialog("Add Topic", "Enter topic name:", self.add_topic_callback)

    def add_topic_callback(self, topic_name):
        if not topic_name:
            return

        data = self.data_manager.load_data()
        if topic_name not in data[self.subject]["topics"]:
            data[self.subject]["topics"][topic_name] = {"subtopics": {}}
            self.data_manager.save_data(data)
            TopicFrame(
                self.topics_frame,
                self.subject,
                topic_name,
                data[self.subject]["topics"][topic_name],
                self.data_manager,
                self.progress_calculator,
                self.update_progress
            )