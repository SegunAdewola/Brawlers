# from tabnanny import check
import threading
import pygame
import random


class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.frame_width = data[0]
        self.frame_height = data[1]
        self.image_scale = data[2]
        self.offset = data[3]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0:idle #1:run #2:jump #3:kick #4:elbow #5:special #6:block 7:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0  # velocity
        self.running = False
        self.jump = False  # controls jump
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):  # similar to doing y+=1 at the end of loop. this is just neater
            temp_img_list = []
            for x in range(animation):
                # Calculate position on the sprite sheet for each frame
                frame_x = x * self.frame_width
                frame_y = y * self.frame_height

                # Ensure that subsurface is within bounds
                if frame_x + self.frame_width <= sprite_sheet.get_width() and frame_y + self.frame_height <= sprite_sheet.get_height():
                    temp_img = sprite_sheet.subsurface(
                        pygame.Rect(frame_x, frame_y, self.frame_width, self.frame_height))
                    # Scale the image if needed
                    scaled_img = pygame.transform.scale(temp_img, (
                        self.frame_width * self.image_scale, self.frame_height * self.image_scale))
                    temp_img_list.append(scaled_img)
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = False

        # get key presses
        key = pygame.key.get_pressed()

        # can only perform other actions if not currently attacking - AI
        if self.attacking == False and self.alive == True and round_over == False:

            # check player 2 controls
            if self.player == 2:
                # movement
                if key[pygame.K_LEFT]:  # checks key pressed
                    dx = -SPEED  # SETS X coordinate
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # attack
                if key[pygame.K_1] or key[pygame.K_2] or key[pygame.K_3]:
                    self.attack(target)
                    # determine which attach type was used
                    if key[pygame.K_1]:
                        self.attack_type = 1
                    if key[pygame.K_2]:
                        self.attack_type = 2
                    if key[pygame.K_3]:
                        self.attack_type = 3
                # hit
                if key[pygame.K_SPACE]:
                    self.hit = True

        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:  # 110 is the pixels for floor height
            self.vel_y = 0
            self.jump = 0  # resets jump to 0, to allow jump again
            dy = screen_height - 110 - self.rect.bottom  # dif between floor and bottom of rectangle

        # If the character is hit, apply knockback (e.g., temporarily push the character back)
        if self.hit:
            knockback_force = 15  # How much the character is pushed back
            if self.flip:  # If facing left
                dx = knockback_force  # Move to the right
            else:  # If facing right
                dx = -knockback_force  # Move to the left

            self.hit = False  # Reset hit state after knockback or apply a cooldown timer

        # ensure players face each other only when crossing over
        # if target.rect.centerx > self.rect.centerx:  # If AI is to the left of target and not already facing right
        #     self.flip = True  # face right
        # else:
        #     self.flip = False  # Flip to face left
        if self.rect.centerx < target.rect.centerx and not self.flip:  # If AI is to the left of target and not already facing right
            self.flip = False  # face right
        elif self.rect.centerx > target.rect.centerx and self.flip:  # If AI is to the right of target
            self.flip = True  # Flip to face left

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

    # handle animation updates
    def update(self):  # we can use this for intro
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(7)  # 8:death
        elif self.hit == True:
            self.update_action(6)  # 6:hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)  # attack1: #3:kick
            elif self.attack_type == 2:
                self.update_action(4)  # attack2:4:elbow #punch for boss
            elif self.attack_type == 3:
                self.update_action(5)  # attack2: 5:special
        elif self.jump == True:
            self.update_action(2)  # 2:jump
        elif self.running == True:
            self.update_action(1)  # 1:run
        else:
            self.update_action(0)  # 0:idle

        animation_cooldown = 80

        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            # update time
            self.update_time = pygame.time.get_ticks()
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # check if the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check if an attack was executed
                if self.action == 3 or self.action == 4 or self.action == 5:
                    self.attacking = False
                    self.attack_cooldown = 20
                # check if damage was taken
                if self.action == 6:
                    self.hit = False
                    # if the player was in the middle of an attack then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, target):
        if self.attack_cooldown == 0 and not target.hit:
            self.attacking = True
            # Play sound fx
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                         2 * self.rect.width,
                                         self.rect.height)  # creates rect space in front of player for attack
            if attacking_rect.colliderect(target.rect):
                if not target.hit:  # Only apply damage if the target is not blocking
                    target.health -= 10
                    target.hit = True

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale),
                           self.rect.y - (self.offset[1] * self.image_scale)))


class AI(Fighter):

    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, sound)
        # Set up a cooldown time (for example 100 ticks)
        self.attack_cooldown_time = 20
        self.attack_cooldown = 0  # Start with no cooldown

    # Define the function to be called when the timer finishes
    def timer_finished(self):
        self.attack_cooldown = 0

    # Call the parent class's move method, but add AI-specific logic
    def move(self, screen_width, screen_height, surface, target, round_over):

        super().move(screen_width, screen_height, surface, target, round_over)

        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = False

        # can only perform other actions if not currently attacking - AI
        if self.attacking == False and self.alive == True and round_over == False:

            # check player 1 controls - player 1 as AI
            if self.player == 1:
                # movement
                if self.rect.centerx < target.rect.centerx:  # move AI towards target
                    dx = SPEED  # SETS X coordinate
                    self.running = True
                elif self.rect.centerx > target.rect.centerx:
                    # self.flip = True
                    dx = -SPEED
                    self.running = True

                # jump when target is above
                if target.rect.y < self.rect.y and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                if target.attacking == False:
                    # Only attack if cooldown is 0
                    if self.attack_cooldown == 0:
                        # Trigger attack only when in range
                        if abs(self.rect.centerx - target.rect.centerx) < 50:
                            self.attack(target)
                            self.attack_type = random.choice([1, 3])  # Randomly choose attack type 1, 2, or 3
                            self.attack_cooldown = 1  # Set cooldown so the attack doesn't repeat continuously
                            duration = self.attack_cooldown_time / 1000  # Convert milliseconds to seconds
                            timer = threading.Timer(duration, self.timer_finished)
                            timer.start()  # Start cooldown timer

                # **Jump only if the target is jumping**
                if target.jump == True and random.random() < 0.05:  # Small chance to jump while the player is jumping
                    self.jump = True  # AI jumps when the player jumps

        # Handle gravity movement(same as before)
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:  # 110 is the pixels for floor height
            self.vel_y = 0
            self.jump = False  # resets jump to False
            dy = screen_height - 110 - self.rect.bottom  # dif between floor and bottom of rectangle

        # Update player position
        self.rect.x += dx
        self.rect.y += dy




