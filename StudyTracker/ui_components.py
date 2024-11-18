import tkinter as tk
from tkinter import simpledialog

class SubjectWindow:
    def __init__(self, parent, subject_name):
        self.window = tk.Toplevel(parent)
        self.window.title(f"{subject_name} - Topics")

        tk.Label(self.window, text=f"Topics for {subject_name}", font=("Arial", 16)).pack(pady=10)
        self.topic_list_frame = tk.Frame(self.window)
        self.topic_list_frame.pack(pady=10)

        add_topic_btn = tk.Button(self.window, text="+ Add Topic", font=("Arial", 14),
                                  command=self.add_topic)
        add_topic_btn.pack(pady=10)

        self.topics = {}

    def add_topic(self):
        """Add a new topic."""
        new_topic_name = simpledialog.askstring("New Topic", "Enter Topic Name:")
        if new_topic_name:
            self.topics[new_topic_name] = []
            self.refresh_topic_list()

    def refresh_topic_list(self):
        """Refresh the topic list."""
        for widget in self.topic_list_frame.winfo_children():
            widget.destroy()

        for topic in self.topics:
            topic_frame = tk.Frame(self.topic_list_frame)
            topic_frame.pack(pady=5)

            tk.Label(topic_frame, text=topic, font=("Arial", 12)).pack(side="left")
            tk.Button(topic_frame, text="+ Add Subtopic", command=lambda t=topic: self.add_subtopic(t)).pack(side="left")

    def add_subtopic(self, topic):
        """Add a subtopic."""
        subtopic_name = simpledialog.askstring("New Subtopic", f"Enter Subtopic for {topic}:")
        if subtopic_name:
            self.topics[topic].append({"name": subtopic_name, "completed": False})
