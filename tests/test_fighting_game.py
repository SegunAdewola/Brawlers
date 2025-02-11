import unittest
import pygame
from fighting_game import show_bg_selection
from fighting_game import main
from fighter import AI, Fighter

# create game window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# load background image
bg_image = pygame.image.load("assets/images/background/background_1.jpeg").convert_alpha()
bg_image2 = pygame.image.load("assets/images/background/background_2.jpeg").convert_alpha()
bg_image3 = pygame.image.load("assets/images/background/background_3.jpeg").convert_alpha()

# Scale background options to fit on the screen
scaled_bg_1 = pygame.transform.scale(bg_image, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
scaled_bg_2 = pygame.transform.scale(bg_image2, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
scaled_bg_3 = pygame.transform.scale(bg_image3, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))

# Define positions for the background options
bg_option_rects = [
    pygame.Rect(SCREEN_WIDTH // 6 - (SCREEN_WIDTH // 6), SCREEN_HEIGHT // 3, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3),
    # Option 1
    pygame.Rect(SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 6), SCREEN_HEIGHT // 3, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3),
    # Option 2
    pygame.Rect(SCREEN_WIDTH * 5 // 6 - (SCREEN_WIDTH // 6), SCREEN_HEIGHT // 3, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3)
    # Option 3
]

# Background selection variable
selected_bg = None


class TestFighter(unittest.TestCase):

    def test_background_selection(self):
        global selected_bg

        # Call show_bg_selection to render the options
        show_bg_selection()

        # Simulate mouse click on the first background option (bg_option_rects[0])
        mouse_pos = (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3)  # Coordinates for the first option
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=mouse_pos))  # Post the event

        # Simulate mouse click on the first background option
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the click was within any of the background option rectangles
                if bg_option_rects[0].collidepoint(event.pos):
                    global selected_bg
                    selected_bg = bg_image  # Set the selected background

            # Update the screen (since show_bg_selection works in the main loop)
            pygame.display.update()

        self.assertIsNotNone(selected_bg)

    def setUp(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load actual sprite sheets
        self.timmy_sprite_sheet = pygame.image.load("assets/images/timmy/timmy_sprints.png").convert_alpha()
        self.boss_sprite_sheet = pygame.image.load("assets/images/boss/boss_sprites.png").convert_alpha()

        # Define animation steps (you can adjust these based on your sprite sheet)
        self.timmy_animation_steps = [10, 10, 12, 12, 10, 12, 6, 12]  # Example animation steps for Timmy
        self.boss_animation_steps = [8, 10, 12, 10, 8, 11, 10, 11]  # Example animation steps for Boss

        # Character action sound fx
        punch_fx = pygame.mixer.Sound("assets/audio/punch.mp3")

        # Create fighter instances with loaded sprite sheets
        self.fighter_1 = AI(1, 700, 310, True, [1152, 864, 0.25, [1, 24]], self.timmy_sprite_sheet,
                            self.timmy_animation_steps,punch_fx)
        self.fighter_2 = Fighter(2, 200, 310, False, [1152, 864, 0.55, [1, 102]], self.boss_sprite_sheet,
                                 self.boss_animation_steps,punch_fx)

    def test_health_update_AI(self):

        # Initially, fighter_2 should have full health
        initial_health = self.fighter_2.health

        # Ensure that fighter_1 is not moving during the attack (set move direction to 0)
        self.fighter_1.x_velocity = 0

        # Simulate multiple attacks from AI to player
        for _ in range(20):
            if self.fighter_1.attack(self.fighter_2):
                # Ensure the health of fighter_2 has decreased after the attack
                self.assertLess(self.fighter_2.health, initial_health)

    def test_health_update_player(self):
        # Initially, fighter_1 should have full health
        initial_health = self.fighter_1.health

        # Ensure that fighter_2 is not moving during the attack (set move direction to 0)
        self.fighter_2.x_velocity = 0

        # Simulate the attack to check if health is updated
        if self.fighter_2.attack(self.fighter_1):
            self.assertLess(self.fighter_1.health, initial_health)

    def test_attacking(self):

        # Set attack cooldown to 0 to allow attacking
        self.fighter_2.attack_cooldown = 0

        # Set target not hit so the attack can proceed
        self.fighter_1.hit = False

        # Call the attack method
        self.fighter_2.attack(self.fighter_1)

        # Assert that the attacker is in attacking state
        self.assertTrue(self.fighter_2.attacking)


    def test_update(self):
        self.fighter_2.update()
        self.assertFalse(self.fighter_2.attacking)


if __name__ == '__main__':
    unittest.main()



