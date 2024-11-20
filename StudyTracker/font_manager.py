import os
import sys
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
import tkinter as tk
from tkinter import ttk


class FontManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.custom_font = self.load_custom_font()
            self.initialized = True

    def load_custom_font(self):
        try:
            # Get the absolute path to the font file
            if getattr(sys, 'frozen', False):
                # If running as exe
                application_path = os.path.dirname(sys.executable)
            else:
                # If running as script
                application_path = os.path.dirname(os.path.abspath(__file__))

            # Try TTF first, then OTF
            font_path = os.path.join(application_path, 'fonts', 'Dune_Rise.ttf')
            if not os.path.exists(font_path):
                font_path = os.path.join(application_path, 'fonts', 'Dune_Rise.otf')

            if not os.path.exists(font_path):
                print(f"Font file not found at {font_path}")
                return "Helvetica"

            # Windows API call to load the font
            FR_PRIVATE = 0x10
            FR_NOT_ENUM = 0x20

            # Load the font file
            path_buf = create_unicode_buffer(font_path)
            AddFontResourceEx = windll.gdi32.AddFontResourceExW
            AddFontResourceEx(byref(path_buf), FR_PRIVATE, 0)

            # Get the font name
            font_name = "Dune Rise"  # The actual name of the font family

            return font_name

        except Exception as e:
            print(f"Error loading custom font: {e}")
            return "Helvetica"

    def configure_styles(self, root=None):
        """
        Configure styles for the entire application with the custom font
        """
        style = ttk.Style()

        # General styles
        style.configure('TLabel', font=(self.custom_font, 10))
        style.configure('TButton', font=(self.custom_font, 10))
        style.configure('Clock.TLabel', font=(self.custom_font, 48))
        style.configure('Header.TLabel', font=(self.custom_font, 14, 'bold'))
        style.configure('Sidebar.TButton', font=(self.custom_font, 11, 'bold'))
        style.configure('Topic.TLabel', font=(self.custom_font, 12))
        style.configure('Subtopic.TLabel', font=(self.custom_font, 10))

        # Specific styles for each component
        # Add more specific style configurations here as needed
        style.configure("Subject.TButton", font=(self.custom_font, 11))
        style.configure("Delete.TButton", font=(self.custom_font, 8))
        style.configure("AddTopic.TButton", font=(self.custom_font, 12, 'bold'))
        style.configure("Sidebar.TButton", font=(self.custom_font, 11, 'bold'))

        # Dialog styles
        style.configure("Dialog.TLabel", font=(self.custom_font, 12))
        style.configure("Dialog.TButton", font=(self.custom_font, 10))

        # Topic Frame styles
        style.configure(
            "Topic.TLabelframe.Label",
            font=(self.custom_font, 12, "bold")
        )
        style.configure(
            "Subtopic.TCheckbutton",
            font=(self.custom_font, 10)
        )

    def get_font(self):
        """
        Return the custom font name
        """
        return self.custom_font