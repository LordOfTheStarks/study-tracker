import tkinter as tk
import os
from tkinter import font


class FontManager:
    def __init__(self, font_path):
        """
        Initialize the font manager with the path to the custom font file.

        Args:
            font_path (str): Path to the .ttf or .otf font file
        """
        self.font_path = font_path
        self.font_family = self._load_custom_font()

    def _load_custom_font(self):
        """Load the custom font and return the font family name."""
        try:
            # Add the font to Tkinter
            font_path = os.path.abspath(self.font_path)
            temp_root = tk.Tk()
            font_family = font.families(temp_root)[0]  # Get the first available font family as fallback
            custom_font = font.Font(family=font_family)

            # Load the custom font
            temp_root.tk.call('tk', 'fontCreate', 'CustomFont', '-file', font_path)
            font_family = 'CustomFont'

            temp_root.destroy()
            return font_family

        except Exception as e:
            print(f"Error loading custom font: {e}")
            return "Helvetica"  # Fallback font

    def get_font(self, size, weight="normal"):
        """
        Get the font configuration tuple.

        Args:
            size (int): Font size
            weight (str): Font weight ("normal" or "bold")

        Returns:
            tuple: Font configuration tuple (family, size, weight)
        """
        return (self.font_family, size, weight)

    def configure_styles(self, style):
        """
        Configure all ttk styles with the custom font.

        Args:
            style (ttk.Style): The ttk style object to configure
        """
        # Main text styles
        style.configure("TLabel", font=self.get_font(10))
        style.configure("TButton", font=self.get_font(10))
        style.configure("TEntry", font=self.get_font(10))

        # Header styles
        style.configure("Header.TLabel", font=self.get_font(14, "bold"))
        style.configure("Title.TLabel", font=self.get_font(24, "bold"))

        # Sidebar styles
        style.configure("Sidebar.TButton", font=self.get_font(11, "bold"))
        style.configure("Sidebar.TLabel", font=self.get_font(14, "bold"))

        # Dialog styles
        style.configure("Dialog.TLabel", font=self.get_font(12))
        style.configure("Dialog.TButton", font=self.get_font(10))

        # Topic styles
        style.configure("Topic.TLabelframe.Label", font=self.get_font(12, "bold"))
        style.configure("Subtopic.TCheckbutton", font=self.get_font(10))

        # Add Topic/Subject button styles
        style.configure("AddTopic.TButton", font=self.get_font(12, "bold"))