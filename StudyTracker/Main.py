import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from data_manager import DataManager
from progress_calc import ProgressCalculator
from subject_window import SubjectWindow
from add_dialog import AddDialog
from font_manager import FontManager
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import sys
from spotify_player import SpotifyPlayer


class StudyTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Tracker")
        self.root.geometry("1280x720")
        self.root.configure(bg="#f0f0f0")

        # Initialize FontManager
        self.font_manager = FontManager()

        # Configure styles with custom font
        self.font_manager.configure_styles()

        # Center the window
        self.center_window()

        self.data_manager = DataManager()
        self.progress_calculator = ProgressCalculator(self.data_manager)

        # Initialize the Spotify player
        self.spotify_player = SpotifyPlayer()

        self.setup_ui()

    def setup_ui(self):
        # Main container with sidebar
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar = ttk.Frame(self.main_container, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.setup_sidebar()

        # Content area
        self.content_frame = ttk.Frame(self.main_container, style="Content.TFrame")
        self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Configure styles for the content frame
        style = ttk.Style()
        style.configure(
            "Content.TFrame",
            background="#D2DCE5"  # Light blue-gray
        )

        # Create a frame for the top buttons
        self.top_buttons_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        self.top_buttons_frame.pack(fill="x", pady=(0, 20))  # Add some space below the buttons

        # Background canvas for the clock
        self.clock_canvas = tk.Canvas(
            self.content_frame,
            width=500,  # Adjust width to suit your layout
            height=200,  # Adjust height to suit your layout
            bg="#D2DCE5",  # Match content frame background
            highlightthickness=0
        )
        self.clock_canvas.pack(pady=20)

        # Load and display the image using Pillow (for .jpeg support)
        self.clock_bg_image = Image.open("clock_bg.jpeg")  # Open JPEG image using Pillow
        self.clock_bg_image = self.clock_bg_image.resize((500, 200))  # Resize if needed
        self.clock_bg_image = ImageTk.PhotoImage(self.clock_bg_image)  # Convert to Tkinter-compatible format

        self.clock_canvas.create_image(0, 0, anchor="nw", image=self.clock_bg_image)

        # Clock in the center of the canvas
        self.clock_label = tk.Label(
            self.clock_canvas,
            font=("Helvetica", 48),
            foreground="#483C32",  # Dark taupe
            background="#D2DCE5"  # Ensure transparency with the canvas
        )
        self.clock_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the clock label
        self.update_clock()

        # Study tracker content
        self.study_tracker_frame = ttk.Frame(self.content_frame, style="Content.TFrame")
        self.study_tracker_frame.pack(fill="both", expand=True)
        self.setup_study_tracker()

        # Load headset icon
        self.headset_icon = Image.open("headset_icon.png")  # Path to headset icon
        self.headset_icon = self.headset_icon.resize((40, 40))  # Resize icon
        self.headset_icon = ImageTk.PhotoImage(self.headset_icon)

        # Load headset icon
        self.headset_icon = Image.open("headset_icon.png")
        self.headset_icon = self.headset_icon.resize((30, 30))  # Made icon slightly smaller
        self.headset_icon = ImageTk.PhotoImage(self.headset_icon)

        # Style for the Spotify connect button
        style.configure(
            "Spotify.TButton",
            padding=5,
            font=(self.font_manager.get_font(), 10),
            background="#1DB954",  # Spotify green
        )

        # Headset Button (top left)
        self.headset_button = ttk.Button(
            self.top_buttons_frame,
            image=self.headset_icon,
            command=self.toggle_mute,
            style="Spotify.TButton"
        )
        self.headset_button.pack(side="left", padx=10)

        # Spotify Connect Button (top right)
        self.spotify_button = ttk.Button(
            self.top_buttons_frame,
            text="Connect to Spotify",
            command=self.connect_spotify,
            style="Spotify.TButton"
        )
        self.spotify_button.pack(side="right", padx=10)

    def toggle_mute(self):
        try:
            current_playback = self.sp.current_playback()
            if current_playback and current_playback['is_playing']:
                # Toggle between 0 and 100 volume
                current_volume = current_playback.get('device', {}).get('volume_percent', 100)
                new_volume = 0 if current_volume > 0 else 100
                self.sp.volume(new_volume)
        except Exception as e:
            print(f"Error toggling volume: {e}")

    def add_spotify_button(self):
        spotify_button = tk.Button(self.content_frame, text="Connect to Spotify", command=self.connect_spotify)
        spotify_button.place(relx=1.0, rely=0.5, anchor="e", x=10)  # Position to the right

    # In Main.py, modify the connect_spotify method:

    def connect_spotify(self):
        try:
            # Attempt to authenticate
            self.spotify_player.authenticate()

            # Create a frame for playback controls
            self.playback_frame = ttk.Frame(self.top_buttons_frame, style="Content.TFrame")
            self.playback_frame.pack(side="right", padx=(0, 10))

            # Style for the playback buttons
            style = ttk.Style()
            style.configure(
                "Playback.TButton",
                padding=5,
                font=(self.font_manager.get_font(), 10),
            )

            # Add preset album button first
            preset_album_button = ttk.Button(
                self.playback_frame,
                text="Play Album",
                command=self.spotify_player.play_preset_playlist,
                style="Playback.TButton"
            )
            preset_album_button.pack(side="left", padx=2)

            # Add regular playback controls
            play_button = ttk.Button(
                self.playback_frame,
                text="▶",
                command=self.spotify_player.play,
                style="Playback.TButton"
            )
            pause_button = ttk.Button(
                self.playback_frame,
                text="❚❚",
                command=self.spotify_player.pause,
                style="Playback.TButton"
            )
            next_button = ttk.Button(
                self.playback_frame,
                text="⏭",
                command=self.spotify_player.next,
                style="Playback.TButton"
            )

            # Pack the buttons horizontally
            play_button.pack(side="left", padx=2)
            pause_button.pack(side="left", padx=2)
            next_button.pack(side="left", padx=2)

            messagebox.showinfo("Spotify", "Successfully connected to Spotify!")
        except Exception as e:
            messagebox.showerror("Spotify Connection Error", str(e))

    def setup_sidebar(self):
        # Sidebar header
        ttk.Label(
            self.sidebar,
            text="Trackers",
            font=(self.font_manager.get_font(), 14, "bold"),  # Changed this line
            foreground="#D2DCE5",  # Light blue-gray for text
            background="#493428"  # Dark brown for background
        ).pack(pady=20)

        # Configure sidebar style
        style = ttk.Style()
        style.configure(
            "Sidebar.TFrame",
            background="#493428"  # Dark brown
        )
        style.configure(
            "Sidebar.TButton",
            padding=10,
            font=(self.font_manager.get_font(), 11, "bold"),  # Changed this line
            background="#BE8464",  # Light brown
            foreground="#483C32",  # Dark taupe
        )
        style.configure(
            "Sidebar.TLabel",
            background="#493428",  # Dark brown
            foreground="#D2DCE5",  # Light blue-gray
            font=(self.font_manager.get_font(), 14, "bold")  # Changed this line
        )

        # Apply the sidebar frame style
        self.sidebar.configure(style="Sidebar.TFrame")

        # Buttons for trackers
        study_tracker_btn = ttk.Button(
            self.sidebar,
            text="Study Tracker",
            command=self.show_study_tracker,
            style="Sidebar.TButton"
        )
        study_tracker_btn.pack(fill="x", padx=10, pady=5)

        # Other tracker button
        other_tracker_btn = ttk.Button(
            self.sidebar,
            text="Other Tracker",
            command=lambda: print("Other Tracker (Placeholder)"),
            style="Sidebar.TButton"
        )
        other_tracker_btn.pack(fill="x", padx=10, pady=5)

        # Optional: Configure sidebar background
        self.sidebar.configure(style="Sidebar.TFrame")

    def update_clock(self):
        if self.clock_label.winfo_exists():
            now = datetime.now().strftime("%H:%M:%S")
            self.clock_label.config(
                text=now,
                font=(self.font_manager.get_font(), 48),
                foreground="#483C32",  # Dark taupe for text
            )
            self.root.after(1000, self.update_clock)

    def setup_study_tracker(self):
        # Create a frame for the list
        self.list_frame = ttk.Frame(self.study_tracker_frame)
        self.list_frame.pack(fill="both", expand=True)

        # Create subject list in the list frame
        self.create_subject_list()

        # Create add button frame
        self.button_frame = ttk.Frame(self.study_tracker_frame)
        self.button_frame.pack(side="bottom", fill="x")

        # Create add button in the button frame
        self.create_add_button()

    def show_study_tracker(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Recreate clock label
        self.clock_label = ttk.Label(self.content_frame, font=("Helvetica", 48), anchor="center")
        self.clock_label.pack(pady=20)
        self.update_clock()

        # Rebuild the study tracker UI
        self.study_tracker_frame = ttk.Frame(self.content_frame)
        self.study_tracker_frame.pack(fill="both", expand=True)
        self.setup_study_tracker()

    def create_subject_list(self):
        # Clear existing widgets in list frame only
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        # Create outer frame to manage boundaries
        self.outer_frame = ttk.Frame(self.list_frame)
        self.outer_frame.pack(fill="both", expand=True)

        # Subjects list with scrollbar
        self.canvas = tk.Canvas(self.outer_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.outer_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configure scrolling behavior
        def _on_frame_configure(event):
            # Update the scrollregion to match the frame's actual size
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            # Get the visible height of the canvas
            visible_height = self.canvas.winfo_height()
            # Get the total height of the content
            total_height = self.scrollable_frame.winfo_reqheight()

            if total_height > visible_height:
                # Only show scrollbar when content exceeds visible area
                scrollbar.pack(side="right", fill="y")
                self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
            else:
                # Hide scrollbar when all content is visible
                scrollbar.pack_forget()
                self.canvas.unbind_all("<MouseWheel>")

        def _on_mousewheel(event):
            # Get current scroll position
            current_pos = self.canvas.yview()

            # Calculate scroll direction
            if event.delta > 0:  # Scrolling up
                if current_pos[0] <= 0:  # At the top
                    return
            else:  # Scrolling down
                if current_pos[1] >= 1:  # At the bottom
                    return

            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_canvas_configure(event):
            # Update the width of the scrollable frame when canvas is resized
            self.canvas.itemconfig(canvas_window, width=event.width)

        # Bind configuration events
        self.scrollable_frame.bind("<Configure>", _on_frame_configure)
        self.canvas.bind("<Configure>", _on_canvas_configure)

        # Create the window for the scrollable frame
        canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            tags="self.scrollable_frame"
        )

        # Configure canvas and scrollbar
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create subject buttons
        data = self.data_manager.load_data()
        for subject in data:
            self.create_subject_button(subject)

    def create_subject_button(self, subject):
        frame = ttk.Frame(self.scrollable_frame)
        frame.pack(fill="x", padx=5, pady=5)

        completion = self.progress_calculator.calculate_subject_completion(subject)

        # Create a frame for the button and delete button
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", expand=True)

        button = ttk.Button(
            button_frame,
            text=f"{subject} ({completion} Complete)",
            command=lambda s=subject: self.open_subject_window(s),
            style="Subject.TButton"  # Added style for consistency
        )
        button.pack(side="left", fill="x", expand=True)

        delete_btn = ttk.Button(
            button_frame,
            text="X",
            command=lambda s=subject: self.delete_subject(s),
            width=3,
            style="Delete.TButton"
        )
        delete_btn.pack(side="right", padx=(5, 0))

    def create_add_button(self):
        style = ttk.Style()
        style.configure(
            "AddButton.TButton",
            background="#BE8464",  # Light brown
            foreground="#483C32",  # Dark taupe
            font=(self.font_manager.get_font(), 14, "bold"),  # Increased font size
            padding=(10, 5)
        )
        add_button = ttk.Button(
            self.button_frame,
            text="+ Add Subject",
            command=self.add_subject,
            style="AddButton.TButton"
        )
        add_button.pack(pady=20)

    def add_subject(self):
        AddDialog("Add Subject", "Enter subject name:", self.add_subject_callback)

    def add_subject_callback(self, subject_name):
        if not subject_name:
            return

        data = self.data_manager.load_data()
        if subject_name not in data:
            data[subject_name] = {"topics": {}}
            self.data_manager.save_data(data)
            self.create_subject_list()  # This now only updates the list, not the button

    def delete_subject(self, subject):
        data = self.data_manager.load_data()
        del data[subject]
        self.data_manager.save_data(data)
        self.create_subject_list()

    def open_subject_window(self, subject):
        # Clear main menu
        for widget in self.root.winfo_children():
            widget.destroy()

        # Open subject window
        SubjectWindow(self.root, subject, self.data_manager, self.progress_calculator, self.return_to_main_menu)

    def return_to_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()

    def center_window(self):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window width and height relative to screen size
        width = int(screen_width * 0.8)  # 80% of screen width
        height = int(screen_height * 0.8)  # 80% of screen height

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = StudyTrackerApp(root)
    root.mainloop()