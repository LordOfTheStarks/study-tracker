from tkinter import ttk

import tk


class TopicFrame:
    def __init__(self, parent, subject, topic_name, topic_data, data_manager,
                 progress_calculator, update_callback):
        self.frame = ttk.LabelFrame(parent, text=topic_name)
        self.frame.pack(fill="x", padx=5, pady=5)

        self.subject = subject
        self.topic_name = topic_name
        self.data_manager = data_manager
        self.progress_calculator = progress_calculator
        self.update_callback = update_callback

        self.display_subtopics(topic_data)
        self.create_add_subtopic_button()

    def display_subtopics(self, topic_data):
        for subtopic_name, subtopic_data in topic_data["subtopics"].items():
            self.create_subtopic_frame(subtopic_name, subtopic_data)

    def create_subtopic_frame(self, subtopic_name, subtopic_data):
        frame = ttk.Frame(self.frame)
        frame.pack(fill="x", padx=5, pady=2)

        var = tk.BooleanVar(value=subtopic_data["completed"])

        def on_checkbox_click():
            data = self.data_manager.load_data()
            data[self.subject]["topics"][self.topic_name]["subtopics"][subtopic_name]["completed"] = var.get()
            self.data_manager.save_data(data)
            self.update_callback()

        checkbox = ttk.Checkbutton(frame, text=subtopic_name, variable=var, command=on_checkbox_click)
        checkbox.pack(side="left")

        delete_btn = ttk.Button(
            frame,
            text="×",
            command=lambda: self.delete_subtopic(subtopic_name, frame),
            width=3
        )
        delete_btn.pack(side="right")

    def create_add_subtopic_button(self):
        add_subtopic_btn = ttk.Button(
            self.frame,
            text="+",
            command=self.add_subtopic,
            width=3
        )
        add_subtopic_btn.pack(pady=5)

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