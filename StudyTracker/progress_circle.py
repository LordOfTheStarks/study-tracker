# data_manager.py
import json
import os


class DataManager:
    def __init__(self, filename="study_data.json"):
        self.filename = filename

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data(self, data):
        with open(self.filename, "w") as file:
            json.dump(data, file)


# progress_circle.py
import tkinter as tk


class ProgressCircle:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self, percentage):
        self.canvas.delete("all")

        # Constants for circle
        center_x, center_y = 100, 100
        radius = 80

        # Draw background circle
        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill="#e0e0e0"
        )

        # Draw progress arc
        angle = percentage * 3.6  # Convert percentage to degrees
        if angle > 0:
            self.canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=90, extent=-angle,
                fill="#4CAF50"
            )

        # Draw percentage text
        self.canvas.create_text(
            center_x, center_y,
            text=f"{percentage}%",
            font=("Arial", 20, "bold"),
            fill="#333333"
        )