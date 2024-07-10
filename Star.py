import random
import pygame

class Star: 
    def __init__(self, star_img, screen_width, screen_height):
        self.star_img = star_img
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.opacity = 255 #full opaque
        self.reset()

    def reset(self):
        self.pos_x = random.randint(0, self.screen_width)
        self.pos_y = random.randint(0, self.screen_height)
        self.speed = random.uniform(50, 500) #varying speeds for parallax effect 
        self.set_random_opacity()
    
    def set_random_opacity(self):
        self.opacity = random.randint(50, 200) #Random opacity between 50 and 200

    def move(self, dt):
        self.pos_y += self.speed * dt
        if self.pos_y > self.screen_height:
            self.pos_y = 0
            self.pos_x = random.randint(0, self.screen_width)  # Reset position to top edge

    def draw(self, screen):
        # Create a copy of the image with the desired opacity
        temp_img = self.star_img.copy()
        temp_img.set_alpha(self.opacity)

        screen.blit(temp_img, (self.pos_x, self.pos_y))
