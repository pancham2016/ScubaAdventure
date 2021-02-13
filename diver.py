import pygame
# TO DO: (1) Make the pressure consumption increase and decrease with depth
class Diver:
    """A class to manage the diver."""
    def __init__(self, sa_game):
        """Initialize the diver and set its starting position."""
        self.screen = sa_game.screen
        self.settings = sa_game.settings
        self.screen_rect = sa_game.screen.get_rect()

        # Load the diver image and get its rect
        self.image = pygame.image.load('images/scuba_diver.bmp')
        self.rect = self.image.get_rect()

        # Start the diver near the top of the screen
        self.rect.midtop = self.screen_rect.midtop

        # Store a decimal value for the diver's horizontal position.
        self.x = float(self.rect.x)

        # Store the image of the squeeze
        self.squeeze_image = pygame.image.load("images/squeeze.bmp")
        self.squeeze_rect = self.squeeze_image.get_rect()

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.squeeze_rect = self.squeeze_image.get_rect()

        # Prepare the initial squeeze image
        self.prep_squeeze()

    def turn_diver(self, flip_integer):
        """Flips the orientation of the diver if the diver is moving left or moving right.
            1 means that diver is moving right; -1 means that diver is moving left."""
        diver_right = pygame.image.load('images/scuba_diver.bmp')
        diver_left = pygame.transform.flip(diver_right, True, False)
        if flip_integer == 1:
            self.image = diver_right
        if flip_integer == -1:
            self.image = diver_left

    def change_pressure_with_depth(self):
        """Change the pressure consumption as the depth is increased or decreased"""
        # Divide the screen's vertical depth into four divisions
        ten_meter_division = (self.settings.screen_height)/4

        # check if the diver has passed 10 meters depth
        if self.rect.y >= ten_meter_division:
            return True

    def prep_squeeze(self):
        """Position and display the squeeze image at the top left of the screen"""

    def show_squeeze(self):
        """Display the squeeze symbol when the diver passes 10 meters depth."""
        self.squeeze_rect.left = self.screen_rect.left + 20
        self.squeeze_rect.top = self.screen_rect.top + 20

        self.screen.blit(self.squeeze_image, self.squeeze_rect)
        print("You have reached the 10 meter limit.")

    def center_diver(self):
        """Center the diver on the screen."""
        self.rect.midtop = self.screen_rect.midtop
        self.x = float(self.rect.x)

    def update(self):
        """Update the diver's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.diver_speed
            self.turn_diver(1)
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.rect.x -= self.settings.diver_speed
            self.turn_diver(-1)
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.rect.y -= self.settings.diver_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.settings.diver_speed
            if self.change_pressure_with_depth():
                self.show_squeeze()


    def blitme(self):
        """Draw the diver at his current location"""
        self.screen.blit(self.image, self.rect)