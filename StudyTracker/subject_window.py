import tkinter as tk
from tkinter import ttk
from progress_circle import ProgressCircle
from topic_frame import TopicFrame
from add_dialog import AddDialog
from font_manager import FontManager


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
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def _on_mousewheel(self, event):
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class ModernSidebar(ttk.Frame):
    def __init__(self, parent, current_subject, data_manager, subject_callback, return_callback):
        super().__init__(parent)

        # Get font manager instance
        self.font_manager = FontManager()
        self.data_manager = data_manager
        self.subject_callback = subject_callback
        self.return_callback = return_callback
        self.current_subject = current_subject

        # Configure sidebar style
        style = ttk.Style()
        style.configure("Sidebar.TFrame", background="#493428")
        self.configure(style="Sidebar.TFrame")

        # Create a canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(self, bg="#493428", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="Sidebar.TFrame")

        # Configure canvas scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bind mouse wheel scrolling only when hovering over the sidebar
        self.bind_mouse_scroll()

        # Setup the UI
        self.setup_ui()

        # Configure canvas size
        self.canvas.bind("<Configure>", self._configure_canvas)

    def bind_mouse_scroll(self):
        # Bind mousewheel events when mouse enters the widget
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)
        self.scrollbar.bind("<Enter>", self._bind_mousewheel)
        self.scrollbar.bind("<Leave>", self._unbind_mousewheel)

    def _bind_mousewheel(self, event):
        # Bind the mousewheel event to the canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        # Unbind the mousewheel event when mouse leaves
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        # Scroll the canvas when mousewheel is used
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _configure_canvas(self, event):
        self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=event.width)

    def setup_ui(self):
        header = ttk.Label(
            self.scrollable_frame,
            text="Subjects",
            font=(self.font_manager.get_font(), 12, "bold"),
            foreground="#D2DCE5",
            background="#493428"
        )
        header.pack(pady=20, padx=10)

        # Subject buttons frame
        self.subject_buttons_frame = ttk.Frame(self.scrollable_frame, style="Sidebar.TFrame")
        self.subject_buttons_frame.pack(fill="both", expand=True)

        # Populate subject buttons
        subjects = self.data_manager.load_data().keys()
        for subject in subjects:
            self.create_subject_button(subject)

        # Return button container (outside scrollable area)
        self.return_button_frame = ttk.Frame(self, style="Sidebar.TFrame")
        self.return_button = ttk.Button(
            self.return_button_frame,
            text="Return to Main Menu",
            command=self.return_callback,
            style="Sidebar.TButton"
        )
        self.return_button.pack(fill="x", padx=10, pady=10)

        # Pack everything in the correct order
        self.canvas.pack(side="top", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.return_button_frame.pack(side="bottom", fill="x", before=self.canvas)

    def create_subject_button(self, subject):
        is_current = subject == self.current_subject
        bg_color = "#BE8464" if is_current else "#493428"

        button_frame = tk.Frame(self.subject_buttons_frame, bg=bg_color)
        button_frame.pack(fill="x", pady=2)

        button = tk.Label(
            button_frame,
            text=subject,
            bg=bg_color,
            fg="#D2DCE5",
            font=(self.font_manager.get_font(), 11),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        button.pack(fill="x")

        # Bind mousewheel events to the button and frame
        button.bind("<Enter>", self._bind_mousewheel)
        button.bind("<Leave>", self._unbind_mousewheel)
        button_frame.bind("<Enter>", self._bind_mousewheel)
        button_frame.bind("<Leave>", self._unbind_mousewheel)

        # In hover effects
        def on_enter(e):
            if not is_current:
                button_frame.configure(bg="#7D685F")
                button.configure(bg="#7D685F")

        def on_leave(e):
            if not is_current:
                button_frame.configure(bg="#493428")
                button.configure(bg="#493428")

        def on_click(e):
            if not is_current:
                self.subject_callback(subject)

        button.bind("<Enter>", lambda e: [on_enter(e), self._bind_mousewheel(e)])
        button.bind("<Leave>", lambda e: [on_leave(e), self._unbind_mousewheel(e)])
        button.bind("<Button-1>", on_click)
        button_frame.bind("<Button-1>", on_click)

    def update_subjects(self, current_subject):
        self.current_subject = current_subject

        # Clear existing subject buttons
        for widget in self.subject_buttons_frame.winfo_children():
            widget.destroy()

        # Recreate subject buttons
        subjects = self.data_manager.load_data().keys()
        for subject in subjects:
            self.create_subject_button(subject)

class SubjectWindow:
    def __init__(self, parent, subject, data_manager, progress_calculator, return_callback):
        # Get font manager instance
        self.font_manager = FontManager()
        self.window = parent
        self.subject = subject
        self.data_manager = data_manager
        self.progress_calculator = progress_calculator
        self.return_callback = return_callback

        # Create main container
        self.main_container = ttk.Frame(self.window, style="Modern.TFrame")
        self.main_container.pack(fill="both", expand=True)

        # Configure styles
        self.setup_styles()

        # Setup sidebar
        self.sidebar = ModernSidebar(
            self.main_container,
            self.subject,
            self.data_manager,
            self.switch_subject,
            self.return_callback
        )
        self.sidebar.pack(side="left", fill="y")

        # Content area
        self.content_frame = ttk.Frame(self.main_container, style="Modern.TFrame")
        self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Build the content area
        self.setup_ui()

        # Configure styles with custom font
        self.font_manager.configure_styles()

    def setup_styles(self):
        style = ttk.Style()
        # Sidebar button style
        style.configure(
            "Sidebar.TButton",
            padding=10,
            font=("Helvetica", 11, "bold"),
            background="#493428",
            foreground="#D2DCE5"
        )

        # Modern frame style
        style.configure("Modern.TFrame", background="#D2DCE5")
        style.configure("Modern.TButton",
                        padding=10,
                        font=("Helvetica", 11),
                        background="#BE8464",
                        foreground="#483C32")
        style.configure("AddTopic.TButton",
                        padding=10,
                        font=("Helvetica", 12, "bold"),
                        background="#BE8464")
    def setup_ui(self):
        # Progress circle
        self.canvas = tk.Canvas(self.content_frame, width=200, height=200, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.progress_circle = ProgressCircle(self.canvas)
        self.update_progress()

        # Scrollable topics area
        self.scroll_frame = ModernScrollFrame(self.content_frame)
        self.scroll_frame.pack(fill="both", expand=True, pady=20)

        self.topics_frame = self.scroll_frame.scrollable_frame
        self.display_topics()

        # Add topic button
        self.create_add_topic_button()

    def setup_content_ui(self):
        # Progress circle
        self.canvas = tk.Canvas(self.content_frame, width=200, height=200, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.progress_circle = ProgressCircle(self.canvas)
        self.update_progress()

        # Scrollable topics area
        self.scroll_frame = ModernScrollFrame(self.content_frame)
        self.scroll_frame.pack(fill="both", expand=True, pady=20)

        self.topics_frame = self.scroll_frame.scrollable_frame
        self.display_topics()

        # Add topic button
        self.create_add_topic_button()

    def switch_subject(self, new_subject):
        self.subject = new_subject

        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Update sidebar buttons
        self.sidebar.update_subjects(new_subject)

        # Rebuild the content area
        self.setup_content_ui()

    def update_progress(self):
        percentage = max(0, min(100, self.progress_calculator.calculate_subject_completion(self.subject)))
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
            style="AddTopic.TButton"
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

            # Clear and rebuild topics display
            for widget in self.topics_frame.winfo_children():
                widget.destroy()
            self.display_topics()