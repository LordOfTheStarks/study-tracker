# add_dialog.py
import tkinter as tk
from tkinter import ttk


class AddDialog:
    def __init__(self, title, prompt, callback):
        self.dialog = tk.Toplevel()
        self.dialog.title(title)
        self.dialog.geometry("400x200")
        self.dialog.configure(bg="#ffffff")
        self.callback = callback

        # Make dialog modal
        self.dialog.transient(self.dialog.master)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

        # Remove window decorations
        self.dialog.overrideredirect(True)

        # Add custom title bar
        self.create_title_bar(title)

        self.setup_styles()

        # Create main frame
        self.main_frame = ttk.Frame(self.dialog, style="Dialog.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

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

        # Make dialog draggable
        self.title_bar.bind("<Button-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.drag)

        # Focus entry
        self.entry.focus_set()

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
            fieldbackground="#f8f9fa",
            padding=5
        )

        # Button styles
        style.configure(
            "Save.TButton",
            padding=10,
            background="#3498db",
            foreground="#ffffff",
            font=("Helvetica", 10, "bold")
        )

        style.configure(
            "Cancel.TButton",
            padding=10,
            background="#e74c3c",
            foreground="#ffffff",
            font=("Helvetica", 10)
        )

        # Button hover effects
        style.map("Save.TButton",
                  background=[("active", "#2980b9")],
                  foreground=[("active", "#ffffff")]
                  )

        style.map("Cancel.TButton",
                  background=[("active", "#c0392b")],
                  foreground=[("active", "#ffffff")]
                  )

    def create_title_bar(self, title):
        # Create title bar
        self.title_bar = tk.Frame(self.dialog, bg="#2c3e50", height=30)
        self.title_bar.pack(fill="x")

        # Title label
        title_label = tk.Label(
            self.title_bar,
            text=title,
            bg="#2c3e50",
            fg="#ffffff",
            font=("Helvetica", 10)
        )
        title_label.pack(side="left", padx=10)

        # Close button
        close_button = tk.Label(
            self.title_bar,
            text="✕",
            bg="#2c3e50",
            fg="#ffffff",
            cursor="hand2",
            font=("Helvetica", 10)
        )
        close_button.pack(side="right", padx=10)

        # Bind close button
        close_button.bind("<Button-1>", lambda e: self.dialog.destroy())

        # Hover effects for close button
        def on_enter(e):
            close_button.configure(fg="#e74c3c")

        def on_leave(e):
            close_button.configure(fg="#ffffff")

        close_button.bind("<Enter>", on_enter)
        close_button.bind("<Leave>", on_leave)

    def create_buttons(self, button_frame):
        # Cancel button
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            style="Cancel.TButton",
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="left", padx=5)

        # Save button
        save_btn = ttk.Button(
            button_frame,
            text="Save",
            style="Save.TButton",
            command=lambda: self.save(self.callback)
        )
        save_btn.pack(side="left", padx=5)

        # Bind Enter key to save
        self.dialog.bind("<Return>", lambda e: self.save(self.callback))

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.dialog.winfo_x() + deltax
        y = self.dialog.winfo_y() + deltay
        self.dialog.geometry(f"+{x}+{y}")

    def save(self, callback):
        value = self.entry.get().strip()
        if value:  # Only save if there's a value
            callback(value)
            self.dialog.destroy()