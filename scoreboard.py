import pygame.font
from diver import Diver
import game_stats
# TO DO: (1) Fix the position of the squeeze image 
#
class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, sa_game):
        """Initialize scorekeeping attributes."""
        self.screen = sa_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = sa_game.settings
        self.stats = sa_game.stats
        self.sa_game = sa_game
        self.timer = 0
        self.gauge_image = pygame.image.load("images/gauge.bmp")
        self.gauge_rect = self.gauge_image.get_rect()

        # Assign the coordinates of the gauge
        self.gauge_rect.right = self.screen_rect.right - 20
        self.gauge_rect.top = 20

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial tank pressure image
        self.prep_tank_pressure()

        # Prepare the initial gauge image
        # self.prep_gauge()

        # Gauge movement flag
        self.gauge_moving_left = False

    def prep_tank_pressure(self):
        """Turn the starting tank pressure into a rendered image."""
        tank_press_str = str(self.stats.tank)
        self.tank_press_image = self.font.render(tank_press_str, True,
                                self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.tank_press_rect = self.tank_press_image.get_rect()
        self.tank_press_rect.right = self.screen_rect.right - 20
        self.tank_press_rect.top = 20

    def show_tank_pressure(self):
        """Draw the tank pressure to the screen."""
        self.screen.blit(self.tank_press_image, self.tank_press_rect)

    def decrease_tank_pressure(self):
        """Decrease the tank pressure a certain amount per time interval during the dive."""
        self.stats.tank -= int(self.stats.tank * (self.stats.tank / self.settings.dive_time))
        self.prep_tank_pressure()

    # def prep_gauge(self):
    #     """Position the gauge at the start of the game."""
    #     # Position 20 pixels from top and right.
    #     self.gauge_rect.right = self.screen_rect.right - 20
    #     self.gauge_rect.top = 20

    # def show_gauge(self):
    #     # Display the gauge at the top right of the screen.
    #     self.gauge_rect = self.gauge_image.get_rect()  # get the area of the gauge image

    def slide_gauge(self):
        """Slide the gauge when the space_bar is pressed.
        When position is reached, return True to say that gauge is no longer moving to left."""
        # Slide the gauge to the left
        if(self.gauge_moving_left == True and self.gauge_rect.x >
                (self.screen_rect.width - self.tank_press_rect.width - self.gauge_rect.width)):
            self.gauge_rect.x -= self.settings.gauge_slide_speed
        elif(self.stats.sb_active == False and self.gauge_rect.x <=
             (self.screen_rect.width - self.tank_press_rect.width - self.gauge_rect.width)):
            self.gauge_rect.x += self.settings.gauge_slide_speed
            self.gauge_moving_left = False

