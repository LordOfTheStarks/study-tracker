# add_dialog.py
import tkinter as tk
from tkinter import ttk

class AddDialog:
    def __init__(self, title, prompt, callback):
        self.dialog = tk.Toplevel()
        self.dialog.title(title)
        self.dialog.geometry("400x250")
        self.dialog.configure(bg="#ffffff")
        self.callback = callback

        # Make dialog modal
        self.dialog.transient(self.dialog.master)
        self.dialog.grab_set()

        # Center the dialog
        self.center_dialog()

        # Create main frame
        self.main_frame = ttk.Frame(self.dialog, style="Dialog.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.setup_styles()

        # Create prompt label
        ttk.Label(
            self.main_frame,
            text=prompt,
            style="Dialog.TLabel"
        ).pack(pady=20)

        # Create entry field
        self.entry = ttk.Entry(
            self.main_frame,
            style="Dialog.TEntry",
            width=30
        )
        self.entry.pack(pady=10)

        # Create button frame
        button_frame = ttk.Frame(self.main_frame, style="Dialog.TFrame")
        button_frame.pack(pady=20)

        # Create buttons
        self.create_buttons(button_frame)

        # Focus entry and bind keys
        self.entry.focus_set()
        self.dialog.bind("<Return>", lambda e: self.save())
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())

        # Wait for dialog to be closed
        self.dialog.wait_window()

    def center_dialog(self):
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        style = ttk.Style()

        # Dialog frame style
        style.configure(
            "Dialog.TFrame",
            background="#ffffff"
        )

        # Dialog label style
        style.configure(
            "Dialog.TLabel",
            background="#ffffff",
            foreground="#2c3e50",
            font=("Helvetica", 12)
        )

        # Entry style
        style.configure(
            "Dialog.TEntry",
            fieldbackground="#ffffff",
            padding=5
        )

        # Button styles
        style.configure(
            "Dialog.TButton",
            padding=(20, 10),
            font=("Helvetica", 10)
        )

    def create_buttons(self, button_frame):
        # Cancel button
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            style="Dialog.TButton",
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="left", padx=10)

        # Save button
        save_btn = ttk.Button(
            button_frame,
            text="Save",
            style="Dialog.TButton",
            command=self.save
        )
        save_btn.pack(side="left", padx=10)

    def save(self):
        value = self.entry.get().strip()
        if value:
            self.dialog.destroy()
            self.callback(value)