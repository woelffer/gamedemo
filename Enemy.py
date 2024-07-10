import pygame 

class Enemy:
    def __init__(self):
        self.enemy_img = pygame.image.load("assets/Enemy_Spaceship.png")
        self.pos_x, self.pos_y = 600, 0
        self.enemy_img = pygame.transform.rotate(self.enemy_img, 180)