
###Player class below
import pygame


class Player:
    def __init__(self):
        self.player_img = pygame.image.load("assets/Spaceship.png")
        self.pos_x, self.pos_y = 600, 600
        self.vel_x, self.vel_y = 400, 400
        self.lives = 3
        self.circle_radius = 0
        self.circle_max_radius = 64*2   #twice the size of player sprite
        self.circle_growth_rate = 400 #pixels per second
        self.circle_active = False
        self.ability_cooldown = 5 # Cooldown in seconds
        self.last_ability_use_time = -self.ability_cooldown #initialization allows ability to be used on startup
        self.shift_ability_cooldown = 5
        self.last_shift_ability_time = -self.shift_ability_cooldown
        self.last_move_direction = pygame.math.Vector2(0,0)
        self.game_over = False #Flag to indicate game state


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
        
    def activate_shift_ability(self, dt):
        move_amount = 192
        self.pos_x += self.last_move_direction.x * move_amount
        self.pos_y += self.last_move_direction.y * move_amount





    def rect(self):
        return self.player_img.get_rect(topleft=(self.pos_x, self.pos_y))
    
    def take_dmg(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True #Indicates player has died
        return self.game_over
        #handle player death ******NEED TO CHANGE HOW THIS OPERATES 
    
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

  

            
