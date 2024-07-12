
###Player class below
import pygame


class Player:
    def __init__(self):
        self.player_img = pygame.image.load("assets/Spaceship.png")
        self.pos_x, self.pos_y = 600, 600
        self.vel_x, self.vel_y = 400, 400
        self.lives = 3


    def movement(self, movement, dt, screen_width, screen_height):
        if movement == 'a':
            self.pos_x -= self.vel_x * dt
            
        if movement == 'd':
            self.pos_x += self.vel_x * dt
          
        if movement == 'w':
            self.pos_y -= self.vel_y * dt

        if movement == 's':
            self.pos_y += self.vel_y * dt
        
        # Boundary checks
        self.pos_x = max(0, min(screen_width - self.player_img.get_width(), self.pos_x))
        self.pos_y = max(0, min(screen_height - self.player_img.get_height(), self.pos_y))

    def handle_keys(self, dt, screen_width, screen_height):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.movement('a', dt, screen_width, screen_height)
        if keys[pygame.K_d]:
            self.movement('d', dt, screen_width, screen_height)
        if keys[pygame.K_w]:
            self.movement('w', dt, screen_width, screen_height)
        if keys[pygame.K_s]:
            self.movement('s', dt, screen_width, screen_height)

    def rect(self):
        return self.player_img.get_rect(topleft=(self.pos_x, self.pos_y))
    
    def take_dmg(self):
        self.lives -= 1
        if self.lives <= 0:
            pygame.quit()
        #handle player death ******
            pass
