import math
import random
import pygame
from pygame.sprite import Sprite
from diver import Diver

# TO DO: (1) Figure out how to refactor the positioning of each fish into a
# method called position_fish()
# (2) Figure out why only turtle is flipping


class Fish(Sprite):
    """A class to manage fish, like sharks, eels, etc."""
    def __init__(self, sa_game):
        """Initialize all the fish and set their starting positions."""
        super().__init__()
        self.screen = sa_game.screen
        self.settings = sa_game.settings

        # Load the image of the fish
        self.image = pygame.image.load('images/shark.bmp') # Is there a way to leave this empty

        # Set an instance of a diver as an attribute
        self.diver = Diver(self)

    def position_fish(self):
        """Get the area of the fish and use to
                position a fish at a randomly generated position."""
        self.rect = self.image.get_rect()
        self.rect.x = self.settings.screen_width - (2 * self.rect.width)
        self.rect.y = random.randint(0, self.settings.screen_height)

        # Store the fish's position as a decimal value
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """Return True if the given fish is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            image = pygame.transform.flip(self.image, True, False)
            self.image = image
            return True

    def update(self):
        """Move the fish to the left."""
        self.x -= self.settings.fish_speed * self.settings.fish_direction
        self.rect.x = self.x

class FriendlyFish(Fish):
    """A simple attempt to model a friendly fish."""
    # To Do: Add new methods to the fish child classes

    def __init__(self, sa_game, image):
        """Initialize attributes of the parent class."""
        super().__init__(sa_game)
        self.screen = sa_game.screen

        # Position the friendly fish on the screen
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = self.settings.screen_width - (2 * self.rect.width)
        self.rect.y = random.randint(0, self.settings.screen_height)

        # Store the friendly fish's exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """Return True if the given fish is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            image = pygame.transform.flip(self.image, True, False)
            self.image = image
            return True

class DangerousFish(Fish):
    def __init__(self, sa_game, image):
        """Initialize attributes of the parent class."""
        super().__init__(sa_game)
        self.screen = sa_game.screen

        # Position the dangerous fishes on the screen
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = self.settings.screen_width - (2 * self.rect.width)
        self.rect.y = random.randint(0, self.settings.screen_height)

        # Store the dangerous fish's exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Create an instance of a diver as an attribute
        diver = Diver(self)

    def sting(self):
        """Prints a simple message that the diver has been stung by the jellyfish"""
        print("You've been stung by a jellyfish. Swim to the surface.")

    def bite(self):
        """Prints a simple message that you've been bitten by a dangerous fish"""
        print("You've been bitten by a dangerous fish.")

    def chase_diver(self, diver):
        """Has the dangerous fish chase the diver if they get too close."""
        # Find direction vector between the diver and the dangerous fish
        dx, dy = diver.rect.x - self.rect.x, diver.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx/dist, dy/dist # Normalize
        # Move along this normalized vector towards the diver at current speed
        self.rect.x += dx * self.settings.fish_speed
        self.rect.y += dy * self.settings.fish_speed

    def diver_too_close(self, diver):
        """If the diver is within a certain proximity to the dangerous fish,
            then return True."""
        dx, dy = diver.rect.x - self.rect.x, diver.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize
        if dx == self.settings.dangerous_fish_proximity \
                or dy == self.settings.dangerous_fish_proximity:
            print("The diver is too close.")
            return True

    def update(self):
        """Move the dangerous fish to the left."""
        diver = Diver(self)
        self.x -= self.settings.fish_speed * self.settings.fish_direction
        self.rect.x = self.x
        self.diver_too_close(diver)

