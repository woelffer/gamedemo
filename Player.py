
###Player class below
import pygame
from pygame import mixer
import math

class Player:
    def __init__(self):
        self.player_img = pygame.image.load("assets/Spaceship.png").convert_alpha()
        self.original_img = self.player_img.copy() 
        self.pos_x, self.pos_y = 600, 600
        self.vel_x, self.vel_y = 600, 600
        self.original_pos = (self.pos_x, self.pos_y) #store original position
        self.lives = 5
        self.circle_radius = 0
        self.circle_max_radius = 64*2   #twice the size of player sprite
        self.circle_growth_rate = 400 #pixels per second
        self.circle_active = False
        self.ability_cooldown = 5 # Cooldown in seconds
        self.last_ability_use_time = -self.ability_cooldown #initialization allows ability to be used on startup
        self.shift_ability_cooldown = 2
        self.last_shift_ability_time = -self.shift_ability_cooldown
        self.last_move_direction = pygame.math.Vector2(0,0)
        self.game_over = False #Flag to indicate game state
        self.is_flashing = False
        self.flash_duration = 0.1
        self.flash_timer = 0
        self.flash_color = (255, 0, 0)  # Red tint for flash effect
        self.phase_sound = mixer.Sound("audio/Spaceship_Phase.wav")
        self.phase_sound.set_volume(2.0)
        self.dmg_sound = mixer.Sound("audio/Spaceship_DMG.wav")
        self.dmg_sound.set_volume(0.7)
        self.animation_duration = 0
        self.animation_speed = 0.1
        self.line_start_pos = None
        self.line_end_pos = None
        self.line_color = (0, 204, 255) #color matches circle

        #Load animation frames
        self.animations = {
            "default": [pygame.image.load('assets/Spaceship.png').convert_alpha()],
            "shift": [
                pygame.image.load('assets/Spaceship_Anim/Spaceship_Anim9.png').convert_alpha(),
                pygame.image.load('assets/Spaceship_Anim/Spaceship_Anim8.png').convert_alpha(),
                pygame.image.load('assets/Spaceship_Anim/Spaceship_Anim7.png').convert_alpha(),
                pygame.image.load('assets/Spaceship_Anim/Spaceship_Anim6.png').convert_alpha(),
                pygame.image.load('assets/Spaceship_Anim/Spaceship_Anim5.png').convert_alpha(),
                pygame.image.load('assets/Spaceship_Anim/Spaceship_Anim4.png').convert_alpha(),
                pygame.image.load('assets/Spaceship_Anim/Spaceship_Anim3.png').convert_alpha(),
                pygame.image.load('assets/Spaceship_Anim/Spaceship_Anim2.png').convert_alpha(),
                pygame.image.load('assets/Spaceship_Anim/Spaceship_Anim1.png').convert_alpha()
            ]
        }

        self.current_animation = "default"
        self.animation_index = 0
        self.animation_timer = 0

    def reset(self):
        self.player_img = pygame.image.load("assets/Spaceship.png").convert_alpha()
        self.pos_x, self.pos_y = 600, 600
        self.vel_x, self.vel_y = 600, 600
        self.lives = 5
        self.circle_radius = 0
        self.circle_active = False
        self.last_ability_use_time = -self.ability_cooldown
        self.last_shift_ability_time = -self.shift_ability_cooldown
        self.last_move_direction = pygame.math.Vector2(0, 0)
        self.is_flashing = False
        self.flash_timer = 0     

    def movement(self, movement, dt, screen_width, screen_height):
        move_direction = pygame.math.Vector2(0,0)

        if movement == 'a':
            self.pos_x -= self.vel_x * dt
            move_direction.x = -1
            
        if movement == 'd':
            self.pos_x += self.vel_x * dt
            move_direction.x = 1
          
        if movement == 'w':
            self.pos_y -= self.vel_y * dt
            move_direction.y = -1

        if movement == 's':
            self.pos_y += self.vel_y * dt
            move_direction.y = 1
        
        #Update the last move direction if there's movement
        if move_direction.length() > 0:
            self.last_move_direction = move_direction.normalize()
        
        # Boundary checks
        self.pos_x = max(0, min(screen_width - self.player_img.get_width(), self.pos_x))
        self.pos_y = max(0, min(screen_height - self.player_img.get_height(), self.pos_y))

    def handle_keys(self, dt, screen_width, screen_height):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks() / 1000 

        if keys[pygame.K_a]:
            self.movement('a', dt, screen_width, screen_height)
        if keys[pygame.K_d]:
            self.movement('d', dt, screen_width, screen_height)
        if keys[pygame.K_w]:
            self.movement('w', dt, screen_width, screen_height)
        if keys[pygame.K_s]:
            self.movement('s', dt, screen_width, screen_height)
        if keys[pygame.K_e] and (current_time - self.last_ability_use_time >= self.ability_cooldown):
            self.circle_active = True
            self.circle_radius = 0
            self.last_ability_use_time = current_time
        if keys[pygame.K_LSHIFT] and current_time - self.last_shift_ability_time >= self.shift_ability_cooldown:
            self.activate_shift_ability(dt)
            self.last_shift_ability_time = current_time
            self.start_animation("shift", duration=0.08)  # Set animation duration here
            self.line_end_pos = (self.pos_x + self.player_img.get_width() // 2,
                            self.pos_y + self.player_img.get_height() // 2)
        else:
            self.line_start_pos = None  # Hide the line when Shift is not pressed
            self.line_end_pos = None
            self.line_color = (0, 204, 255)  # Match the circle color
        
    def start_animation(self, animation_name, duration):
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.animation_index = 0
            self.animation_timer = 0
            self.player_img = self.animations[self.current_animation][self.animation_index]
            self.animation_duration = duration


        
    def activate_shift_ability(self, dt):
        move_amount = 192
        channel = pygame.mixer.Channel(4)
        channel.play(self.phase_sound)
        self.line_start_pos = (self.pos_x + self.player_img.get_width() // 2,
                           self.pos_y + self.player_img.get_height() // 2)
        self.pos_x += self.last_move_direction.x * move_amount
        self.pos_y += self.last_move_direction.y * move_amount
        self.line_end_pos = (self.pos_x + self.player_img.get_width() // 2,
                         self.pos_y + self.player_img.get_height() // 2)


    def rect(self):
        return self.player_img.get_rect(topleft=(self.pos_x, self.pos_y))
    
    def take_dmg(self):
        self.lives -= 1
        channel = pygame.mixer.Channel(5)
        channel.play(self.dmg_sound)
        if self.lives <= 0:
            self.game_over = True #Indicates player has died
        
        #Trigger Flash
        self.is_flashing = True
        self.flash_timer = self.flash_duration

        return self.game_over

    def update(self, dt):
        print(f"Current Animation: {self.current_animation}")
        print(f"Animation Timer: {self.animation_timer}")
        print(f"Animation Duration: {self.animation_duration}")
        
        # Handle animation
        if self.current_animation:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_index = (self.animation_index + 1) % len(self.animations[self.current_animation])
                self.player_img = self.animations[self.current_animation][self.animation_index]
                self.animation_timer = 0

            # Update animation duration
            self.animation_duration -= dt
            if self.animation_duration <= 0:
                self.current_animation = "default"
                self.player_img = self.animations["default"][0]
                self.animation_duration = 0
                self.animation_timer = 0  # Reset animation timer
        else:
            self.player_img = self.animations["default"][0]
        if self.is_flashing:
            self.flash_timer -= dt
            if self.flash_timer <= 0:
                self.is_flashing = False
                self.player_img = self.original_img.copy()  # Restore original image
            else:
                # Apply flash effect by tinting the image
                self.player_img = self.original_img.copy()
                flash_surface = pygame.Surface(self.player_img.get_size()).convert_alpha()
                flash_surface.fill(self.flash_color + (128,))  # Apply transparency to the tint
                self.player_img.blit(flash_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        

        
         
    
    def update_circle(self, dt):
        if self.circle_active:
            self.circle_radius += self.circle_growth_rate * dt
            if self.circle_radius >= self.circle_max_radius:
                self.circle_radius = self.circle_max_radius
                self.circle_active = False #Deatcivate once fully expanded
    
    def draw_circle(self, screen):
        if self.circle_active:
            center = (self.pos_x + self.player_img.get_width() // 2, self.pos_y + self.player_img.get_height() // 2)
            outer_radius = int(self.circle_radius)
            inner_radius = int(self.circle_radius * 0.9)  # Adjust this value to control the thickness of the outline

            #Create a surface wieh per-pixel alpha
            circle_surface = pygame.Surface((outer_radius * 2, outer_radius * 2), pygame.SRCALPHA)

            #Draw the cerulean cirlce with reduced opacity
            cerulean_color = (0, 204, 255, 128) 
            pygame.draw.circle(circle_surface, cerulean_color, (outer_radius, outer_radius), inner_radius)
            
            #Blit the cerulean circle surface onto the main screen
            screen.blit(circle_surface, (center[0] - outer_radius, center[1] - outer_radius))

            pygame.draw.circle(screen, (0, 128, 255), center, outer_radius, 2)  # Blue outer circle
    
    def update_position(self, dt):
        #Update the original position if the player has moved during shift
        if self.current_animation == "shift":
            self.original_pos = (self.pos_x, self.pos_y)
        
        self.update(dt)

    def draw(self, screen):
        screen.blit(self.player_img, (self.pos_x, self.pos_y))
         # Draw the line if it's active
        if self.line_start_pos and self.line_end_pos:
            pygame.draw.line(screen, self.line_color, self.line_start_pos, self.line_end_pos, 2)
            self.draw_parallel_lines(screen, self.line_start_pos, self.line_end_pos, 5)  # 5 pixels offset for parallel lines
    

    def draw_hitbox(self, screen):
        rect = self.rect()
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)  # Red color, 2 pixels thick

    def draw_parallel_lines(self, screen, start_pos, end_pos, offset):
        # Calculate the direction of the primary line
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length == 0:
            return
        
        # Normalize the direction vector
        dx /= length
        dy /= length
        
        # Calculate the perpendicular direction
        perp_dx = -dy
        perp_dy = dx

        # Calculate offsets for the parallel lines
        offset_dx1 = start_pos[0] + perp_dx * offset
        offset_dy1 = start_pos[1] + perp_dy * offset
        offset_dx2 = end_pos[0] + perp_dx * offset
        offset_dy2 = end_pos[1] + perp_dy * offset
        offset_dx3 = start_pos[0] - perp_dx * offset
        offset_dy3 = start_pos[1] - perp_dy * offset
        offset_dx4 = end_pos[0] - perp_dx * offset
        offset_dy4 = end_pos[1] - perp_dy * offset

        # Draw the parallel lines
        pygame.draw.line(screen, self.line_color, (offset_dx1, offset_dy1), (offset_dx2, offset_dy2), 2)
        pygame.draw.line(screen, self.line_color, (offset_dx3, offset_dy3), (offset_dx4, offset_dy4), 2)


            
