import tkinter as tk
from tkinter import ttk
from progress_circle import ProgressCircle
from topic_frame import TopicFrame
from add_dialog import AddDialog


class SubjectWindow:
    def __init__(self, parent, subject, data_manager, progress_calculator):
        self.window = tk.Toplevel(parent)
        self.window.title(f"{subject} - Topics")
        self.window.geometry("800x600")

        self.subject = subject
        self.data_manager = data_manager
        self.progress_calculator = progress_calculator

        self.setup_ui()

    def setup_ui(self):
        # Create canvas for progress circle
        self.canvas = tk.Canvas(self.window, width=200, height=200, bg="#f0f0f0")
        self.canvas.pack(pady=20)

        self.progress_circle = ProgressCircle(self.canvas)
        self.update_progress()

        self.window.configure(bg="#f8f9fa")
        self.canvas.configure(bg="#f8f9fa")

        # Topics frame
        self.topics_frame = ttk.Frame(self.window)
        self.topics_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.display_topics()
        self.create_add_topic_button()

    def update_progress(self):
        percentage = self.progress_calculator.calculate_subject_completion(self.subject)
        self.progress_circle.draw(percentage)

    def display_topics(self):
        data = self.data_manager.load_data()
        for topic_name, topic_data in data[self.subject]["topics"].items():
            TopicFrame(self.topics_frame, self.subject, topic_name, topic_data,
                       self.data_manager, self.progress_calculator, self.update_progress)

    def create_add_topic_button(self):
        add_topic_btn = ttk.Button(
            self.window,
            text="+",
            command=self.add_topic,
            style="Custom.TButton"
        )
        add_topic_btn.pack(side="bottom", pady=20)

    def add_topic(self):
        AddDialog("Add Topic", "Enter topic name:", self.add_topic_callback)

    def add_topic_callback(self, topic_name):
        if not topic_name:
            return

        data = self.data_manager.load_data()
        if topic_name not in data[self.subject]["topics"]:
            data[self.subject]["topics"][topic_name] = {"subtopics": {}}
            self.data_manager.save_data(data)
            TopicFrame(self.topics_frame, self.subject, topic_name,
                       data[self.subject]["topics"][topic_name],
                       self.data_manager, self.progress_calculator, self.update_progress)