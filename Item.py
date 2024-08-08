import pygame
import random
import json 

FRAME_WIDTH = 59
FRAME_HEIGHT = 47
ANIMATION_SPEED = 0.1

class Item():
    def __init__(self, position, path, spritesheet):
        self.x, self.y = position
        self.spritesheet = pygame.image.load(spritesheet).convert_alpha()
        self.hover_frames = [self.spritesheet.subsurface(pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT)) for i in range(6)]
        self.frame_index = 0
        self.frame_counter = 0
        self.rect = pygame.Rect(self.x, self.y, FRAME_WIDTH, FRAME_HEIGHT)
        self.speed = random.randint(100, 200)

    def load_frames(self, path):
        with open(path) as f:
            data = json.load(f)
        frames = []
        for frame_name in data['frames']:
            frame_info = data['frames'][frame_name]['frame']
            x, y, w, h = frame_info['x'], frame_info['y'], frame_info['w'], frame_info['h']
            frame_surface = self.spritesheet.subsurface(pygame.Rect(x,y,w,h))
            self.hover_frames.append(frame_surface)
        
        self.rect = self.hover_frames[0].get_rect(topleft=(self.x, self.y))

    
    def update(self, dt):
        #Update animation 
        self.frame_counter += ANIMATION_SPEED
        if self.frame_counter >= 1:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.hover_frames)
        
        self.y += self.speed * dt

        #Get the current frame's bounding rect 
        current_frame = self.hover_frames[self.frame_index]
        self.rect = pygame.Rect(self.x, self.y, current_frame.get_width(), current_frame.get_height())
        
    def draw(self, screen):
        screen.blit(self.hover_frames[self.frame_index], (self.x, self.y))
        pygame.draw.rect(screen, (255,0,0,127), self.rect, 2) #Draws the item collision box for troubleshooting