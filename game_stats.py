class GameStats:
    """Track statistics for Scuba Adventure."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        # self.reset_stats()
        self.level = 1

        # Initialize the starting tank air pressure
        self.tank = 4500

        # Initialize the maximum air pressure of the Submersible Pressure Gauge (SPG)
        self.SPG = 5000

        # Start game in inactive state.
        self.game_active = False

        # Initially do not show the scoreboard.
        self.sb_active = False

    # def reset_stats(self):
    #     """Initialize statistics that can change during the game."""
    #     self.tank_press_left = self.tank