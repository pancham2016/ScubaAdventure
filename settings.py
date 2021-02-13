class Settings:
    """A class to store all settings of Scuba Adventure."""

    def __init__(self):
        """Initialize the settings for Scuba Adventure"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 255)

        # Diver settings
        self.diver_speed = 1.5

        # Fish settings
        self.fish_speed = 2.0
        # Fish_direction of -1 represents left; value of 1 represents right
        self.fish_direction = 1
        self.dangerous_fish_proximity = 20

        # Diving settings
        self.dive_time = 300000

        # Gauge settings
        self.gauge_slide_speed = 80.0 # Create a time setting to have this slow down

        # Bubble settings
        self.bubble_speed = 1.0