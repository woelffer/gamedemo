
###Player class below
import pygame


class Player:
    def __init__(self):
        self.player_img = pygame.image.load("assets/Spaceship.png")
        self.pos_x, self.pos_y = 500, 500
        self.vel_x, self.vel_y = 200, 200


    def printer():
        print("Printer func")

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