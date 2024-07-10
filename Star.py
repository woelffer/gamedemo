import random
import pygame

class Star: 
    def __init__(self, star_img, screen_width, screen_height):
        self.star_img = star_img
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        self.pos_x = random.randint(0, self.screen_width)
        self.pos_y = random.randint(0, self.screen_height)
        self.speed = random.uniform(0,-100) #varying speeds for parallax effect 
    
    def move(self, dt):
        self.pos_y -= self.speed * dt
        if self.pos_y < 0:
            self.reset()
            self.pos_y = self.screen_height  # Reset position to top edge

    def move_vertical(self, delta_y):
        self.pos_y += delta_y
        if self.pos_y > self.screen_height:
            self.pos_y = 0
        elif self.pos_y < 0:
            self.pos_y = self.screen_height


    def move_horizontal(self, delta_x):
        self.pos_x += delta_x
        if self.pos_x > self.screen_width:
            self.pos_x = 0
        elif self.pos_x < 0:
            self.pos_x = self.screen_width

    def draw(self, screen):
        screen.blit(self.star_img, (self.pos_x, self.pos_y))   