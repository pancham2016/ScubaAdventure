# In Scuba Adventure, the diver swims through the water finding friendly sea creatures and avoiding
# dangerous sea creatures. If the diver gets too close to a dangerous fish, the dangerous fish will
# chase the diver and possibly injure them.
# TO DO: (1) Figure out how to keep the SPG in one spot at the start of the game.
import sys

import pygame
import random
from settings import Settings
from time import sleep
from diver import Diver
from bubble import Bubble
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from fish import Fish, FriendlyFish, DangerousFish

class ScubaAdventure:
    """Overall class to manage the game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Scuba Adventure")

        # Create an instance to store the game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Set the background color.
        self.bg_color = (0, 0, 255)

        # Create a clock object for limiting the FPS and count time in ms
        clock = pygame.time.Clock()

        # Start timer: use USEREVENT+n for name; t in ms
        pygame.time.set_timer(pygame.USEREVENT+1, 6000)

        # Create an instance of the diver as an attribute
        self.diver = Diver(self)
        self.bubbles = pygame.sprite.Group()

        # List containing all the FriendlyFish filepaths
        ffish_paths = ['images/turtle.bmp',
                        'images/tuna.bmp',
                        'images/bluecrab.bmp'
                        ]

        # List containing all the DangerousFish filepaths
        dfish_paths = ['images/shark.bmp',
                        'images/jellyfish.bmp'
                        ]

        # Create a dictionary containing all the fishes
        self.fishes = pygame.sprite.Group()

        # Create a dictionary containing all the FriendlyFish()
        self.friendly_fishes = pygame.sprite.Group()

        # Create a dictionary containing all the DangerousFish()
        self.dangerous_fishes = pygame.sprite.Group()

        # Create a school of fishes that contains all the fish
        self._create_school(ffish_paths, dfish_paths)

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.diver.update()
                self.bubbles.update()
                self._update_fishes(self.friendly_fishes, self.dangerous_fishes)

                # Get rid of bubbles that have disappeared
                for bubble in self.bubbles.copy():
                    if bubble.y <= 0:
                        self.bubbles.remove(bubble)
                print(len(self.bubbles))

            self._update_screen()

    def _create_school(self, ffish_paths, dfish_paths):
        """Create the school of friendly fish and dangerous fish."""
        # Load all the friendly filepaths from ffish_paths into list of friendly images
        ffish_images = []
        for path in ffish_paths:
            ffish_image = pygame.image.load(path)
            ffish_images.append(ffish_image)

        # Load all the dangerous filepaths from dfish_paths into a list of dangerous images
        dfish_images = []
        for path in dfish_paths:
            dfish_image = pygame.image.load(path)
            dfish_images.append(dfish_image)

        # Create instances of FriendlyFish and Dangerous Fish and add them to sprite groups
        for image in ffish_images:
            friendly_fish = FriendlyFish(self, image)
            self.friendly_fishes.add(friendly_fish)

        for image in dfish_images:
            dangerous_fish = DangerousFish(self, image)
            self.dangerous_fishes.add(dangerous_fish)

    def _update_fishes(self, friendly_fishes, dangerous_fishes):
        """Check if the school of fish is at an edge,
                        then update the position of the fishes"""
        self.friendly_fishes.update()
        self.dangerous_fishes.update()
        self.check_school_edges(friendly_fishes, dangerous_fishes)
        self._check_fish_diver_collisions()

    def check_school_edges(self, friendly_fishes, dangerous_fishes):
        """Respond if any fish has reached an edge."""
        for f_fish,d_fish in zip(friendly_fishes.sprites(), dangerous_fishes.sprites()):
            # change the swim direction of each individual fish
            if f_fish.check_edges():
                self.change_friendly_direction()
                break
            elif d_fish.check_edges():
                dangerous_fishes.change_dangerous_direction()
                break

    def _check_fish_diver_collisions(self):
        """TO DO: Modify so that something significant happens when you collide
                    with different fishes."""
        if pygame.sprite.spritecollideany(self.diver, self.dangerous_fishes):
            print("You've been stung by a jellyfish. End your dive. Swim to the surface.")
        elif pygame.sprite.spritecollideany(self.diver, self.friendly_fishes):
            print("You've encountered a turtle. Isn't that amazing!")

    def change_friendly_direction(self):
        """Change the direction of the friendly fish"""
        self.settings.fish_direction *= -1

    def change_dangerous_direction(self):
        """Change the direction of the dangerous fish"""
        self.settings.fish_direction *= -1

    # def tank_out(self):
    #     """End the game when the tank runs out of air."""
    #     # Get rid of any remaining fish and diver
    #     self.friendly_fishes.empty()
    #     self.dangerous_fishes.empty()
    #
    #     # Create a new dive and center the diver
    #     self.diver.center_diver()
    #     self._create_school(ffish_paths, dfish_paths)
    #
    #     # Pause.
    #     sleep(0.5)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.USEREVENT+1 and self.stats.game_active:
                self.sb.decrease_tank_pressure()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.game_active = True

    def _check_score_display(self, event):
        if event.type == pygame.KEYDOWN():
            self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            # Move the diver to the right
            self.diver.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the diver to the left
            self.diver.moving_left = True
        elif event.key == pygame.K_UP:
            # Move the diver up
            self.diver.moving_up = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            # Release bubbles
            self._release_bubble()
            self.diver.moving_down = True
        elif event.key == pygame.K_s and self.stats.game_active:
            # Press 's' to look at SPG pressure
                self.sb.gauge_moving_left = True
                self.sb.slide_gauge()
                self.stats.sb_active = True

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.diver.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.diver.moving_left = False
        elif event.key == pygame.K_UP:
            self.diver.moving_up = False
        elif event.key == pygame.K_s and self.stats.game_active:
            self.stats.sb_active = False
            self.sb.slide_gauge()
        elif event.key == pygame.K_SPACE:
            self.diver.moving_down = False

    def _release_bubble(self):
        """Create a new bubble and add it to the bubble."""
        new_bubble = Bubble(self)
        self.bubbles.add(new_bubble)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.sb.gauge_image, self.sb.gauge_rect) # Issue with blit of gauge_image.
        # Need to assign coordinates of gauge_image to rect.
        self.diver.blitme()
        self.friendly_fishes.draw(self.screen)
        self.dangerous_fishes.draw(self.screen)
        for bubble in self.bubbles:
            bubble.blit_bubble()

        if self.diver.change_pressure_with_depth():
            self.diver.show_squeeze()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Draw the score information
        if self.stats.sb_active and self.stats.game_active:
            self.sb.show_tank_pressure()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

 # Main loop
if __name__ == '__main__':
    # Make a game instance, and run the game.
    sa = ScubaAdventure()
    sa.run_game()