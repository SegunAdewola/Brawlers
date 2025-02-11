import pygame
from pygame import mixer
from fighter import Fighter, AI
import fighter

# Initialise pygame and the mixer
mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

Screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BRAWLERS")

#define colours
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

#load background image
bg_image = pygame.image.load("assets/images/background/2.png").convert_alpha()
bg_image2 = pygame.image.load("assets/images/background/1.png").convert_alpha()
bg_image3 = pygame.image.load("assets/images/background/3.png").convert_alpha()

# Scale background options to fit on the screen
scaled_bg_1 = pygame.transform.scale(bg_image, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
scaled_bg_2 = pygame.transform.scale(bg_image2, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
scaled_bg_3 = pygame.transform.scale(bg_image3, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))

# Define positions for the background options
bg_option_rects = [
    pygame.Rect(SCREEN_WIDTH // 6 - (SCREEN_WIDTH // 6), SCREEN_HEIGHT // 3, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3),  # Option 1
    pygame.Rect(SCREEN_WIDTH // 2 - (SCREEN_WIDTH // 6), SCREEN_HEIGHT // 3, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3),  # Option 2
    pygame.Rect(SCREEN_WIDTH * 5 // 6 - (SCREEN_WIDTH // 6), SCREEN_HEIGHT // 3, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3)   # Option 3
]

# Background selection variable
selected_bg = None

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    Screen.blit(img,(x,y))

# Function to draw the selected background
def draw_bg():
    if selected_bg:
        scaled_bg = pygame.transform.scale(selected_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        Screen.blit(scaled_bg, (0, 0))
        # Background is selected, allow fighters to start moving
        return True
    return False

# Function to display background options
def show_bg_selection():
    # Create a font object
    font = pygame.font.Font("assets/fonts/Baskerville.ttc", 36)

    # Render the text (prompt to click on an image to select a background)
    text = font.render("SELECT YOUR ARENA!", True, (255, 255, 255))

    # Calculate position to center the text at the top of the selection area
    text_x = SCREEN_WIDTH // 2 - text.get_width() // 2  # Center the text horizontally
    text_y = SCREEN_HEIGHT // 1.4  # Position the text towards the top of the screen

    # Blit the text onto the screen
    Screen.blit(text, (text_x, text_y))

    Screen.blit(scaled_bg_1, bg_option_rects[0])  # Draw option 1
    Screen.blit(scaled_bg_2, bg_option_rects[1])  # Draw option 2
    Screen.blit(scaled_bg_3, bg_option_rects[2])  # Draw option 3

#function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health/100
    pygame.draw.rect(Screen, BLACK, (x-2, y-2, 404, 34))
    pygame.draw.rect(Screen, RED, (x, y, 400, 30))
    pygame.draw.rect(Screen, YELLOW, (x,y,400*ratio,30))

def main():
    # define fighter variables
    TIMMY_WIDTH = 1152
    TIMMY_HEIGHT = 864
    TIMMY_SCALE = 0.25
    TIMMY_OFFSET = [1, 24]
    TIMMY_DATA = [TIMMY_WIDTH, TIMMY_HEIGHT, TIMMY_SCALE, TIMMY_OFFSET]
    BOSS_WIDTH = 1152
    BOSS_HEIGHT = 864
    BOSS_SCALE = 0.55
    BOSS_OFFSET = [1, 102]
    BOSS_DATA = [BOSS_WIDTH, BOSS_HEIGHT, BOSS_SCALE, BOSS_OFFSET]

    # Load music and sounds
    pygame.mixer.music.load("assets/audio/lady-of-the-80.mp3")
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1, 0.0, 5000)

    # Character action sound fx
    kick_fx = pygame.mixer.Sound("assets/audio/kick.mp3")
    kick_fx.set_volume(0.25)
    punch_fx = pygame. mixer.Sound("assets/audio/punch.mp3")
    punch_fx.set_volume(0.75)

    # load sprite sheets
    timmy_sheet = pygame.image.load("assets/images/timmy/timmy_sprints.png").convert_alpha()
    boss_sheet = pygame.image.load("assets/images/boss/boss_sprites.png").convert_alpha()

    # define number of steps in each animation
    TIMMY_ANIMATION_STEPS = [10, 10, 12, 12, 10, 12, 6, 12]
    BOSS_ANIMATION_STEPS = [8, 10, 12, 10, 8, 11, 10, 11]

    # define game variables
    intro_count = 0
    last_count_update = pygame.time.get_ticks()
    score = [0, 0]  # player scores. [p1, p2]
    round_over = False
    ROUND_OVER_COOLDOWN = 2000

    # create two instances of fighters
    fighter_1 = AI(1, 200, 310, True, TIMMY_DATA, timmy_sheet, TIMMY_ANIMATION_STEPS, kick_fx)
    fighter_2 = Fighter(2, 600, 310, False, BOSS_DATA, boss_sheet, BOSS_ANIMATION_STEPS, punch_fx)

    # define font
    count_font = pygame.font.Font("assets/fonts/Baskerville.ttc", 80)
    score_font = pygame.font.Font("assets/fonts/Baskerville.ttc", 30)

    # set frame rate
    clock = pygame.time.Clock()  # helps contain how far the left and right run
    FPS = 60

    global selected_bg

    #game loop
    run = True
    while run:

        clock.tick(FPS) #sets how far players move

        # Draw selected background if selected
        draw_bg()

        # If background is selected, allow the fighters to act
        if selected_bg:
            # show player stats
            draw_health_bar(fighter_1.health, 20, 20)
            draw_health_bar(fighter_2.health, 780, 20)
            draw_text("COMPUTER:" + str(score[0]), score_font, BLACK, 20, 60)
            draw_text("PLAYER:" + str(score[1]), score_font, BLACK, 780, 60)

            #update countdown
            if intro_count <= 0:
                # move fighters
                fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, Screen, fighter_2, round_over)
                fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, Screen, fighter_1,round_over)
            else:
                #display count timer
                draw_text(str(intro_count), count_font,RED, SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
                #update count timer
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count-= 1
                    last_count_update = pygame.time.get_ticks()
                    print(intro_count)


            #update fighters
            fighter_1.update()
            fighter_2.update()

            #draw fighters
            fighter_1.draw(Screen)
            fighter_2.draw(Screen)

            #check for player defeat
            if round_over == False:
                if fighter_1.alive == False: # If Fighter 1 (AI) loses
                    score[1]+=1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                elif fighter_2.alive == False: # If Fighter 2 (human) loses
                    score[0]+=1
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
            else:
                #display victory or defeat image based on who won
                if fighter_1.alive == False:  # If Fighter 1 (AI) lost
                    font = pygame.font.Font("assets/fonts/Baskerville.ttc", 64)
                    text = font.render("YOU WIN!", True, WHITE)
                    Screen.blit(text, (320, 250))  # Display victory message in the middle

                elif fighter_2.alive == False:  # If Fighter 2 (human) lost
                    font = pygame.font.Font("assets/fonts/Baskerville.ttc", 64)
                    text = font.render("YOU LOSE!", True, RED)
                    Screen.blit(text, (420, 250))  # Display defeat message in the middle


                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    #reser the round
                    round_over = False
                    intro_count = 3 #reset intro count down

                    # Reset fighters to initial positions
                    fighter_2 = Fighter(2, 600, 310, False, BOSS_DATA, boss_sheet, BOSS_ANIMATION_STEPS, punch_fx)
                    fighter_1 = AI(1, 200, 310, True, TIMMY_DATA, timmy_sheet, TIMMY_ANIMATION_STEPS, kick_fx)

        # If no background is selected, show the selection options
        if not selected_bg:
            show_bg_selection()

        # Event handler to handle background selection
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                run = False
            # Check for mouse click on background options
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the click was within any of the background option rectangles
                if bg_option_rects[0].collidepoint(event.pos):
                    selected_bg = bg_image
                elif bg_option_rects[1].collidepoint(event.pos):
                    selected_bg = bg_image2
                elif bg_option_rects[2].collidepoint(event.pos):
                    selected_bg = bg_image3

        #update display
        pygame.display.update()

    #exit pygame
    pygame.quit()


if __name__ == '__main__':
    main()