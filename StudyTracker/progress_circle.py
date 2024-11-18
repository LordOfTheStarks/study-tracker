class ProgressCircle:
    def __init__(self, canvas):
        self.canvas = canvas
        # Modern color scheme
        self.colors = {
            'background': '#f8f9fa',
            'circle_bg': '#e9ecef',
            'progress_start': '#4CAF50',
            'progress_end': '#45B649',
            'text': '#212529'
        }
        self.congrats_shown = False

    def draw(self, percentage):
        self.canvas.delete("all")

        # Constants for circle
        center_x, center_y = 100, 100
        radius = 80
        inner_radius = radius - 10  # Create a thicker circle

        # Draw shadow (subtle depth effect)
        self.canvas.create_oval(
            center_x - radius + 2, center_y - radius + 2,
            center_x + radius + 2, center_y + radius + 2,
            fill='#dee2e6', outline='#dee2e6'
        )

        # Draw background circle
        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=self.colors['circle_bg'], outline=self.colors['circle_bg']
        )

        # Draw progress arc
        angle = percentage * 3.6  # Convert percentage to degrees
        if angle > 0:
            # Create gradient effect for progress
            for i in range(int(angle)):
                self.canvas.create_arc(
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius,
                    start=90 - i, extent=-1,
                    fill=self.colors['progress_end'],
                    outline=self.colors['progress_end']
                )

        # Draw inner circle for cleaner look
        self.canvas.create_oval(
            center_x - inner_radius, center_y - inner_radius,
            center_x + inner_radius, center_y + inner_radius,
            fill=self.colors['background'], outline=self.colors['background']
        )

        # Draw percentage text with shadow
        self.canvas.create_text(
            center_x + 1, center_y + 1,
            text=f"{percentage}%",
            font=("Helvetica", 24, "bold"),
            fill="#cccccc"
        )
        self.canvas.create_text(
            center_x, center_y,
            text=f"{percentage}%",
            font=("Helvetica", 24, "bold"),
            fill=self.colors['text']
        )

        # Show congratulations message when reaching 100%
        if percentage == 100 and not self.congrats_shown:
            self.show_congratulations(center_x, center_y + radius + 30)
            self.congrats_shown = True
        elif percentage < 100:
            self.congrats_shown = False

    def show_congratulations(self, x, y):
        # Create celebration text with animation
        self.canvas.create_text(
            x, y,
            text="Congratulations!",
            font=("Helvetica", 16, "bold"),
            fill="#28a745",
            tags="congrats"
        )

        # Add subtle animation
        def animate():
            self.canvas.move("congrats", 0, -1)
            self.canvas.after(50, animate)

        animate()