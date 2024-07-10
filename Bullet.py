import pygame

class Bullet: 
    def __init__(self, position, speed):
        self.bullet_img = pygame.image.load("assets/Bullet.png")
        self.pos_x, self.pos_y = position
        self.speed = speed
    
    def move(self, dt):
        self.pos_y += self.speed * dt