
###Player class below
import pygame

class Player:
    def __init__(self):
        self.player_img = pygame.image.load("Spaceship.png")
        self.pos_x, self.pos_y = 500, 500
        self.vel_x, self.vel_y = 600,600


    def printer():
        print("Printer func")

    def movement(self, movement, dt):
        if movement == 'a':
            self.pos_x -= self.vel_x * dt
            
        if movement == 'd':
            self.pos_x += self.vel_x * dt
          
        if movement == 'w':
            self.pos_y -= self.vel_y * dt

        if movement == 's':
            self.pos_y += self.vel_y * dt