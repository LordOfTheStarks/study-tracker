import tkinter as tk
from tkinter import ttk
from add_dialog import AddDialog
from font_manager import FontManager


class TopicFrame:
    def __init__(self, parent, subject, topic_name, topic_data, data_manager,
                 progress_calculator, update_callback):

        self.font_manager = FontManager()
        # Get font manager instance
        self.style = ttk.Style()
        self.setup_styles()  # Add this line

        # Configure styles with custom font
        self.style.configure(
            "Topic.TLabelframe",
            background="#ffffff",
            padding=15
        )
        self.style.configure(
            "Topic.TLabelframe.Label",
            font=(self.font_manager.get_font(), 12, "bold"),
            foreground="#2c3e50",
            background="#ffffff"
        )

        self.frame = ttk.LabelFrame(
            parent,
            text=topic_name,
            style="Topic.TLabelframe"
        )
        self.frame.pack(fill="x", padx=5, pady=5)

        self.subject = subject
        self.topic_name = topic_name
        self.data_manager = data_manager
        self.progress_calculator = progress_calculator
        self.update_callback = update_callback

        self.setup_styles()
        self.display_subtopics(topic_data)
        self.create_add_subtopic_button()

    def setup_styles(self):
        self.style.configure(
            "Topic.TLabelframe",
            background="#D2DCE5",
            padding=15
        )
        self.style.configure(
            "Topic.TLabelframe.Label",
            font=(self.font_manager.get_font(), 12, "bold"),
            foreground="#483C32",
            background="#D2DCE5"
        )

        # Configure styles for all buttons
        self.style.configure(
            "AddSubtopic.TButton",
            padding=(15, 8),
            font=(self.font_manager.get_font(), 10),
            background="#BE8464",
            foreground="#483C32"
        )

        self.style.configure(
            "Delete.TButton",
            padding=5,
            font=(self.font_manager.get_font(), 8),
            background="#D2DCE5",
            foreground="#7D685F"
        )

        self.style.configure(
            "Subtopic.TCheckbutton",
            background="#D2DCE5",
            font=(self.font_manager.get_font(), 10)
        )
    def display_subtopics(self, topic_data):
        self.subtopics_frame = ttk.Frame(self.frame)
        self.subtopics_frame.pack(fill="x", expand=True)

        for subtopic_name, subtopic_data in topic_data["subtopics"].items():
            self.create_subtopic_frame(subtopic_name, subtopic_data)

    def create_subtopic_frame(self, subtopic_name, subtopic_data):
        frame = ttk.Frame(self.subtopics_frame)
        frame.pack(fill="x", padx=5, pady=2)

        var = tk.BooleanVar(value=subtopic_data["completed"])

        checkbox = ttk.Checkbutton(
            frame,
            text=subtopic_name,
            variable=var,
            command=lambda: self.on_checkbox_click(subtopic_name, var),
            style="Subtopic.TCheckbutton"
        )
        checkbox.pack(side="left")

        delete_btn = ttk.Button(
            frame,
            text="x",
            command=lambda: self.delete_subtopic(subtopic_name, frame),
            style="Delete.TButton",
            width=3
        )
        delete_btn.pack(side="right")

    def create_add_subtopic_button(self):
        add_subtopic_btn = ttk.Button(
            self.frame,
            text="+ Add Subtopic",
            command=self.add_subtopic,
            style="AddSubtopic.TButton"
        )
        add_subtopic_btn.pack(pady=10)

    def add_subtopic(self):
        AddDialog("Add Subtopic", "Enter subtopic name:", self.add_subtopic_callback)

    def add_subtopic_callback(self, subtopic_name):
        if not subtopic_name:
            return

        data = self.data_manager.load_data()
        if subtopic_name not in data[self.subject]["topics"][self.topic_name]["subtopics"]:
            data[self.subject]["topics"][self.topic_name]["subtopics"][subtopic_name] = {"completed": False}
            self.data_manager.save_data(data)
            self.create_subtopic_frame(subtopic_name, {"completed": False})
            self.update_callback()

    def delete_subtopic(self, subtopic_name, frame):
        data = self.data_manager.load_data()
        del data[self.subject]["topics"][self.topic_name]["subtopics"][subtopic_name]
        self.data_manager.save_data(data)
        frame.destroy()
        self.update_callback()

    def on_checkbox_click(self, subtopic_name, var):
            # Update the completion status of the subtopic
            data = self.data_manager.load_data()
            data[self.subject]["topics"][self.topic_name]["subtopics"][subtopic_name]["completed"] = var.get()
            self.data_manager.save_data(data)

            # Trigger a callback to update the progress circle
            self.update_callback()
