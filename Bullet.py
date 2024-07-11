import pygame
from pygame import mixer 

class Bullet: 
    def __init__(self, position, speed):
        self.bullet_img = pygame.image.load("assets/Bullet.png")
        self.bullet_sound = mixer.Sound("audio/8-bit-machine-gun.aiff")
        self.bullet_sound.set_volume(0.2)
        self.pos_x, self.pos_y = position
        self.speed = speed
    
    def move(self, dt):
        self.pos_y += self.speed * dt
    
    def rect(self):
        return self.bullet_img.get_rect(topleft =(self.pos_x, self.pos_y))
    
    def play_sound(self):
        self.bullet_sound.play()