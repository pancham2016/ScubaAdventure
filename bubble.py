import pygame
from pygame.sprite import Sprite

class Bubble(Sprite):
    """A class that manages bubbles released from the diver."""

    def __init__(self, sa_game):
        """create a bubble object at the diver's current position."""
        super().__init__()
        self.screen = sa_game.screen
        self.settings = sa_game.settings

        # import the bubble image
        self.image = pygame.image.load("images/bubble.bmp")
        self.bubble_rect = self.image.get_rect()
        self.bubble_rect.topright = sa_game.diver.rect.topright

        # Store the bubble's position as a decimal value
        self.y = float(self.bubble_rect.y)

    def update(self):
        """Move the bubble up the screen."""
        # Update the decimal position of the bubble
        self.y -= self.settings.bubble_speed
        # Update the rect position.
        self.bubble_rect.y = self.y

    def blit_bubble(self):
        """Draw the bubble at the diver's current location"""
        self.screen.blit(self.image, self.bubble_rect.topright)